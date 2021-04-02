---
layout: default
title: Create and Add Fixtures
parent: Testing
nav_order: 1
---
# {{ page.title }}

During the process of development, you may want to create a new fixture record and add it to the project to demonstrate or test a new feature. This page demonstrates sample strategies and workflows.

## Making a new metadata record

First, generate a new metadata record that has only the descriptive invenio schema elements and no "system-generated" elements. A quick and convenient way to do this is to launch the application locally, log in as `deposit@test.com` and use the deposit form to create a record from scratch.

Once it's submitted, visit that item show page and view it as JSON. Just change the item URL to `https://localhost:5000/api/records/2`. Note that the `2` will change, depending on how many records you have already indexed, so change accordingly. Copy the file and paste it into a new text file and strip out all of the "system generated" elements.

## Preparing the data

If your fixture points to data (or you intend to upload data locally as a fixture), you'll need to commit it to the [invenio_nyu/fixtures/data](./invenio_nyu/fixtures/data/) folder. However, for the connection to happen, you also need to add the appropriate element to the [invenio_nyu/fixtures/records.json](./invenio_nyu/fixtures/records.json) file.

## Indexing locally to test

Once the data is in place, also place the metadata record in the `fixtures/records` folder and then re-run the index script in a separate tab.

## Submitting a pull request

If all looks good, stage your changes and submit them to the project as a pull request.
