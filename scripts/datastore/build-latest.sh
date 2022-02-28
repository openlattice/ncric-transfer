#!/usr/bin/env bash

if [ ! -d ~/openlattice ]; then
  echo >&2 'Git repo ~/openlattice not found!'
  exit 1
fi

set -euxo pipefail
cd ~/openlattice

git checkout main && git pull && git submodule update
./gradlew clean :datastore:distTar -x test

if [ -d /opt/openlattice/datastore ]; then
  mv /opt/openlattice/datastore /opt/openlattice/datastore_$(date +"%Y-%m-%d_%H-%M-%S")
else
  mkdir -p /opt/openlattice
fi
mv -f ./datastore/build/distributions/datastore.tgz /opt/openlattice/

cd /opt/openlattice
tar xzvf datastore.tgz
