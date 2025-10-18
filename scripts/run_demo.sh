#!/usr/bin/env bash
set -euo pipefail

# Invoice example (needs approval)
curl -s -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d @demo_fixtures/invoice_email.json

# Customer complaint (auto)
curl -s -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d @demo_fixtures/complaint_email.json

# Sheet alert (auto)
curl -s -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d @demo_fixtures/sheet_alert.json

echo
echo "Open the dashboard: http://localhost:8000"
