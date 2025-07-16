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
  ai)
    exec python -m cluedo_game.game_with_ai
    ;;
  *)
    echo "Usage: $0 {game|test|lint|ai}"
    exit 1
    ;;
esac
