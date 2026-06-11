# caperadar.org

Static site for `caperadar.org`, served by Nginx in Docker.

## Contents

- `index.html`: single-page site with a Cloudflare Access setup generator
- `Dockerfile`: minimal Nginx image
- `docker-compose.yml`: local container runner

## Run

```bash
docker compose up --build
```

The site will be available at `http://localhost:8080`. The Cloudflare Access App Builder runs in the browser, can optionally query existing Cloudflare Tunnel records with a read-scoped API token, and generates local `cloudflared` commands, ingress YAML, and API payloads without storing API tokens.

## Notes

The USMT Python tooling has been moved out of this repository into `/root/usmt-tui`.
