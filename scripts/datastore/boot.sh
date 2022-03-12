#!/usr/bin/env bash

set -euxo pipefail
cd /opt/openlattice

killall java || true
sleep 2

JAVA_OPTS="${DATASTORE_XMS} ${DATASTORE_XMX}" ./datastore/bin/datastore aws postgres > /dev/null 2>&1 &
echo $! > ./datastore.pid
