#!/usr/bin/env python3
"""Fernando - Stage 6 solver: confirm both hops with tshark, reassemble the chunked Base64 flag."""
import base64
import os
import re
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PCAP = os.path.join(HERE, "..", "stage1", "files", "incident.pcap")
SERVER = "10.10.20.15"


def tshark(pcap, *args):
    return subprocess.run(["tshark", "-r", pcap] + list(args),
                          capture_output=True, text=True, timeout=60).stdout


tmp = tempfile.mkdtemp()
pcap = os.path.join(tmp, "incident.pcap")
shutil.copy(PCAP, pcap)             # tshark is blocked by AppArmor in home folders

# 1. connections that START at the internal server's IP (SYN without ACK)
syns = tshark(pcap, "-Y", "ip.addr==%s && tcp.flags.syn==1 && tcp.flags.ack==0" % SERVER,
              "-T", "fields", "-e", "ip.src", "-e", "ip.dst", "-e", "tcp.dstport",
              "-e", "tcp.stream").strip().splitlines()
print("connections involving %s: %d" % (SERVER, len(syns)))
hop2_stream = None
for line in syns:
    src, dst, port, stream = line.split("\t")
    label = {"8080": "Hop 1 (matches Stage 4)", "4444": "Hop 2 (matches Stage 5)"}.get(port, "other")
    print("  %-12s -> %-12s port %-5s stream %-3s %s" % (src, dst, port, stream, label))
    if port == "4444":
        hop2_stream = stream
if hop2_stream is None:
    raise SystemExit("Hop 2 (port 4444) not found")

# 2. follow Hop 2 and rebuild the flag from CHUNK n/m lines
text = tshark(pcap, "-q", "-z", "follow,tcp,ascii,%s" % hop2_stream)
chunks = {int(n): data for n, _, data in re.findall(r"^CHUNK (\d+)/(\d+) (\S+)", text, re.M)}
print("chunks seen (stream order):", [int(n) for n, _, _ in re.findall(r"^CHUNK (\d+)/(\d+) (\S+)", text, re.M)])
joined = "".join(chunks[i] for i in sorted(chunks))
flag = base64.b64decode(joined).decode()
print("flag:", flag if os.environ.get("SHOW_FLAG") else flag[:16] + "...}")
shutil.rmtree(tmp, ignore_errors=True)
