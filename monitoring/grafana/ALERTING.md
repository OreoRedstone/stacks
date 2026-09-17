# Grafana alerting

Alerting resources in `alerting/` are provisioned into Grafana at startup.
Grafana-managed rules query the provisioned Prometheus datasource and send
notifications through the `ntfy` webhook contact point.

## Required variables

Set these as Komodo stack variables or in an ignored local `.env` file for the
`monitoring` stack:

- `NTFY_ALERT_URL` — the HTTPS ntfy topic URL used for publishing alerts. The
  Grafana template query parameter is added by the provisioned contact point.
- `NTFY_ALERT_TOKEN` — an ntfy access token with publish permission for that
  topic.

They are deliberately not stored in Git. Grafana substitutes these variables
when it provisions `contact-points.yaml`.

## Endpoint opt-in

Only Blackbox targets labelled `alerting: enabled` are included in endpoint
alerts and certificate-expiry alerts. This prevents intentionally stopped
applications from generating notifications. Arr routes are currently marked
`disabled` while their HTTPS redirect behavior is being repaired.

Provisioned resources are managed from Git and should not be edited in the
Grafana UI. Change the files in `alerting/` and redeploy or reload Grafana
provisioning.
