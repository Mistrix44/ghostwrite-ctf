#!/usr/bin/env python3
"""Member 4: T3, T4, Stage 6 PCAP integrity, and T7 recovery tests."""
import datetime
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT / "logs"
PCAP = ROOT / "stage1" / "files" / "incident.pcap"
APP = ROOT / "stage4-5" / "diag" / "app.py"
results = []
lines = []


def record(test_id, description, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    message = f"[{status}] {test_id}: {description}"
    if detail:
        message += f" ({detail})"
    print(message, flush=True)
    lines.append(message)
    results.append(bool(passed))


def run(args, timeout=30):
    try:
        return subprocess.run(
            args, cwd=ROOT, capture_output=True,
            text=True, timeout=timeout
        )
    except Exception as exc:
        return subprocess.CompletedProcess(args, 1, "", str(exc))


PROBE = (
    "import sys,urllib.request,urllib.error,json\n"
    "req=urllib.request.Request("
    "'http://127.0.0.1:8080/agent/checkin',"
    "headers={'X-Agent-Key':sys.argv[1]})\n"
    "try:\n"
    " r=urllib.request.urlopen(req,timeout=5)\n"
    " body=json.loads(r.read().decode())\n"
    " print('STATUS='+str(r.status))\n"
    " print('REGISTERED='+str(body.get('agent_registered') is True))\n"
    " print('FLAG_PRESENT='+str(bool(body.get('flag'))))\n"
    "except urllib.error.HTTPError as e:\n"
    " print('STATUS='+str(e.code))\n"
    " print('FLAG_PRESENT=False')\n"
)


def checkin(key):
    return run([
        "docker", "compose", "exec", "-T", "stage45",
        "python3", "-c", PROBE, key
    ], timeout=20)


print("GHOSTWRITE Member 4 automated tests")
print(datetime.datetime.now().isoformat(timespec="seconds"))

key_match = None
if APP.exists():
    key_match = re.search(
        r"""(?m)^AGENT_KEY\s*=\s*["']([^"']+)["']""",
        APP.read_text()
    )

if key_match:
    good = checkin(key_match.group(1))
    out = good.stdout
    record(
        "T3", "Valid agent key is accepted",
        good.returncode == 0
        and "STATUS=200" in out
        and "REGISTERED=True" in out
        and "FLAG_PRESENT=True" in out,
        out.strip() or good.stderr.strip()
    )

    bad = checkin("invalid-test-key")
    out = bad.stdout
    record(
        "T4", "Invalid agent key is rejected",
        bad.returncode == 0
        and "STATUS=403" in out
        and "FLAG_PRESENT=False" in out,
        out.strip() or bad.stderr.strip()
    )
else:
    record("T3/T4", "Agent key source is available", False,
           "Could not find AGENT_KEY in stage4-5/diag/app.py")

if PCAP.exists():
    data = PCAP.read_bytes()
    valid_magic = data[:4] in (
        b"\xd4\xc3\xb2\xa1", b"\xa1\xb2\xc3\xd4",
        b"\x4d\x3c\xb2\xa1", b"\xa1\xb2\x3c\x4d"
    )
    record(
        "S6-a", "PCAP has a valid capture header",
        valid_magic and len(data) > 24,
        f"{len(data)} bytes"
    )
    record(
        "S6-b", "PCAP has no raw plaintext flag marker",
        b"GHOSTWRITE{" not in data,
        "Raw-byte check only; inspect streams separately in Wireshark"
    )
else:
    record("S6-a", "PCAP file exists", False, str(PCAP))

if "--reset" in sys.argv:
    restart = run(
        ["docker", "compose", "restart", "stage45"], timeout=60
    )
    record(
        "T7-a", "Stage 45 restart command succeeds",
        restart.returncode == 0,
        restart.stderr.strip() or restart.stdout.strip()
    )

    recovered = False
    for _ in range(30):
        active = run([
            "docker", "compose", "exec", "-T", "stage45",
            "systemctl", "is-active", "ghost-diag.service"
        ], timeout=10)
        if active.returncode == 0 and active.stdout.strip() == "active":
            recovered = True
            break
        time.sleep(2)

    record(
        "T7-b", "Diagnostic service recovers after restart",
        recovered,
        "ghost-diag.service active" if recovered else "Timed out"
    )

    if recovered and key_match:
        after = checkin(key_match.group(1))
        out = after.stdout
        record(
            "T7-c", "Valid check-in works after recovery",
            after.returncode == 0
            and "STATUS=200" in out
            and "REGISTERED=True" in out,
            out.strip() or after.stderr.strip()
        )
else:
    print("[INFO] Recovery test enabled by running with --reset")
    lines.append("[INFO] Recovery test enabled by running with --reset")

LOG_DIR.mkdir(parents=True, exist_ok=True)
summary = (
    f"RESULT: {sum(results)}/{len(results)} checks passed"
    if results else "RESULT: No checks executed"
)
print("\n" + summary)
lines.append(summary)

log_path = LOG_DIR / (
    "ranasinghe_tests_" + datetime.date.today().isoformat() + ".txt"
)
log_path.write_text("\n".join(lines) + "\n")
print("Log saved:", log_path.relative_to(ROOT))

sys.exit(0 if results and all(results) else 1)
