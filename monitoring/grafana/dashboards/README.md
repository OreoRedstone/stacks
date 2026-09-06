# Grafana dashboards

All dashboards in this directory are provisioned into Grafana's `Homelab`
folder by `../dashboards.yaml`.

## Dashboard structure

- `overview.json` — fleet-level status and links to detailed dashboards.
- `hosts.json` — Ansible-managed Node Exporter metrics for VPS, Applications VM,
  and Proxmox, selected with the `Host` variable.
- `docker.json` — container metrics from cAdvisor.
- `proxmox.json` — Proxmox metrics from InfluxDB.

## Adding a dashboard

1. Export a classic dashboard JSON compatible with Grafana 12.
2. Remove the database-generated `id` and keep a stable unique `uid`.
3. Use the provisioned datasource UIDs: `stacks-prometheus` or
   `stacks-influxdb`.
4. Add cross-dashboard navigation only to `overview.json`; detail dashboards
   should remain focused and should not create reciprocal menu entries.
5. Add the file to this directory and validate it with `jq empty`.

The provider intentionally keeps all dashboards in one Grafana folder. The
filename is organizational only; the UID is the identity Grafana uses when
reconciling a dashboard.

## Long-term direction

Grafana is the centrepoint for metrics for the foreseeable future. Glance
remains the preferred personal service launcher and quick status page; it does
not need to duplicate Grafana's time-series analysis, alerting, or historical
investigation features.

The intended navigation is:

1. `Homelab Overview` for a quick operational summary and the only
   cross-dashboard navigation menu.
2. `Homelab Hosts` for Ansible-managed host and Node Exporter metrics.
3. `Docker` for container-level resource and network metrics.
4. `Proxmox` for hypervisor, guest, and storage metrics from InfluxDB.
5. Additional focused dashboards as a domain grows, linked from the overview.

## Remaining Grafana improvements

### Dashboard quality

- [ ] Add a fleet status table showing every scrape target, host, and service.
- [ ] Add clear thresholds and value mappings for `UP`, degraded, and failed
  states.
- [ ] Add dashboard-level time-range and refresh conventions consistently.
- [ ] Add useful dashboard links and service links without duplicating Glance's
  full application catalogue.
- [ ] Add annotations for deployments, backups, outages, and major maintenance.
- [ ] Add a small owner-only custom landing page in Grafana if a single starting
  point becomes preferable to the current overview.

### Metrics and data sources

- [ ] Add Node Exporter to any future hosts through Ansible and add their named
  targets to the host dashboard.
- [ ] Add backup freshness and backup size metrics for restic, Borg, or Komodo
  jobs.
- [ ] Add SMART, ZFS, UPS/NUT, GPU, database, Redis, Jellyfin, and WireGuard
  exporters where they provide actionable data.
- [ ] Decide which Proxmox metrics should remain in InfluxDB and whether any
  should also be exported to Prometheus for common dashboard variables.
- [ ] Add Prometheus and InfluxDB self-health panels, including scrape age,
  storage usage, query errors, and retention status.
- [ ] Add service-specific metrics for Nextcloud, Immich, media automation, and
  other applications only when they answer a useful operational question.

### Alerts and operations

- [ ] Provision alert rules from Git for target loss, disk pressure, memory
  pressure, high CPU, elevated Traefik 5xx responses, certificate expiry, and
  stale backups.
- [ ] Route alerts through ntfy with severity-aware notification policies.
- [ ] Add alert links to the relevant dashboard and runbook.
- [ ] Document recovery steps for Grafana, Prometheus, InfluxDB, and their
  persistent data.
- [ ] Test dashboard provisioning after upgrades and verify that UIDs remain
  stable.

### Security and maintainability

- [ ] Keep Grafana, Prometheus, and monitoring endpoints owner-only through the
  chosen VPN/authentication design.
- [ ] Keep datasource credentials out of dashboard JSON and browser-visible
  configuration.
- [ ] Review Docker socket and host-mount exposure whenever a new exporter is
  added.
- [ ] Pin new exporter images by digest after verifying the exact release.
- [ ] Keep dashboard JSON reasonably focused; use a new dashboard when a panel
  group needs its own variables, retention assumptions, or audience.

## Custom landing page idea

Keep this as a future Grafana experiment rather than a separate dashboard
product. A custom landing page could be a provisioned Text panel or a small
owner-only dashboard containing links to the overview, host, Docker, Proxmox,
alert, and runbook views. It should remain optional while the current Glance
landing page is working well.
