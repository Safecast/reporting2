#!/usr/bin/env bash

set -e

if rpm -q grafana; then
  echo "Grafana already installed."
  exit 0
fi

wget https://dl.grafana.com/oss/master/grafana-7.2.0~f3e4bfd9pre-1.x86_64.rpm
sudo yum install grafana-7.2.0~f3e4bfd9pre-1.x86_64.rpm

/usr/sbin/grafana-cli plugins install petrslavotinek-carpetplot-panel
/usr/sbin/grafana-cli plugins install grafana-worldmap-panel
/usr/sbin/grafana-cli plugins install grafana-googlesheets-datasource
/usr/sbin/grafana-cli plugins install simpod-json-datasource
/usr/sbin/grafana-cli plugins install dalvany-image-panel


/usr/sbin/grafana-cli --pluginUrl https://github.com/panodata/grafana-map-panel/archive/4f4765b68b2c02ca7de2b36dcc24349b5e10ef47.zip plugins install grafana-worldmap-panel-ng

/sbin/chkconfig --add grafana-server
/sbin/service grafana-server start

ls -ll -a
