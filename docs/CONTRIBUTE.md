# Contribute

There are a lot of moving parts to Ultraviolet, NYU's implementation of the InvenioRDM framework. 
This page is meant to be a guide to contributing to this project.

TOC
- [Contribute](#contribute)
    - [How we Organize (Project Management)](#how-we-organize-project-management)
    - [How we Communicate](#how-we-communicate)
    - [How we Document](#how-we-document)
    - [How we Develop](#how-we-develop)
        - [Issue tracking](#issue-tracking)
        - [Branching Strategy](#branching-strategy)
        - [Hosted instances](#hosted-instances)
    - [Continuous Integration (CI)](#continuous-integration-ci)
    - [Continuous Deployment (CD)](#continuous-deployment-cd)

## How we Organize (Project Management)

- [UltraViolet roadmap](https://docs.google.com/document/d/1s3qWChu32uAkO9ghEaILE5u6gQY8__RqUA0X7L52aZo/edit?usp=sharing)
- [NYU/Ultraviolet SB3 Google Drive](https://drive.google.com/drive/folders/1q40bQ5bVZYn5_QhxbPDhhIAYZk3R7434?usp=sharing)

There are two project boards that manage tickets for Ultraviolet:
- [Github Project Board](https://github.com/nyudlts/ultraviolet/projects?type=classic): is out of sync with Jira but is used as an entrypoint for Issues on the application.
- Jira Project Board (link TBD)

### Issue tracking

- [Github Issues](https://github.com/nyudlts/ultraviolet/issues).

## How we Communicate

- [NYU DLTS Slack](https://nyu-dlts.slack.com): comments and questions for team members. Ask Kate for an invite.
- [UltraViolet tech email group](mailto:data-repository-tech@nyu.edu): Internal Google Group for team communications

## How we Document

- [Instructions](docs/DOCUMENT.md) on how to contribute to this documentation.
- [Libraries SB3 project documentation](https://drive.google.com/drive/folders/1q40bQ5bVZYn5_QhxbPDhhIAYZk3R7434?usp=sharing): All of the narratives and documentation over the years associated with this project

## How we Develop

<!-- - [UltraViolet 💜 codebase](https://github.com/nyudlts/ultraviolet) -->
- Learn about Architecture, System Requirements, Setup steps in our [DEVELOP documentation](./DEVELOP.md)


### Branching Strategy

- `main` represents truth
- branch naming convention: `<ticketNumber>-<summary-title>`

### Hosted instances

We currently have two instances available for preview:

- [UltraViolet sandbox GCP hosted instance](https://34.66.53.163/) (requires log-in credentials to view, and requires Firefox to bypass the lack of CA certificates. Ask NYU DLTS for [credentials](https://nyu.app.box.com/notes/805001772990).)
- [UltraViolet staging instance](https://stagewebapp1.dlib.nyu.edu/) (requires VPN)

## Continuous Integration (CI)

We currently have two main CI pipelines:

- CI:test for Ultraviolet (workflows/test.yml)
- CI for building Ultraviolet's docs (will be deprecated once we move documentation away from Jekyll + Github Pages)

## Continuous Deployment (CD)

Go to our [Deployment docs](./DEPLOY.md)