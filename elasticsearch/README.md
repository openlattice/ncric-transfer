## Mount EBS Volume
Attach an EBS volume to the box (assume device is `/dev/xvdb`). Initially, it's not formatted:
```bash
[ubuntu ~]$ sudo file -s /dev/xvdb
/dev/xvdb: data
```

Format is as XFS:
```bash
[ubuntu ~]$ sudo mkfs.xfs /dev/xvdb
[ubuntu ~]$ sudo file -s /dev/xvdb
/dev/xvdb: SGI XFS filesystem data (blksz 4096, inosz 512, v2 dirs)
```

Update `/etc/fstab` to mount at `/opt/elasticsearch`:
```bash
UUID=<device uuid> /opt/elasticsearch xfs defaults,nofail 0 2
```

Mount:
```bash
[ubuntu ~]$ sudo mount -a
```

## Java
Install Java 11.

```bash
[ubuntu ~]$ sudo apt install openjdk-11-jdk
[ubuntu ~]$ java --version
openjdk 11.0.13 2021-10-19
OpenJDK Runtime Environment (build 11.0.13+8-Ubuntu-0ubuntu1.20.04)
OpenJDK 64-Bit Server VM (build 11.0.13+8-Ubuntu-0ubuntu1.20.04, mixed mode)
```

Set `JAVA_HOME`:
```bash
[ubuntu ~]$ echo "JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64" | sudo tee -a /etc/environment
[ubuntu ~]$ source /etc/environment
```

## Elasticsearch Configuration
Install elasticsearch.

https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html

```bash
[ubuntu ~]$ wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
[ubuntu ~]$ sudo apt-get install apt-transport-https
[ubuntu ~]$ echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
[ubuntu ~]$ sudo apt update && sudo apt install elasticsearch
```

Create the `data` and `logs` directories, and set `group` and `owner` to `elasticsearch`.
```bash
[ubuntu ~]$ sudo mkdir -p /opt/elasticsearch/data
[ubuntu ~]$ sudo mkdir -p /opt/elasticsearch/logs
[ubuntu ~]$ sudo chown -R elasticsearch:elasticsearch /opt/elasticsearch
```

Install the "analysis-phonetic" plugin.
```bash
[ubuntu ~]$ sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install analysis-phonetic
-> Downloading analysis-phonetic from elastic
[=================================================] 100%  
-> Installed analysis-phonetic
```

Update limits in `/etc/security/limits.conf`.
```bash
* soft nofile  300000
* hard nofile  300000
* hard memlock unlimited
* soft memlock unlimited
elasticsearch soft memlock unlimited
elasticsearch hard memlock unlimited
```

Set overrides in `/etc/systemd/system/elasticsearch.service.d/override.conf`:
```bash
[Service]
LimitMEMLOCK=infinity
LimitNOFILE=300000
```

