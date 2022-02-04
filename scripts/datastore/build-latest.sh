#!/usr/bin/env bash

set -eux -o pipefail

currentDir=$(pwd)
cd ~/openlattice

git pull
git submodule update
./gradlew clean :datastore:distTar -x test

mv /opt/openlattice/datastore/ /opt/openlattice/datastore_$(date +"%Y-%m-%d_%H-%M-%S")
rm -f /opt/openlattice/datastore.tgz

mv ~/openlattice/datastore/build/distributions/datastore.tgz /opt/openlattice

cd /opt/openlattice
tar -xzvf datastore.tgz

cd $currentDir
