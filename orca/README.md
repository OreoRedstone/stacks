# Orca Remote Server

This stack builds the official Orca Linux server bundle into a small local
image and runs `orca-ide serve`. It is not an upstream-published container
image. The release version and SHA-256 checksums are pinned in the Dockerfile;
update them together after reviewing a new upstream release.

## Host preparation

The default port binding and pairing address use `10.44.0.2`, matching the
WireGuard-bound management services in this repository. Confirm that address
belongs to the Docker host. If it differs, set `ORCA_HOST_BIND_IP` and
`ORCA_PAIRING_ADDRESS` in the Komodo Stack environment or a local ignored
`.env` file. Keep the host firewall restricted to intended VPN clients.

Create the persistent directories and make them writable by the container's
UID/GID `1000:1000` before the first start:

```sh
sudo install -d -o 1000 -g 1000 /mnt/docker-data/orca/home
sudo install -d -o 1000 -g 1000 /mnt/docker-data/orca/projects
```

Deploy `orca/compose.yaml` through Komodo or run `docker compose up --build -d`
from this directory. The service starts with pairing disabled so a bearer
pairing link is not printed into persistent container logs.

## Pair a client

Create a one-time pairing link on the host:

```sh
docker compose exec orca /bin/bash -lc \
  'exec /opt/orca-server/bin/orca-ide pair --address "$ORCA_PAIRING_ADDRESS"'
```

Run this command in a trusted terminal and deliver the link only to the client
being paired. For mobile pairing, add `--mobile`; the phone must still be able
to reach the advertised address. This stack advertises its WireGuard address,
so the phone needs WireGuard enabled. Orca Relay can provide off-network mobile
access for desktop hosts, but support for Relay pairing from headless `orca
serve` is still an [open upstream change](https://github.com/stablyai/orca/pull/22435)
and is not available in the pinned server release. Revoke a grant if its link
or paired device is exposed. Do not route port 6768 through Traefik or forward
it publicly.

## Agent CLIs and accounts

The image includes `git` and the OpenSSH client but no provider CLI or account
credentials. Add only the desired, version-pinned agent CLI to the Dockerfile,
then rebuild. Authenticate it inside the container as UID 1000; its home under
`/home/orca` is persistent and contains sensitive provider credentials. Do not
copy credentials into the image, Git, Compose labels, or logs. No host
directories other than this service's home and projects are mounted, and the
Docker socket is not available to Orca.

Agent CLIs execute commands against mounted project files. Treat paired-client
access and the `/projects` contents as trusted administrative access.

## State, updates, and recovery

- Back up `/mnt/docker-data/orca/home` and `/mnt/docker-data/orca/projects`.
  The home directory includes Orca state and provider credentials; protect the
  backup accordingly.
- To update, select a reviewed upstream release, update the version and both
  architecture checksums in `Dockerfile`, update the image tag and build arg in
  `compose.yaml`, then rebuild and redeploy.
- No healthcheck is configured because the upstream server documentation does
  not specify a health endpoint. Inspect `docker compose ps` and logs for
  process failures; logs should not contain pairing links with this setup.
- Orca's per-terminal memory limits depend on systemd user scopes and cgroup
  v2. They are not configured here; the container still needs suitable host
  resource limits and monitoring.
