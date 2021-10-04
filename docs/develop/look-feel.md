---
layout: default
title: Make Look and Feel Changes
parent: Develop
nav_order: 2
redirect_from:
  - /development/look-feel/
---
# {{ page.title }}

You may want to suggest look and feel changes, which are often overrides of the `invenio.less` template. UltraViolet 💜 inherits the theme from the [invenio-theme](https://github.com/inveniosoftware/invenio-theme) repository by default, unless a discrete `.html` file is inserted into our codebase. There are some look and feel configurations that are established within the `invenio.cfg` file, while others are in the `/assets/less/site/globals` area. A big part of the process is knowing where to look and where to insert changes.

This page offers general instructions on how to mock up look and feel changes and submit them for review. However, you will also want to refer to the Invenio RDM project documentation links for insight:
- <https://inveniordm.docs.cern.ch/customize/styling/>
- <https://inveniordm.docs.cern.ch/customize/styling-logo/>
- <https://inveniordm.docs.cern.ch/customize/styling-theme/>
- <https://inveniordm.docs.cern.ch/customize/styling-templates/>

## Overrides to the theme

Let's suppose that you want to change the way that the application footer looks. Begin with a clean working branch named after the issue or design change in question. It may take some time to locate the appropriate file. Another strategy is to look through the codebases of existing InvenioRDM projects and examine how they have made theme overrides. Once you have located the existing `.html` file from the [invenio-theme](https://github.com/inveniosoftware/invenio-theme) repository, copy it, and place it in our project directory. This could look something like the following:

1. Navigate to `/templates/semantic-ui/invenio_app_rdm`

2. Create a file with `touch footer.html`

3. Open the file and paste the contents you copied from the `invenio-theme` repository. The beginning of the file will look something like

```
{#

  Copyright (C) 2019-2020 CERN.
  Copyright (C) 2019-2020 Northwestern University.
  Copyright (C) 2021 Graz University of Technology.

  Invenio App RDM is free software; you can redistribute it and/or modify it
  under the terms of the MIT License; see LICENSE file for more details.


#}
```
Once the file is copied, immediately add info that indicates that URL you copied the file from, the date, and the tagged release of the file. Insert this into the commented out section.

```
footer.html copied from https://github.com/inveniosoftware/invenio-app-rdm/blob/v6.0.4/invenio_app_rdm/theme/templates/semantic-ui/invenio_app_rdm/footer.html
on YYYY-MM-DD
from v6.0.4
```

## Implement changes

1. Make the appropriate customizations (wording changes, e.g.).

2. Check and see how the changes look in the app. More than likely, you will need to first re-build all of the app assets by running `invenio-cli assets build -d`. This will take several minutes. When it's done, run `invenio-cli run` and the server will be started. You can see your changes in Firefox at `https://127.0.0.1:5000/`

If you plan on iterating or making many changes, it behooves you to run `invenio-cli assets watch`. This opens up an assets server, which allows you to make modifications without having to re-build each time. After you run this, open up a new Terminal tab, navigate back to the project, and run `invenio-cli run`

## Include a test

After making an override to the theme, you'll also need to include a test that asserts something and expects a result related to the change you made. Documentation on our approach to testing is at the Run Tests section.

Depending on the change you're making, you can copy a template of an existing test and modify it to check the change being made. For example, if a change is made to add a link to the NYU Scholarly Communication and Information Policy department, I could modify the `tests/ui/test_front_view.py` file to include the following:

```python
def test_view1(base_client):
    # Depends on 'base_app' fixture
    front_view = base_client.get("/").data

    assert (
        "https://library.nyu.edu/departments/scholarly-communications-information-policy/"
        in front_view.decode("utf-8")
    )
    assert "NYU Scholarly Communication and Information Policy" in front_view.decode(
        "utf-8"
    )
```
The test makes sure that the string "NYU Scholarly Communication and Information Policy" is appropriately in place.

Tests should be placed in the `tests/ui` directory.

## Run the tests

While you're on your checked out branch, it doesn't hurt to run the tests. However, the services must be started for the tests to work. In a separate Terminal tab, navigate back to the main project directory and run `invenio-cli services start` and then `bash run_tests.sh`.
