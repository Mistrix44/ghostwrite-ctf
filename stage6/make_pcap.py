#!/usr/bin/env python3
"""GHOSTWRITE Stage 6 - builds stage1/files/incident.pcap with scapy."""
import base64
import datetime
import os
import random

from scapy.all import Ether, IP, TCP, UDP, DNS, DNSQR, DNSRR, Raw, wrpcap

FLAG = "GHOSTWRITE{full_ch41n_c0nf1rm3d_bca2cc}"
AGENT_KEY = "5d17cad2c773a3b388f20f94cbfdf5e2"

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "stage1", "files", "incident.pcap")

VICTIM = "10.10.10.25"
BUILD = "10.10.20.15"
C2 = "10.10.30.15"
RESOLVER = "10.10.10.2"

rng = random.Random(1907)
T0 = datetime.datetime(2026, 9, 20, 14, 0, 0,
                       tzinfo=datetime.timezone.utc).timestamp()
packets = []


def mac_for(ip):
    o = [int(x) for x in ip.split(".")]
    return "02:42:%02x:%02x:%02x:%02x" % tuple(o)


def emit(pkt, t):
    pkt.time = t
    packets.append(pkt)


def tcp_session(c, s, sport, dport, t, msgs, rtt=0.0015, gap=0.01):
    """Full TCP conversation: handshake, data, close. msgs = [("c"|"s", bytes)]."""
    cseq = rng.randrange(1000, 2 ** 31)
    sseq = rng.randrange(1000, 2 ** 31)

    def mk(src, dst, sp, dp, flags, seq, ack, payload=b"", opts=None):
        ttl = 128 if src.startswith("10.10.10.") else 64
        ip = IP(src=src, dst=dst, id=rng.randrange(1, 65535), ttl=ttl, flags="DF")
        tcp = TCP(sport=sp, dport=dp, flags=flags, seq=seq, ack=ack,
                  window=64240, options=opts or [])
        pkt = Ether(src=mac_for(src), dst=mac_for(dst)) / ip / tcp
        if payload:
            pkt = pkt / Raw(payload)
        return pkt

    emit(mk(c, s, sport, dport, "S", cseq, 0,
            opts=[("MSS", 1460), ("SAckOK", b""), ("WScale", 8)]), t)
    t += rtt
    emit(mk(s, c, dport, sport, "SA", sseq, cseq + 1, opts=[("MSS", 1460)]), t)
    cseq += 1
    sseq += 1
    t += rtt
    emit(mk(c, s, sport, dport, "A", cseq, sseq), t)
    for who, data in msgs:
        t += gap
        if who == "c":
            emit(mk(c, s, sport, dport, "PA", cseq, sseq, data), t)
            cseq += len(data)
            t += rtt
            emit(mk(s, c, dport, sport, "A", sseq, cseq), t)
        else:
            emit(mk(s, c, dport, sport, "PA", sseq, cseq, data), t)
            sseq += len(data)
            t += rtt
            emit(mk(c, s, sport, dport, "A", cseq, sseq), t)
    t += gap
    emit(mk(c, s, sport, dport, "FA", cseq, sseq), t)
    cseq += 1
    t += rtt
    emit(mk(s, c, dport, sport, "FA", sseq, cseq), t)
    sseq += 1
    t += rtt
    emit(mk(c, s, sport, dport, "A", cseq, sseq), t)
    return t


def dns_lookup(client, name, ip, t):
    sport = rng.randrange(40000, 60000)
    qid = rng.randrange(1, 65535)
    q = (Ether(src=mac_for(client), dst=mac_for(RESOLVER)) /
         IP(src=client, dst=RESOLVER) / UDP(sport=sport, dport=53) /
         DNS(id=qid, rd=1, qd=DNSQR(qname=name)))
    r = (Ether(src=mac_for(RESOLVER), dst=mac_for(client)) /
         IP(src=RESOLVER, dst=client) / UDP(sport=53, dport=sport) /
         DNS(id=qid, qr=1, rd=1, ra=1, qd=DNSQR(qname=name),
             an=DNSRR(rrname=name, type="A", ttl=300, rdata=ip)))
    emit(q, t)
    emit(r, t + 0.012)


def ntp_exchange(client, server, t):
    sport = rng.randrange(40000, 60000)
    q = (Ether(src=mac_for(client), dst=mac_for(server)) /
         IP(src=client, dst=server) / UDP(sport=sport, dport=123) /
         Raw(b"\x1b" + b"\x00" * 47))
    r = (Ether(src=mac_for(server), dst=mac_for(client)) /
         IP(src=server, dst=client) / UDP(sport=123, dport=sport) /
         Raw(b"\x1c" + rng.randbytes(47)))
    emit(q, t)
    emit(r, t + 0.03)


def http_resp(body, ctype="text/html", server="nginx"):
    head = ("HTTP/1.1 200 OK\r\nServer: %s\r\nContent-Type: %s\r\n"
            "Content-Length: %d\r\nConnection: close\r\n\r\n"
            % (server, ctype, len(body)))
    return head.encode() + body


def http_get(host, path, extra=""):
    return ("GET %s HTTP/1.1\r\nHost: %s\r\n"
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
            "Accept: */*\r\n%sConnection: close\r\n\r\n" % (path, host, extra)).encode()


def background():
    clients = ["10.10.10.25", "10.10.10.31", "10.10.10.42", "10.10.10.57"]
    sites = [
        ("cdn.engine-assets.example", "203.0.113.10"),
        ("telemetry.studio-tools.example", "203.0.113.20"),
        ("packages.mirror-hub.example", "203.0.113.30"),
        ("docs.vendor-sdk.example", "203.0.113.40"),
    ]
    for _ in range(45):
        c = rng.choice(clients)
        name, ip = rng.choice(sites)
        t = T0 + rng.uniform(1, 355)
        dns_lookup(c, name, ip, t)
        t += 0.05
        sport = rng.randrange(49152, 65000)
        if rng.choice(["https", "https", "http"]) == "https":
            msgs = [
                ("c", b"\x16\x03\x01" + rng.randbytes(rng.randrange(180, 320))),
                ("s", b"\x16\x03\x03" + rng.randbytes(rng.randrange(900, 1300))),
                ("c", b"\x17\x03\x03" + rng.randbytes(rng.randrange(60, 200))),
                ("s", b"\x17\x03\x03" + rng.randbytes(rng.randrange(200, 1200))),
            ]
            tcp_session(c, ip, sport, 443, t, msgs)
        else:
            path = "/" + rng.choice(["index.html", "status", "manifest.json", "version.txt"])
            tcp_session(c, ip, sport, 80, t, [
                ("c", http_get(name, path)),
                ("s", http_resp(b"<html><body>ok</body></html>")),
            ])
    for _ in range(6):
        ntp_exchange(rng.choice(clients), "203.0.113.123", T0 + rng.uniform(1, 355))


def decoys():
    # Decoy 1: unrelated workstation talking to a different :8080 service
    tcp_session("10.10.10.31", "10.10.20.40", 50211, 8080, T0 + 95,
                [("c", http_get("10.10.20.40:8080", "/health")),
                 ("s", http_resp(b'{"status":"ok"}', "application/json", "Werkzeug/3.0.3"))])
    # Decoy 2: unrelated :4444 traffic, plain text, no Base64
    tcp_session("10.10.10.57", "10.10.30.99", 51877, 4444, T0 + 210,
                [("c", b"PING\n"), ("s", b"PONG\n"),
                 ("c", b"PING\n"), ("s", b"PONG\n")])
    # Decoy 3 and 4: harmless Base64 inside normal HTTP traffic
    b1 = base64.b64encode(b"sync_manifest_v2_ok")
    tcp_session("10.10.10.42", "203.0.113.30", 52044, 80, T0 + 130,
                [("c", http_get("packages.mirror-hub.example", "/manifest.b64")),
                 ("s", http_resp(b1, "text/plain"))])
    b2 = base64.b64encode(b"telemetry_batch_0042_accepted")
    tcp_session("10.10.10.31", "203.0.113.20", 52390, 80, T0 + 250,
                [("c", http_get("telemetry.studio-tools.example", "/ack")),
                 ("s", http_resp(b2, "text/plain"))])


def hop1():
    """Victim PC -> build host, TCP/8080 (matches Stage 4)."""
    dns_lookup(VICTIM, "build-internal.nightfall.lan", BUILD, T0 + 153.9)
    req = http_get("build-internal.nightfall.lan:8080", "/agent/checkin",
                   "X-Agent-Key: %s\r\n" % AGENT_KEY)
    req = req.replace(b"Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                      b"Mozilla/5.0 (Windows NT 10.0; Microsoft Windows 10.0.26100; en-US) "
                      b"WindowsPowerShell/5.1.26100.1")
    body = b'{"status":"accepted","agent":"GW-ECLIPSE-07","interval":30}'
    tcp_session(VICTIM, BUILD, 49731, 8080, T0 + 154,
                [("c", req),
                 ("s", http_resp(body, "application/json", "Werkzeug/3.0.3 Python/3.12.3"))])


def hop2():
    """Build host -> simulated C2, TCP/4444 (matches Stage 5). Flag is chunked Base64."""
    b64 = base64.b64encode(FLAG.encode()).decode()
    n = -(-len(b64) // 3)
    parts = [b64[i:i + n] for i in range(0, len(b64), n)]
    total = len(parts)

    def chunk(i):
        return ("CHUNK %d/%d %s\n" % (i + 1, total, parts[i])).encode()

    status = base64.b64encode(b"beacon_nominal")
    tcp_session(BUILD, C2, 41822, 4444, T0 + 182, [
        ("c", b"GW-SYNC/1.0 HELLO\nhost: build-internal.nightfall.lan\n"
              b"campaign: GW-ECLIPSE-07\n"),
        ("s", b"READY\n"),
        ("c", b"STATUS " + status + b"\n"),
        ("s", b"ACK 0\n"),
        ("c", chunk(1)),
        ("s", b"ACK 2\n"),
        ("c", chunk(2)),
        ("s", b"ACK 3\n"),
        ("c", chunk(0)),
        ("s", b"ACK 1\n"),
        ("c", b"DONE\n"),
        ("s", b"BYE\n"),
    ])


background()
decoys()
hop1()
hop2()
packets.sort(key=lambda p: float(p.time))
wrpcap(OUT, packets)
print("wrote %d packets to %s" % (len(packets), os.path.normpath(OUT)))
