# Docker Socket Proxy

This stack provides a restricted read-only Docker API over the internal
`docker-socket-proxy` network. It is intended to replace direct
`/var/run/docker.sock` mounts where applications only need Docker discovery,
labels, events, or read-only status.

The proxy has no published ports. The Docker socket is mounted only into the
proxy, and `POST=0` blocks Docker API write operations. The proxy still has
significant access to Docker metadata, so only explicitly trusted consumers
should join its network.

## Start

```sh
docker compose up -d
docker compose logs docker-socket-proxy
```

Start this stack before migrating any consumer. Keep the direct socket mount in
place until the replacement has been tested, then remove it from that
consumer's Compose file.

## Consumers to migrate

The repository currently contains direct socket mounts in:

| Consumer | Required implementation |
| --- | --- |
| `networking/` / Traefik | Implemented. Traefik joins this external network and uses `--providers.docker.endpoint=tcp://docker-socket-proxy:2375`; the proxy retains `CONTAINERS`, `EVENTS`, `INFO`, `NETWORKS`, and `VERSION`. |
| `glance/` | Implemented. Glance joins this external network and each Docker Containers widget uses `sock-path: http://docker-socket-proxy:2375`; the direct socket mount is removed. |
| `monitoring/` / cAdvisor | Attach cAdvisor to this external network and set `--docker=tcp://docker-socket-proxy:2375`; keep its host filesystem mounts because those provide cgroup and filesystem metrics, independently of the Docker API. |
| `minecraft/` / mc-router | Verify that the image honours `DOCKER_HOST` for `-in-docker`; migrate only after testing server discovery and event handling. |

Prometheus can later use Docker service discovery through this proxy for
label-driven Blackbox targets, but it should be migrated separately and only
after the required read-only API endpoints are confirmed.

## Migration order

1. Deploy this stack and verify the proxy is reachable only from its Docker
   network.
2. Migrate Glance or cAdvisor first, since failure is easy to detect and
   reverse.
3. Migrate Traefik during a maintenance window; routing depends on its Docker
   provider.
4. Migrate mc-router only after testing its Docker event and label behaviour.
5. Remove each direct socket mount after successful verification.
6. Check that no direct mounts remain:

   ```sh
   rg -n '/var/run/docker.sock' --glob 'compose.yaml' --glob '!archive/**' .
   ```

The proxy image deliberately has `privileged: true` because the upstream
project documents that it may be required for socket access under
SELinux/AppArmor. Confirm whether it is required on this host before reducing
or removing it; do not expose the proxy port or network to untrusted services.
