---
layout: default
title: Docker CLI Cheatsheet
parent: Tips and Gotchas
nav_order: 1
---
# {{ page.title }}  

This document contains quick tips and tricks for Docker Desktop, Docker Engine, and Docker Compose.

## Commands

- [docker CLI](https://docs.docker.com/engine/reference/commandline/cli/)
- [docker compose CLI](https://docs.docker.com/compose/reference/)
- Information and plugins
```sh
docker info
```
- Check running containers
  ```sh
  docker ps
  ```
- Stop a specific container
  ```sh
  docker stop CONTAINER-ID
  ```
- Delete a specific container
  ```sh
  docker rm CONTAINER-ID
  ```
- Check existing images
  ```sh
  docker images
  ```
- Delete an existing image (all containers which use the image must be deleted)
  ```sh
  docker rmi IMAGE-ID
  ```
- Delete all unused resources
  ```sh
  docker system prune -s
  ```
- Debug a docker-compose container
  ```sh
  docker logs --tail 50 --follow --timestamps CONTAINER-NAME
  ```
- Cleanup/clobber docker-compose to start over
  ```sh
  docker-compose down --rmi all --volumes  --remove-orphans
  ```
