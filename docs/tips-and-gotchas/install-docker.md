---
layout: default
title: Docker Installation
parent: Tips and Gotchas
nav_order: 0
---
# Install Docker

If you are running the application on your local machine then you need to install Docker and Docker Compose. You do not need to perform these steps if you are using the Vagrant configuration.

### For Mac  
- [Docker](https://docs.docker.com/docker-for-mac/install/)

### For CentOS 7
- [Docker](https://docs.docker.com/install/linux/docker-ce/centos/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- `sysctl -w vm.max_map_count=262144`
