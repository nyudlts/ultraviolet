# UltraViolet 💜
[![ci:test](https://github.com/nyudlts/ultraviolet/workflows/ci:test/badge.svg)](https://github.com/nyudlts/ultraviolet/actions)
[![ci:test:docs](https://github.com/nyudlts/ultraviolet/workflows/ci:test:docs/badge.svg)](https://nyudlts.github.io/ultraviolet/)

UltraViolet is NYU Libraries' platform for long-term access to a broad range of NYU-related digital content, including open access data associated with research and scholarly output and data licensed for use by members of the NYU community. This repository is the codebase for UltraViolet, a local deployment of the [InvenioRDM project](https://inveniordm.docs.cern.ch/).

## Getting Started

We recommend you visit our [Documentation Wiki](https://nyudlts.github.io/ultraviolet/) to get started. 
You can also check [InvenioRDM documentation] (https://inveniordm.docs.cern.ch/)
Have Questions? Please submit them at the [Issues tab](https://github.com/nyudlts/ultraviolet/issues).


## Overview

Following is an overview of the generated files and folders:

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
