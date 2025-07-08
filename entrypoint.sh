#!/bin/sh
set -e

case "$1" in
  game)
    exec python play_cluedo.py
    ;;
  test)
    exec pytest --cov=cluedo_game --cov-report=term-missing
    ;;
  lint)
    exec pylint cluedo_game
    ;;
  code-server)
    exec code-server --bind-addr 0.0.0.0:8080 .
    ;;
  *)
    echo "Usage: $0 {game|test|lint|code-server}"
    exit 1
    ;;
esac
