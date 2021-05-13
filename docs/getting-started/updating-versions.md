---
layout: default
title: Updating Versions
parent: Getting Started
nav_order: 3
has_toc: true
---
# {{ page.title }}


## Updating UltraViolet

The InvenioRDM project is on a development schedule that cuts monthly releases on the core project and command line interface, `invenio-cli`. Our development of UltraViolet will follow accordingly. These instructions guide you through the process, which you should do when we deploy UltraViolet version updates. InvenioRDM status updates are usually posted on the [project blog.](https://inveniosoftware.org/blog/) We will send out notifications on the DLTS Slack when updates have been merged into the `main` branch.

1. Check to make sure you have the latest version of Invenio-CLI tool. To check your version run `invenio-cli --version`. Versions are released about once per month, so if it's out of date, run `pip install --upgrade invenio-cli`

2. Run `git pull` to bring in the updates to your local codebase.

3. Destroy existing images. To do this, make sure that Docker Desktop is up and then run `invenio-cli services destroy`

4. Follow steps 4-12 on the [Docker development guide]({{ 'getting-started/dev-docker-setup' | absolute_url }})
