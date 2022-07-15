---
layout: default
title: Update RDM Version
parent: Develop
nav_order: 5
has_toc: true
redirect_from:
  - /getting-started/updating-versions/
---
# {{ page.title }}


## Updating UltraViolet

The InvenioRDM project is on a development schedule that cuts monthly releases on the core project and command line interface tool, `invenio-cli`. Our development of UltraViolet will follow accordingly. These instructions guide you through the upgrade process, which you should do when we deploy UltraViolet version updates. InvenioRDM status updates are usually posted on the [project blog.](https://inveniosoftware.org/blog/) We will send out notifications on the DLTS Slack when updates have been merged into the `main` branch.

## Upgrading to Version 4 of UltraViolet

As of June 1, 2021, the InvenioRDM project is on Version 4. We anticipate that upgrade instructions will change slightly as new versions are released, so it is advised to check in with these instructions. See also the [InvenioRDM instructions.](https://inveniordm.docs.cern.ch/releases/upgrading/upgrade-v4.0/)

1. First, make sure you have the most recent Docker images installed. Run `docker pull inveniosoftware/centos8-python:3.8`

2. Check to make sure you have the latest version of `invenio-cli`. Versions are released about once per month, so if it's out of date, run `pip install --upgrade invenio-cli`

3. Run `git pull` to bring in the UltraViolet updates to your local codebase.

4. Next, you'll need to purge your existing ElasticSearch indices. Run `pipenv run invenio index destroy --yes-i-know`

5. Incorporate the `invenio-cli` patch. Run `invenio-cli packages update 4.0.1`

6. Build your assets. Make sure that you're on Node 14. You can check by running `node-v`. Then, run `invenio-cli assets build -d`

7. In a separate terminal tab or window, navigate to the UltraViolet directory and then run `invenio-cli run` to start the server.

8. Once the server is started, return to your original prompt and complete the migration. Run `pipenv run invenio rdm-records fixtures`

9. Finish by running `invenio-cli upgrade --script $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_3_0_to_4_0.py)`

10. Your new version should be running locally, but you will have to create a user with admin credentials again to log into it. Run `invenio users create admin@test.com --password=123456 --active` and then `invenio roles create admin`

You should now have a functioning version 4 of UltraViolet.

## Upgrading to Version 6 of UltraViolet

Currently, as of August 6, 2021, the InvenioRDM project is on Version 6. Below please see the instructions on how to upgrade from version 4 to version 6
See also the [InvenioRDM instructions.](https://inveniordm.docs.cern.ch/releases/upgrading/upgrade-v6.0/) Note that this upgrade assumes that you have already installed version 4 locally and have not deleted any files or images associated with it.

1. First, make sure you have the most recent Docker images installed. Run `docker pull inveniosoftware/centos8-python:3.8`

2. Check to make sure you have the latest version of `invenio-cli`. Versions are released about once per month, so if it's out of date, run `pip install --upgrade invenio-cli`

3. Run `git pull` to bring in the UltraViolet updates to your local codebase.

4. Incorporate the `invenio-cli` patch. Run `invenio-cli packages update`

5. Build your assets. Make sure that you're on Node 14. You can check by running `node-v`. Then, run `invenio-cli assets build -d`

6. Upgrade the DB `pipenv run invenio alembic upgrade`

7. In a separate terminal tab or window, navigate to the UltraViolet directory and then run `invenio-cli run` to start the server.

8. Once the server is started, return to your original prompt and complete the migration.

9. If you do not mind losing your data just rebuild the service by running `invenio-cli services setup --force`

10. If you need your existing data, follow the instructions [provided by InvenioRDM](https://inveniordm.docs.cern.ch/releases/upgrading/upgrade-v6.0/). Note that for the purposes of the UltraViolet sprint, you will likely not have any (or need to preserve any) data from your local machine.
