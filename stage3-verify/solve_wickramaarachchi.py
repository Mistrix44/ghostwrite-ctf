#!/usr/bin/env python3
"""
GHOSTWRITE Stage 3 - What Did They Run?
Personal solver script by Wickramaarachchi (Member 2).

Reads the evidence zip directly, keeps only the sync_token on rows at the 
incident time (ignoring the decoys), and brute-forces the order with 
itertools.permutations against the IOC Correlator API.
"""

import itertools
import os
import re
import zipfile
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ZIP = os.path.join(HERE, "..", "stage1", "files", "evidence_GW-ECLIPSE-07.zip")
URL = "http://localhost/correlate/api/correlate"
FIELD = "password"  # Correct field name based on the reference script
WANTED = ["timeline.csv", "process_log.csv", "file_activity.csv", "powershell_history.txt"]
TIME_RE = re.compile(r"14:02:1[1-9]")          # Incident window
TOKEN_RE = re.compile(r"sync_token=([A-Za-z0-9]+)")


def real_fragments():
    frags = []
    with zipfile.ZipFile(ZIP) as z:
        for name in z.namelist():
            base = os.path.basename(name)
            if base not in WANTED:
                continue
            hits = []
            for line in z.read(name).decode("utf-8", "replace").splitlines():
                m = TOKEN_RE.search(line)
                if m and TIME_RE.search(line):
                    hits.append(m.group(1))
            print("%-24s real fragment(s): %s" % (base, hits))
            frags += hits
    return frags


def try_key(key):
    try:
        resp = requests.post(URL, json={FIELD: key}, timeout=8)
        return resp.text
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    print("[*] Extracting real fragments from evidence zip...")
    frags = real_fragments()
    print("[*] Total fragments found:", len(frags))

    if len(frags) != 4:
        raise SystemExit("[-] Expected exactly 4 fragments. Check row-time filter in the script.")

    tries = 0
    for perm in itertools.permutations(frags):
        tries += 1
        key = "".join(perm)
        print("[*] Trying: %s" % key)
        reply = try_key(key)
        
        if "GHOSTWRITE{" in reply:
            flag = re.search(r"GHOSTWRITE\{[^}]*\}", reply).group(0)
            print("[+] MATCH FOUND after %d tries!" % tries)
            print("[+] Order: %s" % key)
            print("[+] Flag: %s" % flag)
            break
    else:
        print("[-] No ordering accepted after %d tries. Check fragments or API connection." % tries)
