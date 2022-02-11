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

