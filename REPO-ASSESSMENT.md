# Repository Assessment

Date: 2026-09-19

This is a static audit of the Arr cleanup repository and the adjacent stacks repository. No files were changed during the audit. Docker runtime validation was unavailable because the Docker CLI was not installed in the audit environment.

## Highest-priority findings

### Monitoring failure detection

InfluxDB, Prometheus, cAdvisor, and blackbox-exporter have no healthchecks. The Proxmox dashboard can therefore appear empty without Compose or Komodo clearly reporting a failure.

The existing Proxmox NIC issue also explains intermittent failures to `10.44.0.2:8086`.

Recommended changes:

- Add an InfluxDB healthcheck.
- Add a Proxmox-to-Influx freshness alert.
- Alert when the latest `cpustat` or `memory` sample is stale.
- Mount the Prometheus configuration as read-only.

Relevant files:

- `../stacks/monitoring/compose.yaml`
- `../stacks/monitoring/prometheus.yml`
- `../stacks/monitoring/grafana/dashboards/proxmox.json`

### Timezone inconsistency

Current configuration is mixed:

- `Europe/London`: most Arr services, Wizarr, and Kavita.
- `UTC`: ntfy.
- Missing: Exportarr, Jellyfin, Navidrome, Grafana, Prometheus, InfluxDB, Immich, Nextcloud, Vaultwarden, and several other services.
- Only Sonarr and Radarr currently mount `/etc/localtime`.

Recommended policy:

- Use `TZ=Europe/London` for user-facing media and notification services.
- Retain UTC for metrics and database services unless local display time is required.
- Configure application-level timezone settings separately for Home Assistant, Immich, Nextcloud, and Jellyfin.
- Add `TZ=Europe/London` to Exportarr, Jellyfin, Navidrome, and likely Seerr.
- Decide deliberately whether ntfy schedules should use UTC or local time.

### Authentication and routing

`actual-budget` references `authentik@docker`, but the checked-in networking configuration does not provide a matching Authentik middleware. Several services are exposed through Traefik without explicit authentication labels.

Auth should be applied consistently to browser-facing dashboards and administrative services. Native authentication should remain enabled for applications such as Sonarr, Radarr, Deluge, and databases where integrations depend on it.

### Backup gap

There is no visible active backup and restore system for important state, including:

- Nextcloud
- Immich
- Arr databases
- Grafana dashboards
- InfluxDB
- Game servers
- Vaultwarden

Kopia, Restic/Borgmatic, or Proxmox Backup Server integration would be appropriate. Restore testing should be part of the implementation.

### Image update policy

Most images have digests, but tags communicate inconsistent update channels:

- `latest@digest`
- `develop@digest`
- `main@digest`
- Immich using `${IMMICH_VERSION:-release}` without a digest

The largest concern is `immich2`, where the version is floating and the service is directly exposed on `2283:2283`. Pin it to an explicit version and digest, and route it consistently through Traefik or bind it to the intended interface.

### Healthchecks and restart policies

Many services have no healthcheck, including monitoring, games, networking, Vaultwarden, and several media services. `immich2` uses `restart: always` while most services use `unless-stopped`.

Renovate is configured as a persistent service even though it is fundamentally a scheduled or one-shot job. It should run through Komodo, cron, or `docker compose run --rm`.

## Documentation drift

The main stacks README does not list Cleanuparr or the Exportarr services, despite them being present in `mediarr/compose.yaml`.

It also references TODO files currently deleted in the worktree:

- `todo/dashboard.md`
- `todo/docker-socket-proxy.md`
- `todo/komodo.md`
- `todo/networking.md`

The README, `SECURITY.md`, and actual Compose files should be brought back into agreement.

## Arr-specific assessment

There are now overlapping cleanup responsibilities between:

- this `arr-cleanup` project;
- Cleanuparr; and
- qBittorrent/Deluge cleanup features.

Recommended separation:

- Keep `arr-cleanup` as the read-only reconciliation and reporting tool.
- Use Cleanuparr for carefully scoped operational cleanup.
- Do not allow multiple systems to independently delete files until their candidate logic and exclusions have been compared.

Cleanuparr covers adjacent cases such as stalled downloads, orphaned files, hardlink issues, and torrents no longer referenced by Arr applications, but it should not replace the more explainable reconciliation reports being developed here.

## Recommended additions

### 1. Backup and restore system

Kopia, Restic/Borgmatic, or Proxmox Backup Server integration. This is the highest-value addition.

### 2. Authentik

Central identity, MFA, and browser access control for services behind Traefik.

### 3. Paperless-ngx

Useful alongside Nextcloud and Actual Budget for searchable OCR document storage and API access.

### 4. Forgejo

Self-hosted Git, issue tracking, and Actions. It pairs well with Renovate and Komodo.

### 5. Uptime Kuma

Useful if a simple operator-facing status UI is wanted. Prometheus and blackbox-exporter already provide the underlying monitoring, so this is optional.

### 6. Dozzle

Convenient container-log viewing, but lower priority because Komodo already provides management functionality.

## Suggested implementation order

1. Add monitoring healthchecks and Influx freshness alerts.
2. Define and document the timezone policy.
3. Fix Authentik middleware and routing inconsistencies.
4. Implement and test backups.
5. Pin remaining floating images.
6. Update the stack inventory and remove or restore stale documentation.
7. Add Paperless-ngx and Forgejo.
8. Reassess whether Uptime Kuma or Dozzle adds enough value.

The next useful application is probably a backup system rather than another dashboard.
