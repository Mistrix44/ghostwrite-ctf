from flask import Flask, request, jsonify

app = Flask(__name__)

CORRECT_PASSWORD = "EYPO5JSVTV7HDO44"
FLAG = "GHOSTWRITE{pwsh_upd4te_dr0pp3d_tmp_b04d6e}"

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IOC Correlator</title>
<style>
:root{--bg:#0a0e0f;--panel:#10161a;--cy:#00fff2;--rd:#ff003c;--tx:#d8f5f2;--mu:#667}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--tx);font:15px/1.6 ui-monospace,Menlo,Consolas,monospace;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px}
.card{background:var(--panel);border:1px solid #23264a;border-radius:10px;max-width:480px;width:100%;padding:36px}
h1{color:var(--cy);font-size:1.3rem;margin-bottom:8px}
p.sub{color:var(--mu);font-size:.88rem;margin-bottom:24px}
label{display:block;font-size:.8rem;color:var(--mu);margin-bottom:4px}
input{width:100%;background:#000;border:1px solid #23264a;color:var(--tx);padding:10px 12px;border-radius:6px;margin-bottom:16px;font-family:inherit;letter-spacing:2px}
button{width:100%;background:var(--cy);color:#000;font-weight:700;border:none;padding:12px;border-radius:6px;cursor:pointer}
button:hover{opacity:.85}
#result{margin-top:20px;padding:14px;border-radius:6px;display:none;font-size:.85rem}
#result.ok{display:block;border:1px solid var(--cy);background:rgba(0,255,242,.08);color:var(--cy)}
#result.bad{display:block;border:1px solid var(--rd);background:rgba(255,0,60,.08);color:var(--rd)}
code{display:block;background:#000;padding:10px;border-radius:6px;margin-top:8px;word-break:break-all;user-select:all}
</style>
</head>
<body>
<div class="card">
  <h1>IOC CORRELATOR</h1>
  <p class="sub">Nightfall SOC will not confirm an incident chain without correlating indicators recovered from all four evidence sources. Four sync tokens are recoverable from the evidence bundle - their source order is not recorded here.</p>
  <form id="f">
    <label>16-character incident key (4 tokens, concatenated)</label>
    <input id="key" maxlength="16" autocomplete="off" placeholder="XXXXXXXXXXXXXXXX">
    <button type="submit">Correlate</button>
  </form>
  <div id="result"></div>
</div>
<script>
document.getElementById('f').addEventListener('submit', async function(e){
  e.preventDefault();
  const guess = document.getElementById('key').value.trim().toUpperCase();
  const r = await fetch('/api/correlate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({password: guess})
  });
  const data = await r.json();
  const box = document.getElementById('result');
  box.classList.remove('ok','bad');
  if (data.status === 'confirmed') {
    box.classList.add('ok');
    box.innerHTML = '<strong>Incident chain confirmed.</strong><code>'+data.flag+'</code>';
  } else {
    box.classList.add('bad');
    box.textContent = 'No correlation. Indicators do not match a known incident.';
  }
});
</script>
</body>
</html>"""

@app.route("/")
def index():
    return PAGE

@app.route("/api/correlate", methods=["POST"])
def correlate():
    data = request.get_json(silent=True) or {}
    guess = (data.get("password") or "").strip().upper()
    if guess == CORRECT_PASSWORD:
        return jsonify({"status": "confirmed", "flag": FLAG})
    return jsonify({"status": "no_match"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
