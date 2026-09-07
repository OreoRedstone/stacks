# Docker socket proxy migration

## Goal

Replace direct Docker socket mounts with the dedicated
`docker-socket-proxy` Compose stack wherever a service needs only read-only
Docker API access.

## Current stack

Deploy `docker-socket-proxy/compose.yaml` on the application VM. It creates the
named internal Docker network `docker-socket-proxy`, mounts the host socket in
one place, enables only read-oriented API sections, and sets `POST=0`.

## Required consumer changes

### Traefik — migrated

Implemented in `networking/compose.yaml`:

1. Traefik attaches to the external `docker-socket-proxy` network.
2. The Docker socket mount is replaced with
   `--providers.docker.endpoint=tcp://docker-socket-proxy:2375`.
3. Traefik remains on the `traefik` network for routing.
4. The proxy must be started before Traefik is recreated.
5. Confirm all Docker-labelled routers and certificates load after deployment.

If the proxy is unavailable, Traefik cannot discover Docker routers. Keep the
previous Compose definition available for rollback until the proxy migration
has been observed through a complete restart.

Required proxy permissions: `CONTAINERS`, `EVENTS`, `INFO`, `NETWORKS`, and
`VERSION`. Traefik is the most important migration because a proxy failure can
remove all dynamically discovered routes.

### Glance — migrated

Implemented in `glance/compose.yaml` and `glance/config/home.yml`:

1. Glance attaches to the external `docker-socket-proxy` network.
2. Each Docker Containers widget uses the documented `sock-path` setting with
   `http://docker-socket-proxy:2375`.
3. The direct socket mount is removed.
4. Confirm the Docker containers widgets still display the expected labels.

If the widget is no longer important, remove the Docker integration instead of
granting Glance Docker metadata access.

### cAdvisor — test carefully

In `monitoring/compose.yaml`:

1. Attach cAdvisor to the external proxy network.
2. Change its Docker endpoint to
   `--docker=tcp://docker-socket-proxy:2375`.
3. Keep `/`, `/sys`, and `/var/lib/docker` read-only mounts because cAdvisor
   uses host filesystem and cgroup data as well as Docker API data.
4. Confirm container metrics continue to arrive before removing the socket.

The cAdvisor endpoint flag is documented upstream. If the proxy does not
provide an endpoint cAdvisor needs, keep cAdvisor's direct read-only socket
mount as an explicit exception rather than enabling broad proxy permissions.

### mc-router — verify before migration

`minecraft/compose.yaml` uses mc-router's `-in-docker` mode and currently has a
direct socket mount. Verify the image supports `DOCKER_HOST` over TCP and that
it only needs read/event access. Test server discovery, server start/stop
events, and routing before changing it.

## Future Blackbox integration

Prometheus may use Docker service discovery through the proxy to find opted-in
containers, but labels should explicitly provide the public probe target. Do
not infer public URLs solely from arbitrary Traefik rules. A future label model
could be:

```yaml
monitoring.blackbox.enabled: "true"
monitoring.blackbox.target: https://service.example.net
monitoring.blackbox.module: http_any
```

Use relabeling to convert discovered labels into Blackbox `/probe` requests.
Test the required Docker API endpoints first and keep Prometheus off the proxy
network until this is implemented.

## Verification and rollback

- [x] Deploy the proxy stack definition.
- [ ] Confirm it has no published host port.
- [x] Migrate Traefik to the proxy endpoint.
- [ ] Migrate one low-risk consumer.
- [ ] Check logs, routing, widgets, or metrics.
- [ ] Migrate Traefik during a maintenance window.
- [ ] Remove direct socket mounts only after verification.
- [ ] Search active Compose files for remaining direct socket mounts.
- [ ] Keep the proxy stack available as a prerequisite for all migrated
  consumers.
- [ ] Roll back by restoring the consumer's direct read-only socket mount and
  removing its proxy endpoint/network if a migration fails.
