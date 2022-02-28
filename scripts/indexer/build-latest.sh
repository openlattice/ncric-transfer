#!/usr/bin/env bash

if [ ! -d ~/openlattice ]; then
  echo >&2 'Git repo ~/openlattice not found!'
  exit 1
fi

set -euxo pipefail
cd ~/openlattice

git checkout main && git pull && git submodule update
./gradlew clean :indexer:distTar -x test

if [ -d /opt/openlattice/indexer ]; then
  mv /opt/openlattice/indexer /opt/openlattice/indexer_$(date +"%Y-%m-%d_%H-%M-%S")
else
  mkdir -p /opt/openlattice
fi
mv -f ./indexer/build/distributions/indexer.tgz /opt/openlattice/

cd /opt/openlattice
tar xzvf indexer.tgz
