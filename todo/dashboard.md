# Dashboard roadmap

## Direction

Grafana is the metrics centrepoint for the foreseeable future. Glance is
working well as the personal service launcher and quick status page, so there
is no current plan to replace it or duplicate its full application catalogue
inside Grafana.

The current split is:

- Glance: personal landing page, service links, feeds, and quick availability.
- Grafana: historical metrics, dashboards, variables, alerting, and incident
  investigation.
- Prometheus: host, container, proxy, and endpoint metrics.
- InfluxDB: existing Proxmox metrics and Flux dashboards.

## Current Grafana dashboards

- `Homelab Overview` — fleet status, host summary, container count, public
  probes, and links to detailed views.
- `Homelab Hosts` — Ansible-managed Node Exporter metrics for VPS,
  Applications VM, and Proxmox, selected by friendly host name.
- `Docker` — cAdvisor container resource and network metrics.
- `Proxmox` — Proxmox and guest metrics from InfluxDB.

Dashboard JSON is stored in `monitoring/grafana/dashboards/`. All dashboards
are provisioned into Grafana's `Homelab` folder. Stable UIDs are required for
safe reconciliation and URL stability.

## Remaining work

### Dashboard quality

- [ ] Add a fleet status table covering every Prometheus scrape target.
- [ ] Add consistent thresholds and value mappings for healthy, degraded, and
  failed states.
- [ ] Standardise dashboard time ranges, refresh intervals, units, and legends.
- [ ] Add deployment, backup, outage, and maintenance annotations.
- [ ] Add focused dashboards only when a service or metric group warrants its
  own variables and troubleshooting workflow.
- [ ] Keep the optional custom Grafana landing page idea available: an
  owner-only page with links to dashboards, alerts, and runbooks.

### Metrics

- [ ] Prioritise Jellyfin metrics: server health, active sessions, playback
  method, transcoding activity, stream errors, bandwidth, and library or
  scheduled-task health where supported.
- [ ] Prioritise mediarr metrics: Sonarr, Radarr, Lidarr, Bazarr, Prowlarr,
  Seerr, Bindery, Deluge, Gluetun, and FlareSolverr availability, queue size,
  download activity, indexer health, failures, and VPN status.
- [ ] Decide which Jellyfin and mediarr metrics should be collected through
  native exporters, application APIs, Docker healthchecks, or existing
  cAdvisor/Traefik metrics before adding exporters.
- [ ] Add Node Exporter to future hosts through Ansible and assign each a
  friendly Prometheus `host` label.
- [ ] Add backup freshness, backup size, and backup failure metrics for restic,
  Borg, and Komodo jobs.
- [ ] Add SMART, ZFS, UPS/NUT, GPU, database, Redis, Jellyfin, and WireGuard
  exporters where they provide actionable information.
- [ ] Add Prometheus and InfluxDB self-health panels for scrape age, storage,
  query errors, and retention.
- [ ] Add useful application metrics for Nextcloud, Immich, and media services
  without turning Grafana into a duplicate service launcher.

### Alerting and operations

- [ ] Provision alert rules from Git for target loss, disk pressure, memory
  pressure, high CPU, Traefik 5xx responses, certificate expiry, and stale
  backups.
- [ ] Route alerts through ntfy with severity-aware notification policies.
- [ ] Link alerts to the relevant dashboard and an actionable runbook.
- [ ] Document recovery for Grafana, Prometheus, InfluxDB, and persistent data.
- [ ] Test dashboard provisioning after Grafana upgrades and keep UIDs stable.

### Security and maintainability

- [ ] Keep Grafana, Prometheus, and monitoring endpoints owner-only through the
  chosen VPN/authentication design.
- [ ] Keep datasource credentials out of dashboard JSON and browser-visible
  configuration.
- [ ] Review Docker socket and host-mount exposure whenever an exporter is
  added.
- [ ] Pin new exporter images by digest after verifying the exact release.
- [ ] Keep Glance's current deployment unchanged unless a specific need emerges.
