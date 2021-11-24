---
layout: default
title: Policy
parent: Project Orientation
nav_order: 2
has_toc: true

---
# {{ page.title }}


## Policy

Policies surrounding the UltraViolet project are in progress.

### Metadata

#### Openness of metadata

NYU Libraries commits to providing versioned metadata records of assets within UltraViolet. This includes records that expose items licensed or held by NYU Libraries and records that represent the deposits of researchers. Versions for discovery will be committed to a public repository and will be accompanied with instructions for re-use and ingest in other contexts. Note that UltraViolet system-generated fields and protected bitstreams may be redacted from these metadata records, when appropriate.

UltraViolet metadata is made available under a [CC0 License](https://creativecommons.org/share-your-work/public-domain/cc0/). It is available for consumption via the REST API. As new features are added to Invenio RDM, metadata will be made available via additional harvesting protocols, such as OAI-PMH. For library collection material, when appropriate, UltraViolet staff also sends metadata to shared library systems (such as Bobcat, WorldCat, and knowledge bases). To encourage widespread indexing of UltraViolet metadata, UltraViolet staff establishes relationships with aggregators such as Google Dataset Search, SHARE, and others.

#### Metadata versioning and provenance

In order to provide contextual information and align with [FAIR principle R1.2: (Meta)data are associated with detailed provenance](https://www.go-fair.org/fair-principles/r1-2-metadata-associated-detailed-provenance/), metadata records are versioned and may include notes about corrections or amendments. Previous versions of metadata records are made available in in Github. Small errors might be documented in a running version description narrative, while major changes and all updates would be given a new version.

#### Internal application of profile

In NYU Data Services' management and curation of the UltraViolet project, we apply the InvenioRDM metadata schema. Departures and local applications of the schema are documented here.

##### Creator Roles

The `creator role` is a sub-element that comes from the DataCite schema. We define it accordingly.
