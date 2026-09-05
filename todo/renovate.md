# Renovate and Git hosting

## Goal

Run Renovate as a transient Compose service launched by Komodo, while deciding whether this repository should remain on GitHub or move to a self-hosted Git provider.

## Current repository state

- Renovate is defined in [`../renovate/compose.yaml`](../renovate/compose.yaml).
- Repository rules are in [`../renovate.json`](../renovate.json).
- `archive/**` is excluded from update scans.
- The Compose service expects `RENOVATE_TOKEN` and currently targets GitHub.
- The current non-major update rules enable automerging; disable this while testing.

## Provider options

### GitHub with a dedicated PAT — simplest

- [ ] Create a dedicated Renovate bot account.
- [ ] Create a fine-grained token restricted to this repository.
- [ ] Grant only Contents, Issues, Pull requests, Commit statuses, and Metadata access as required.
- [ ] Store the token as a Komodo secret named `RENOVATE_TOKEN`.
- [ ] Keep `RENOVATE_PLATFORM=github` and `RENOVATE_REPOSITORIES=oreoredstone/stacks`.
- [ ] Run a manual test before scheduling.

This avoids GitHub App installation-token generation. It is the fastest route, but keeps the repository dependent on GitHub.

Reference: https://docs.renovatebot.com/modules/platform/github/

### Forgejo — preferred self-hosted option

- [ ] Choose a hostname, for example `git.74services.net`.
- [ ] Deploy Forgejo with persistent storage.
- [ ] Put Forgejo behind Traefik and HTTPS.
- [ ] Disable open registration.
- [ ] Enable MFA for administrators.
- [ ] Configure backups for repositories, database, attachments, and configuration.
- [ ] Create a dedicated `renovate` bot account.
- [ ] Grant it access only to this repository.
- [ ] Create a repository-scoped access token.
- [ ] Migrate this repository and verify branches, tags, and rewritten history.
- [ ] Update the local Git remote and Komodo repository source.
- [ ] Set `RENOVATE_PLATFORM=forgejo`.
- [ ] Set `RENOVATE_ENDPOINT=https://git.74services.net/api/v1`.
- [ ] Change `RENOVATE_REPOSITORIES` to the Forgejo owner/repository name.
- [ ] Store the bot token in Komodo as `RENOVATE_TOKEN`.
- [ ] Run Renovate manually and confirm it creates a test pull request.

Forgejo is the recommended balance of low resource use, self-hosting, pull requests, and Renovate compatibility.

Reference: https://docs.renovatebot.com/modules/platform/forgejo/

### Gitea

- [ ] Deploy Gitea with persistent storage, HTTPS, backups, and registration disabled.
- [ ] Create a dedicated bot account and repository-scoped token.
- [ ] Migrate the repository and update Komodo.
- [ ] Set `RENOVATE_PLATFORM=gitea`.
- [ ] Set `RENOVATE_ENDPOINT=https://git.example.net/api/v1`.
- [ ] Test pull-request creation before scheduling.

Reference: https://docs.renovatebot.com/modules/platform/gitea/

### GitLab CE

- [ ] Choose GitLab only if its CI/CD, registry, and project-management features justify the additional resource cost.
- [ ] Deploy GitLab with adequate CPU, memory, storage, HTTPS, SMTP, backups, and restore testing.
- [ ] Create a project access token or dedicated bot account with the `api` scope.
- [ ] Migrate the repository and update Komodo.
- [ ] Set `RENOVATE_PLATFORM=gitlab`.
- [ ] Set `RENOVATE_ENDPOINT=https://git.example.net/api/v4`.
- [ ] Test merge-request creation before scheduling.

Reference: https://docs.renovatebot.com/modules/platform/gitlab/

## Komodo setup

- [ ] Create a Komodo Stack named `renovate`.
- [ ] Use the repository-backed Compose file `renovate/compose.yaml`.
- [ ] Set the run directory to the repository root containing `renovate/`.
- [ ] Add the Git provider token as a masked Stack secret.
- [ ] Do not deploy it as a long-running service.
- [ ] Use Komodo’s one-time stack-service execution, equivalent to `docker compose run --rm renovate`.
- [ ] Create a Komodo Procedure scheduled every 6–12 hours.
- [ ] Enable alerts for failed executions.
- [ ] Keep automatic image redeployment disabled for the Renovate stack.

References:

- https://github.com/moghtech/komodo/blob/main/docsite/docs/deploy/compose.md
- https://komo.do/docs/automate/procedures

## Testing and rollout

- [ ] Set `automerge` to `false` temporarily.
- [ ] Run `npx renovate --platform=local --dry-run=extract` if local CLI testing is useful.
- [ ] Run the transient Komodo service manually.
- [ ] Confirm active Compose files are detected.
- [ ] Confirm `archive/**` is ignored.
- [ ] Confirm image tags and digests are updated correctly.
- [ ] Review generated PRs or merge requests.
- [ ] Re-enable automerging only after several successful runs.
- [ ] Pin the Renovate image to a reviewed digest.

## Alternatives without pull requests

- Komodo image polling and redeployment: simple, but no review history.
- Watchtower: automatic updates, but little control and no PR workflow.
- Diun: notifications only.
- Renovate local mode: reporting/testing only; it cannot create branches or pull requests.
