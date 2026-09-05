# Guide for AI agents

## Repository purpose

This repository contains self-hosted application stacks. Each active application generally has its own directory and `compose.yaml`. The repository is operational infrastructure, so changes can affect persistent data, public services, credentials, and recovery paths.

## Reading order

1. Read this file.
2. Read [`README.md`](README.md) for the inventory and shared conventions.
3. Read the relevant project file in [`todo/`](todo/) before making changes.
4. Inspect the target project’s `compose.yaml` and adjacent configuration files.
5. Inspect `networking/compose.yaml` and `networking/dynamic.yaml` when changing routing, TLS, or authentication.
6. Inspect `SECURITY.md` for known open findings.
7. Check `git status --short` before editing and preserve unrelated user changes.

## Directory conventions

- Active applications live at the repository root: `monitoring/`, `networking/`, `mediarr/`, and so on.
- `archive/` contains inactive projects and must not be treated as deployed.
- `todo/` contains project plans, not deployment configuration.
- `renovate/` contains the transient Renovate Compose runner.
- Persistent data is normally outside the repository under `/mnt/docker-data` or `/mnt/nas`.
- Secrets should come from Komodo, environment files excluded by Git, Docker secrets, or an external secret manager.

## Important operational relationships

- Most web services use the external Docker network `traefik`.
- `networking/compose.yaml` creates that network and runs Traefik.
- Traefik labels determine public hostnames and backend ports.
- Authentication changes must account for Komodo and the identity provider’s own recovery path.
- Archived files may still contain historical configuration or secrets; moving a service to `archive/` does not remove it from Git history.

## Safe change procedure

- Do not expose credentials in command output, commits, logs, or documentation.
- Do not remove, rotate, or overwrite persistent data without confirming the exact target and recovery plan.
- Prefer `apply_patch` for repository edits.
- Validate YAML/Compose syntax when Docker is available.
- Review image changes and preserve digest pinning where possible.
- Make the smallest scoped change, then inspect the diff.
- For service changes, check dependencies, networks, mounts, ports, health checks, and restart behavior.
- Do not run production deployments, force-pushes, or destructive Git commands unless explicitly requested.

## Security review priorities

Pay particular attention to:

- Docker socket mounts
- Root containers and broad host mounts
- Publicly published administrative ports
- Hard-coded passwords, tokens, keys, and secrets
- Authentication middleware naming and circular dependencies
- Image tags such as `latest` or `develop`
- Changes to `/mnt/docker-data` and `/mnt/nas` paths

## Reporting

When finishing work, report:

- Files changed
- Validation performed and any unavailable tools
- Remaining risks or manual steps
- Any pre-existing worktree changes left untouched
