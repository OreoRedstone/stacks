# Networking roadmap

## Private administration routing

- [ ] Keep Deluge hostname access deferred while the current Traefik instance
  makes routed services Internet-facing by default.
- [ ] Evaluate a separate private Traefik instance, or a dedicated private
  entrypoint, for owner-only administration services such as Deluge.
- [ ] If implemented, route Deluge through the existing Gluetun namespace on
  port `8112`, remove its direct host binding, and retain Deluge-native
  authentication.
- [ ] Ensure any second proxy has an independent recovery path and does not
  introduce authentication or networking circular dependencies.

## Network structure

- [ ] Keep `traefik` as the edge network and avoid attaching databases to it.
- [ ] Keep `arr` private, adding services only when they need media-automation
  communication.
- [ ] Add `traefik.docker.network: traefik` to multi-network routed services
  where explicit network selection improves resilience.
- [ ] Review whether the VPN-shared services should eventually move into a
  dedicated stack with a clearly documented ingress path.
