# Setup


## System Requirements

Follow the instructions provided in the InvenioRDM documentation for system requirements [InvenioRDM System Requirements](https://inveniordm.docs.cern.ch/install/requirements/).

Currently, we use Python 3.9 and node 18 for development version of UltraViolet. 

[NVM](https://github.com/nvm-sh/nvm#installing-and-updating) is recommended for managing node versions. 
 
[pyenv](https://github.com/pyenv/pyenv#installation) is recommended for managing Python versions. 

Although postgres is running as container You might  need to install [Postgres](http://postgresguide.com/setup/install.html) to be able to use postgres client withing your application.


## Setup and Installation for Running Application Locally for Development 
[back to top](#setup)

1. Get the local copy of the UltraViolet source code:
  ```sh
  git clone https://github.com/nyudlts/ultraviolet.git && cd ultraviolet
  ```
2. Load correct python version in current environment.
  ```sh
  pyenv install --skip-existing
  ```
  > (Check result with `python --version`)

3. Load correct node version in current environment. (Check result with `node --version`)
  ```sh
  nvm install
  ```

4. Install and/or update pip, pipenv, and [invenio-cli](https://invenio-cli.readthedocs.io/en/latest/)
  ```sh
  pip install -U --upgrade pip pipenv invenio-cli
  ```

5. Check Invenio's requirements
  ```sh
  invenio-cli check-requirements --development 
  ```
  > If there are any requirements missing consult invenio system requirements list mentioned above 

6. Create an `.invenio.private` file which is used by the invenio-cli tool
  ```sh
  touch .invenio.private
  echo -e "[cli]\nproject_dir = "$PWD"\nservices_setup = False" >> .invenio.private
  ```

7. Add .env file which will contain FLASK_SECRET_KEY
  ```sh
  touch .env
  echo FLASK_SECRET_KEY="some random value" > .env
  ```

8. Complete building application python environment and web assets
  ```sh
  invenio-cli install
  ```

9. Build application services (database, search, cache) and setup the application for running
  ```sh
  invenio-cli services setup -N
  ```
  IMPORTANT: if services setup reported any errors, and you have to restart the setup process, make sure to run
  destroy service command first (or you will get "Failed to setup services" error ) and delete db files by running `invenio-cli services destroy` and `rm -r app_data/db/*`


10. Start the application.
  ```sh
  invenio-cli run
  ```

  The UltraViolet instance should now be available at this URL: <https://127.0.0.1:5000/>  
  Because of the invalid TLS warning, you will need to use Firefox.

  For local instance admin user password in defined in invenio.cfg file. Check RDM_RECORDS_USER_FIXTURE_PASSWORDS variable. By default yuo can login as user `admin@test.com` which you've just created and start uploading data. 

11. Quit the application with `Ctr-C` and spin down the containers with `invenio-cli containers stop`



## Setup and Installation for Previewing Application 
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



## InvenioRDM File Overview
[back to top](#setup)

Following installation, the project folder will include the following. 

| Name | Description |
|---|---|
| ``Dockerfile`` | Dockerfile used to build your application image. |
| ``Pipfile`` | Python requirements installed via [pipenv](https://pipenv.pypa.io) |
| ``Pipfile.lock`` | Locked requirements (generated on first install). |
| ``app_data`` | Application data such as vocabularies. |
| ``assets`` | Web assets (CSS, JavaScript, LESS, JSX templates) used in the Webpack build. |
| ``docker`` | Example configuration for NGINX and uWSGI. |
| ``docker-compose.full.yml`` | Example of a full infrastructure stack. |
| ``docker-compose.yml`` | Backend services needed for local development. |
| ``docker-services.yml`` | Common services for the Docker Compose files. |
| ``invenio.cfg`` | The Invenio application configuration. |
| ``logs`` | Log files. |
| ``static`` | Static files that need to be served as-is (e.g. images). |
| ``templates`` | Folder for your Jinja templates. |
| ``.invenio`` | Common file used by Invenio-CLI to be version controlled. |
| ``.invenio.private`` | Private file used by Invenio-CLI *not* to be version controlled. |
