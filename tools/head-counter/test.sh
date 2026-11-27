#!/bin/sh
set -eu
cd "$(dirname "$0")"
ROOT=$(cd ../.. && pwd)
python3 -m unittest discover -p 'test_*.py'
(cd "$ROOT" && python3 tools/smoke_build.py tools/head-counter)
