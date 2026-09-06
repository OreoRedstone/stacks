# Authentication provider and access control

## Goal

Protect the owner-only backend and management plane first, then provide appropriate multi-user access to frontend services without creating a lockout or circular dependency. Dashboard and monitoring access is owner-only; services such as Jellyfin and Seerr have additional users.

## Service groups

### Backend / management

Komodo, Traefik dashboard, Grafana, InfluxDB, Prometheus, Prowlarr, Sonarr, Radarr, Lidarr, Bazarr, Deluge, Bindery, Actual Budget, Home Assistant administration, Immich administration, Nextcloud administration, Vaultwarden administration, ROMM administration, databases, and backup tooling.

These should be owner/admin-only, preferably LAN/VPN-only as well as authenticated.

### Frontend / multi-user services

Jellyfin, Seerr, Wizarr, Navidrome, Kavita, Nextcloud user access, Immich user access, ntfy, and game endpoints.

These need separate administrator, household, and possibly guest policies. Do not assume that proxy authentication works with mobile apps, APIs, WebSockets, invitation links, or desktop clients.

## Recommended architecture

```text
Internet / LAN → Traefik → access policy → service-native authentication
```

- [ ] Use SSO or forward authentication for backend web UIs.
- [ ] Restrict backend routes to administrator groups.
- [ ] Keep native local admin accounts as break-glass accounts.
- [ ] Prefer native authentication for Jellyfin, Seerr, Immich, Nextcloud, and Vaultwarden until each integration is tested.
- [ ] Use OIDC directly where an application supports it reliably.
- [ ] Use forward authentication only where it does not break application clients.

## Lockout and circular-dependency prevention

- [ ] Keep SSH, host console, or hypervisor console access available.
- [ ] Back up the identity-provider database and configuration before changes.
- [ ] Deploy the identity provider and database before its protected services.
- [ ] Create two administrator identities or one administrator plus a protected recovery account.
- [ ] Keep the identity provider’s own route unprotected by its own middleware.
- [ ] Keep Komodo on a separate trusted route during migration.
- [ ] Do not make Komodo depend on the identity provider to deploy or recover it.
- [ ] Keep known-good Compose files and recovery credentials directly on the host.
- [ ] Apply authentication to one low-risk service at a time.
- [ ] Test recovery while the identity provider is stopped.
- [ ] Document the command or label change that temporarily removes authentication middleware.

## Option 1: Authentik — primary recommendation

Pros:

- Full identity provider with users, groups, MFA, OIDC, SAML, LDAP, and proxy providers.
- Strong fit for Traefik and group-based backend/frontend policies.
- Good direct OIDC integration potential.

Cons:

- Heavier than Authelia.
- Requires a database and reliable backups.
- More configuration and policy complexity.

Compatibility:

- Traefik: good through forward authentication or proxy providers.
- Grafana, Nextcloud, Immich, and similar OIDC applications: generally good, but test per client.
- Jellyfin and Seerr: retain native accounts until OIDC/proxy behavior is verified.
- Sonarr/Radarr/Prowlarr and Deluge: prefer native auth plus LAN/VPN restrictions because API clients may fail behind proxy auth.
- Vaultwarden: preserve native authentication and test browser extensions/mobile clients carefully.
- Komodo: protect only after an independent recovery route exists.

Tasks:

- [ ] Restore or create an Authentik Compose stack with pinned images.
- [ ] Store its database password and secret key outside Git.
- [ ] Back up database, media, and configuration.
- [ ] Remove the worker Docker socket unless a specific integration requires it.
- [ ] Create administrator, household, and guest groups where appropriate for frontend services.
- [ ] Configure MFA and recovery.
- [ ] Reconcile the existing `authentik@docker` reference in Actual Budget with the `auth` middleware in `networking/dynamic.yaml`.
- [ ] Apply verified middleware to one service at a time.

Documentation: https://docs.goauthentik.io/

## Option 2: Authelia — lightweight alternative

Pros:

- Smaller operational footprint.
- Excellent Traefik forward-auth integration.
- Strong MFA and access-control-list model.

Cons:

- Less comprehensive as a user directory and application portal.
- More frontend applications may need native accounts.
- Per-application OIDC compatibility must be tested.

Tasks:

- [ ] Deploy Authelia with persistent configuration and storage.
- [ ] Configure MFA and account recovery.
- [ ] Configure Traefik forward authentication.
- [ ] Create separate administrator, household, and guest rules for frontend services.
- [ ] Test redirects, WebSockets, APIs, and mobile clients.

Documentation: https://www.authelia.com/integration/proxies/traefik/

## Option 3: Keycloak — standards-heavy option

Use this only if broad OIDC/SAML integration is more important than simplicity.

Pros: mature realms, clients, roles, groups, MFA, and federation.

Cons: heavier deployment and administration; usually requires an intermediary for Traefik forward authentication; native app authentication is still needed for some services.

- [ ] Deploy only if the operational cost is justified.
- [ ] Test OIDC with Grafana, Nextcloud, Immich, Jellyfin, and Seerr independently.
- [ ] Preserve local recovery accounts and an out-of-band management route.

Documentation: https://www.keycloak.org/documentation

## Option 4: OAuth2 Proxy

OAuth2 Proxy is a compatibility layer, not a user directory. It needs Authentik, Authelia OIDC, Keycloak, or another identity provider.

- [ ] Use only where direct OIDC or forward-auth integration is unavailable.
- [ ] Test APIs, WebSockets, redirects, logout, and mobile clients.
- [ ] Avoid adding it globally unless the extra failure point is justified.

Documentation: https://oauth2-proxy.github.io/oauth2-proxy/

## Option 5: VPN-only backend access

Use Tailscale, WireGuard, or another VPN for management services and retain native application authentication.

Pros: lowest complexity, excellent backend compatibility, and reduced public attack surface.

Cons: no SSO; the owner must use the VPN for private services; every application retains separate accounts.

- [ ] Make Komodo, monitoring, databases, and media automation tools LAN/VPN-only.
- [ ] Keep public frontend routes separate.
- [ ] Verify the VPN itself has an independent recovery path.

## Decision checklist

- [ ] Provider selected: ____________________
- [ ] Backend policy selected: SSO / forward-auth / VPN-only
- [ ] Frontend policy selected: native auth / OIDC / proxy auth
- [ ] Recovery route tested: ____________________
- [ ] Identity-provider backups tested: [ ]
- [ ] Komodo remains independently recoverable: [ ]
- [ ] One backend service tested: ____________________
- [ ] Dashboard owner-only access tested: [ ]
- [ ] Frontend multi-user access tested: [ ]
