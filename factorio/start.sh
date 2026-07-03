#!/bin/sh
set -eu

mkdir -p /factorio/mods /factorio/config
cp /tmp/mod-list.json /factorio/mods/mod-list.json
cp /tmp/server-settings.json /factorio/config/server-settings.json

exec /docker-entrypoint.sh