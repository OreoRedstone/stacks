# Homelab knowledge organisation system

## Goal

Choose and deploy a self-hosted knowledge-management system for homelab documentation, procedures, architecture notes, troubleshooting records, service credentials references, and household guidance.

The system should be easy to back up, accessible through Traefik, compatible with the future authentication provider, and usable by both the owner and selected household users.

## Requirements

- [ ] Markdown or another exportable format.
- [ ] Full-text search.
- [ ] Internal links, tags, and backlinks where useful.
- [ ] Attachments and images.
- [ ] Page history or Git history.
- [ ] Mobile-friendly browser experience.
- [ ] Optional desktop/offline workflow.
- [ ] User and group permissions.
- [ ] OIDC, LDAP, SAML, or reliable reverse-proxy authentication.
- [ ] Simple Docker Compose deployment.
- [ ] Backups with a documented restore process.
- [ ] Export that remains readable if the application is abandoned.
- [ ] API or automation support for AI tools and scripts, if available.
- [ ] Clear separation between private infrastructure notes and household-facing documentation.

## Proposed content structure

```text
Home
├── Homelab overview
├── Network and DNS
├── Hosts, storage, and backups
├── Applications
│   ├── Management runbooks
│   ├── Media services
│   ├── Photos and files
│   └── Game servers
├── Monitoring and incident notes
├── Security and recovery
├── How-to guides
├── Household services
└── Archive
```

Keep secrets out of the knowledge base. Store only secret locations, rotation procedures, and recovery instructions. Never document passwords, private keys, recovery codes, or API tokens in plain text.

## Deferred alternatives

BookStack, Wiki.js, Outline, Docmost, and DokuWiki remain possible fallback
choices if collaboration, structured manuals, or database-free operation become
more important than a personal Markdown workflow. They are intentionally not
the current evaluation focus. Revisit them only if Obsidian plus the selected
publishing workflow fails a requirement.

## Primary direction: Git-backed Markdown

Keep the source of truth as Markdown in a private Git repository. Use Obsidian
for authoring and choose a separate frontend only if browser access for other
household users is needed.

Pros:

- Maximum portability, version history, and recovery confidence.
- Works naturally with AI agents, VS Code, scripts, and pull requests.
- No application database is required for the source content.
- Publishing can be added without changing the authoring workflow.

Cons:

- Multi-user editing and permissions are weaker than a collaborative wiki.
- Mobile editing and synchronisation require an explicit strategy.
- Private/public publishing boundaries need careful repository and deployment
  design.
- Attachments, comments, and search vary by frontend.

Compatibility:

- Traefik: excellent for a static frontend.
- Authentication: protect any published site at Traefik or keep it VPN-only;
  authoring access is controlled by Git.
- Backups: excellent through Git plus repository backups.
- Existing `wiksite`: remains separate as a personal website/blog for the
  owner and a friend; it is not the knowledge-base frontend.

### Obsidian authoring

Obsidian is the preferred first test because it provides local Markdown files,
backlinks, graph navigation, templates, properties, and a strong desktop/mobile
workflow without making the repository depend on a database.

- [ ] Create a private knowledge-base repository or a clearly separated
  directory; do not mix private notes into the public `wiksite` source.
- [ ] Test Obsidian desktop and mobile editing against the chosen sync method.
- [ ] Compare Git sync, Syncthing, and Obsidian Sync for conflict handling,
  offline use, and multi-device recovery.
- [ ] Decide how attachments, plugins, templates, and workspace files are
  handled in Git.
- [ ] Keep community plugins to a reviewed allowlist.

### Frontend options

| Frontend | Strength | Main trade-off |
| --- | --- | --- |
| Obsidian Publish | Lowest maintenance and native Obsidian integration | Hosted service and less control over private infrastructure |
| MkDocs Material | Excellent documentation, search, navigation, and Git workflow | Structured documentation rather than a personal graph-oriented workspace |
| Quartz | Strong Obsidian-style backlinks, graph features, and static publishing | More customisation and frontend maintenance |
| Hugo | Fast, mature static publishing and themes | Requires more authoring conventions and theme work |
| Gitiles/Git web UI | Minimal and close to the source repository | Weak household-facing navigation and search |

Preferred order: Obsidian alone first, then MkDocs Material for operational
documentation, or Quartz if backlinks and graph navigation are central.

### Publishing and sharing

- [ ] Decide whether the source content should live in this repository or a
  separate private repository.
- [ ] Define private infrastructure, household, and optionally public content
  boundaries using separate directories or repositories.
- [ ] Choose MkDocs Material, Quartz, or Hugo only if a browser frontend is
  actually needed.
- [ ] Keep publishing read-only and build it from a controlled branch.
- [ ] Test publishing, rollback, and backup recovery.

## Comparison summary

| Approach | Best for | Operational cost | Portability | Multi-user access |
| --- | --- | ---: | ---: | ---: |
| Obsidian + Git | Personal notes and infrastructure source material | Low | Very high | Low/medium |
| Obsidian + MkDocs | Searchable operational documentation | Low/medium | Very high | Medium |
| Obsidian + Quartz | Linked notes with a web frontend | Medium | Very high | Medium |
| Obsidian + Hugo | Custom static publishing | Medium | Very high | Medium |
| Deferred wiki platform | Collaboration-first requirements | Medium/high | Medium | High |

## Recommended evaluation order

1. Obsidian with a private Git-backed Markdown vault.
2. Obsidian plus MkDocs Material for searchable operational documentation.
3. Obsidian plus Quartz if backlinks and graph navigation should be visible in
   the browser.
4. Hugo if the publishing experience needs substantial customisation.
5. Revisit the deferred wiki platforms only if collaborative editing or
   permissions become more important than portability.

## Deployment and integration checklist

- [ ] Choose a hostname, such as `wiki.74services.net`.
- [ ] Add a dedicated Compose stack to this repository.
- [ ] Use persistent storage under `/mnt/docker-data`.
- [ ] Attach the application to the external `traefik` network.
- [ ] Add an explicit Traefik backend port.
- [ ] Keep the database on the internal Compose network.
- [ ] Decide whether the site is private, household-only, or partly public.
- [ ] Integrate with the chosen authentication provider only after the provider’s recovery path is tested.
- [ ] Keep a local admin/recovery account.
- [ ] Add the application and database to backup coverage.
- [ ] Test a full restore on a separate path.
- [ ] Document ownership, update procedure, and export procedure.
- [ ] Keep `wiksite` separate as the personal website/blog for the owner and a friend.
- [ ] Decide whether the knowledge base should publish any selected content to `wiksite`; do not share private infrastructure notes by default.
- [ ] Add the selected application to Renovate coverage.

## AI and automation considerations

- [ ] Decide whether AI agents need read-only access, write access, or no direct access.
- [ ] Prefer an API token scoped to the knowledge base rather than administrator credentials.
- [ ] Keep secrets and sensitive recovery data excluded from agent-accessible collections.
- [ ] Log or review automated edits.
- [ ] Test export before allowing automated restructuring.
- [ ] Consider a separate private infrastructure collection and a household-safe collection.
