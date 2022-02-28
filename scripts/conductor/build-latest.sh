#!/usr/bin/env bash

if [ ! -d ~/openlattice ]; then
  echo >&2 'Git repo ~/openlattice not found!'
  exit 1
fi

set -euxo pipefail
cd ~/openlattice

git checkout main && git pull && git submodule update
./gradlew clean :conductor:distTar -x test

if [ -d /opt/openlattice/conductor ]; then
  mv /opt/openlattice/conductor /opt/openlattice/conductor_$(date +"%Y-%m-%d_%H-%M-%S")
else
  mkdir -p /opt/openlattice
fi
mv -f ./conductor/build/distributions/conductor.tgz /opt/openlattice/

cd /opt/openlattice
tar xzvf conductor.tgz
