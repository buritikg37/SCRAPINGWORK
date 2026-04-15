from __future__ import annotations

import threading
import webbrowser

from waitress import serve

from app import app

HOST = "127.0.0.1"
PORT = 5000
URL = f"http://{HOST}:{PORT}"


def open_browser() -> None:
    webbrowser.open(URL)


if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    serve(app, host=HOST, port=PORT, threads=8)
