#!/usr/bin/env bash
set -euo pipefail

echo "Posting invoice_email.json ..."
curl -s -X POST http://localhost:8000/ingest   -H "Content-Type: application/json"   -d @demo_fixtures/invoice_email.json
echo
echo "----"

echo "Posting complaint_email.json ..."
curl -s -X POST http://localhost:8000/ingest   -H "Content-Type: application/json"   -d @demo_fixtures/complaint_email.json
echo
echo "----"

echo "Posting sheet_alert.json ..."
curl -s -X POST http://localhost:8000/ingest   -H "Content-Type: application/json"   -d @demo_fixtures/sheet_alert.json
echo
echo "----"

echo "Open the dashboard: http://localhost:8000"
