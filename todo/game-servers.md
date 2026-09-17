# Game-server management and upgrades

## Scope

This plan covers the Minecraft, Factorio, and Space Engineers servers. The
current deployment is Compose-based and updated through Komodo, with the
repository remaining the intended source of truth.

Current stacks:

- `minecraft` — mc-router plus JJK, Vanilla, and DeceasedCraft servers. ATM10
  and several older servers remain commented out.
- `factorio` — Factorio Space Exploration data with repository-managed mod and
  server settings.
- `space-engineers` — Space Engineers Dedicated Server running from the
  `devidian/spaceengineers` Wine-based image.
- `immich2` is intentionally unrelated to this plan: it is the secondary
  Immich deployment for a friend on the backup host.

## Current observations

- Minecraft uses `itzg/minecraft-server` and `itzg/mc-router`.
- mc-router discovers Minecraft containers through the Docker socket proxy.
- JJK uses a remote Modrinth pack URL. The URL should be made immutable or
  otherwise version-pinned before treating it as a reproducible deployment.
- The active Minecraft servers do not currently have a consistent automated
  backup sidecar. The checked-in Simple Backups configuration belongs to the
  commented-out ATM10 service.
- Factorio copies `mod-list.json` and `server-settings.json` into persistent
  storage at startup through `start.sh`.
- Factorio has no repository-visible backup, restore, or health-monitoring
  workflow.
- Space Engineers has no restart policy, healthcheck, or repository-visible
  backup workflow.
- At the time of review, JJK and Vanilla were stopped on the applications VM;
  DeceasedCraft and Factorio were running. Confirm stopped-server intent before
  changing lifecycle behavior.

## Phase 1 — improve the existing Compose deployment

### Minecraft

- [ ] Add an `itzg/mc-backup` sidecar for every active Minecraft server.
- [ ] Enable and protect RCON with secrets supplied by Komodo rather than
  storing passwords in Compose.
- [ ] Configure save-safe scheduled backups with sensible retention.
- [ ] Store backups under `/mnt/nas/backups/minecraft/<server>` or another
  separately protected destination.
- [ ] Exclude caches, logs, temporary files, and generated artifacts from
  backups where safe.
- [ ] Add a documented restore procedure and test restoring to a separate
  temporary server.
- [ ] Add healthchecks for server readiness and make sure mc-router does not
  advertise an unhealthy instance.
- [ ] Add graceful shutdown timeouts so world data is saved before a container
  is stopped.
- [ ] Pin the JJK Modrinth pack to a reviewed immutable release or archive.
- [ ] Keep Java versions explicit per server, especially for modded packs.
- [ ] Review whether mc-router needs Docker discovery long-term; reduce socket
  proxy permissions if a static routing model is sufficient.

The `itzg/mc-backup` sidecar supports RCON-aware saves, scheduled backups,
retention, and restic/rclone destinations:

https://github.com/itzg/docker-mc-backup

### Factorio

- [ ] Add a healthcheck that verifies the server process and expected save
  availability.
- [ ] Define a repeatable save-backup schedule and retention policy.
- [ ] Back up saves, map metadata, configuration, and the reviewed mod list;
  do not rely only on the repository copy of the mod list.
- [ ] Test Factorio save restoration on an alternate instance.
- [ ] Decide whether `UPDATE_MODS_ON_START` should remain enabled. Automatic
  mod changes should not silently alter a live world without a backup and
  compatibility review.
- [ ] Pin or record the exact Factorio, mod, and Space Age versions used by a
  save.
- [ ] Add an operational console/RCON path if routine administration requires
  more than container logs.

### Space Engineers

- [ ] Confirm the Wine-based image and current server version remain suitable.
- [ ] Add `restart: unless-stopped` if the server is intended to run
  continuously.
- [ ] Add a healthcheck that verifies the dedicated server is accepting
  connections.
- [ ] Document the world-save location and backup consistency requirements.
- [ ] Add scheduled backups and test a world restore.
- [ ] Confirm UDP port requirements and whether additional Steam/query ports
  are needed.
- [ ] Add console administration and crash-recovery behavior.

## Komodo integration

Each repository-backed Stack must track non-compose files as Komodo
`config_files` with `requires = "Redeploy"`. Otherwise a Git pull can update a
file on disk without restarting the affected service.

The relevant paths are documented in [`todo/komodo.md`](komodo.md). For game
servers, the important entries are:

| Stack | Files to track |
| --- | --- |
| `factorio` | `mod-list.json`, `server-settings.json`, `start.sh` |
| `minecraft` | `jjk/lostcities-server.toml`, plus `atm10-backup.conf` and `atm10-ftbchunks.snbt` if ATM10 is re-enabled |
| `space-engineers` | No repository-managed runtime config currently exists; add files here if the image is later configured from Git |

Keep the deployment procedure in this order:

1. Pull the shared repository.
2. Select only currently running stacks.
3. Run `BatchDeployStackIfChanged` for those stacks.

This preserves intentionally stopped servers while still reacting to Compose
and tracked configuration changes.

## Management-panel options

### Continue with Compose and Komodo — recommended first

Advantages:

- Git remains the source of truth.
- Existing persistent data and networking remain unchanged.
- Works naturally with Renovate and the current infrastructure repository.
- No additional management database or panel dependency.

Complete Phase 1 before deciding whether a panel is still needed.

### Crafty Controller — Minecraft-focused option

Crafty provides a web UI, console, file management, player controls, server
settings, and scheduled backups for Minecraft Java and Bedrock servers.

Trade-offs:

- Primarily a Minecraft management platform.
- It introduces its own database and configuration state.
- Migrated servers would be managed by Crafty rather than directly by Compose
  and Komodo.
- It is not the preferred common control plane for Factorio and Space
  Engineers.

References:

- https://docs.craftycontrol.com/
- https://craftycontrol.com/

### AMP — strongest broad game-server candidate

AMP supports Minecraft, Factorio, and Space Engineers, as well as many other
games. It provides a unified web panel, instance management, console access,
scheduled backups, update workflows, permissions, and crash recovery.

Trade-offs:

- Commercial software and licensing cost.
- Migration changes the source of truth from Compose/Komodo to AMP.
- It adds panel state, user management, and another recovery path.
- Space Engineers may involve Wine or Torch-specific operational quirks and
  should be tested rather than assumed to be seamless.

Trial AMP on a separate VM or isolated test instance. Do not point it at the
production world directories until backup and rollback procedures are proven.

Reference:

- https://cubecoders.com/AMP/csgo
- https://discourse.cubecoders.com/t/supported-applications-compatibility/1828

### Pterodactyl — multi-user hosting option

Pterodactyl provides Docker-isolated game servers and is strongest when
multiple users need controlled access to their own instances. Minecraft is a
first-class use case; Factorio and Space Engineers would require community or
generic templates and more operational work.

Trade-offs:

- Larger deployment footprint: panel, Wings, database, and supporting
  services.
- More complex migration and backup requirements.
- Better suited to multi-tenant hosting than a small private homelab.
- Community templates need review and maintenance.

Reference:

- https://pterodactyl.io/project/introduction.html

## Decision criteria

Before migrating, compare candidates against:

- Minecraft modpack and Java-version compatibility.
- Factorio mod and save handling.
- Space Engineers Linux/Wine/Torch support.
- RCON and interactive console quality.
- Safe scheduled backups and tested restores.
- Update pinning, rollback, and offline recovery.
- Per-server CPU, memory, disk, and network isolation.
- User permissions for friends without exposing infrastructure controls.
- Compatibility with Traefik, ntfy, Grafana, and Komodo.
- Whether the panel can be backed up and rebuilt independently.
- License cost and dependence on a proprietary control plane.

## Proposed decision

- [ ] Complete backup, restore, healthcheck, and Komodo improvements first.
- [ ] Run a time-boxed AMP trial on an isolated VM if unified management of
  Minecraft, Factorio, and Space Engineers remains desirable.
- [ ] Consider Crafty only if Minecraft-specific administration is the main
  requirement.
- [ ] Consider Pterodactyl only if friend-facing multi-user isolation becomes
  a requirement.
- [ ] Do not migrate production world directories without a verified backup,
  restore test, and rollback plan.
