# Offline reference library: Project NOMAD and alternatives

Researched 2026-11-18. Scope: a local reserve of useful public knowledge,
separate from the private Markdown/Obsidian workflow in
[`knowledge-base.md`](knowledge-base.md). Research only; nothing installed.

## Recommendation

**Trial Project NOMAD in a dedicated VM, initially without AI.** It closely
matches the desired experience: a coherent interface for selecting and using
offline reference material, courses, maps, and utilities. Keep independently
readable copies of the content outside that VM. If the real requirement settles
at “Wikipedia plus a carefully chosen reference shelf”, **Kiwix Serve is the
simpler long-term fit for this Compose repository**. NOMAD itself uses Kiwix;
these choices can share the same underlying ZIM archives. This recommendation
is an assessment of the architectures below, not a runtime test.

## What Project NOMAD actually provides

Crosstalk Solutions' Project NOMAD is a Docker orchestrator with a browser
“Command Center”, rather than a new Wikipedia archive format. It brings together
Kiwix for reference archives, Kolibri for courses, regional ProtoMaps maps,
CyberChef, FlatNotes, and optional Ollama plus Qdrant for local AI/document
retrieval. Its setup wizard and curated collections are the main advantage over
assembling those applications separately. Installing the dashboard does not
automatically download all useful knowledge. [Official README](https://github.com/Crosstalk-Solutions/project-nomad/blob/main/README.md)

The documented minimum is a 2 GHz dual-core machine, 4 GB system RAM and 5 GB
free disk, with 10 GB suggested for comfortable installation. Upstream says the
non-AI stack uses under 1 GB RAM. Ubuntu 26.04 LTS is currently recommended;
Ubuntu 24.04 and Debian 12 are also supported. The much larger 32 GB RAM,
GPU and 250 GB recommendations concern AI use. A GPU is unnecessary for reading
Wikipedia. Confirm architecture support before buying an ARM device: the FAQ's
ARM answer describes unsupported community builds, and some FAQ answers are
explicitly dated rather than synchronized with every release. [Requirements](https://github.com/Crosstalk-Solutions/project-nomad/blob/main/README.md#device-requirements), [FAQ](https://github.com/Crosstalk-Solutions/project-nomad/blob/main/FAQ.md)

Downloaded resources are designed to work without internet; installation,
additional downloads and updates require connectivity. Local AI also needs its
models downloaded first; an external API endpoint adds that endpoint as a
dependency. Offline operation does not mean network silence: the application
documents connectivity probes and external catalog/update endpoints. Optional
scheduled updates cover software, apps and content. The core is Apache-2.0;
bundled applications and downloaded works retain their own licenses. A live
GitHub API check returned stable **v1.35.1, published 2026-10-05**; cached web
results showed an older release. [README](https://github.com/Crosstalk-Solutions/project-nomad/blob/main/README.md), [release](https://github.com/Crosstalk-Solutions/project-nomad/releases/tag/v1.35.1)

The operational cost deserves attention. The installer runs as root. The current
Compose template gives the admin, updater and optional Dozzle access to the
Docker socket, gives the updater writable access to `/opt/project-nomad`, and
mounts the host filesystem read-only into a disk collector. Several images use
`latest` and `pull_policy: always`. NOMAD explicitly has no built-in
authentication. These are substantial host privileges for a content browser;
a dedicated VM provides a clearer boundary than adding it to the existing
shared Docker daemon. A restrictive read-only socket proxy cannot replace the
Docker write operations its orchestrator needs. [Security statement](https://github.com/Crosstalk-Solutions/project-nomad/blob/main/README.md#about-security), [management Compose](https://github.com/Crosstalk-Solutions/project-nomad/blob/main/install/management_compose.yaml)

## Alternatives worth considering

| Option | What it offers | Fit here |
| --- | --- | --- |
| **Kiwix / Kiwix Serve** | Downloaded ZIM archives opened by a local reader or served over HTTP. Official container accepts local archives mounted at `/data`; the documented local-file deployment needs no Docker socket or database. | Best minimal Compose choice. Less integrated content curation, courses and maps than NOMAD. [Container documentation](https://github.com/kiwix/kiwix-tools/blob/main/docker/server/README.md) |
| **Internet-in-a-Box (IIAB)** | A complete learning hotspot: Wikipedia, books, educational apps, maps, optional learning systems, and an admin console. Uses Ansible to install/configure the host; provides Raspberry Pi images. | Closest broad appliance alternative, especially for a portable low-power box. Treat as its own machine/VM rather than an ordinary additional Compose service. [Official repository](https://github.com/iiab/iiab) |
| **RACHEL, World Possible** | A Wi-Fi educational server/router with curated Wikipedia, Khan Academy, Gutenberg and other modules; packaged devices and deployment support. Current store promotes RACHEL 6 with offline semantic search. | Attractive for a classroom/community or a supported appliance; weaker fit for maintaining a small custom Compose stack. Confirm current DIY installation, update/support terms and each module's license before committing. [Project description](https://rachel.worldpossible.org/about), [current products](https://worldpossible.org/) |
| **Kolibri** | Offline-first learning platform with courses, learner accounts and progress tracking, rather than a general encyclopedia archive. Included in NOMAD. Linux guidance recommends 1 GB RAM; storage depends on imported channels. MIT-licensed application. | Add when structured education matters; unnecessary just to preserve reference articles. [User guide](https://kolibri.readthedocs.io/en/latest/install/system_requirements.html), [source/license](https://github.com/learningequality/kolibri) |
| **ArchiveBox** | Captures chosen URLs into ordinary HTML, PDF, screenshots, text, WARC and other files; Docker/Compose supported. Capture needs access to the source; retained files are locally readable. | Complement for practical sites, manuals and articles absent from curated archives. Every important capture needs offline inspection; retaining a URL does not prove every interactive feature or external dependency was captured. [Official documentation](https://docs.archivebox.io/latest/README.html) |

Kiwix tools are GPLv3-or-later; the live release API returned **3.8.2,
2026-03-02**. IIAB's latest stable release API returned **8.2, 2025-01-01**,
but its README recommends continuously tested prereleases: the stable date alone
does not establish inactivity. IIAB's repository license is GPLv2; packaged
components have their own licenses. ArchiveBox is MIT-licensed. RACHEL should
not be assumed to have one permissive license covering every module. Exact
latest Kolibri/ArchiveBox releases and RACHEL software support lifecycle were
not independently established in this pass. [Kiwix source](https://github.com/kiwix/kiwix-tools), [Kiwix release](https://github.com/kiwix/kiwix-tools/releases/tag/3.8.2), [IIAB release](https://github.com/iiab/iiab/releases/tag/release-8.2), [IIAB license](https://github.com/iiab/iiab/blob/master/LICENSE), [ArchiveBox source](https://github.com/ArchiveBox/ArchiveBox)

## Content matters more than the dashboard

For English Wikipedia, distinguish **article coverage** (`all` versus a subset
such as `top`) from **detail level**:

- `mini`: introduction and infobox only; unsuitable as the only detailed reference.
- `nopic`: full article text without images; closest to the original text-only idea.
- `maxi`: full edition with images; a better primary library when storage permits.

Images have practical value for diagrams, identification, anatomy and repairs;
prefer retaining them over adding AI first. That priority is a judgment, while
the edition definitions come from [Kiwix's FAQ](https://get.kiwix.org/en/faq-items/what-do-mini-nopic-and-maxi-mean-in-the-wikipedia-zim-files/).
Archives are dated snapshots, not live Wikipedia or a guarantee that every
linked external reference/media item is included. Kiwix currently requires a
replacement download rather than incremental archive updates. [General FAQ](https://get.kiwix.org/en/faq/)

**Planning allowances, not measured requirements:** reserve roughly 100–150 GB
for an illustrated full English Wikipedia archive, 50–70 GB for full text,
and 10–20 GB for an abbreviated edition; verify the chosen dated file before
provisioning. A 500 GB SSD is a reasonable first target for Wikipedia plus
selected manuals, books and regional maps; 1–2 TB offers room for video courses,
more languages and replacement snapshots. Keep space for old and new archives
during updates. For a modest household trial, 2 vCPUs/4 GB RAM without AI is a
starting allocation, then measure search and concurrent use. RACHEL's commercial
500 GB/1 TB/2 TB storage options illustrate how curated media libraries grow,
not a universal minimum. [World Possible storage FAQ](https://worldpossible.org/pages/main-faqs)

Start with Wikipedia, regional maps, relevant first-aid/public-health references,
home/equipment manuals and repair documentation. Select languages and local
relevance deliberately. Keep source dates and licenses alongside downloads;
an old reference archive and a generative answer should not be mistaken for
current professional guidance.

## Integration and a useful trial

For Kiwix, a future stack can follow this repository's existing conventions:
pinned image, read-only content under `/mnt/docker-data` or `/mnt/nas`, explicit
backend port, and the external `traefik` network. For NOMAD, let its dedicated
VM own its Docker daemon and application lifecycle; avoid competing Komodo and
NOMAD updates of the same child containers. Review and pin the selected release
rather than executing an unreviewed moving installer. These are proposed
integration choices, not deployment instructions already validated here.

Keep the library LAN/VPN-accessible, and give it a documented local address
that works when external DNS, TLS renewal or the identity provider is unavailable.
The authentication inconsistencies already recorded in [`../SECURITY.md`](../SECURITY.md)
make that recovery path particularly relevant. Also retain ZIM files, a matching
Kiwix desktop/mobile reader and its installer on a second device or USB SSD;
ordinary PDFs/EPUBs should remain separately readable. [Kiwix Reader](https://get.kiwix.org/en/solutions/applications/kiwix-reader/)

Before choosing permanently: disconnect WAN, reboot the appliance, search/read
sample material and maps from a phone, then repeat with Traefik/auth unavailable.
Test the portable copy with the main host and NAS unavailable. Record content
dates, checksums, a refresh schedule and a restore procedure. This tests the
actual goal: access to useful knowledge after the surrounding infrastructure
fails, rather than merely having a working dashboard today.
