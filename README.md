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
| `docker-socket-proxy` | Restricted read-only Docker API for Docker-aware consumers |
| `networking` | Traefik reverse proxy |
| `nextcloud` | Nextcloud, Collabora, and PostgreSQL |
| `ntfy` | ntfy notifications |
| `romm` | ROMM and PostgreSQL |
| `renovate` | One-shot dependency update runner for this repository |
| `space-engineers` | Space Engineers server |
| `streaming` | Jellyfin, Wizarr, Navidrome, and Kavita |
| `archive/tdarr` | Archived Tdarr media processing stack (inactive) |
| `vaultwarden` | Vaultwarden |
| `wiksite` | Personal website/blog for the repository owner and a friend |

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

### Service labels and canonical routes

Intentionally reachable services should carry one neutral canonical route:

```yaml
homelab.canonical-route: https://service.74services.net
```

This is the single preferred route for dashboards, future endpoint discovery,
and operational documentation. HTTP routes use `https://`; non-HTTP services
may use an appropriate scheme such as `tcp://`. Traefik aliases may remain in
the router rule, but only one hostname should be used as the canonical route.
Internal-only containers, databases, and infrastructure services should not
define this label. Consumer-specific labels such as `traefik.*`, `mc-router.*`,
and `glance.*` remain necessary for those applications and should not be
treated as the canonical inventory.

## Monitoring

`monitoring/prometheus.yml` scrapes cAdvisor every five seconds. The monitoring stack stores Grafana and InfluxDB data in:

- `/mnt/docker-data/monitoring/grafana-data`
- `/mnt/docker-data/monitoring/influx-data`

The `monitoring/influx-configs` file/directory is mounted into InfluxDB for additional configuration.

Application metrics are also defined in Git:

- Jellyfin is scraped directly at `jellyfin:8096/metrics` over the private
  `monitoring` network. Enable Jellyfin's native metrics in its persistent
  `system.xml` before expecting data; do not expose `/metrics` through Traefik.
- Exportarr runs one private exporter per supported *arr application in
  `mediarr/compose.yaml`. API keys are supplied through the ignored
  `mediarr/.env` file or Komodo variables named in
  [`mediarr/.env.example`](mediarr/.env.example).
- Exportarr targets Sonarr, Radarr, Lidarr, Prowlarr, and Bazarr. Bazarr is
  scraped every 60 seconds because its episode walk can be expensive; the
  other Exportarr targets are scraped every 10 seconds by the global default.

The exporters do not publish host ports or receive Traefik routes. Prometheus
and the exporters use the external `monitoring` network, while exporters also
join the application network needed to query their target. The Prowlarr
exporter queries the VPN network namespace through the `vpn` service.

## Configuration and secrets

Service-specific configuration lives alongside each Compose file. Examples include:

- `factorio/mod-list.json`, `factorio/server-settings.json`, and `factorio/start.sh`
- `minecraft/` world and server configuration files
- `ntfy/server.yml`
- `romm/config.yml`
- `archive/tdarr/configs/`

Renovate is defined in `renovate/compose.yaml` and is intended to be run as a
transient service by Komodo. Its GitHub credentials should be supplied as
Komodo stack environment variables, not committed to the repository. Archived
stacks under `archive/` are excluded by `renovate.json`.

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

## Project plans and AI-agent guidance

Detailed project plans are stored in the [`todo/`](todo/) directory:

- [`todo/renovate.md`](todo/renovate.md) — Renovate, Git hosting, and Komodo execution
- [`todo/authentication.md`](todo/authentication.md) — backend/frontend access control and identity-provider options
- [`todo/knowledge-base.md`](todo/knowledge-base.md) — homelab knowledge organisation system options and deployment plan
- [`todo/dashboard.md`](todo/dashboard.md) — dashboard, service portal, and monitoring overhaul options
- [`todo/networking.md`](todo/networking.md) — private administration routing and network structure
- [`todo/docker-socket-proxy.md`](todo/docker-socket-proxy.md) — Docker socket proxy migration plan and consumer integrations
- [`todo/paperless.md`](todo/paperless.md) — Paperless-ngx document archive evaluation and deployment plan

Repository-reading and safe-change guidance for AI agents is in [`AGENTS.md`](AGENTS.md). Agents should read it before modifying infrastructure, then consult the relevant project plan and [`SECURITY.md`](SECURITY.md).
