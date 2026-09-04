# Security findings and remediation

Audit scope: tracked Docker Compose files and service configuration in this repository.

Status values: `OPEN`, `IN PROGRESS`, and `DONE`.

## Critical

| Status | Finding | Location | Recommended fix |
| --- | --- | --- | --- |
| DONE | InfluxDB uses a hard-coded admin password. | [`monitoring/compose.yaml:38-41`](monitoring/compose.yaml#L38-L41) | Rotate the password and any existing tokens. Use an environment variable or Docker secret, and avoid publishing port `8086` publicly. |

## High

| Status | Finding | Location | Recommended fix |
| --- | --- | --- | --- |
| OPEN | Glance can access the Docker socket. | [`glance/compose.yaml:9-10`](glance/compose.yaml#L9-L10) | Remove the socket or use a restricted read-only socket proxy. Treat `:ro` as insufficient API authorization. |
| OPEN | cAdvisor has broad host mounts, including a writable `/var/run`. | [`monitoring/compose.yaml:55-59`](monitoring/compose.yaml#L55-L59) | Use only the documented mounts required by cAdvisor, make them read-only where possible, and drop unnecessary capabilities. |
| OPEN | Several services run as root or use root-equivalent UIDs. | [`monitoring/compose.yaml:5`](monitoring/compose.yaml#L5), [`streaming/compose.yaml:4`](streaming/compose.yaml#L4), [`mediarr/compose.yaml:34-35`](mediarr/compose.yaml#L34-L35), [`tdarr/compose.yaml:10-11`](tdarr/compose.yaml#L10-L11) | Use dedicated unprivileged UIDs/GIDs, adjust host ownership, and make media mounts read-only unless writes are required. |

## Medium

| Status | Finding | Location | Recommended fix |
| --- | --- | --- | --- |
| OPEN | Administrative interfaces are published directly on all host interfaces. | Glance, InfluxDB, Tdarr, and Deluge Compose files | Remove direct publishing where possible; otherwise bind to `127.0.0.1`, route through Traefik, require authentication, and restrict access with firewall rules. |
| OPEN | Traefik dashboard is enabled without a defined protected route. | [`networking/compose.yaml:11-12`](networking/compose.yaml#L11-L12) | Disable it unless needed. If enabled, expose it only behind TLS, authentication, and an IP allowlist. |
| OPEN | Gluetun requires powerful networking privileges. | [`mediarr/compose.yaml:5-8`](mediarr/compose.yaml#L5-L8) | Retain only required capabilities, test the VPN kill switch, and do not expose Deluge management publicly. |
| OPEN | Space Engineers public IP is hard-coded. | [`space-engineers/compose.yaml:10`](space-engineers/compose.yaml#L10) | Use `${PUBLIC_IP:?required}` or dynamic DNS, and expose only the required UDP port. |

## Inconsistencies and reliability

| Status | Finding | Location | Recommended fix |
| --- | --- | --- | --- |
| OPEN | Some images use unpinned `latest`, `develop`, or tag-only references. | Authentik, ROMM, MariaDB, media services, and Seerr | Pin reviewed release versions and immutable digests; avoid `latest` and `develop` in production. |
| OPEN | Kavita data path appears misspelled as `steeaming`. | [`streaming/compose.yaml:82`](streaming/compose.yaml#L82) | Verify and correct it to `/mnt/docker-data/streaming/kavita-config` if that is the intended path. |
| OPEN | `monitoring/influx-configs` is a regular executable file, despite README wording implying a file/directory. | [`monitoring/influx-configs`](monitoring/influx-configs), [`README.md`](README.md) | Confirm its intended format and purpose; document it accurately and remove executable permission if it is configuration. |
| OPEN | Traefik service ports are specified inconsistently. | Routed services across Compose files | Define `traefik.http.services.<name>.loadbalancer.server.port` consistently. |

## Suggested remediation order

1. Rotate InfluxDB credentials and the Tdarr secret.
2. Remove or restrict Docker socket access.
3. Close or firewall direct administrative ports.
4. Correct the Kavita path and verify persistent volumes.
5. Standardize image pinning, privilege settings, restart policies, and Traefik labels.

## Validation checklist

- [ ] `git log --all -- backups/ssh/id_ed25519` no longer exposes usable key material.
- [ ] Public port scans show only intentionally exposed services.
- [ ] Docker socket access is removed or constrained through a socket proxy.
- [ ] Tdarr and all Internet-facing applications require authentication.
- [ ] A backup completes on schedule and a restore test succeeds.
- [ ] Persistent data paths have been checked after any path correction.
