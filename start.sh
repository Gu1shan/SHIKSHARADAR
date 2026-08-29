#!/usr/bin/env bash
# Shiksha Radar launcher — bootstraps venv, demo data, and starts the dashboard.
set -euo pipefail

PORT="${PORT:-8501}"
HEADLESS=false
for arg in "$@"; do
  case "$arg" in
    --no-browser) HEADLESS=true ;;
    *) echo "Unknown option: $arg (supported: --no-browser)"; exit 1 ;;
  esac
done

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()  { printf "${GREEN}✓${NC} %s\n" "$1"; }
step()  { printf "→ %s\n" "$1"; }
fail()  { printf "${RED}✗ %s${NC}\n" "$1"; exit 1; }

cd "$(dirname "$0")"

# --- 1. Virtual environment -------------------------------------------------
DEPS_OK() {
  venv/bin/python -c "import streamlit, pandas, numpy, plotly, scipy, sklearn, requests, reportlab" > /dev/null 2>&1
}

if [ ! -d venv ]; then
  step "venv/ not found — creating virtual environment..."
  python3 -m venv venv || fail "could not create venv (is python3 installed?)"
fi

if ! DEPS_OK; then
  step "installing/checking dependencies (first run may take a minute)..."
  venv/bin/pip install -q --upgrade pip
  venv/bin/pip install -q -r requirements.txt || fail "dependency install failed"
  DEPS_OK || fail "dependencies still missing after install"
fi
info "venv ready"

# --- 2. Demo data ------------------------------------------------------------
if [ ! -f data/synthetic/responses.csv ]; then
  step "demo data missing — generating synthetic dataset..."
  venv/bin/python scripts/generate_synthetic.py || fail "synthetic data generation failed"
fi
info "demo data found"

# --- 3. Launch ----------------------------------------------------------------
HEADLESS_FLAG=""
if [ "$HEADLESS" = true ]; then
  HEADLESS_FLAG="--server.headless true"
fi

info "starting dashboard on http://localhost:${PORT}"
exec venv/bin/streamlit run streamlit_app.py \
  --server.port "$PORT" $HEADLESS_FLAG
