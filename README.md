# Cluedo_Game

A Python implementation of the classic Cluedo game, with Docker-based development and CI pipeline.

## Features
- Dockerized environment
- Automated testing with pytest and coverage
- Linting with pylint
- Ready for GitHub Actions CI

## Quickstart

### Build & Run Tests
```bash
docker build -t cluedo_game .
docker run --rm cluedo_game
```

### Lint
```bash
docker run --rm cluedo_game pylint src/
```
