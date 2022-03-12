#!/usr/bin/env bash

set -exo pipefail
cd /opt/openlattice

killall java || true
sleep 2

APP_FLAGS=(aws postgres "$@")
JAVA_OPTS="${CONDUCTOR_XMS} ${CONDUCTOR_XMX}" ./conductor/bin/conductor "${APP_FLAGS[@]}" > /dev/null 2>&1 &
echo $! > ./conductor.pid
