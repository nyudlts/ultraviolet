# Setup

TOC
- [Setup](#setup)
  - [Introduction](#introduction)
  - [System Requirements](#system-requirements)
  - [Setup and Installation](#setup-and-installation)
  - [Testing only](#testing-only)
  - [Testing with Vagrant](#testing-with-vagrant)


## Introduction
[back to top](#setup)

Like the InvenioRDM application, you can run Ultraviolet in two modes:

- Fully Dockerized Mode: Containerized application and services (good for a quick preview).  
- Partially Dockerized Mode: Local dev tools runnig parts of InvenioRDM with containerized services (good for developers) also considered [instance development](https://inveniordm.docs.cern.ch/develop/getting-started/instance-development/#integrating-react-development-modules).

> More on the [InvenioRDM Architecture](https://inveniordm.docs.cern.ch/develop/architecture/)  

## System Requirements
[back to top](#setup)

> Production Ultraviolet installation currently uses InvenioRDM version 10
> Development Ultraviolet Installation currently uses InvenioRDM version 11

The following instructions were modified from the [InvenioRDM System Requirements:](https://inveniordm.docs.cern.ch/install/requirements/):

- Supported Hardware
  + At least 8GB of RAM and 4 cores.
- Supported Operating Systems
  - MacOS or Linux-based systems (Windows not supported)
- System Requirements to Install Ultraviolet (ensure you have these installed on your system)
  - Git
  - **Simple Python Version Management (Pyenv)**
    + [Installation instructions](https://github.com/pyenv/pyenv#installation)
    + Restart Terminal and Check for successful installation with `pyenv --version`
    IMPORTANT: If you already have pyenv installed make sure to update it to latest version by running `pyenv update`
    + Why does InvenioRDM use [Virtual Environments](https://inveniordm.docs.cern.ch/install/requirements/#python-virtual-environments)?
  - **Docker**
    + Use the [Install Docker Documentation]({{'tips-and-gotchas/install-docker/' | absolute_url }})
    + Check for successful installation with `docker --version` and `docker-compose --version` (note the usage of standalone docker-compose).
    + If you are doing a fully containerized testing this is all you need to quick start the application; jump to the [Testing Only](#testing-only). If you are doing development, continue forth!
  - **Node Version Manager (NVM)**
    + Use these [Installation instructions](https://github.com/nvm-sh/nvm#installing-and-updating) following the CLI installation (for MacOS install nvm from scratch not from brew).
    + Restart Terminal and Check for successful installation with `nvm --version`. [troubleshooting tips](https://github.com/nvm-sh/nvm#troubleshooting-on-linux). 
    + Optional: configure your SHELL to recognize the existence of `.nvmrc` and switch node versions [post](https://medium.com/allenhwkim/bash-profile-for-git-and-nodejs-users-15d3fbc301f0) 
  - **Cairo**
    + [Installation instructions](https://invenio-formatter.readthedocs.io/en/latest/installation.html)
  - **ImageMagick**
    + MacOS (brew) [Installation instructions](https://imagemagick.org/script/download.php#macosx)
    + Linux [Installation from source code instructions](https://imagemagick.org/script/download.php#linux)
  - **Libraries needed for SAML Integration**
    + Ubuntu
    ```sh
    sudo apt-get install libxml2-dev libxmlsec1-dev libxmlsec1-openssl
    ```
    + Rocky Linux/RHEL
    ```sh
      sudo dnf install xmlsec1-devel libtool-ltdl-devel
    ```
    + MacOS
    ```sh
    xcode-select --install
    brew upgrade
    brew install libxml2 libxmlsec1
    ```
    IMPORTANT: Upgrade of xmlsec1 to version 1.3.0 introduced an issue described [here](https://github.com/xmlsec/python-xmlsec/issues/254). You might need to use a work around
    described at the provided link to complete your installation.
   

> From the InvenioRDM documentation: During Setup and Installation we start these services, but you can also just as well use externally hosted options for these:
> - postgresql
> - opensearch
> - redis memcached

## Setup and Installation
[back to top](#setup)

1. Get the local copy of the UltraViolet source code:
  ```sh
  git clone https://github.com/nyudlts/ultraviolet.git && cd ultraviolet
  ```
2. Make sure your Docker Desktop is running. If planning to do sustained work, you may want to increase the memory allocation to at least 4 GB but this isn't necessary.

3. Load correct python version in current environment. 
  ```sh
  pyenv install --skip-existing
  ```
  > (Check result with `python --version`)

4. Load correct node version in current environment. (Check result with `node --version`)
  ```sh
  nvm install
  ```
  > reads `.nvmrc` for a node version and installs it. Installs NPM (Node Package Manager) alongside Node.
  > `node --version` to confirm Node has been installed
  > `npm --version` to confirm NPM has been installed
  > IF `npm --version` >= 7, run: `echo "legacy-peer-deps = true" >> ~/.npmrc`

5. Install and/or update pip, pipenv, and [invenio-cli](https://invenio-cli.readthedocs.io/en/latest/)
  ```sh
  pip install -U --upgrade pip pipenv invenio-cli
  ```

6. Check Invenio's requirements
  ```sh
  invenio-cli check-requirements
  ```
  > error docker-compose not found possible, see [Docker Compose Troubleshooting]({{ site.baseurl }}{% link tips-and-gotchas/docker.md %})

7. Create an `.invenio.private` file which is used by the invenio-cli tool
  ```sh
  touch .invenio.private
  echo -e "[cli]\nproject_dir = "$PWD"\nservices_setup = False" >> .invenio.private
  ```

8. Add .env file which will contain FLASK_SECRET_KEY
  ```sh
  touch .env
  echo FLASK_SECRET_KEY="some random value" > .env
  ```

9. Reset and build application python environment and web assets
  ```sh
  pipenv --rm
  invenio-cli packages lock --pre --dev
  ```
  > possible `No virtualenv has been created for this project yet`


10. Complete building application python environment and web assets
  ```sh
  invenio-cli install --pre --development
  ```

11. Pipfile automatically installs version of 4.18.a3 of jsonschema which is a pre-release version and thus, unstable. Install stable version of v4.17.3. 
  ```sh
  pipenv run pip install -U jsonschema==4.17.3 
  ```

12. If you have used the Invenio Framework before, this is a good time to make sure that you do not have old images or running containers. (Check [Docker troubleshooting tips]({{ 'tips-and-gotchas/docker' | absolute_url }}) for helpful commands).

13. Build application services (database, search, cache) and setup the application for running
  ```sh
  invenio-cli services setup -N
  ```
  IMPORTANT: if services setup reported any errors, and you have to restart the setup process, make sure to run
  destroy service command first (or you will get "Failed to setup services" error ) and delete db files by running `invenio-cli services destroy` and `rm -r app_data/db/*`

14. If you do any local UI customization you need to rebuild applications web assets
  ```sh
  invenio-cli assets build --development
  ```
  > will run webpack and JS bundlers 

15. Start the application.
  ```sh
  invenio-cli run
  ```

  The UltraViolet instance should now be available at this URL: <https://127.0.0.1:5000/>  
  Because of the invalid TLS warning, you will need to use Firefox.

  You can login using account `admin@test.com` which you've just created and start uploading data.

16. Quit the application with `Ctr-C` and spin down the containers with `invenio-cli containers stop`

## Testing only
[back to top](#setup)

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

## Testing with Vagrant
[back to top](#setup)

Currently, we do not have a Vagrant image of UltraViolet in place, but one is coming soon. In the meantime, consider local development and testing with Docker.
