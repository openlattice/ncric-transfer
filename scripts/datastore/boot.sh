#!/usr/bin/env bash

# boot.sh [flags] ...
# optional flags for conductor in addition to "aws" and "postgres"

set -exo pipefail
cd /opt/openlattice

killall java || true
sleep 2

APP_FLAGS=(aws postgres "$@")
JAVA_OPTS="${DATASTORE_XMS} ${DATASTORE_XMX}" ./datastore/bin/datastore "${APP_FLAGS[@]}" > /dev/null 2>&1 &
echo $! > ./datastore.pid
