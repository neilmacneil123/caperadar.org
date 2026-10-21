# CapeRadar music launcher

A responsive, buildless homepage for https://caperadar.org and https://www.caperadar.org, based on the original CapeRadar site and its mascot.

Six direct links launch SynthWeb, CS-30, 606 Drums, Pocket Band, Fretboard, and Tuner. No analytics, third-party assets, runtime JavaScript or installation required. The previous IT landing page is preserved in `legacy-index.html` but is not published in the image.

Run locally with `docker compose up --build` (port 8080). Production uses the existing webapps Compose project on VM195, exposing port 8088 through the existing Cloudflare Tunnel. Nginx makes the homepage revalidate so updates are visible.
