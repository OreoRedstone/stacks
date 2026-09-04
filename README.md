# Homelab stacks

Docker Compose definitions and service configuration for a self-hosted homelab. Each directory is an independent stack that can be started, updated, and stopped separately.

## Stacks

| Directory | Services / purpose |
| --- | --- |
| `actual-budget` | Actual Budget |
| `auth` | Authentik and PostgreSQL |
| `backups` | Restic backup job |
| `factorio` | Factorio server and server configuration |
| `glance` | Glance dashboard |
| `home-assistant` | Home Assistant |
| `immich` | Immich photo server, machine learning, Redis, and PostgreSQL |
| `mediarr` | Deluge, Prowlarr, Sonarr, Radarr, Lidarr, Bazarr, Seerr, Bindery, and FlareSolverr |
| `minecraft` | Minecraft router and multiple servers, including ATM10 and JJK worlds |
| `monitoring` | Grafana, Prometheus, InfluxDB, and cAdvisor |
| `networking` | Traefik reverse proxy |
| `nextcloud` | Nextcloud, Collabora, and PostgreSQL |
| `ntfy` | ntfy notifications |
| `romm` | ROMM and PostgreSQL |
| `space-engineers` | Space Engineers server |
| `streaming` | Jellyfin, Wizarr, Navidrome, and Kavita |
| `archive/tdarr` | Archived Tdarr media processing stack (inactive) |
| `vaultwarden` | Vaultwarden |
| `wiksite` | Wiki site |

## Prerequisites

- Docker Engine with the Compose plugin (`docker compose`)
- Persistent storage mounted at `/mnt/docker-data` for stacks that use host-mounted data
- A DNS setup for the hostnames configured in the Compose labels
- A Docker network named `traefik`; the networking stack creates it

Start the proxy first:

```sh
cd networking
docker compose up -d
```

## Running a stack

From the repository root, run Compose in the directory for the service you want:

```sh
cd monitoring
docker compose up -d
docker compose ps
docker compose logs -f
```

Stop a stack with:

```sh
docker compose down
```

The Compose files pin container images by digest where applicable. Review image updates and configuration changes before recreating services.

## Reverse proxy and networking

Traefik is defined in `networking/compose.yaml`. It listens on host port `9999` and routes services attached to the external `traefik` network using Docker labels. Most web-facing stacks join this network and do not publish their application ports directly.

The `monitoring` stack exposes InfluxDB on host port `8086`. Grafana is routed through Traefik at the hostname configured in its labels. Hostnames and TLS behavior are managed through the Traefik configuration in `networking/dynamic.yaml` and the labels in each stack.

## Monitoring

`monitoring/prometheus.yml` scrapes cAdvisor every five seconds. The monitoring stack stores Grafana and InfluxDB data in:

- `/mnt/docker-data/monitoring/grafana-data`
- `/mnt/docker-data/monitoring/influx-data`

The `monitoring/influx-configs` file/directory is mounted into InfluxDB for additional configuration.

## Configuration and secrets

Service-specific configuration lives alongside each Compose file. Examples include:

- `factorio/mod-list.json`, `factorio/server-settings.json`, and `factorio/start.sh`
- `minecraft/` world and server configuration files
- `ntfy/server.yml`
- `romm/config.yml`
- `archive/tdarr/configs/`

Do not commit passwords, tokens, private keys, or generated application data. The repository currently contains initialization values in some Compose files, so replace those values with secure secrets before exposing services and rotate any credentials that have been used outside a disposable environment. Files matching `.env` and `.log` are ignored by Git.

## Updating services

Review a stack's Compose file, pull the pinned images, and recreate only that stack:

```sh
cd <stack-directory>
docker compose pull
docker compose up -d
docker compose ps
```

Check the service logs after updates and make sure persistent data and backups are healthy before removing old images.
