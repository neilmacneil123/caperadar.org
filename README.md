# caperadar.org

Static site for `caperadar.org`, served by Nginx in Docker.

## Contents

- `index.html`: single-page site
- `Dockerfile`: minimal Nginx image
- `docker-compose.yml`: local container runner

## Run

```bash
docker compose up --build
```

The site will be available at `http://localhost:8080`.

## Notes

The USMT Python tooling has been moved out of this repository into `/root/usmt-tui`.
