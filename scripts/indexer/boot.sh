#!/usr/bin/env bash

set -exo pipefail
cd /opt/openlattice

killall java || true
sleep 2

APP_FLAGS=(aws postgres "$@")
JAVA_OPTS="${INDEXER_XMS} ${INDEXER_XMX}" ./indexer/bin/indexer "${APP_FLAGS[@]}" > /dev/null 2>&1 &
echo $! > ./indexer.pid
