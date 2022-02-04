#!/usr/bin/env bash

set -eux -o pipefail

currentDir=$(pwd)
cd ~/openlattice

git pull
git submodule update
./gradlew clean :indexer:distTar -x test

mv /opt/openlattice/indexer/ /opt/openlattice/indexer_$(date +"%Y-%m-%d_%H-%M-%S")
rm -f /opt/openlattice/indexer.tgz

mv ~/openlattice/indexer/build/distributions/indexer.tgz /opt/openlattice

cd /opt/openlattice
tar -xzvf indexer.tgz

cd $currentDir
