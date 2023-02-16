---
layout: default
title: Make Look and Feel Changes
parent: Develop
nav_order: 2
redirect_from:
  - /development/look-feel/
---
# {{ page.title }}

This page offers general instructions on how to mock up look and feel changes and submit them for review. Use the Invenio RDM project documentation for further/updated instructions:
- <https://inveniordm.docs.cern.ch/customize/look-and-feel/>
- <https://inveniordm.docs.cern.ch/customize/look-and-feel/logo/>
- <https://inveniordm.docs.cern.ch/customize/look-and-feel/theme/>
- <https://inveniordm.docs.cern.ch/customize/look-and-feel/templates/>
- <https://inveniordm.docs.cern.ch/develop/>

> InvenioRDM/Ultraviolet uses a front-end based on a Flask Server using [Jinja Templates](https://jinja.palletsprojects.com/en/3.1.x/)
> You do not need the entire architecture running in order to locally develop and test these changes, only your python installation and environment

**TL;DR**
Look and Feel can be better understood as Style and Content. Can be changed in the following ways:
- Style (Changing the Theme)
- Content (Changing the Templates)

> A big part of the process is knowing where to look and where to insert changes.

## Changing Theme (Style changes)

<https://inveniordm.docs.cern.ch/customize/look-and-feel/theme/>  

UltraViolet 💜 inherits the theme from the [invenio-theme](https://github.com/inveniosoftware/invenio-theme). Themes are a grouping of Templates and CSS assets that provide a starter setup.
[Understanding the Theme Structure](https://inveniordm.docs.cern.ch/develop/topics/theming/).

- Changing the Theme can be done in the following:
  - overriding `invenio.less` CSS file
  - changes to `assets/less/site/globals/site.variables` or `assets/less/site/globals/site.overrides`
  - some style changes might go in the classes used for semantic-ui on the html templates.

### Run Locally (transpile Less and React) and View changes

1. Run the asset server in the background to watch changes:
  ```sh
  invenio-cli assets watch
  ```

2. Make sure the app is running:
  ```sh
  invenio-cli run
  ```

3. Make the appropriate customizations in your text editor (style or content changes, e.g.).

4. Check and see how the changes look in the app. You can see your changes in Firefox at `https://127.0.0.1:5000/`

## Changing the Templates

<https://inveniordm.docs.cern.ch/customize/look-and-feel/templates/>

- overriding templates
  - creating new `.html` template and pointing at it either by:
    - environment variables that override values in the `invenio.cfg` file pointing a new templates
    - or through `invenio.cfg` more permanently pointing at new templates

UltraViolet 💜 inherits the theme from the [invenio-theme](https://github.com/inveniosoftware/invenio-theme) repository by default, unless a discrete `.html` file is inserted into our codebase. 
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

### Run locally and View changes

Stop the server and restart to view changes in Templates
```
<Ctrl+C>
invenio-cli run
```

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

See the [Run Tests]({{ 'develop/run-tests/' | absolute_url }}) wiki page.
