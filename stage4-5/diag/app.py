from flask import Flask, request, jsonify

app = Flask(__name__)
AGENT_KEY = "5d17cad2c773a3b388f20f94cbfdf5e2"
FLAG = "GHOSTWRITE{4g3nt_ch3ck1n_4cc3pt3d_8c27fa}"

@app.route("/agent/checkin")
def checkin():
    key = request.headers.get("X-Agent-Key", "")
    if key == AGENT_KEY:
        return jsonify({"status": "ok", "flag": FLAG})
    return jsonify({"status": "denied"}), 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
