# Self-hosted application stacks

This repository is a collection of Docker Compose projects for running and
maintaining a varied self-hosted environment. Each active application is kept
in its own directory, with its deployment definition and relevant service
configuration alongside it.

## What’s here

The stacks cover several areas of infrastructure and application hosting:

- **Networking:** reverse proxying and service discovery
- **Observability:** metrics, dashboards, and host monitoring
- **Home services:** home automation, photo management, file sharing, and
  media applications
- **Game hosting:** dedicated servers and supporting configuration
- **Maintenance:** dependency update automation

## Selected work

- **Monitoring:** Prometheus collects host and application metrics, with
  Grafana dashboards and alerting for service health and resource usage.
  Node Exporter and cAdvisor cover hosts and containers; application exporters
  and HTTP probes cover application metrics and endpoint reachability.
  Dashboards, data sources, and alerting configuration are versioned in Git.
  Proxmox storage alerts cover capacity thresholds and missing telemetry.
- **Networking:** a Traefik based reverse proxy routes services across
  independently managed stacks.
- **Media and personal services:** applications for photo libraries, media
  streaming, file sharing, and home automation are composed with their
  supporting databases and background services.
- **Game hosting:** dedicated game servers are managed as separate stacks with
  service-specific configuration.

## Maintenance

[Renovate](renovate.json) groups container updates by stack and separates major
upgrades from routine updates. Application-specific constraints account for
database compatibility and staged upgrades. Many container images use immutable
digests to identify the selected image precisely.

Active applications have separate directories with their Compose definitions
and supporting configuration. Retired projects live in `archive/` and do not
represent active deployments.
