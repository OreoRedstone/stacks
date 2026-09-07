# Docker socket proxy

## Scope

Keep Docker API access behind `docker-socket-proxy` and grant consumers only
the read-only API sections they require. The proxy is infrastructure, not a
general-purpose application endpoint.

## Current consumers

- Traefik uses the proxy for Docker provider discovery.
- Glance uses it for container status widgets.
- cAdvisor uses it for Docker container metrics.
- Minecraft router uses it for container-aware routing.

## Current implementation

The stack is defined in [`../docker-socket-proxy/compose.yaml`](../docker-socket-proxy/compose.yaml).
It enables `CONTAINERS`, `EVENTS`, `IMAGES`, `INFO`, `NETWORKS`, and `VERSION`,
while disabling `POST`. The proxy network is external and is joined only by
approved consumers.

## Remaining work

- [ ] Verify that every consumer still needs its current API sections.
- [ ] Replace `privileged: true` with the least-privilege configuration
  supported by the selected proxy image, after testing on the target host.
- [ ] Keep the Docker socket mounted read-only and never publish port `2375`.
- [ ] Add health/dependency handling to consumers where startup ordering matters.
- [ ] Pin and periodically review the proxy image digest.
- [ ] Document recovery: start the proxy before Traefik, Glance, cAdvisor, and
  the Minecraft router.
- [ ] Recheck this boundary whenever a Docker-aware service is added.

## Security boundary

Anyone who can reach the proxy can learn information about the Docker host and
containers. Do not attach ordinary application containers to its network, do
not route it through Traefik, and do not expose it on a host port. A compromise
of a consumer should be treated as a host-information disclosure risk until
the proxy permissions and image behavior have been reviewed.
