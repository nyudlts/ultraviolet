---
layout: default
title: Dev Mode Setup (Docker)
parent: Getting Started
nav_order: 2
has_toc: true
---
# {{ page.title }}

## Prerequisites
- **Docker**
  + [Installation instructions]({{ 'tips-and-gotchas/install-docker' | absolute_url }})
- **Python 3.7**
  + To test which version you have, type `python` into the command prompt
  + There are different ways you can setup your python environment. We recommend using [pyenv](https://realpython.com/intro-to-pyenv/) to switch between python versions
- **Pip3**
  + [Installation instructions](https://pip.pypa.io/en/stable/installing/)
- **Node 14 and npm**
  + We recommend installing [nvm](https://github.com/nvm-sh/nvm#about) to manage node and npm versions.
  + Note that node versions are tied to bash profiles, so you may need to switch to a bash profile to deploy locally. Type `bash` in Terminal.

## Steps
1. Install [invenio-cli](https://invenio-cli.readthedocs.io/en/latest/)
  ```sh
  pip3 install invenio-cli
  ```
  IMPORTANT: Check to make sure you have the latest version of Invenio-CLI tool. To check your version run `invenio-cli --version`. Versions are released about once per month, so if it's out of date, run `pip3 install --upgrade invenio-cli`

2. Get the local copy of the UltraViolet source code:
  ```sh
  git clone https://github.com/nyudlts/ultraviolet.git && cd ultraviolet
  ```

3. Create an `.invenio.private` file which is used by the invenio-cli tool
  ```sh
  touch .invenio.private
  echo -e "[cli]\nproject_dir = "$PWD"\nservices_setup = False" >> .invenio.private
  ```
4. Add directory for persistent db volume
  ```sh
  mkdir -p app_data/db
  ```
5. Assign application key. For local development version it can be any random value
  ```sh
  export FLASK_SECRET_KEY=myrandomvalue
  ```

6. Build application python environment and web assets (make sure that you use node 14; check by running `node -v`)
  ```sh
  invenio-cli packages lock --pre --dev
  invenio-cli install --pre --development
  ```
7. If you have used Invenio Framework before, this is a good time to make sure that you do not have old images or running containers. (Check [Docker troubleshooting tips]({{ 'tips-and-gotchas/docker' | absolute_url }}) for helpful commands).

8. Build application services (database, search, cache) and setup the application for running
  ```sh
  invenio-cli services setup
  ```
  IMPORTANT: if services setup reported any errors, and you have to restart the setup process, make sure to run
  destroy service command first (or you will get "Failed to setup services" error ) and delete db files by running `invenio-cli services destroy` and `rm -r app_data/db/*`

9. Add local admin user
  ```sh
  invenio-cli shell
  invenio users create admin@test.com --password=123456 --active
  invenio roles add admin@test.com admin
  ```
10. If you do any local UI customization you need to rebuild applications web assets
  ```sh
  invenio-cli assets build --development
  ```

11. Start the application.
  ```sh
  invenio-cli run
  ```

  The Invenio instance should now be available at this URL: <https://127.0.0.1:5000/>!  
  Because of the invalid TLS warning, you will need to use Firefox.

  You can login using account `admin@test.com` which you've just created and start uploading data.

11. Quit the application with `Ctr-C` and spin down the containers with `invenio-cli containers stop`
