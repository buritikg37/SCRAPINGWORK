from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path
from typing import Any

import pandas as pd
from flask import Flask, redirect, render_template, request, send_file, url_for

from PetshopRed import DEFAULT_SEARCH_TERM, ScraperPetshops

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
    RESOURCE_DIR = Path(getattr(sys, "_MEIPASS", BASE_DIR))
else:
    BASE_DIR = Path(__file__).resolve().parent
    RESOURCE_DIR = BASE_DIR

RESULTS_JSON = BASE_DIR / "petshops_resultados.json"
RESULTS_CSV = BASE_DIR / "petshops_resultados.csv"

app = Flask(
    __name__,
    template_folder=str(RESOURCE_DIR / "templates"),
    static_folder=str(RESOURCE_DIR / "static"),
)


def _repair_text(value: Any) -> Any:
    if not isinstance(value, str):
        return value

    try:
        repaired = value.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return value
    return repaired


def phone_digits(value: Any) -> str:
    if not isinstance(value, str):
        return ""

    cleaned = re.sub(r"\D+", "", value)
    if not cleaned:
        return ""
    if cleaned.startswith("57"):
        return cleaned
    if len(cleaned) >= 10:
        return f"57{cleaned}"
    return cleaned


app.jinja_env.filters["phone_digits"] = phone_digits


def load_results() -> list[dict[str, Any]]:
    if RESULTS_JSON.exists():
        with open(RESULTS_JSON, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    elif RESULTS_CSV.exists():
        data = pd.read_csv(RESULTS_CSV).fillna("").to_dict(orient="records")
    else:
        data = []

    cleaned: list[dict[str, Any]] = []
    for row in data:
        cleaned.append({key: _repair_text(value) for key, value in row.items()})
    return cleaned


def dataset_search_term(results: list[dict[str, Any]]) -> str:
    if not results:
        return DEFAULT_SEARCH_TERM
    return str(results[0].get("busqueda") or DEFAULT_SEARCH_TERM)


def filter_results(results: list[dict[str, Any]], query: str) -> list[dict[str, Any]]:
    if not query:
        return results

    normalized = query.strip().lower()
    filtered: list[dict[str, Any]] = []
    for row in results:
        haystack = " ".join(str(row.get(key, "")) for key in row.keys()).lower()
        if normalized in haystack:
            filtered.append(row)
    return filtered


@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()
    results = load_results()
    filtered = filter_results(results, query)
    active_search = dataset_search_term(results)

    stats = {
        "total": len(results),
        "filtered": len(filtered),
        "with_phone": sum(1 for row in results if str(row.get("telefono", "")).strip() not in {"", "No disponible"}),
        "with_address": sum(1 for row in results if str(row.get("direccion", "")).strip() not in {"", "No disponible"}),
        "with_both": sum(
            1
            for row in results
            if str(row.get("telefono", "")).strip() not in {"", "No disponible"}
            and str(row.get("direccion", "")).strip() not in {"", "No disponible"}
        ),
    }
    last_updated = filtered[-1].get("hora_extraccion") if filtered else None

    return render_template(
        "index.html",
        results=filtered,
        query=query,
        active_search=active_search,
        status=status,
        stats=stats,
        last_updated=last_updated,
    )


@app.route("/scrape", methods=["POST"])
def scrape():
    search_term = request.form.get("search_term", "").strip() or DEFAULT_SEARCH_TERM
    try:
        scraper = ScraperPetshops(search_term)
        scraper.ejecutar()
        return redirect(url_for("index", status=f"Extraccion completada para: {search_term}"))
    except Exception as exc:
        return redirect(url_for("index", status=f"Error en la extraccion: {exc}"))


@app.route("/export/excel")
def export_excel():
    query = request.args.get("q", "").strip()
    results = filter_results(load_results(), query)

    df = pd.DataFrame(results)
    if df.empty:
        df = pd.DataFrame(
            columns=["nombre", "direccion", "telefono", "latitud", "longitud", "url_actual", "hora_extraccion"]
        )

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Petshops")
        sheet = writer.sheets["Petshops"]
        for column_cells in sheet.columns:
            max_length = max(len(str(cell.value or "")) for cell in column_cells)
            sheet.column_dimensions[column_cells[0].column_letter].width = min(max_length + 2, 50)

    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name="petshops_resultados.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
