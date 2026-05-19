# Setup

## System Requirements

Follow the instructions provided in the InvenioRDM documentation for system requirements [InvenioRDM System Requirements](https://inveniordm.docs.cern.ch/install/requirements/).

Currently, we use Python 3.9 and node 18 for the development version of UltraViolet. 

[NVM](https://github.com/nvm-sh/nvm#installing-and-updating) is recommended for managing node versions. 
 
[pyenv](https://github.com/pyenv/pyenv#installation) is recommended for managing Python versions. 

Although postgres is running as a container, you might need to install [Postgres](http://postgresguide.com/setup/install.html) to be able to use a Postgres client within your application.

### ImageMagick & IIIF Images

In order for IIIF Canvases to be generated, you must have [ImageMagick](https://imagemagick.org/#gsc.tab=0) installed.

On macOS, you will need a few exports set up for it to run correctly:

```
export MAGICK_HOME="/opt/homebrew/opt/imagemagick"
export DYLD_LIBRARY_PATH="$MAGICK_HOME/lib:$DYLD_LIBRARY_PATH"
export PATH="$MAGICK_HOME/bin:$PATH"
export PKG_CONFIG_PATH="$MAGICK_HOME/lib/pkgconfig:$PKG_CONFIG_PATH"
```

## Setup and Installation for Running Application Locally for Development 

### 1. Clone the UltraViolet Source Code

```sh
git clone https://github.com/nyudlts/ultraviolet.git
cd ultraviolet
```

### 2. Load the Correct Python Version

```sh
pyenv install --skip-existing
python --version # to check the result
```

### 3. Load the Correct Node Version

```sh
nvm install
node --version # to check the result
```
### 4. Install Python Dependencies

```sh
pip install -U --upgrade pip pipenv invenio-cli
```

### 5. Check Invenio's Requirements

```sh
invenio-cli check-requirements --development 
```

If there are any missing requirements, consult the [InvenioRDM System Requirements](https://inveniordm.docs.cern.ch/install/requirements/).

### 6. Create an `.invenio.private` file

This file is used by the `invenio-cli` tool.

```sh
touch .invenio.private
echo -e "[cli]\nproject_dir = "$PWD"\nservices_setup = False" >> .invenio.private
```

### 7. Add an `.env` file

```sh
touch .env
echo FLASK_SECRET_KEY="some random value" > .env
```

### 8. Install Python Dependencies and Build Web Assets

```sh
invenio-cli install
```

### 9. Set Up Application Services (database, search, cache)

```sh
invenio-cli services setup -N
```

IMPORTANT: if services setup reported any errors, and you have to restart the setup process, make sure to run
destroy service command first (or you will get a `Failed to setup services` error) and delete db files by running `invenio-cli services destroy` and `rm -r app_data/db/*`

### 10. Starting the Application

```sh
invenio-cli run
```

UltraViolet should now be available at <https://127.0.0.1:5000/>.

Note: The application uses a self-signed SSL certificate, which means you will likely get a warning in your browser. It's safe to continue locally.

For a local instance the admin user password is defined in `invenio.cfg file` with the `RDM_RECORDS_USER_FIXTURE_PASSWORDS` variable. You can log in as the user `adminUV@test.com` and start uploading data.

### 11. Stopping the Application

To stop the local instance:

- Press `Ctr-C` to stop the application
- Spin down Dockers containers with `invenio-cli services stop`

## Setup and Installation for Previewing Application 

### 1. Clone the UltraViolet Source Code

```sh
git clone https://github.com/nyudlts/ultraviolet
cd ultraviolet
```

### 2. Create an `.invenio.private` File

```sh
touch .invenio.private
echo -e "[cli]\nproject_dir = "$PWD"\nservices_setup = False" >> .invenio.private
```

### 3. Build and Run the Docker Containers

```sh
invenio-cli containers start --build --setup
```

The UltraViolet instance should now be running at <https://127.0.0.1>.

For a local instance the admin user password is defined in `invenio.cfg file` with the `RDM_RECORDS_USER_FIXTURE_PASSWORDS` variable. You can log in as the user `adminUV@test.com` and start uploading data.

## InvenioRDM File Overview

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
