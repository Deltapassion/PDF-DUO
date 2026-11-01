#!/bin/sh
# Lance PDF DUO sous Linux / macOS
cd "$(dirname "$0")"
exec python3 pdfduo.py "$@"
