#!/usr/bin/env sh
set -e

# Honor Azure's PORT if provided; default to 8080
PORT="${PORT:-8080}"

exec streamlit run /app/app.py \
  --server.address 0.0.0.0 \
  --server.port "${PORT}" \
  --server.headless true \
  --browser.gatherUsageStats false


