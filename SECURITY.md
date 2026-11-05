# Security findings and remediation

Last reviewed: 2026-09-07

## Public release review — 2026-11-05

Publication is still blocked pending secret rotation and a full history scan.
This review does not certify the environment as free of vulnerabilities.

- Removed the archived Tdarr authentication secret from the working tree.
  Local history was rewritten with git-filter-repo and the exact value was
  verified absent from all reachable Git objects. GitHub has not been updated;
  remote refs and other clones still require cleanup. Invalidate the key
  anywhere it was used before publishing.
  Archived Tdarr still has authentication disabled and must remain inactive.
- Made the Prometheus and Traefik configuration mounts read-only and changed
  Seerr logging from debug to info. Deployment verification is outstanding.
- Added ignore patterns for local environment variants and common private-key
  files. Ignore rules do not protect already tracked files or history.
- Searched reachable Git blobs for PEM private-key headers; none were found.
  This is a limited check, not a complete secret scan.
- Docker, Gitleaks, and Trivy were unavailable locally. Compose validation,
  comprehensive secret scanning, image vulnerability scanning, and runtime
  access checks remain outstanding.
- The privileged Docker socket proxy remains a critical trust boundary.
  `POST=0` and a read-only socket mount do not guarantee that permitted GET
  endpoints cannot disclose secrets. Review the pinned implementation against
  the upstream [filesystem exposure report](https://github.com/Tecnativa/docker-socket-proxy/pull/183)
  and verify endpoint restrictions before treating consumers as isolated.

The findings below are the earlier review inventory; changes listed above
are repository fixes awaiting deployment verification, not closed findings.

This is a repository-level review of tracked Compose files and service
configuration. It is not a host audit, vulnerability scan, or confirmation
that a service is currently running. `archive/` is not deployed, but archived
files remain relevant because they are still part of the repository and its
history.

Status values are `OPEN`, `IN PROGRESS`, and `DONE`. A finding should be marked
`DONE` only after the change is deployed and the relevant behavior has been
verified.

## High

| Status | Finding | Location | Recommended fix |
| --- | --- | --- | --- |
| OPEN | Archived Tdarr configuration has authentication disabled and contains a committed authentication secret. | [`archive/tdarr/configs/Tdarr_Server_Config.json:12-17`](archive/tdarr/configs/Tdarr_Server_Config.json#L12-L17) | Treat the secret as exposed: rotate it, remove it from reachable history where appropriate, enable authentication before reactivation, keep the UI internal, and protect any route with authentication. |
| OPEN | The Docker socket proxy runs privileged and has read-only access to the host Docker socket. | [`docker-socket-proxy/compose.yaml:3-18`](docker-socket-proxy/compose.yaml#L3-L18) | Keep the proxy isolated and unpublished, verify enabled API sections, and test whether the image can run without `privileged: true`. Review every consumer after changing the boundary. |
| OPEN | cAdvisor has broad read-only host mounts, including the host root, `/sys`, and Docker’s data directory. | [`monitoring/compose.yaml:73-86`](monitoring/compose.yaml#L73-L86) | Retain only mounts required by the selected cAdvisor mode, keep them read-only, pin the image, and treat cAdvisor as a host-observability component. |
| IN PROGRESS | Grafana still runs explicitly as root for a permissions workaround, and the Docker socket proxy remains privileged/root-equivalent. Archived Tdarr also retains `PUID=0`/`PGID=0`, but is not deployed. The media and streaming services have been changed in Compose to use UID/GID `1000:1000`; deployment verification remains outstanding. | [`monitoring/compose.yaml:3-7`](monitoring/compose.yaml#L3-L7), [`docker-socket-proxy/compose.yaml:2-18`](docker-socket-proxy/compose.yaml#L2-L18), [`archive/tdarr/compose.yaml:1-24`](archive/tdarr/compose.yaml#L1-L24), [`streaming/compose.yaml:3-11`](streaming/compose.yaml#L3-L11), [`streaming/compose.yaml:61-71`](streaming/compose.yaml#L61-L71), [`streaming/compose.yaml:84-92`](streaming/compose.yaml#L84-L92), [`mediarr/compose.yaml:199-213`](mediarr/compose.yaml#L199-L213) | Migrate Grafana to a documented unprivileged UID/GID after correcting its data-volume ownership, assess whether the socket proxy can run without `privileged: true`, and keep archived Tdarr inactive until its configuration is reviewed. Verify the media-stack deployment and make media mounts read-only wherever writes are not required. |

## Medium

| Status | Finding | Location | Recommended fix |
| --- | --- | --- | --- |
| OPEN | Glance and InfluxDB publish host ports on the WireGuard address, and Deluge publishes its Web UI and daemon port there through Gluetun. | [`glance/compose.yaml:11-15`](glance/compose.yaml#L11-L15), [`monitoring/compose.yaml:54-67`](monitoring/compose.yaml#L54-L67), [`mediarr/compose.yaml:3-14`](mediarr/compose.yaml#L3-L14) | Confirm the WireGuard interface is the intended trust boundary, restrict it with host firewall rules, prefer private proxy/VPN access, and remove direct publication where unnecessary. Keep Deluge native authentication enabled. |
| OPEN | Traefik’s edge port is published on all host interfaces, while no checked-in authentication middleware is attached to the Traefik service itself. | [`networking/compose.yaml:6-24`](networking/compose.yaml#L6-L24), [`networking/dynamic.yaml`](networking/dynamic.yaml) | Confirm upstream firewall and TLS/HTTP termination, expose only intended routes, and attach authentication per route where native authentication is insufficient. Keep an independent recovery path. |
| OPEN | Publicly routed applications do not share one consistently documented access policy; some rely on native authentication and others may have no shared middleware label. | Routed labels across `actual-budget/`, `home-assistant/`, `immich/`, `mediarr/`, `monitoring/`, `nextcloud/`, `ntfy/`, `romm/`, `streaming/`, `vaultwarden/`, and `wiksite/` | Inventory every hostname, classify it as owner-only, household, guest, or public, then apply native auth, OIDC, or forward-auth deliberately. Test mobile apps, APIs, WebSockets, invitations, and break-glass access. |
| OPEN | Authentication middleware references are inconsistent: Actual Budget references `authentik@docker`, while the checked-in file provider defines `auth` and points to an authentication hostname whose stack is not present in this repository. | [`actual-budget/compose.yaml:30-32`](actual-budget/compose.yaml#L30-L32), [`networking/dynamic.yaml:1-5`](networking/dynamic.yaml#L1-L5) | Choose the deployed identity provider, make the middleware name/provider explicit, verify the provider route and health independently, and test an emergency path before applying it to management services. |
| OPEN | Prometheus’s configuration bind is writable from the container. | [`monitoring/compose.yaml:27-34`](monitoring/compose.yaml#L27-L34) | Change the bind to `:ro` after confirming Prometheus does not write configuration, then validate reload and redeploy behavior. |
| OPEN | Seerr runs from a `develop` image channel and enables debug logging. | [`mediarr/compose.yaml:175-195`](mediarr/compose.yaml#L175-L195) | Use a reviewed stable release, pin its digest, and use normal logging unless debug output is needed for a controlled investigation. Check existing logs for sensitive data. |

## Supply chain and consistency

| Status | Finding | Location | Recommended fix |
| --- | --- | --- | --- |
| OPEN | Several services use moving tags such as `latest`, while the five Exportarr services are tag-only and have no digest. | `streaming/compose.yaml`, `mediarr/compose.yaml`, `romm/compose.yaml` | Prefer reviewed stable version tags plus immutable digests. Configure Renovate to update the tag and digest together. |
| OPEN | Traefik backend ports are not declared consistently for routed services. | Routed labels across the Compose files; examples include `streaming/compose.yaml` and `mediarr/compose.yaml` | Add an explicit `traefik.http.services.<name>.loadbalancer.server.port` for every routed service and select `traefik` explicitly for multi-network services. |
| OPEN | Compose services generally use `restart: "no"`, so a crash or host reboot does not provide automatic service recovery. | Active `compose.yaml` files | Decide the lifecycle per stack. Use a restart policy for long-running services only after dependency ordering, backup behavior, and Komodo ownership are documented. Keep transient jobs such as Renovate non-restarting. |
| OPEN | Ignore rules cover `.env` and logs but do not protect against accidentally adding private-key files. | [`.gitignore`](.gitignore) | Add narrowly scoped local secret/key patterns after checking tracked fixtures, and use secret scanning in CI. Do not rely on `.gitignore` alone. |

## Closed or owner-accepted items

- The previously exposed SSH key incident is treated as resolved by the owner:
  the key was believed unused and the affected machine is expected to be wiped.
  Keep the key invalidated and rotate it if that has not already happened.
- Docker socket access for Traefik, Glance, cAdvisor, and the Minecraft router
  is routed through the socket proxy. The proxy itself remains open because it
  is privileged and is a high-value trust boundary.

## Validation checklist

- [ ] Archived Tdarr secret is rotated/removed and Tdarr remains inactive until secured.
- [ ] Public and WireGuard-bound port scans show only intentionally exposed services.
- [ ] Socket-proxy permissions and privileged operation are reviewed after consumer testing.
- [ ] cAdvisor mounts and exporter privileges are reviewed.
- [ ] Root services are migrated to dedicated unprivileged UIDs where supported.
- [ ] Every routed hostname has an access classification and authentication decision.
- [ ] Stable image tags and reviewed digests are used consistently.
- [ ] Every Traefik route declares its backend port and intended Docker network.
- [ ] Restart policies match each stack’s documented lifecycle.
- [ ] Secret scanning runs before merges and no credentials are present in new commits.
