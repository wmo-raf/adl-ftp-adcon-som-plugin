# ADL ADCON FTP Somalia Plugin

A **decoder plugin** for the [ADL FTP Plugin](https://github.com/wmo-raf/adl-ftp-plugin):
lets an ADL FTP/SFTP connection decode the daily CSV observation export files
the ADCON addVANTAGE server of Somalia's meteorological service pushes to an
FTP server. It adds the *ADCON FTP Somalia* entry to the FTP connection's
Decoder list and nothing else — hosts, credentials and station links are the
FTP plugin's.

**Operator guide:** [docs/guide.md](docs/guide.md) — the file format, how to
configure the FTP connection and station links for it, collection behaviour,
diagnostics, troubleshooting and the current **compatibility status** (read
it: this release does not produce observations on the current FTP plugin and
ADL core). The guide is also published on the central ADL documentation site.

## Development setup

The plugin runs inside the ADL core image, which must already contain the
ADL FTP Plugin. Build the `adl:latest` image from the
[ADL core repository](https://github.com/wmo-raf/adl) with the FTP plugin in
its `plugins.toml`, then:

```bash
git clone https://github.com/wmo-raf/adl-ftp-adcon-som-plugin.git
cd adl-ftp-adcon-som-plugin
cp .env.sample .env        # set PLUGIN_BUILD_UID=$(id -u), PLUGIN_BUILD_GID=$(id -g), ADL_DB_PASSWORD
docker compose -f docker-compose.dev.yml build
docker compose -f docker-compose.dev.yml up
docker compose -f docker-compose.dev.yml exec adl adl createsuperuser
```

The admin is served by the bundled nginx proxy on `ADL_WEB_PROXY_PORT`
(default 80). The plugin source is bind-mounted, so code changes reload the
dev server. If the build fails with `pull access denied` for `adl:latest`,
prefix the build with `DOCKER_BUILDKIT=0`.

See [CONTRIBUTING.md](CONTRIBUTING.md) — a change to the decoder's file
format or to any admin surface must update the guide in the same PR.
