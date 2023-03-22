# Document

TOC
- [Document](#document)
    - [Introduction](#introduction)
    - [Contributing to Developer Documetation](#contributing-to-developer-documentation)
    - [Contributing to User Documetation](#contributing-to-user-documentation)
    - Back to [CONTRIBUTE.md](./CONTRIBUTE.md)

## Introduction 

There are two documentations available for Ultraviolet: 
- User Facing documentation: teaches the client how to use Ultraviolet.
    - motivation: this is a hosted system that operates as an external site for all to view, and easy to access.
- Developer/Manager documentation: teaches developers how to contribute to the codebase of ultraviolet AND invenioRDM framework.  
    - previoysly: Jekyll + Github Actions + Github Pages website. 
    - current motivation: maintaining a Ruby + Gems system that runs aligned with [Github Pages' dependency versions](https://pages.github.com/versions/). To reduce this technical burden we chose (as of March 2023) to simplify documentation with the following principles
        - documentation will live in the same location as the repository it documents (`/docs` directory)
        - documentation is tracked with version control.
        - documenting does not require setup and only requires using [Github Flavored Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).
        - documentation can be edited by non-developer teams directly on Github.

## Contributing to Developer Documentation

There are two different ways to contribute to this documentation:
1. Web: Use GitHub's Markdown editing web interface to edit a file and when saving create a new branch with your edits, and create a PR to include them into `main`. 
2. Locally cloned: clone, create a new branch, commit your local changes and push, create a PR to the `main` branch when ready.

> If you have questions or encounter errors with the docs, you can [submit an issue](https://github.com/nyudlts/ultraviolet/issuess) and use the `documentation` issue tag.

## Contributing to User Documentation

TBD how to contribute to User Guides
