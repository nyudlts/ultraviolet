# Develop

This guide contains an overview of the repositories and sources that you may need in order to understand the project, write code, and make changes to the project.

TOC
- [Develop](#develop)
  - [Learning InvenioRDM Resources](#learning-inveniordm-resources)
  - [File Overview](#file-overview)
  - [Visual Changes](#visual-changes)
  - [Add Fixtures](#add-fixtures)
  - [SAML Integration](#saml-integration)
  - [Updating InvenioRDM Versions](#updating-inveniordm-versions)

## Learning InvenioRDM Resources

Ultraviolet is an application that is built on the InvenioRDM framework.
Understanding how InvenioRDM works and how to develop on it will extend directly into working on Ultraviolet and contributing to this project.

- [InvenioRDM documentation](https://inveniordm.docs.cern.ch/)
- [InvenioRDM Develop](https://inveniordm.docs.cern.ch/develop/#getting-started)
- [InvenioRDM Newcomers Guide](https://inveniordm.docs.cern.ch/maintenance/newcomers/)
- [InvenioRDM sandbox](https://invenio-software.org/products/rdm/): A hosted live version to quickly test out features and functions
- [InvenioRDM codebase](https://github.com/inveniosoftware/invenio-app-rdm): The community product for upstream development
- [InvenioRDM Discord server](https://discord.gg/m3dfukqc5F): The place for questions to the general InvenioRDM community
- [InvenioRDM REST API documentation](https://inveniordm.docs.cern.ch/reference/rest_api_index/)

## File Overview

Following is an overview of the generated files and folders from the scaffolding command:

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


## Visual Changes

- [Look and Feel Changes](./develop/look-feel.md)

## Add Fixtures

- [Add Fixtures](./develop/add-fixtures.md)

## SAML Integration

- [SAML Integration](./develop/SAML-integration.md)

## Updating InvenioRDM Versions

- [Updating Versions](./develop/updating-versions.md)
