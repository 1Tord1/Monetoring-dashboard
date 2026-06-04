from flask import Flask, render_template, jsonify
import csv
import datetime
import os

import psutil

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "access_logs.csv")

LOG_HEADERS = ["timestamp", "cpu_percent", "ram_total_gb", "ram_used_gb", "ram_percent"]


def ensure_log_file():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(LOG_HEADERS)
        return

    with open(LOG_FILE, newline="", encoding="utf-8") as csvfile:
        rows = list(csv.reader(csvfile))

    if not rows or rows[0] != LOG_HEADERS:
        rewritten_rows = []
        for row in rows[1:]:
            extended = row + [""] * (len(LOG_HEADERS) - len(row))
            rewritten_rows.append(extended)
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(LOG_HEADERS)
            writer.writerows(rewritten_rows)


def read_logs():
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                logs.append(row)
    return logs


def add_log(timestamp, cpu_percent, ram_total_gb, ram_used_gb, ram_percent):
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, cpu_percent, ram_total_gb, ram_used_gb, ram_percent])


ensure_log_file()


@app.route("/")
def dashboard():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu_percent = round(psutil.cpu_percent(interval=0.2), 1)
    mem = psutil.virtual_memory()
    ram_total_gb = round(mem.total / (1024 ** 3), 2)
    ram_used_gb = round(mem.used / (1024 ** 3), 2)
    ram_percent = round(mem.percent, 1)

    add_log(now, cpu_percent, ram_total_gb, ram_used_gb, ram_percent)
    logs = list(reversed(read_logs()))[:20]

    return render_template(
        "dashboard.html",
        current_time=now,
        cpu_percent=cpu_percent,
        ram_total_gb=ram_total_gb,
        ram_used_gb=ram_used_gb,
        ram_percent=ram_percent,
        logs=logs,
    )


@app.route("/api/stats")
def api_stats():
    """Returnerer nåværende stats uten å logge."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu_percent = round(psutil.cpu_percent(interval=0.2), 1)
    mem = psutil.virtual_memory()
    ram_total_gb = round(mem.total / (1024 ** 3), 2)
    ram_used_gb = round(mem.used / (1024 ** 3), 2)
    ram_percent = round(mem.percent, 1)

    return jsonify({
        "current_time": now,
        "cpu_percent": cpu_percent,
        "ram_total_gb": ram_total_gb,
        "ram_used_gb": ram_used_gb,
        "ram_percent": ram_percent,
    })


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    app.run(host="0.0.0.0", port=port, debug=False)
