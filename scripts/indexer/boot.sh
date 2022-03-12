#!/usr/bin/env bash

set -euxo pipefail
cd /opt/openlattice

killall java || true
sleep 2

JAVA_OPTS="${INDEXER_XMS} ${INDEXER_XMX}" ./indexer/bin/indexer aws postgres > /dev/null 2>&1 &
echo $! > ./indexer.pid
