#!/usr/bin/env bash

set -euxo pipefail
cd /opt/openlattice

killall java || true
sleep 2

JAVA_OPTS="${CONDUCTOR_XMS} ${CONDUCTOR_XMX}" /opt/openlattice/conductor/bin/conductor aws postgres > /dev/null 2>&1 &
echo $! > /opt/openlattice/conductor.pid
