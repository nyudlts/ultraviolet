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
  - **MacOS prep**
    - Download full Xcode via the appstore (this will bring in development tools like gcc, git, and fulfills a future requirement for libxmlsec1). Check for installation with `xcode-select -p`. Ensure to open Xcode to accept license agreement or run `sudo xcodebuild -license accept`.
    - Install [homebrew package manager](brew.sh), restart your terminal.
  - **Version Control (Git 2.41.0+)**
      - Use system git OR install newer git with homebrew `brew install git`
      - Validate with `git --version` and `which git`
  - **Python Version Management (Pyenv 2.3.20+)**
    + Pyenv will install and switch you to the correct version of Python 
    + Version required: 2.3.20+
    + To check version: `pyenv --version`
    + To update: `pyenv update` (for non-brew install) or `brew update && brew upgrade pyenv` (for brew installations).
    + [Installation instructions](https://github.com/pyenv/pyenv#installation), restart your terminal after installation.
    + Why does InvenioRDM use [Python Virtual Environments](https://inveniordm.docs.cern.ch/install/requirements/#python-virtual-environments)?
  - **Conainter Management (Docker 20.10.10+ & Docker Compose 1.17.0+)**
    + Docker version required: 20.10.10+
    + Docker-Compose version required: 1.17.0+
    + Check version with `docker --version` and `docker-compose --version` (note the usage of standalone docker-compose).
    + To install, use the [Install Docker Documentation](tips-and-gotchas/install-docker.md)
    + If you are doing a fully containerized testing, this is all you need to quick start the application — jump to the [Testing Only](#testing-only). If you are doing development, continue forth!
  - **Node Version Manager (NVM 0.39.3+)**
    - Version required: 0.39.3+
    - Use these [Installation and updating instructions](https://github.com/nvm-sh/nvm#installing-and-updating).  Be sure to use the approach described there (running a script) rather than using homebrew because the NVM supported by homebrew is outdated.
    - Optional: configure your SHELL to recognize the existence of `.nvmrc` and switch node versions [post](https://medium.com/allenhwkim/bash-profile-for-git-and-nodejs-users-15d3fbc301f0) 
  - **Cairo**
    - [Installation instructions](https://invenio-formatter.readthedocs.io/en/latest/installation.html)
    - MacOs(arm): will require you to symlink cairo packages from your homebrew installation to your local ultraviolet directory as recommended by [Issue385 in CairoSVG](https://github.com/Kozea/CairoSVG/issues/385)
  - **ImageMagick**
    - MacOS (brew) [Installation instructions](https://imagemagick.org/script/download.php#macosx)
    - Linux [Installation from source code instructions](https://imagemagick.org/script/download.php#linux)
  - **Libraries needed for SAML Integration**
    - Ubuntu
    ```sh
    sudo apt-get install libxml2-dev libxmlsec1-dev libxmlsec1-openssl
    ```
    - Rocky Linux/RHEL
    ```sh
    sudo dnf install libxml2-devel xmlsec1-devel xmlsec1-openssl-devel libtool-ltdl-devel
    ```
    - MacOS
    ```sh
    # ensure xcode-select is installed (using full xcode is necessary)
    xcode-select -p   # => /Applications/Xcode.app/Contents/Developer
    # update homebrew and package definitions homebrew uses
    brew update
    # update all possible local unpinned packages in homebrew
    brew upgrade
    # install libxml2 and libxmlsec1
    brew install libxml2 libxmlsec1
    ```
    **IMPORTANT**: The latest `libxmlsec1` version 1.3.0 introduced a breaking bug. Follow [this work around](https://github.com/xmlsec/python-xmlsec/issues/254) to downgrade the package manually.

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
  pip install --upgrade pip pipenv invenio-cli
  ```

6. Check Invenio's requirements
  ```sh
  invenio-cli check-requirements
  ```
  > error docker-compose not found possible, see [Docker Compose Troubleshooting](tips-and-gotchas/install-docker.md#troubleshooting-docker-compose)

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
  invenio-cli services setup --no-demo-data
  # `invenio-cli services setup --help` for more info
  # `-N` means `--no-demo-data`
  ```
  IMPORTANT: if services setup reported any errors, and you have to restart the setup process, make sure to run
  destroy service command first (or you will get "Failed to setup services" error ) and delete db files by running `invenio-cli services destroy` and `rm -r app_data/db/*`
  IMPORTANT: if services setup fails to connect to the docker.sock you will need to run first `pipenv run invenio-cli run` (process stays on the tail of your docker logs), open a separate terminal window and now run `invenio-cli services setup`

14. If you do any local UI customization you need to rebuild applications web assets
  ```sh
  invenio-cli assets build --development
  ```
  > will run webpack and JS bundlers 

15. Start the application.
  ```sh
  invenio-cli run
  # if this doesn't work use
  pipenv run invenio-cli run
  ```

  The UltraViolet instance should now be available at this URL: <https://127.0.0.1:5000/>  
  Because of the invalid TLS warning, you will need  configure your browser
  of choice to skip certificate verification for localhost or use Firefox

  To start uploading data you can login with default admin account adminUV@test.com (password for that account is defined
  by the variable RDM_RECORDS_USER_FIXTURE_PASSWORDS in your invenio.cfg). 
 
  First you need to create default community to which users will be adding records. It can be done through UI by accessing <https://localhost:5000/communities/new>
  Create community with identifier 'opendata' (That step will be automated soon)

  After login an option "My dashboard" will become
  available. Click on it and then use "New upload" button to add new records.
  
  NOTE: Do not click on "Deposit" option, it is used in production by non-admin users to request curated upload 

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
