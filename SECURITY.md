# Security findings and remediation

Audit scope: tracked Docker Compose files and service configuration in this repository. Findings below reflect the current tree; resolved findings have been removed.

Status values: `OPEN`, `IN PROGRESS`, and `DONE`.

## Critical

| Status | Finding | Location | Recommended fix |
| --- | --- | --- | --- |
| OPEN | Archived Tdarr configuration has authentication disabled and contains a secret value. | [`archive/tdarr/configs/Tdarr_Server_Config.json:12-17`](archive/tdarr/configs/Tdarr_Server_Config.json#L12-L17) | Before reactivation, rotate the committed `authSecretKey`, enable authentication, keep port `8266` internal, and put the web UI behind authenticated Traefik access. |

## High

| Status | Finding | Location | Recommended fix |
| --- | --- | --- | --- |
| OPEN | Glance can access the Docker socket. | [`glance/compose.yaml:9-10`](glance/compose.yaml#L9-L10) | Remove the socket or use a restricted Docker socket proxy. Treat `:ro` as insufficient API authorization. |
| OPEN | Minecraft router runs as root and can access the Docker socket. | [`minecraft/compose.yaml:8-10`](minecraft/compose.yaml#L8-L10) | Remove the socket if dynamic discovery is unnecessary; otherwise use a restricted proxy and run the router with the least privileges supported. |
| OPEN | Several active services run as root or use root-equivalent UIDs. | [`monitoring/compose.yaml:5`](monitoring/compose.yaml#L5), [`streaming/compose.yaml:4`](streaming/compose.yaml#L4), [`mediarr/compose.yaml:34-35`](mediarr/compose.yaml#L34-L35), [`mediarr/compose.yaml:199`](mediarr/compose.yaml#L199) | Use dedicated unprivileged UIDs/GIDs, adjust host ownership, and make media mounts read-only unless writes are required. |

## Medium

| Status | Finding | Location | Recommended fix |
| --- | --- | --- | --- |
| OPEN | Administrative interfaces are published directly on all host interfaces. | [`glance/compose.yaml:11-12`](glance/compose.yaml#L11-L12), [`monitoring/compose.yaml:34-35`](monitoring/compose.yaml#L34-L35), [`mediarr/compose.yaml:12-14`](mediarr/compose.yaml#L12-L14) | Remove direct publishing where possible; otherwise bind to `127.0.0.1`, route through Traefik, require authentication, and restrict access with firewall rules. |
| OPEN | Traefik dashboard is enabled without a defined protected route. | [`networking/compose.yaml:11-12`](networking/compose.yaml#L11-L12) | Disable it unless needed. If enabled, expose it only behind TLS, authentication, and an IP allowlist. |
| OPEN | Gluetun requires powerful networking privileges. | [`mediarr/compose.yaml:5-8`](mediarr/compose.yaml#L5-L8) | Retain only required capabilities, test the VPN kill switch, and do not expose Deluge management publicly. |

## Supply-chain and configuration consistency

| Status | Finding | Location | Recommended fix |
| --- | --- | --- | --- |
| OPEN | Several images use `latest`, `develop`, or a tag that does not describe a stable release, even though digests currently pin the content. | `mediarr/compose.yaml`, `romm/compose.yaml`, `streaming/compose.yaml`, `wiksite/compose.yaml` | Pin reviewed stable release tags and immutable digests; avoid `latest` and `develop` in production. |
| OPEN | Traefik service ports are specified inconsistently. | Routed services across Compose files | Define `traefik.http.services.<name>.loadbalancer.server.port` consistently. |

## Validation checklist

- [ ] Archived Tdarr configuration is securely updated before any reactivation.
- [ ] Public port scans show only intentionally exposed services.
- [ ] Docker socket access is removed or constrained through a socket proxy.
- [ ] Root services have been migrated to dedicated unprivileged UIDs where supported.
- [ ] All Internet-facing applications require authentication.
- [ ] Stable image tags and reviewed digests are used consistently.
- [ ] Traefik routes specify their backend ports explicitly.
