# Komodo stack change detection

## Problem

This repository is a monorepo. Komodo tracks `compose.yaml` by default, but
files mounted or consumed by Compose are not automatically included in
`BatchDeployStackIfChanged`. A change to `networking/dynamic.yaml`,
`monitoring/prometheus.yml`, or Grafana provisioning files can therefore be
pulled without restarting the affected service.

Komodo Stack configuration is stored outside this repository, so these entries
must be added to each Stack in Komodo under **Config → Config files**. Set
`Requires` to **Redeploy** for every entry. Do not add `.env` here; configure
that as an additional environment file if it needs tracking.

## Config files to register

Paths are relative to the Stack run directory, which should be the matching
repository directory under the cloned `stacks` repo.

| Stack | Config files requiring redeploy |
| --- | --- |
| `factorio` | `mod-list.json`, `server-settings.json`, `start.sh` |
| `glance` | `config/glance.yml`, `config/home.yml`, `assets/user.css` |
| `immich` | `immich.json` |
| `minecraft` | `atm10-backup.conf`, `atm10-ftbchunks.snbt`, `jjk/lostcities-server.toml` |
| `monitoring` | `blackbox.yml`, `prometheus.yml`, `grafana/datasources.yaml`, `grafana/dashboards.yaml`, `grafana/alerting/contact-points.yaml`, `grafana/alerting/policies.yaml`, `grafana/alerting/rules.yaml`, `grafana/dashboards/docker.json`, `grafana/dashboards/endpoints.json`, `grafana/dashboards/hosts.json`, `grafana/dashboards/media-applications.json`, `grafana/dashboards/overview.json`, and `grafana/dashboards/proxmox.json` |
| `networking` | `dynamic.yaml` |
| `ntfy` | `server.yml` |
| `romm` | `config.yml` |

The remaining repository stacks currently have no tracked non-compose runtime
configuration. `immich2` intentionally uses the secondary backup-host stack
and currently has only its Compose file plus externally supplied environment
and persistent data.

Komodo does not currently support a wildcard config-file entry reliably, so
list each monitoring dashboard JSON explicitly. When a new file is added,
register it in Komodo before relying on automatic deployment.

## Procedure

Keep the repository pull as the first stage. The deploy stage should target
only currently running stacks, then use `BatchDeployStackIfChanged` so both
Compose files and the registered config files are diffed:

```toml
[[procedure.config.stage]]
name = "Pull repository"
executions = [
  { execution.type = "PullRepo", execution.params.repo = "stacks", enabled = true },
]

[[procedure.config.stage]]
name = "Deploy changed running stacks"
executions = [
  { execution.type = "RunAction", execution.params.action = "deploy-changed-running-stacks", enabled = true },
]
```

The Action should list stacks linked to the `stacks` Repo, keep only stacks
whose state is `Types.StackState.Running`, and pass those names to
`BatchDeployStackIfChanged`. This preserves an intentional stopped/down state.

After adding the config files, trigger one controlled commit and verify the
affected service is recreated or restarted, its deployed hash/config changes,
and an unchanged stack remains untouched.

## Known limitation

Komodo's current source documents `config_files` as part of change detection,
but entries synchronized through ResourceSync/TOML have had reports of not
wiring the redeploy trigger correctly. Add these entries through the Stack UI
first, or verify the Stack's tracked remote contents and deployed state after
syncing them.
