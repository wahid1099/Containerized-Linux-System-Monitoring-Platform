from flask import Flask, jsonify
from datetime import datetime, timezone
import os
import time
import psutil

app = Flask(__name__)
START_TIME = time.time()


def collect_metrics():
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_count = psutil.cpu_count(logical=True)

    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()

    uptime_seconds = time.time() - START_TIME

    load_avg_1, load_avg_5, load_avg_15 = (0.0, 0.0, 0.0)
    if hasattr(os, "getloadavg"):
        try:
            load_avg_1, load_avg_5, load_avg_15 = os.getloadavg()
        except OSError:
            pass

    return {
        "cpu": {
            "percent": round(cpu_percent, 1),
            "count": cpu_count,
            "load_avg_1": round(load_avg_1, 2),
            "load_avg_5": round(load_avg_5, 2),
            "load_avg_15": round(load_avg_15, 2),
        },
        "memory": {
            "percent": round(mem.percent, 1),
            "used_mb": round(mem.used / (1024 * 1024), 1),
            "total_mb": round(mem.total / (1024 * 1024), 1),
            "available_mb": round(mem.available / (1024 * 1024), 1),
        },
        "disk": {
            "percent": round(disk.percent, 1),
            "used_gb": round(disk.used / (1024 * 1024 * 1024), 1),
            "total_gb": round(disk.total / (1024 * 1024 * 1024), 1),
        },
        "network": {
            "bytes_sent_mb": round(net.bytes_sent / (1024 * 1024), 1),
            "bytes_recv_mb": round(net.bytes_recv / (1024 * 1024), 1),
            "packets_sent": net.packets_sent,
            "packets_recv": net.packets_recv,
        },
        "uptime_seconds": round(uptime_seconds, 1),
        "boot_time": datetime.fromtimestamp(psutil.boot_time(), tz=timezone.utc).isoformat(),
    }


@app.route("/status")
def status():
    return jsonify({
        "status": "ok",
        "service": "metrics-collector",
        "hostname": os.uname().nodename,
        "time": datetime.now(timezone.utc).isoformat(),
        "metrics": collect_metrics(),
    })


@app.route("/")
def home():
    return jsonify({
        "message": "Metrics Collector API",
        "endpoints": ["/status", "/metrics"],
    })


@app.route("/metrics")
def metrics_only():
    return jsonify(collect_metrics())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)