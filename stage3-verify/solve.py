#!/usr/bin/env python3
"""
GHOSTWRITE Stage 3 - What Did They Run?
Once you've found the 4 real sync_token fragments (one per evidence
file, each sitting on the row matching the true incident timestamp,
~14:02 on 2026-09-20), their correct order isn't given. This script
tries every possible ordering against the IOC Correlator until one
is accepted.
"""

import itertools
import requests

# Replace these with the 4 fragments YOU found in the evidence files.
# Order here doesn't matter - the script tries every permutation.
fragments = ["EYPO", "5JSV", "TV7H", "DO44"]

url = "http://localhost/correlate/api/correlate"

for combo in itertools.permutations(fragments):
    guess = "".join(combo)
    print(f"[*] Trying: {guess}")
    resp = requests.post(url, json={"password": guess})
    data = resp.json()
    if data.get("status") == "confirmed":
        print(f"[+] MATCH FOUND: {guess}")
        print(f"[+] Flag: {data['flag']}")
        break
else:
    print("[-] No permutation matched. Check your fragments.")
