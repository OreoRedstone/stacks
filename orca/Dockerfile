FROM debian:bookworm-slim

ARG TARGETARCH
ARG ORCA_VERSION=1.4.258
ARG ORCA_SHA256_AMD64=fd7f23f5fb6fe43fb2982d17438d772fac7cc65c8208a212d0ffb224b504e311
ARG ORCA_SHA256_ARM64=a1279923700196e8ccd94952fea039f6d98f5d4f9485afca0295eddea8ccb033

RUN apt-get update \
    && apt-get install --no-install-recommends --yes \
        bash \
        ca-certificates \
        curl \
        git \
        openssh-client \
    && rm -rf /var/lib/apt/lists/*

RUN set -eu; \
    case "${TARGETARCH}" in \
        amd64) orca_arch=x64; orca_sha256="${ORCA_SHA256_AMD64}" ;; \
        arm64) orca_arch=arm64; orca_sha256="${ORCA_SHA256_ARM64}" ;; \
        *) echo "Unsupported architecture: ${TARGETARCH}" >&2; exit 1 ;; \
    esac; \
    archive="orca-server-linux-${orca_arch}.tar.gz"; \
    curl --fail --show-error --silent --location \
        "https://github.com/stablyai/orca/releases/download/v${ORCA_VERSION}/${archive}" \
        --output "/tmp/${archive}"; \
    printf '%s  %s\n' "${orca_sha256}" "/tmp/${archive}" | sha256sum --check --status -; \
    mkdir -p /opt/orca-server; \
    tar -xzf "/tmp/${archive}" --directory /opt/orca-server --strip-components=1; \
    rm "/tmp/${archive}"; \
    chmod -R a+rX /opt/orca-server

RUN groupadd --gid 1000 orca \
    && useradd \
        --uid 1000 \
        --gid 1000 \
        --create-home \
        --home-dir /home/orca \
        --shell /bin/bash \
        orca \
    && mkdir -p /projects /home/orca/.local/bin \
    && chown -R 1000:1000 /home/orca /projects

ENV HOME=/home/orca
ENV PATH=/home/orca/.local/bin:/usr/local/bin:/usr/bin:/bin

USER 1000:1000
WORKDIR /projects

EXPOSE 6768/tcp

CMD ["/opt/orca-server/bin/orca-ide", "serve", "--bind", "0.0.0.0", "--port", "6768", "--pairing-address", "10.44.0.2", "--no-pairing"]
