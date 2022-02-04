#!/usr/bin/env bash

set -eux -o pipefail

currentDir=$(pwd)
cd ~/openlattice

git pull
git submodule update
./gradlew clean :conductor:distTar -x test

mv /opt/openlattice/conductor/ /opt/openlattice/conductor_$(date +"%Y-%m-%d_%H-%M-%S")
rm -f /opt/openlattice/conductor.tgz

mv ~/openlattice/conductor/build/distributions/conductor.tgz /opt/openlattice

cd /opt/openlattice
tar -xzvf conductor.tgz

cd $currentDir
