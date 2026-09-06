# Paperless-ngx document archive

## Goal

Evaluate and, if useful, deploy Paperless-ngx as a private document archive for scanned paperwork, downloaded PDFs, receipts, invoices, contracts, warranties, tax records, manuals, and other personal or household documents.

Paperless should remain distinct from the homelab knowledge base and Nextcloud:

- Paperless: authoritative archive of documents.
- Knowledge base: notes, explanations, procedures, and links.
- Nextcloud: general files, collaboration, and sharing.

The initial deployment should be owner-only. Any future sharing of documents must be designed deliberately because the archive may contain financial, legal, medical, or identity-related information.

## Why it may be relevant

- [ ] List the paper and PDF documents currently worth preserving.
- [ ] Estimate annual document volume and storage requirements.
- [ ] Identify scanner, phone-scanning, email, and download workflows.
- [ ] Decide whether receipts and invoices need links or references in Actual Budget.
- [ ] Decide whether manuals and homelab purchase records belong in Paperless or the knowledge base.
- [ ] Do not adopt it solely for homelab notes; SilverBullet, BookStack, Wiki.js, or another knowledge tool is a better fit for that purpose.

## Core capabilities to evaluate

- [ ] OCR accuracy for the languages and document quality in use.
- [ ] Full-text search and text selection in scanned PDFs.
- [ ] Tags, correspondents, document types, custom fields, and storage paths.
- [ ] Automatic classification and metadata matching.
- [ ] Consume-folder ingestion.
- [ ] IMAP/mail ingestion and mail rules.
- [ ] PDF/A output while retaining original files.
- [ ] Attachments, bulk import, duplicate handling, and export.
- [ ] REST API and automation options.
- [ ] User, group, ownership, and document permissions if sharing is later required.
- [ ] Optional local AI through Ollama or another compatible endpoint; keep remote AI disabled initially.

Reference documentation: https://docs.paperless-ngx.com/usage/ and https://docs.paperless-ngx.com/api/

## Proposed stack

Create a future `paperless/compose.yaml` containing:

- Paperless-ngx
- PostgreSQL, preferred for a new installation
- Valkey or another supported Redis-compatible message broker
- Optional Apache Tika and Gotenberg for Office documents and email attachments

Reference: https://docs.paperless-ngx.com/setup/ and https://docs.paperless-ngx.com/configuration/

Suggested persistent layout outside Git:

```text
/mnt/docker-data/paperless/
├── data/
├── media/
├── consume/
├── export/
└── postgres/
```

Tasks:

- [ ] Choose the final host and storage location.
- [ ] Confirm NAS performance and free space before storing the archive there.
- [ ] Use image version pinning and add the stack to Renovate coverage.
- [ ] Keep all passwords, database credentials, and API keys in Komodo secrets or excluded environment files.
- [ ] Use the external `traefik` network.
- [ ] Route a private hostname through Traefik with an explicit backend port.
- [ ] Avoid publishing Paperless, PostgreSQL, or Valkey ports directly on the host.
- [ ] Add health checks and an appropriate restart policy after the deployment model is confirmed.

## Ingestion design

Start with a controlled local workflow rather than automatically importing every shared file.

- [ ] Create a restricted consume directory owned by the Paperless container user.
- [ ] Test scanner-to-folder ingestion.
- [ ] Test manual browser uploads.
- [ ] Test email ingestion using a dedicated mailbox if needed.
- [ ] If using Nextcloud, use a controlled export/import directory or the API; do not share Paperless’s internal media directory directly.
- [ ] Define naming, tags, correspondent, document type, and custom-field conventions.
- [ ] Decide how to handle originals, duplicates, failed OCR, and documents requiring manual review.
- [ ] Document a quarantine process for incorrectly classified or suspicious files.

## Compatibility with existing stacks

### Nextcloud

Complementary rather than a replacement. Keep collaborative and general-purpose files in Nextcloud and archive final documents in Paperless. Avoid direct access to Paperless’s internal storage.

- [ ] Test a one-way import/export workflow.
- [ ] Decide which system is authoritative for shared documents.
- [ ] Confirm that shared users cannot browse private Paperless storage through an unrelated mount.

### Actual Budget

Paperless can hold receipts and invoices while Actual Budget remains the financial ledger.

- [ ] Define a consistent transaction reference, tag, or link convention.
- [ ] Test whether API or manual links provide enough value.
- [ ] Keep bank credentials and account secrets out of Paperless.

### Immich and streaming services

No direct integration is required. Immich remains the photo archive; Jellyfin, Kavita, Navidrome, and related services remain media applications.

### Knowledge base and wiksite

Use the knowledge base for procedures and explanations, linking to Paperless documents where appropriate. Keep `wiksite` separate as the personal website/blog for the owner and a friend.

### Monitoring and notifications

- [ ] Add Paperless container, PostgreSQL, Valkey, storage, and processing health to monitoring.
- [ ] Track failed or stalled document processing if a suitable metric or health check is available.
- [ ] Connect operational notifications to ntfy without sending document contents.

### Backups

The database alone is insufficient. Back up and restore as one application set:

- [ ] PostgreSQL database.
- [ ] Paperless media and original documents.
- [ ] Consume and export data where they are part of the recovery workflow.
- [ ] Configuration, secrets locations, and encryption keys as appropriate.
- [ ] Use the repository’s backup strategy after checking its current deployment status.
- [ ] Perform a test restore before importing irreplaceable records.

## Security and privacy checklist

- [ ] Keep the service private behind Traefik, VPN, or LAN access.
- [ ] Do not expose it publicly without a specific requirement and threat review.
- [ ] Use HTTPS and a strong unique application/database password.
- [ ] Test the selected authentication provider without creating a lockout or circular dependency.
- [ ] Preserve a local/admin recovery path independent of the identity provider.
- [ ] Do not mount broad host, Nextcloud, NAS, or Docker-socket paths.
- [ ] Restrict consume-folder permissions.
- [ ] Encrypt backups and verify who can access them.
- [ ] Disable remote OCR and remote AI unless the data-sharing implications are explicitly accepted.
- [ ] Never store passwords, private keys, recovery codes, or API tokens as documents.

## Evaluation deployment

- [ ] Deploy a temporary test instance with non-sensitive sample documents.
- [ ] Test OCR, search, tags, automatic matching, email, export, and API access.
- [ ] Test upgrades and database migration behavior.
- [ ] Test authentication and owner-only access through Traefik.
- [ ] Test backup and full restore on a separate location.
- [ ] Measure storage growth and processing time.
- [ ] Decide whether the service provides enough value to retain permanently.

## Decision

- [ ] Adopt Paperless-ngx as a permanent private archive.
- [ ] Defer until a scanner and ingestion workflow exists.
- [ ] Reject in favour of a simpler file archive or existing Nextcloud workflow.
- [ ] Record the final decision, hostname, storage paths, backup procedure, and access policy here.

