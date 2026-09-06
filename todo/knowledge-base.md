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

## Option 1: SilverBullet

SilverBullet is a browser-based, self-hosted personal knowledge database built around Markdown pages, wiki links, backlinks, queries, tasks, and programmable Lua extensions.

Pros:

- Closest match to the previous workflow.
- Markdown files are portable and easy to back up.
- Powerful linking, queries, templates, and scripting.
- Lightweight compared with full team wiki platforms.
- Good for personal notes and homelab operations journals.

Cons:

- More personal/programmable than structured team documentation.
- Permissions and multi-user workflows need careful evaluation.
- Lua customisations can become difficult to maintain.
- Application and plugin compatibility should be checked before committing to a long-term space.

Compatibility:

- Traefik: straightforward web routing.
- Authentication: test native authentication and future SSO/forward-auth before exposing it to others.
- Storage: simple Markdown space is easy to back up.
- AI tooling: Markdown and APIs/scripts are promising, but verify the exact integration desired.

Tasks:

- [ ] Deploy a temporary SilverBullet instance.
- [ ] Import or reconstruct a sample of previous notes.
- [ ] Test attachments, search, backlinks, queries, and mobile use.
- [ ] Test multi-user access and permissions.
- [ ] Test the selected authentication provider.
- [ ] Test backup and restore of the Markdown space.
- [ ] Decide whether Lua extensions are worth the maintenance cost.

Documentation: https://silverbullet.md/

## Option 2: BookStack

BookStack uses a structured hierarchy of shelves, books, chapters, and pages. It is designed for readable documentation and operational manuals rather than free-form linked notes.

Pros:

- Very approachable for household users and collaborators.
- Strong hierarchy and navigation.
- Good revision history, permissions, and page organisation.
- Official documentation covers OIDC, SAML, LDAP, and other authentication methods.
- Good fit for service runbooks and how-to documentation.

Cons:

- Less natural than SilverBullet for graph-like notes and rapid capture.
- Requires an application and database.
- Content is not naturally a directory of standalone Markdown files, so export testing matters.
- More structured authoring may feel slower for personal notes.

Compatibility:

- Traefik: good.
- Authentik, Authelia, or Keycloak: good through supported OIDC/SAML/LDAP options; test the chosen provider.
- Backups: back up the database, uploaded files, and configuration together.
- Existing services: excellent for documenting runbooks, recovery steps, and user guides.

Tasks:

- [ ] Deploy BookStack and its database in a test stack.
- [ ] Configure Traefik and HTTPS.
- [ ] Test OIDC with the selected identity provider.
- [ ] Configure admin, household, and guest roles.
- [ ] Test export and restore.
- [ ] Create sample books for infrastructure and household documentation.

Documentation: https://www.bookstackapp.com/docs/

## Option 3: Wiki.js

Wiki.js is a general-purpose wiki with a modern editor, multiple storage options, versioning, search, and broad authentication support.

Pros:

- Good balance between personal and collaborative documentation.
- Strong authentication and permissions options.
- Supports Markdown and multiple content/storage backends.
- Familiar wiki model for household and technical users.
- Suitable for public and private sections.

Cons:

- More operational complexity than a file-based system.
- Database and storage configuration need to be backed up together.
- Migration/export behavior should be verified before adoption.
- Some advanced integrations may require more administration.

Compatibility:

- Traefik: good.
- Authentik, Authelia, and Keycloak: generally good through OIDC or proxy authentication; verify current versions.

- AI tooling: API support should be evaluated for the intended agent workflow.

Tasks:

- [ ] Test Wiki.js with the planned database and storage layout.
- [ ] Test OIDC, group permissions, Markdown import, and export.
- [ ] Test public/private page boundaries.
- [ ] Test backup and disaster recovery.

Documentation: https://docs.requarks.io/

## Option 4: Outline

Outline is a polished collaborative knowledge base organised around collections, documents, permissions, comments, revision history, and a modern editor.

Pros:

- Excellent collaborative editing experience.
- Strong collections, groups, permissions, comments, and revision history.
- OIDC-compatible authentication is supported.
- Good fit if the knowledge base will become a shared household or team system.
- Markdown and API export options are available.

Cons:

- More infrastructure than SilverBullet or BookStack.
- Requires database and object/file storage planning.
- Self-hosted authentication and storage configuration require careful setup.
- May be excessive for a single-user homelab notebook.

Compatibility:

- Traefik: good.
- Authentik, Authelia OIDC, and Keycloak: test OIDC configuration.
- Backups: include database, object storage, attachments, and encryption/configuration secrets.
- AI tooling: has API and MCP-related capabilities, but review access controls carefully before enabling agents.

Tasks:

- [ ] Review self-hosted deployment requirements.
- [ ] Test OIDC with the planned identity provider.
- [ ] Test attachment storage and restore.
- [ ] Test Markdown/JSON export.
- [ ] Evaluate whether collaboration and MCP/API access justify the operational cost.

Documentation: https://docs.getoutline.com/

## Option 5: Docmost

Docmost is a collaborative wiki/documentation platform with real-time editing, permissions, pages, databases/boards, and self-hosted features.

Pros:

- Modern collaborative editor.
- Useful for pages, tables, boards, and shared documentation.
- Designed for team-style knowledge management.
- Potentially useful if household documentation grows beyond simple pages.

Cons:

- Newer project and should receive a careful upgrade/backup review.
- May require a paid or limited edition for some advanced features; verify before choosing.
- Less proven for long-term Markdown portability than SilverBullet or a Git-backed wiki.
- Additional operational complexity for a small homelab.

Compatibility:

- Traefik: should be straightforward through its web service.
- Authentication: verify exact OIDC/LDAP support in the edition selected.
- Backups and exports: test before storing authoritative runbooks.
- AI tooling: attractive if self-hosted AI/MCP is a goal, but review privacy and permissions.

Tasks:

- [ ] Confirm licensing and feature availability for self-hosting.
- [ ] Test authentication, permissions, export, and restore.
- [ ] Compare resource use with Outline and Wiki.js.

Documentation: https://docmost.com/

## Option 6: DokuWiki

DokuWiki is a mature file-based wiki with a low infrastructure footprint and no database requirement.

Pros:

- Very reliable and lightweight.
- Pages and media are stored as files, simplifying backup and recovery.
- Mature permissions and plugin ecosystem.
- Excellent fallback if database availability is a concern.

Cons:

- Older-looking editing experience.
- Less fluid for modern collaborative editing.
- Plugins and themes require maintenance.
- Weaker fit for highly linked, programmable personal notes than SilverBullet.

Compatibility:

- Traefik: good.
- Authentication: supports multiple integrations; verify OIDC/LDAP needs.
- Backups: excellent because the data is file-based.
- Existing services: good for stable runbooks and reference documentation.

Tasks:

- [ ] Test the editor and mobile experience.
- [ ] Test authentication and namespace permissions.
- [ ] Test media backup and restore.

Documentation: https://www.dokuwiki.org/dokuwiki

## Option 7: Git-backed Markdown with Obsidian or a static site

Keep the source of truth as Markdown in Git and use Obsidian, VS Code, MkDocs, Quartz, Hugo, or a similar frontend.

Pros:

- Maximum portability and version history.
- Works naturally with this repository and AI agents.
- Easy to review changes and automate publishing.
- No application database required for the source content.

Cons:

- Multi-user editing and permissions are weaker.
- Mobile editing and synchronisation require additional tooling.
- Private/public publishing boundaries need careful repository and deployment design.
- Search, backlinks, comments, and uploads vary by frontend.

Compatibility:

- Traefik: excellent for a static frontend.
- Authentication: protect the published site at Traefik or keep it VPN-only; authoring access is controlled by Git.
- Backups: excellent through Git plus repository backups.
- Existing `wiksite`: is intentionally separate as a personal website/blog for the owner and a friend; do not assume it is the knowledge-base frontend.

Tasks:

- [ ] Decide whether the source content should live in this repository or a separate private repository.
- [ ] Test Obsidian/VS Code editing and mobile synchronisation.
- [ ] Choose a static frontend if household browser access is required.
- [ ] Define private/public content boundaries.
- [ ] Test publishing, rollback, and backup recovery.

## Comparison summary

| Option | Best for | Operational cost | Portability | Multi-user access | Auth integration |
| --- | --- | ---: | ---: | ---: | ---: |
| SilverBullet | Personal linked notes | Low | High | Medium | Verify per deployment |
| BookStack | Structured runbooks | Medium | Medium | High | Good |
| Wiki.js | General-purpose wiki | Medium | Medium | High | Good |
| Outline | Polished collaboration | Medium/high | Medium | High | Good OIDC |
| Docmost | Modern collaborative workspace | Medium/high | Medium | High | Verify edition/version |
| DokuWiki | Stable lightweight wiki | Low | High | Medium/high | Good with plugins |
| Git + Markdown | Versioned technical docs | Low | Very high | Low/medium | Git/VPN/proxy |

## Recommended evaluation order

1. SilverBullet, because it matches the previous workflow.
2. BookStack, because it is a strong choice for durable household and operational runbooks.
3. Wiki.js, if broader wiki/authentication flexibility is required.
4. Outline or Docmost, if collaborative editing becomes the priority.
5. DokuWiki or Git-backed Markdown if minimal infrastructure and portability matter most.

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
