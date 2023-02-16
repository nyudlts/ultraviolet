---
layout: default
title: Docker Installation
parent: Tips and Gotchas
nav_order: 0
---
# Install Docker

If you are running the application on your local machine then you need to install Docker and Docker Compose. You do not need to perform these steps if you are using the Vagrant configuration.

> at the moment the supported architecture is x86_64, not ARM64, not because of Docker but because of some python packages that are not compiled for ARM64.

**Problem:** There's two main ways to install Docker: Docker Engine + Docker Compose or Docker Desktop.  
**Context:** Onboarding and setup of Ultraviolet.  

- Docker Desktop: with a full GUI application that runs a Virtual Machine using Linux that then runs Docker Engine, Docker Compose and other tools.
  - pros: GUI, resource isolation, consistent fast setup, control over Docker RAM consumption, consistency cross-platform, friendlier to work with, easier to update and maintain.
  - cons: larger footprint on your development machine, VM overhead, nested virtualization issues in VM's.
- Docker Server: that uses a CLI only application running Docker Engine directly on the Linux Host. 
  - cons: No GUI, installation by parts, maintenance and updates by parts.
  - InvenioRDM cons: requires docker-compose standalone installation.
  - pros: Custom installation of tools easier for InvenioRDMs needs (docker-compose standalone instead of plugin), can be configured in an EC2 instance or AWS Workspace without nested virtualization.
  - InvenioRDM (hence Ultraviolet) runs with Docker Compose standalone (a pip package). Docker Compose v2 (a go binary) was launched in [April 26 2022](https://www.docker.com/blog/announcing-compose-v2-general-availability/) changing the installation of Compose to be of just a plugin to Docker. If you are installing Ultraviolet in the present you might need to use the [Docker Compose Standalone](https://docs.docker.com/compose/install/other/) instead of installing Compose as a plugin to docker.

> Both of these work with InvenioRDM, but in 2022 docker-compose was updated from a pip package to a Go binary. InvenioRDM still uses the older `docker-compose` v1. Docker Desktop allows backwards compatibility by using an alias solution but if you are going down the Server route we recommend using Docker Compose Standalone installation instead of the newer plugin type installation.

**Solution:** It depends. But [Docker Desktop](https://www.docker.com/blog/guest-blog-deciding-between-docker-desktop-and-a-diy-solution/) is easier to maintain for development.

> InvenioRDM doesn't even recommend to deploy this application in production in containerized form. But development benefits from faster setup this way.

+ Docker Desktop (with Docker Compose included)
  + MacOS (Intel)
    - Install [Docker Desktop](https://docs.docker.com/desktop/install/mac-install/)
    - Increase [Docker Desktop RAM](https://docs.docker.com/desktop/settings/mac/#advanced) allocation to [+6GB](https://inveniordm.docs.cern.ch/install/requirements/#available-memory-for-docker-macos).
  + Linux Desktop
    - Install [Docker Desktop](https://docs.docker.com/desktop/install/linux-install/)
    - Configure Docker for [non-root usage](https://inveniordm.docs.cern.ch/install/requirements/#permissions-to-run-docker-linux)
    - Increase [Docker Desktop RAM](https://docs.docker.com/desktop/settings/linux/#advanced) allocation to [+6GB](https://inveniordm.docs.cern.ch/install/requirements/#available-memory-for-docker-macos).
+ Docker Engine + Docker Compose Standalone (Server-like setup)
  + Debian (apt)
    - Install [Docker Engine](https://docs.docker.com/engine/install/debian/)
    - Configure Docker for [non-root usage](https://inveniordm.docs.cern.ch/install/requirements/#permissions-to-run-docker-linux)
    - Install [Docker Compose Standalone](https://docs.docker.com/compose/install/). `docker compose` plugin written in Go will not be recognized by `invenio-cli`.
    - Docker Engine on Linux can use the entire memory of the host, no RAM adjustments needed.
  + CentOS (yum)
    - Install [Docker Engine](https://docs.docker.com/engine/install/centos/)
    - Install [Docker Compose](https://docs.docker.com/compose/install/)
    - `sysctl -w vm.max_map_count=262144`
+ Check for successful installation with `docker --version` and `docker-compose --version` (note the usage of standalone docker-compose).
+ Post-install (any OS, any installation)
  - Increase memory map areas for [Elastic Search](https://inveniordm.docs.cern.ch/install/requirements/#elasticsearch-and-docker-macos-and-linux)
## Linux Docker Engine and Docker Desktop Post Install

Ensure you are running docker commands without `sudo`. This will allow `invenio-cli` to run docker commands comming from your user.
Even though Docker Desktop makes it possible to run docker commands without sudo, in order for the `invenio-cli` tool to talk to docker it has to be accesible to [non-root users](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)

# Troubleshooting Docker

Note for AWS Workspaces: when adding your user to the `docker` group in AWS workspaces $USER is not the same as [$whoami](https://en.wikipedia.org/wiki/Whoami#:~:text=On%20Unix%2Dlike%20operating%20systems,was%20used%20to%20log%20in.) which can lead to docker still needing sudo to run. Add your `$whoami` user instead of your `$USER` to the docker group.

# Troubleshooting Docker-Compose 

## Docker Compose not recognized by invenio-cli (as of 2023)

- **Problem:** Docker Compose is not recognized by invenio-cli.  
  - Context: Installation and setup of ultraviolet error when running:
  ```sh
  invenio-cli check-requirements --development
  ```
  - **Solution:** Install the `docker-compose` standalone.
- **Problem:** invenio-cli cannot run docker commands.  
  - Context: Installation and setup of Docker Engine and Docker Desktop in Linux.
  - **Solution:** InvenioRDM runs docker commands as a non-root user through the `invenio-cli` package.  
  - Solution 1: Ensure that your user can run docker commands as non-root: [Manage Docker as a non-root user](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user) 
  - Solution 2: Docker Desktop

## `docker compose` (v2) vs `docker-compose` (v1)

[Evolution of Compose](https://docs.docker.com/compose/compose-v2/)

- `docker-compose` v1:
  - InvenioRDM works with docker-compose v1, a python package.
  - v1 is currently in process of being [deprecated](https://www.docker.com/blog/announcing-compose-v2-general-availability/#:~:text=We%E2%80%99ve%20now%20marked%20Compose%20V1%20as%20deprecated) in favor of v2.
  - The default Docker Compose offered in the cli is now v2 in the form of a plugin.
  - For InvenioRDM use the [v1 standalone installer](https://docs.docker.com/compose/install/other/)
- `docker compose` v2:
  - Docker Compose got an update to v2 in June 2022, and became [General Availability in Nov 2022](https://www.docker.com/blog/announcing-compose-v2-general-availability/)
  - Docker Compose v2 is a Go Binary that is installed as a plugin to Docker Engine.
  - Doesn't require pip or python to run.
  - Docker Desktop installations have a symlink from `docker-compose` > `docker compose` to smooth integration of [v2](https://www.docker.com/blog/announcing-compose-v2-general-availability/#:~:text=On%20Docker%20Desktop%20version%204.4.2%2B%2C%20we%20enable%20aliasing%20of%20docker%2Dcompose%20syntax%20to%20docker%20compose%20by%20default)
  - Docker Desktop can be configured to run Docker Compose v1 instead of v2.

