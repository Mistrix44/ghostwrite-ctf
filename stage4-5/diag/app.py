from flask import Flask, request, jsonify
from datetime import datetime, timezone

app = Flask(__name__)
AGENT_KEY = "5d17cad2c773a3b388f20f94cbfdf5e2"
FLAG = "GHOSTWRITE{4g3nt_ch3ck1n_4cc3pt3d_8c27fa}"
START_TIME = datetime.now(timezone.utc)

@app.route("/agent/checkin")
def checkin():
    key = request.headers.get("X-Agent-Key", "")
    uptime = (datetime.now(timezone.utc) - START_TIME).total_seconds()

    if key == AGENT_KEY:
        return jsonify({
            "status": "ok",
            "service": "ghost-diag",
            "host": "build-internal.nightfall.lan",
            "uptime_seconds": round(uptime, 1),
            "agent_registered": True,
            "sync_channel": "stable",
            "flag": FLAG
        })

    return jsonify({
        "status": "denied",
        "service": "ghost-diag",
        "reason": "invalid or missing X-Agent-Key header"
    }), 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
