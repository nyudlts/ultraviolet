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

1. Get the local copy of the ultraviolet app:
  ```sh
  git clone https://github.com/nyudlts/ultraviolet && cd ultraviolet
  ```
2. Create an `.invenio.private` file which is used by the invenio-cli tool
  ```sh
  touch .invenio.private
  echo -e "[cli]\nproject_dir = "$PWD"\nservices_setup = False" >> .invenio.private
  ```
3. If you have used Invenio Framework before, this is a good time to make sure that you do not have old images or running containers. (Check [Docker troubleshooting tips]({{ 'tips-and-gotchas/docker' | absolute_url }}) for helpful commands).
4. Build docker containers using invenio-cli tool
  ```sh
  invenio-cli containers start --lock --build --setup
  ```
  The Ultraviolet instance should now be available at this URL: <https://127.0.0.1/>. You are using self-signed certificate so you might want to use FireFox 

