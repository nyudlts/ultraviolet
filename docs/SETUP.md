# Setup


## System Requirements
[back to top](#setup)

Follow the instructions provided in the InvenioRDM documentation for system requirements [InvenioRDM System Requirements:](https://inveniordm.docs.cern.ch/install/requirements/).

Currently, we use Python 3.9 and node 18 for development version of UltraViolet. 

NVM is recommended for managing node versions. 
- [Installation instructions](https://github.com/nvm-sh/nvm#installing-and-updating)

Pyenv is recommended for managing Python versions. 
- [Installation instructions](https://github.com/pyenv/pyenv#installation)

You will need to install Postgres.
- [Installation instructions](http://postgresguide.com/setup/install.html)


## Setup and Installation for Running Application Locally for Development 
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

4. Load correct node version (14.x) in current environment. (Check result with `node --version`)
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

10. Due to a [known bug in the current version of InvenioRDM](https://github.com/inveniosoftware/invenio-files-rest/issues/264) we can only use `setuptools` version smaller then 58.
  ```sh
  pipenv run python3.8 -m pip install 'setuptools~=57.5.0'
  ```

11. Complete building application python environment and web assets
  ```sh
  invenio-cli install --pre --development
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

## Setup and Installation for Previewing this Application 
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

