#!/bin/bash

# Run PostgreSQL command
node dist/src/index.js \
  --postgresql \
  --host localhost \
  --port 5433 \
  --database steven \
  --user steven \
  --password "Secret!1234"
