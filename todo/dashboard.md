# Dashboard overhaul

## Goal

Review the current Glance and monitoring setup and decide whether to combine the service launcher, homelab overview, status information, and metrics into one dashboard experience or keep specialised dashboards linked together. The dashboard and monitoring interfaces are for the owner only; they do not need household or guest views.

## Current state

- `glance/` provides the main portal and service links/widgets.
- `monitoring/` provides Grafana, Prometheus, InfluxDB, and cAdvisor.
- Grafana is routed through Traefik at `monitoring.74services.net`.
- Glance currently publishes a host port directly and mounts the Docker socket read-only.
- Prometheus currently scrapes cAdvisor; InfluxDB is also exposed separately.
- Glance configuration includes GitHub token references and service links.
- Authentication and backend/frontend access policies are being planned separately in [`authentication.md`](authentication.md).

## Observed current dashboard experience

The supplied Glance screenshot shows a polished application portal with:

- A calendar and service-health monitor.
- Media links for Immich, Jellyfin, Kavita, Navidrome, Nextcloud, ROMM, and Wizarr.
- Media automation links for Bazarr, Bindery, Deluge, Lidarr, Prowlarr, Radarr, Seerr, and Sonarr.
- Management links for Glance, Grafana, Home Assistant, and Komodo.
- Security and networking links for Vaultwarden and Traefik.
- GitHub repository activity, pull requests, issues, and release cards.

The two supplied Grafana exports cover different layers:

1. A Proxmox/host dashboard backed by InfluxDB and Flux, with per-server repeated rows for CPU, memory, storage, and host statistics.
2. A Docker/cAdvisor dashboard backed by Prometheus, including running-container count, total memory usage, CPU usage, and container-level graphs.

This means the current setup already has a useful split between a service portal and detailed observability. A replacement should avoid rebuilding the detailed Grafana time-series work unless it can preserve the InfluxDB/Flux and Prometheus queries.

Specific consolidation opportunities:

- [ ] Add links from Glance directly to the relevant Grafana dashboards and preserve Grafana for time-range analysis.
- [ ] Add a compact Grafana summary panel or image/link to the portal rather than duplicating every graph in Glance.
- [ ] Add container count, host CPU, memory, storage, and backup freshness as a small overview layer.
- [ ] Decide whether to keep the Proxmox InfluxDB dashboard separate from the Docker Prometheus dashboard.
- [ ] Add a dashboard variable or consistent host naming scheme across both data sources.
- [ ] Add service availability and container health separately from resource utilisation.
- [ ] Remove duplicate service entries where Glance’s monitor widget and Docker category widgets show the same service.
- [ ] Keep GitHub repository activity only if it remains useful after the Git-provider decision.

## Desired outcomes

- [ ] One obvious landing page for the owner.
- [ ] Provide one owner/admin view.
- [ ] Clear service health/status indicators.
- [ ] Links to every active application.
- [ ] Useful host, Docker, storage, network, and service metrics.
- [ ] No unnecessary Docker socket exposure.
- [ ] No API keys rendered into browser-side configuration.
- [ ] Authentication compatible with the eventual Authentik, Authelia, Keycloak, or VPN design.
- [ ] Mobile-friendly layout.
- [ ] Easy configuration backup and restore.
- [ ] Archived services excluded from the dashboard.

## Option 1: Keep Glance as the portal and Grafana as monitoring

Use Glance for navigation, feeds, quick service status, and homelab summaries. Link to Grafana for detailed metrics and alert investigation.

Pros:

- Smallest change from the current setup.
- Glance is well suited to a personal start page and configurable YAML layouts.
- Grafana remains the right tool for time-series exploration, dashboards, and alerts.
- Failure of Grafana does not necessarily remove the service launcher.
- Low migration effort.

Cons:

- Two interfaces and two configuration systems.
- Glance’s Docker integration requires careful socket handling.
- High-level health and detailed metrics remain split.
- Users may not know whether to open Glance or Grafana.

Tasks:

- [ ] Remove Glance’s Docker socket if the Docker widget is not essential.
- [ ] If it is essential, replace the host socket with a restricted Docker socket proxy.
- [ ] Put Glance behind the selected authentication policy instead of direct host-port access.
- [ ] Add a prominent Grafana link and a small set of Grafana overview links.
- [ ] Create Grafana dashboards for host resources, Docker containers, storage, network, and backup freshness.
- [ ] Add health/status links for Traefik and critical services.
- [ ] Keep a single owner/admin Glance page.

Reference: https://github.com/glanceapp/glance

## Option 2: Use Grafana as the unified dashboard

Make Grafana the primary portal and use Grafana panels, links, and dashboards for both service navigation and monitoring.

Pros:

- One central interface for monitoring and service links.
- Strong visualisation, alerting, variables, annotations, and time ranges.
- Good OIDC support potential with the future identity provider.
- Excellent for backend/management views.
- Can combine Prometheus and InfluxDB data sources.

Cons:

- Not a natural application launcher.
- Less useful for a simple single-user service launcher.
- Grafana failure removes both the portal and monitoring view.
- Requires more dashboard design work.

Tasks:

- [ ] Decide whether Prometheus or InfluxDB should be the primary metrics store.
- [ ] Add all required exporters and scrape targets.
- [ ] Create an infrastructure overview dashboard.
- [ ] Create an application-health dashboard.
- [ ] Add dashboard links to active services.
- [ ] Configure alert rules and notification routing.
- [ ] Keep Grafana dashboards owner/admin-only.
- [ ] Keep a direct recovery URL and local admin account.

## Option 3: Replace Glance with Homepage

Homepage is a service dashboard focused on application links and integrations, with widgets for many common homelab services.

Pros:

- Strong application/service integration model.
- Good fit for Docker, media, and homelab services.
- Configuration is file-based and suitable for Git backup.
- Can complement Grafana without trying to replace it.

Cons:

- Another migration and another dashboard configuration format.
- Integration credentials must be protected carefully.
- May still require Docker access or API tokens for the desired widgets.
- Detailed monitoring remains in Grafana.

Compatibility to test:

- Jellyfin, Seerr, Sonarr, Radarr, Lidarr, Prowlarr, Bazarr, Deluge, Immich, Nextcloud, Home Assistant, Traefik, and Uptime Kuma integrations.
- Traefik routing and future OIDC/forward-auth.
- Read-only Docker integration without exposing excessive metadata.

Reference: https://gethomepage.dev/

## Option 4: Replace Glance with Homarr

Homarr is a user-oriented dashboard with boards, integrations, widgets, Docker discovery, user access, and OIDC/LDAP support.

Pros:

- Strong candidate if richer integrations are more important than Git-managed configuration.
- Integrations include Jellyfin, Seerr, the Arr stack, Home Assistant, Immich, Navidrome, Nextcloud, ntfy, Traefik, and Docker.
- Supports boards and users, including public/private board concepts.
- Supports internal authentication, LDAP, and OIDC.
- Integration secrets are intended to remain server-side rather than being passed to the browser.

Cons:

- More application state and database/storage management than Glance.
- UI configuration may be less naturally Git-reviewed than Glance YAML.
- Docker discovery still requires careful socket handling.
- Requires testing against the eventual identity provider and owner workflow.

Compatibility to test:

- Admin board for Komodo, Grafana, Traefik, monitoring, and media automation.
- Household board for Jellyfin, Seerr, Wizarr, Navidrome, and Kavita.
- OIDC with Authentik, Authelia, or Keycloak.
- API integrations and token handling.

Reference: https://homarr.dev/docs/

## Option 5: Replace Glance with Dashy

Dashy is a configurable dashboard with pages, sections, widgets, status indicators, search, theming, REST API support, and built-in/OIDC/proxy authentication options.

Pros:

- Broad layout and authentication options.
- Multiple pages can separate management and media views.
- Good status indicators and widget support.
- REST API may help automate service entries.
- Supports OIDC and reverse-proxy authentication.

Cons:

- Configuration and authentication need careful hardening.
- Built-in client-side authentication should not be treated as the main security boundary.
- Can become configuration-heavy.
- Detailed metrics still belong in Grafana.

Compatibility to test:

- Traefik with the future authentication provider.
- Single owner/admin page.
- Status checks for all public hostnames.
- API/widget secret exposure.

Reference: https://dashy.to/docs/

## Option 6: Use a dedicated status page plus Grafana

Use Uptime Kuma, Gatus, or a similar tool for service availability, Grafana for metrics, and either Glance or a simple static homepage for links.

Pros:

- Clear separation between availability, metrics, and navigation.
- Useful incident history and notifications.
- Does not require a dashboard to expose the Docker socket.
- Better monitoring semantics than simple HTTP status widgets.

Cons:

- Three interfaces instead of one.
- More services to maintain and back up.
- More links and authentication policies to manage.

Tasks:

- [ ] Compare Uptime Kuma and Gatus.
- [ ] Monitor HTTP, TCP, UDP, DNS, certificates, and critical container health.
- [ ] Send alerts through ntfy.
- [ ] Link status pages from the primary dashboard.

## Option 7: Build a custom dashboard

Extend the existing Glance configuration or create a small custom frontend that combines links, health checks, and selected metrics.

Pros:

- Precisely matches the desired workflow.
- Can use the existing `wiksite` technology if appropriate, while keeping `wiksite` itself separate as the personal website/blog.
- Can avoid broad integrations and expose only selected data.

Cons:

- Ongoing development and security responsibility.
- More difficult upgrades and testing.
- Easy to create a bespoke system that only one person understands.
- Not recommended until the requirements are stable.

## Comparison

| Option | Navigation | Metrics | Household users | Git-friendly config | Auth potential | Complexity |
| --- | --- | --- | --- | --- | --- | --- |
| Glance + Grafana | Good | Excellent | Medium | High | Medium | Low |
| Grafana only | Medium | Excellent | Low/medium | Medium | High | Medium |
| Homepage + Grafana | Excellent | Excellent via Grafana | Medium | High | Medium | Low/medium |
| Homarr + Grafana | Excellent | Excellent via Grafana | High | Medium | High | Medium |
| Dashy + Grafana | Excellent | Excellent via Grafana | Medium/high | High | High | Medium |
| Status page + Grafana | Medium | Excellent | Medium | Medium | High | Medium/high |
| Custom dashboard | Custom | Custom | Custom | Custom | Custom | High |

## Recommended evaluation order

1. Improve the existing Glance + Grafana split first.
2. Trial Homarr if rich integrations and interactive configuration are the priority.
3. Trial Homepage if a simpler Git-managed application launcher is preferred.
4. Trial Dashy if multiple pages, status indicators, and flexible authentication are important.
5. Consider Grafana-only for an admin-focused interface.

## Migration plan

- [ ] Export or copy current Glance configuration and assets.
- [ ] Inventory active services and remove archived Tdarr links.
- [ ] Inventory which dashboard widgets require API keys.
- [ ] Decide which metrics belong in Prometheus versus InfluxDB.
- [ ] Define one private owner/admin view.
- [ ] Choose the dashboard hostname.
- [ ] Deploy the candidate alongside Glance for comparison.
- [ ] Route it through Traefik with explicit backend port labels.
- [ ] Apply authentication only after an independent recovery path exists.
- [ ] Test mobile access, bookmarks, direct service links, APIs, and WebSockets.
- [ ] Test backup and restore of configuration, database, and assets.
- [ ] Run both dashboards in parallel for at least one week.
- [ ] Decide whether to retain, archive, or remove Glance.
- [ ] Update README, Renovate coverage, and SECURITY.md.

## Security checklist

- [ ] Do not expose Docker socket access unless necessary.
- [ ] If required, use a restricted Docker socket proxy.
- [ ] Keep integration API keys server-side and read-only where possible.
- [ ] Do not put database credentials or recovery secrets in dashboard configuration.
- [ ] Avoid direct host-port publishing for the dashboard.
- [ ] Use Traefik and the selected authentication policy.
- [ ] Keep an unauthenticated local recovery path or host-level access.
- [ ] Review what information is visible on the private dashboard.
- [ ] Ensure dashboard status checks do not leak internal hostnames or sensitive metadata.

## References

- Glance: https://github.com/glanceapp/glance
- Homepage: https://gethomepage.dev/
- Homarr: https://homarr.dev/docs/
- Dashy: https://dashy.to/docs/
- Grafana: https://grafana.com/docs/grafana/latest/
# Implemented observability expansion

The monitoring stack now has the first broader observability layer defined in Git:

- Node Exporter is installed and managed by the infrastructure Ansible playbook on every inventory host. Prometheus scrapes the hosts over the WireGuard management network, so host metrics are no longer coupled to the monitoring Compose stack.
- Prometheus scrapes itself, cAdvisor, Node Exporter, Traefik, and Blackbox Exporter.
- Traefik exposes Prometheus metrics only on the internal `monitoring` Docker network; its metrics port is not published to the host.
- Blackbox Exporter probes selected public HTTPS endpoints and accepts normal success, redirect, and authentication statuses. This tests reachability/TLS/routing without needing application credentials.
- `Homelab Overview` provides a starting point for target health, host resource pressure, container count, Traefik traffic/errors, and public endpoint availability.

## Provisioning and existing dashboards

The existing Docker and Proxmox dashboards retain their UIDs and remain managed by the existing file provider. Grafana will reconcile a provisioned dashboard when its JSON has the same UID as a dashboard already in Grafana. Therefore, changes to those JSON files can overwrite UI edits to those dashboards. The provider currently has `allowUiUpdates: false`, so edits should be made in Git and redeployed.

The new overview dashboard has a new UID and will be created in the `Homelab` folder. Existing dashboards with other UIDs remain in place because `disableDeletion: true`; removing a JSON file from Git does not delete the corresponding dashboard from Grafana. This is intentionally conservative, but it also means stale provisioned dashboards must be removed manually if they are ever retired.

## Rollout

1. Deploy or restart the networking stack first so it creates the external `monitoring` network and Traefik starts its internal metrics entrypoint.
2. Deploy or restart the monitoring stack.
3. In Grafana, check `Connections > Data sources` and confirm Prometheus is healthy.
4. Check Prometheus `Status > Targets`; `prometheus`, `cadvisor`, `node`, and `traefik` should be `UP`. Blackbox targets should be `UP` when the host can resolve and reach the public domains (hairpin NAT/DNS can affect this).
5. Open `Homelab Overview` and confirm the panels have data.

The new exporter images currently use version tags rather than digests because the image digests have not yet been verified. Pin them after pulling/inspecting the exact images, and keep them under Renovate management.

## Follow-up improvements

- Confirm Node Exporter is reachable on all three WireGuard addresses after the Ansible run. The firewall permits port 9100 only from the management VPN and local Docker bridge ranges.
- Add explicit backup-freshness metrics and alerting for restic/borg/Komodo jobs.
- Add SMART, ZFS, UPS/NUT, GPU, database, Redis, Jellyfin, and WireGuard exporters where those systems expose useful data.
- Add Prometheus alert rules for target loss, high disk usage, memory pressure, certificate expiry, elevated HTTP 5xx rates, and stale backups.
- Review the public Blackbox target list and add/remove endpoints according to the actual externally required services.
