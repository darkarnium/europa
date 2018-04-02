![](https://github.com/darkarnium/europa/raw/master/docs/images/europa.png?raw=true)

This repository contains the API and UI service for the Europa project.

### What is it?

The Europa project is a Saturday afternoon project to monitor various parameters
relating to indoor plants. It uses a number of sensors and an LED grow light
in order test for, and modify, current environmental conditions.

This is by no means a serious project and has been developed for 'funsies'.

This project has been built with the following equipment:

  * Raspberry Pi Zero.
  * DS18B20 waterproof sensor (in-soil).
  * AM2302 temperature and humidity sensor (ambient).
  * TP-Link HS-100 Smartplug.

### API Security

There isn't any. It's a free for all!

### UI

The UI in its current form is very simple, it simply uses jQuery, Bootstrap,
Moment.js, popper.js, and Chart.js to graph the last 24-hours of sensor data.

![](https://github.com/darkarnium/europa/raw/master/docs/images/ui-capture.png?raw=true)

### Polling

In order to populate the API with data from sensors, some form of poller is
required. For completeness, a sample poller has been included in this repository
with additional information available under `src/poller/README.md`.

### Samples

#### `poller.py`

As above, a sample poller has been included. Please see the `poller` directory
under `src/` for additional information.

#### `europa-api.cfg`

A sample override configuration file for the Europa API. This is used to
instruct SQLAlchemy which database should be used. By default, without this
file, SQLAlchemy will create a new SQLite database in memory.

Although this is sufficent for testing, any data saved will be lost when the
service restarts. As a result, a persistent backend should be used (such as
PostgreSQL, as below).

```
DEBUG=False
TESTING=False
JSON_AS_ASCII=False
SQLALCHEMY_DATABASE_URI='postgresql://europa:pass@127.0.0.1/europa'
SQLALCHEMY_TRACK_MODIFICATIONS=False
```

#### `europa-poller.service`

A sample systemd Europa Poller unit file has been included below. Currently, the
poller runs as the `root` user as the libraries used in this poller require this
level of privileges to read GPIO and 1-Wire sensors. This may change in future,
but this is sufficent for the moment given the 'one-shot' nature of the machine
on which this code runs.

```
[Unit]
Description=Europa Poller
After=syslog.target

[Service]
Type=simple
User=root
WorkingDirectory=/tmp/
ExecStart=/usr/bin/python3 /opt/europa/src/poller/poller.py
StandardOutput=syslog
StandardError=syslog

[Install]
WantedBy=multi-user.target
```

#### `europa-api.service`

A sample systemd Europa API unit file has been included below. This is the main
interface for the Europa service, into which poller data will be written, and
from which sensor data can be retrieved.

This assumes that this repository has been cloned into `/opt/europa-api` and 
that there is a user named `europa` which has access to this directory. It also
assumes that the `europa-api.cfg` sample, listed above, has been written into
a file called `/opt/europa/api.cfg`.

```
[Unit]
Description=Europa API
After=syslog.target

[Service]
Type=simple
User=europa
WorkingDirectory=/opt/europa
ExecStart=/usr/bin/python3 /opt/europa/src/application.py /opt/europa/api.cfg
StandardOutput=syslog
StandardError=syslog

[Install]
WantedBy=multi-user.target
```
