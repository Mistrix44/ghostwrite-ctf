from flask import Flask, jsonify

app = Flask(__name__)

CAMPAIGN_ID = "GW-ECLIPSE-07"
FLAG = "GHOSTWRITE{n0t_4_r34l_c4ptch4_e51f28}"
EVIDENCE_URL = "/files/evidence_GW-ECLIPSE-07.zip"

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verify you are human</title>
<style>
:root{--ink:#1a1d21;--sub:#6b7280;--line:#e5e7eb;--accent:#2563eb;--bg:#f3f4f6;--ok:#16a34a}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font:15px/1.6 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px}
.card{background:#fff;border:1px solid var(--line);border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.08);max-width:460px;width:100%;padding:40px 36px;text-align:center}
.lock{width:44px;height:44px;margin:0 auto 20px;border-radius:50%;background:#eef2ff;display:grid;place-items:center;color:var(--accent);font-size:20px}
h1{font-size:1.25rem;margin-bottom:8px}
p.sub{color:var(--sub);font-size:.92rem;margin-bottom:28px}
.check{display:flex;align-items:center;gap:12px;border:1px solid var(--line);border-radius:8px;padding:16px 18px;text-align:left;cursor:pointer;user-select:none}
.check:hover{border-color:#c7cdd6}
.box{width:22px;height:22px;border:2px solid #b6bcc4;border-radius:4px;flex:none;display:grid;place-items:center;font-size:14px;color:#fff}
.box.on{background:var(--accent);border-color:var(--accent)}
.spin{width:16px;height:16px;border:2px solid #cdd3db;border-top-color:var(--accent);border-radius:50%;animation:sp .7s linear infinite;display:none}
.spin.show{display:inline-block}
.state{flex:1;font-size:.92rem;color:var(--sub)}
.foot{margin-top:22px;font-size:.75rem;color:#9aa1ab}
.err{display:none;text-align:left;border:1px solid #fca5a5;background:#fef2f2;border-radius:8px;padding:18px 20px;margin-top:20px}
.err.show{display:block}
.err h2{font-size:.95rem;color:#991b1b;margin-bottom:8px}
.err p{font-size:.85rem;color:#7f1d1d;margin-bottom:12px}
.cmdbox{background:#111827;color:#e5e7eb;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.8rem;padding:12px 14px;border-radius:6px;word-break:break-all;position:relative}
.cmdbox .tag{position:absolute;top:-9px;left:12px;background:#7f1d1d;color:#fff;font:600 .65rem system-ui;padding:2px 8px;border-radius:4px}
@keyframes sp{to{transform:rotate(360deg)}}
.reveal{display:none;text-align:left;border:1px solid #bbf7d0;background:#f0fdf4;border-radius:8px;padding:18px 20px;margin-top:20px}
.reveal.show{display:block}
.reveal h2{font-size:.95rem;color:#166534;margin-bottom:12px}
.reveal .row{display:flex;justify-content:space-between;align-items:center;font-size:.82rem;color:#166534;margin-bottom:4px}
.reveal code{display:block;background:#111827;color:#86efac;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.8rem;padding:10px 12px;border-radius:6px;margin:6px 0 14px;word-break:break-all;user-select:all}
.dl{display:block;text-align:center;background:var(--ok);color:#fff;font-weight:600;font-size:.88rem;padding:11px 16px;border-radius:8px;text-decoration:none}
.dl:hover{background:#15803d}
</style>
</head>
<body>
<div class="card">
  <div class="lock">&#128274;</div>
  <h1>Verify you are human</h1>
  <p class="sub">nightfall-interactive.local needs to review the connection before continuing.</p>

  <div class="check" id="checkbox" onclick="runCheck()">
    <div class="box" id="box"></div>
    <div class="state" id="state">I'm not a robot</div>
    <div class="spin" id="spin"></div>
  </div>

  <div class="err" id="err">
    <h2>Automatic verification failed</h2>
    <p>Your browser could not complete the check automatically. Open PowerShell, paste the command below, and press Enter to finish verification.</p>
    <div class="cmdbox"><span class="tag">run this on a windows powershell</span>powershell -nop -w hidden -enc VwByAGkAdABlAC0ASABvAHMAdAAgACcAQgBPAE8ATQAuACAAWQBvAHUAcgAgAGQAZQB2AGkAYwBlACAAaABhAHMAIABiAGUAZQBuACAAYwBvAG0AcAByAG8AbQBpAHMAZQBkAC4AIABUAGgAaQBzACAAaQBzACAAdABoAGUAIABlAHgAYQBjAHQAIAB0AGUAYwBoAG4AaQBxAHUAZQAgAEcASABPAFMAVABXAFIASQBUAEUAIAB1AHMAZQBkACAAYQBnAGEAaQBuAHMAdAAgAEEAbABlAHgAIABNAGUAcgBjAGUAcgAuACcAIAAtAEYAbwByAGUAZwByAG8AdQBuAGQAQwBvAGwAbwByACAAUgBlAGQA</div>
  </div>

  <div class="reveal" id="reveal">
    <h2>Incident evidence recovered</h2>
    <div class="row"><span>Campaign</span></div>
    <code id="campaignCode"></code>
    <div class="row"><span>Flag</span></div>
    <code id="flagCode"></code>
    <a class="dl" id="dlLink" href="#">Download evidence bundle</a>
  </div>

  <div class="foot">Ray ID: 8f2a41c-ghostwrite &middot; Performance &amp; security by nightfall-verify</div>
</div>
<script>
function runCheck(){
  document.getElementById('box').classList.add('on');
  document.getElementById('state').textContent = 'Verifying...';
  document.getElementById('spin').classList.add('show');
  setTimeout(function(){
    document.getElementById('spin').classList.remove('show');
    document.getElementById('state').textContent = 'Verification failed';
    document.getElementById('err').classList.add('show');
  }, 1400);
}
function showReveal(data){
  document.getElementById('err').classList.remove('show');
  document.getElementById('campaignCode').textContent = data.campaign_id;
  document.getElementById('flagCode').textContent = data.flag;
  document.getElementById('dlLink').href = data.download_url;
  document.getElementById('reveal').classList.add('show');
}
</script>
</body>
</html>"""

@app.route("/verify/")
def verify_page():
    return PAGE

@app.route("/verify/api/campaign-info")
def campaign_info():
    return jsonify({
        "campaign_id": CAMPAIGN_ID,
        "flag": FLAG,
        "download_url": EVIDENCE_URL
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
