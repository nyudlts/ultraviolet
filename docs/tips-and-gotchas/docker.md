---
layout: default
title: Docker Troubleshooting
nav_order: 5
parent: Tips and Gotchas
nav_order: 1
---
# {{ page.title }}  
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
