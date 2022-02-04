## Environment
Ensure conductor and datastore environment variables are set in `/etc/environment`:
```bash
CONDUCTOR_XMS=-Xms16g
CONDUCTOR_XMX=-Xmx16g
DATASTORE_XMS=-Xms16g
DATASTORE_XMX=-Xmx16g
INDEXER_XMS=-Xms16g
INDEXER_XMX=-Xmx16g
```
These values will need to be adjusted depending on the instance type.

## Scripts
To run these scripts, be sure to be logged in / switched over to the `openlattice` user.

### To boot the stack
1. First, we boot the conductor service
  - ssh into conductor box
  - switch to openlattice user
  - run the boot script
  - wait for conductor to fully boot up by watching the logs for the banner

```bash
$ ssh conductor
conductor$ sudo su - openlattice
conductor$ ~/scripts/conductor/boot.sh
conductor$ tail -f /opt/openlattice/logging/conductor.log
```
![conductor-banner](https://user-images.githubusercontent.com/440299/152608215-bd982109-dc56-4cdf-953b-10a6392012f4.png)

2. Next, we boot the datastore service
  - ssh into datastore box
  - switch to openlattice user
  - run the boot script
  - wait for datastore to fully boot up by watching the logs for the banner

```bash
$ ssh datastore
datastore$ sudo su - openlattice
datastore$ ~/scripts/datastore/boot.sh
datastore$ tail -f /opt/openlattice/logging/datastore.log
```
![datastore-banner](https://user-images.githubusercontent.com/440299/152608258-4a7a0f60-b10f-454f-b888-6f8a66413abd.png)

3. Finally, we boot the indexer service
  - ssh into indexer box
  - switch to openlattice user
  - run the boot script
  - wait for indexer to fully boot up by watching the logs for the banner

```bash
$ ssh indexer
indexer$ sudo su - openlattice
indexer$ ~/scripts/indexer/boot.sh
indexer$ tail -f /opt/openlattice/logging/indexer.log
```
![indexer-banner](https://user-images.githubusercontent.com/440299/152608311-bbe0b939-f594-4a03-867f-5cef6b7edc17.png)

Once all the services are up and running, the app should be working as expected and talking to the stack via the api:

https://api.openlattice.com
