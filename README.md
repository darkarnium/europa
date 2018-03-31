## Europa API

This repository contains the API service for the Europa project.

### Samples

#### `europa-api.cfg`

A sample override configuration file for the Europa API.

```
DEBUG=False
TESTING=False
JSON_AS_ASCII=False
SQLALCHEMY_DATABASE_URI='postgresql://europa:pass@127.0.0.1/europa'
SQLALCHEMY_TRACK_MODIFICATIONS=False
```

#### `europa-poller.service`

A sample systemd Europa Poller unit file has been included below.

```
[Unit]
Description=Europa Poller
After=syslog.target

[Service]
Type=simple
User=root
WorkingDirectory=/tmp/
ExecStart=/usr/bin/python3 /opt/europa-api/src/europa/poller/poller.py
StandardOutput=syslog
StandardError=syslog

[Install]
WantedBy=multi-user.target
```

#### `europa-api.service`

A sample systemd Europa API unit file has been included below.

```
[Unit]
Description=Europa API
After=syslog.target

[Service]
Type=simple
User=europa
WorkingDirectory=/opt/europa-api
ExecStart=/usr/bin/python3 /opt/europa-api/src/application.py /opt/europa-api/api.cfg
StandardOutput=syslog
StandardError=syslog

[Install]
WantedBy=multi-user.target
```
