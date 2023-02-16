---
layout: default
title: Document
nav_order: 5
# has_children: true
---
# {{ page.title }}


The documentation for Ultraviolet is written in Jekyll, built on Github Actions, and deployed in Github pages.

- [Jekyll Documentation](https://jekyllrb.com/docs/). 
- [Just the Docs theme documentation](https://pmarsceill.github.io/just-the-docs/).
- This website lives in the `docs` directory of the main UltraViolet repo.

## Contributing to the Documentation

There are two different ways to contribute to this documentation:
1. Use GitHub's Markdown editing web interface to create a new branch with your single-page edit, or
2. Clone the repo, make your changes and preview them locally with Jekyll, and push them as a new branch.

Either way, make sure to commit your local branch with changes and submit a PR to the `main` branch when you're ready.

If you have questions or encounter errors with the docs, you can [submit an issue](https://github.com/nyudlts/ultraviolet/issuess) and use the `documentation` issue tag.

## Setting up local Jekyll development environment

- MacOS
    - This documentation is ARM compatible. Go forth with confidence.
    - Install xcode tools `xcode-select --install`
        - brings in `gcc -v`, `g++ -v`, `make -v`, `git`
        - Homebrew might require resintallation to use the x86 versin of brew. Run the installation process again in your Rosetta Terminal.
    - Install [`rbenv`](https://github.com/rbenv/rbenv): `brew install ruby-build rbenv`
        - add the rbenv initializer to `~/.bash_profile`, quit and restart terminal.
        - in general rbenv is just a shimming script that sends your Ruby commands to the correct Ruby version. Rbenv gets help from ruby-build to build from scratch the versions of Ruby you will be using. Ruby-build needs the rigth dependencies for the [build environment](https://github.com/rbenv/ruby-build/wiki#suggested-build-environment) ensure to follow instructions for `Ruby versions 2.x–3.0` (this project currently runs Ruby 2.7.2)
    - Install ruby from `.ruby-version` using: `rbenv install`
    - Install bundler gem: `gem install bundler`
    - Install packages in Gemfiles: `bundle install`
        - An error occurred while installing eventmachine (1.2.7), and Bundler cannot continue. Make sure that `gem install eventmachine -v '1.2.7' --source 'https://rubygems.org/'` succeeds before bundling.
            - [solution](https://stackoverflow.com/questions/70991441/i-cant-install-eventmachine-gem-on-mac-m1)
            - after fixing `eventmachine` you might need to retry `bundle install` to finish installing the rest of the packages.
        - 
    - start the jekyll server: `bundle exec jekyll serve`
- Dockerized documentation coming soon!

## Deploying Jekyll site to Github Pages

The CI/CD pipeline for this project is a Github action [`pages-build-deployment`](https://github.com/nyudlts/ultraviolet/actions/workflows/pages/pages-build-deployment) that will build the Jekyll site and deploy it to Github pages.

## Updating Ruby

https://endoflife.date/ruby
Ruby > 3.0 requires `webrick` to be installed separately.  

- change `.ruby-version` to newer version
- install new ruby version `rbenv install`
- install bundler `gem install bundler`
- reinstall gems from gemfile `bundle install --redownload`

## Updating Jekyll
> Coming soon: [https://jekyllrb.com/docs/upgrading/3-to-4/](https://jekyllrb.com/docs/upgrading/3-to-4/)
- the jekyll version used in this project is a dependency of the github-pages package. Will have to update the package to update Jekyll.
