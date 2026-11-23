# Orca Remote Server deployment

## Goal

Run Orca's headless runtime on an always-on Linux machine so paired clients can
resume agent sessions when their desktops disconnect. Keep the runtime and its
agent credentials private to the trusted VPN.

## Upstream deployment model

Orca is an agent IDE and remote runtime, not a conventional web service. The
official headless Linux path installs Orca's server bundle and runs
`orca-ide serve`; the server owns its projects, worktrees, terminals, provider
accounts, and sessions. Provider CLIs and their logins must exist on the server
itself. The upstream docs do not provide an official Docker image or Compose
deployment. They do say the standalone Linux server bundle suits containers;
this repository builds that bundle into a locally maintained Compose image.

Sources: [Ways to run Orca](https://orca.dev/docs/ways-to-run), [Remote Orca
Servers](https://orca.dev/docs/remote-servers), and the [upstream
README](https://github.com/stablyai/orca).

## Proposed deployment

Build a local Compose image from the official server archive using the pinned
version and per-architecture checksums in [`../orca/Dockerfile`](../orca/Dockerfile).
The image runs as non-root, persists the Orca home and project/worktree
directories, and has no Docker socket mount. The Compose port is bound to the
WireGuard host address and the runtime starts with pairing disabled so pairing
tokens are not printed into container logs. See [`../orca/README.md`](../orca/README.md)
for host preparation and pairing instructions.

Keep the server on the existing private WireGuard network. The stack defaults
to `10.44.0.2`, used by other WireGuard-bound management services in this
repository; confirm that address is assigned to the Docker host. Do not add a
Traefik route or public port-forward. Treat each pairing link as a credential
and revoke a client grant if it is exposed.

Keep the server on the existing private WireGuard network. The repository
already uses `10.44.0.2` for a WireGuard-bound management service; confirm that
this is the selected host before using it. Listen on a fixed port (`6768` is
documented upstream), allow it only from intended VPN clients, and do not add a
Traefik route or public port-forward. Use the reachable VPN address in pairing
links. Treat each pairing link as a credential and revoke a client grant if it
is exposed.

## Implementation checklist

### 1. Confirm host and access boundary

- [ ] Select a dedicated Linux VM/host and confirm its CPU architecture,
  storage, and WireGuard address.
- [ ] Decide which clients may pair and which agent providers are allowed.
- [ ] Confirm the host firewall permits the Orca port only from the intended
  VPN range; verify there is no public forwarding.
- [ ] Create a dedicated non-root service account. Do not grant it Docker socket
  access or mount host secrets unrelated to Orca.

### 2. Install and configure the runtime

- [x] Pin upstream release `1.4.258` and the published SHA-256 checksums for
  both server archives in the Dockerfile.
- [x] Build the Linux server bundle and `git` into the local image.
- [ ] Add the selected, version-pinned agent CLI(s) to the image.
- [ ] Authenticate each provider locally as the `orca` account. Keep credentials
  out of Git, Compose variables, logs, and shared project directories.
- [ ] Run the server once with a fixed port and VPN pairing address. Confirm the
  exact bind and advertisement behavior for the selected host.
- [ ] Pair one desktop client using the generated access link; add mobile
  pairing only if needed.
- [x] Configure Compose restart behavior for container and host restarts.

### 3. Decide storage and recovery

- [ ] Identify Orca's actual state/configuration paths for the selected release
  before setting backup rules.
- [ ] Put projects and worktrees on durable storage with enough free space.
  Avoid mounting the live infrastructure repository or broad host directories
  into agent workspaces.
- [ ] Back up Orca state, worktrees, and any important uncommitted work. Define
  retention and perform a restore test before relying on the service.
- [ ] Document host rebuild, pinned-version update, and rollback procedures.

### 4. Verify operation before wider use

- [ ] Confirm a session and terminal continue after the client disconnects and
  reconnect correctly.
- [ ] Confirm the container restarts after a host reboot and resumes sessions.
- [ ] Check that only intended VPN clients can connect; verify the port is not
  reachable through the public edge.
- [ ] Test revoking a paired client and generating a replacement pairing link.
- [ ] Mobile clients must use WireGuard for this direct-address deployment;
  Orca Relay pairing for headless `orca serve` is not yet supported in the
  pinned release ([upstream PR #22435](https://github.com/stablyai/orca/pull/22435)).
- [ ] Confirm logs do not expose pairing tokens or provider credentials.
- [ ] Review CPU, memory, and disk growth under realistic workloads. Orca's
  documented per-terminal memory limits use systemd user scopes and cgroup v2;
  they are not configured by this Compose stack.

## Container options reviewed

- Orca publishes a standalone Linux server archive (`orcad`, bundled Node, and
  `orca-ide`) for x64 and arm64 and explicitly says it can be used in
  containers. This is a base for a locally built Compose image, not a
  first-party prebuilt container. [Remote Orca Servers](https://orca.dev/docs/remote-servers)
- [talayolabs/orca-docker](https://github.com/talayolabs/orca-docker) creates a
  separate desktop container for each worktree via Orca environment recipes.
  It is not a single persistent Remote Orca Server container or a ready-made
  Compose stack; it currently focuses on Claude Code, and the Orca feature
  discussion flags hardening and credential handling concerns. [Orca
  discussion #29578](https://github.com/stablyai/orca/issues/29578)
- Orca's project recipes can also create local Docker containers per
  workspace, but that is a different model from hosting the shared Orca server
  itself. [Ways to run Orca](https://orca.dev/docs/ways-to-run)

## Repository integration

The Compose implementation is in `orca/` and can be managed as a repository-
backed Komodo Stack. Deployment remains pending host preparation, provider
selection, and runtime verification. The image is locally maintained rather
than upstream-published; update the Orca version and both archive checksums
together after reviewing upstream releases.

## Decisions to record

- Host/VM and WireGuard address: ____________________
- Allowed paired clients: ____________________
- Agent CLIs/providers: ____________________
- Project/worktree storage and backup: ____________________
- Desktop-only pairing or mobile pairing: ____________________
