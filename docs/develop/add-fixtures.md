---
layout: default
title: Create and Add Fixtures
parent: Develop
nav_order: 1
redirect_from:
  - /development/add-fixtures/
---
# {{ page.title }}

During the process of development, you may want to create a new fixture record and add it to the project to demonstrate or test a new feature. This page demonstrates sample strategies and workflows.

## Making a new metadata record

First, generate a new metadata record that has only the descriptive Invenio schema elements and no "system-generated" elements. A quick and convenient way to do this is to launch the application locally, log in as `admin@test.com` pass `adminpassword` and use the deposit form to create a record from scratch.

Once it's submitted, visit that item show page and view it as JSON. Just change the item URL to `https://127.0.0.1:5000/api/records/p6s1v-nzd59/`. Note that the `p6s1v-nzd59` will change, as it is a system-generated ID. Copy the file and paste it into a new text file and strip out all of the "system generated" elements.

## Preparing the data

TBA

## Indexing locally to test

TBA

## Submitting a pull request

If all looks good, stage your changes and submit them to the project as a pull request.
