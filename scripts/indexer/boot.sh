#!/usr/bin/env bash

set -eux -o pipefail

currentDir=$(pwd)
cd /opt/openlattice

killall java || true
sleep 2

JAVA_OPTS="${INDEXER_XMS} ${INDEXER_XMX}" /opt/openlattice/indexer/bin/indexer aws postgres > /dev/null 2>&1&
echo $! > /opt/openlattice/indexer.pid

cd $currentDir