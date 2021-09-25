---
layout: default
title: Dev Mode Setup (Docker)
parent: Getting Started
nav_order: 1
has_toc: true
---
# {{ page.title }}

## Prerequisites
- **Docker**
  + [Installation instructions]({{ 'tips-and-gotchas/install-docker' | absolute_url }})
- **Python 3.7**
  + To test which version you have, type `python` into the command prompt
  + There are different ways you can setup your python environment. We recommend using [pyenv](https://realpython.com/intro-to-pyenv/) to switch between python versions
- **Pip**
  + You should have pip installed as part of your python installation. If it is missing you need to install it [Installation instructions](https://pip.pypa.io/en/stable/installing/)
- **Node 14 and npm**
  + We recommend installing [nvm](https://github.com/nvm-sh/nvm#about) to manage node and npm versions.
  + NOTE: if after nvm installation you are getting `nvm: not found` you can use the following [troubleshooting tips](https://github.com/nvm-sh/nvm#troubleshooting-on-linux)
- **Cairo**
  + [Installation instructions](https://invenio-formatter.readthedocs.io/en/latest/installation.html)

## Steps

1. Install [invenio-cli](https://invenio-cli.readthedocs.io/en/latest/)
  ```sh
  pip install invenio-cli
  ```

  IMPORTANT: Check to make sure you have the latest version of Invenio-CLI tool. To check your version run `invenio-cli --version`. Versions are released about once per month, so if it's out of date, run `pip install --upgrade invenio-cli`

2. Get the local copy of the UltraViolet source code:
  ```sh
  git clone https://github.com/nyudlts/ultraviolet.git && cd ultraviolet
  ```

3. Create an `.invenio.private` file which is used by the invenio-cli tool
  ```sh
  touch .invenio.private
  echo -e "[cli]\nproject_dir = "$PWD"\nservices_setup = False" >> .invenio.private
  ```

4. Add .env file which will contain FLASK_SECRET_KEY
  ```sh
  touch .env
  echo FLASK_SECRET_KEY="some random value" > .env
  ```

5. Build application python environment and web assets (make sure that you use node 14; check by running `node -v` and switch if you need to by running `nvm use 14`)
  ```sh
  invenio-cli packages lock --pre --dev
  invenio-cli install --pre --development
  ```
6. If you have used the Invenio Framework before, this is a good time to make sure that you do not have old images or running containers. (Check [Docker troubleshooting tips]({{ 'tips-and-gotchas/docker' | absolute_url }}) for helpful commands).

7. Build application services (database, search, cache) and setup the application for running
  ```sh
  invenio-cli services setup
  ```
  IMPORTANT: if services setup reported any errors, and you have to restart the setup process, make sure to run
  destroy service command first (or you will get "Failed to setup services" error ) and delete db files by running `invenio-cli services destroy` and `rm -r app_data/db/*`

8. If you do any local UI customization you need to rebuild applications web assets
  ```sh
  invenio-cli assets build --development
  ```

9. Start the application.
  ```sh
  invenio-cli run
  ```

  The UltraViolet instance should now be available at this URL: <https://127.0.0.1:5000/>  
  Because of the invalid TLS warning, you will need to use Firefox.

  You can login using account `admin@test.com` which you've just created and start uploading data.

12. Quit the application with `Ctr-C` and spin down the containers with `invenio-cli containers stop`

## Testing only

1. Get the local copy of the UltraViolet app:
  ```sh
  git clone https://github.com/nyudlts/ultraviolet && cd ultraviolet
  ```
2. Create an `.invenio.private` file which is used by the invenio-cli tool
  ```sh
  touch .invenio.private
  echo -e "[cli]\nproject_dir = "$PWD"\nservices_setup = False" >> .invenio.private
  ```

3. Build docker containers using invenio-cli tool
  ```sh
  invenio-cli containers start --lock --build --setup
  ```
  The UltraViolet instance should now be running at <https://127.0.0.1:5000/>
