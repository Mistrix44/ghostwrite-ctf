#!/usr/bin/env python3
"""Kaldera - platform checks: service health, published ports, isolation (T5), routing (T6)."""
import datetime
import re
import subprocess
import sys
import urllib.error
import urllib.request

SERVICES = ["ctfd", "ctfd_cache", "ctfd_db", "jump", "proxy",
            "stage1", "stage2", "stage3verify", "stage45"]
EXPECTED_PORTS = {80, 2222, 8000}  # proxy, jump host, CTFd admin (intentional)
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print("[%s] %s %s" % ("PASS" if ok else "FAIL", name, detail))


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=60)


def http_status(url):
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return None


print("Platform check - %s" % datetime.datetime.now().isoformat(timespec="seconds"))

# 1. every service is running
r = sh(["docker", "compose", "ps", "--format", "{{.Service}} {{.State}}"])
states = dict(l.split(" ", 1) for l in r.stdout.strip().splitlines() if " " in l)
for svc in SERVICES:
    check("service %s running" % svc, states.get(svc) == "running", "(%s)" % states.get(svc))

# 2. only the intended ports are published to the host
r = sh(["docker", "compose", "ps", "--format", "{{.Ports}}"])
ports = {int(p) for p in re.findall(r":(\d+)->", r.stdout)}
check("published ports are only %s" % sorted(EXPECTED_PORTS), ports == EXPECTED_PORTS,
      "(found %s)" % sorted(ports))

# 3. T5: internal_net is flagged internal and stage45 cannot reach the internet
r = sh(["docker", "network", "inspect", "ghostwrite_internal_net", "--format", "{{.Internal}}"])
check("T5 internal_net has internal=true", r.stdout.strip() == "true", "(%s)" % r.stdout.strip())
probe = ("import socket\n"
         "try:\n"
         "    socket.create_connection(('1.1.1.1', 53), timeout=4)\n"
         "    print('REACHED')\n"
         "except Exception:\n"
         "    print('BLOCKED')\n")
r = sh(["docker", "compose", "exec", "-T", "stage45", "python3", "-c", probe])
check("T5 stage45 cannot reach the internet", "BLOCKED" in r.stdout, "(%s)" % r.stdout.strip())

# 4. T6: everything is reachable through the proxy, and CTFd's own port has no /files/
for path in ["/", "/verify/", "/correlate/", "/files/incident.pcap"]:
    code = http_status("http://localhost" + path)
    check("proxy route %s" % path, code == 200, "(HTTP %s)" % code)
code = http_status("http://localhost:8000/files/incident.pcap")
check("direct :8000 does not serve /files/", code == 404, "(HTTP %s)" % code)

print("\n%d/%d checks passed" % (sum(results), len(results)))
sys.exit(0 if all(results) else 1)
