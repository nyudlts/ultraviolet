---
layout: default
title: Test Mode Setup (Docker)
parent: Getting Started
nav_order: 1
has_toc: true
---
# {{ page.title }}

## Prerequisites
- Docker [(installation instructions)]({{ 'getting-started/install_docker' | absolute_url }})

## Steps

- get the local copy of the ultraviolet app:

```sh
git clone https://github.com/nyudlts/ultraviolet
cd ultraviolet
```
- create .invenio.private file which is used by invenio-cli tool
```sh
touch .invenio.private
```
- add the following lines to .invenio.private
[cli]
project_dir = < path to ultraviolet local directory>
services_setup = False

- build docker containers using invenio-cli tool
```sh
invenio-cli containers start --lock --build --setup
```

The Ultraviolet instance should now be available at this URL: https://127.0.0.1/

## Docker troubleshooting tips  

- Cleanup docker-compose to start over with `$ docker-compose down --rmi all --volumes  --remove-orphans`. Note: this might effect other docker projects if you have them!  
- Debug a docker-compose container with `$ docker logs --tail 50 --follow --timestamps CONTAINER-NAME`
