# Cheatsheets

TOC
- [InvenioCLI Commands](#invenio-cli-commands)
- [Docker Commands](#docker-commands)

# Invenio-cli commands

[Invenio-cli](https://invenio-cli.readthedocs.io/en/latest/) is a tool used to scaffold, manage, build, run, stop, and destroy this application.

- `pip install invenio-cli`
- `invenio-cli --version`
- `invenio-cli check-requirements --development`
- **Fully _Containerized_ application commands (quick start)**
    - `invenio-cli containers start` - start the entire system in containers
    - `invenio-cli containers stop` - stop the containers
    - `invenio-cli containers destroy` - destroy containers
- **Partially Containerized _Services_ (good for development)**
    - `invenio-cli install` - installs project locally (dependencies, directories, linking configs, copying images and statics AND BUILDS FRONT END ASSETS)
        - OR `invenio-cli install --dev` - include dev dependencies
    - `invenio-cli services` - start and setup services, can be done in two separate steps like so:
        - `invenio-cli services setup -N` - builds containers for local serivices; `-N` disables the creation of demo data
        - `invenio-cli services start` - start the services containers
            - if postgres is not starting you might have a local installation of psql running in the same port. `systemctl stop postgresql` to stop it.A
    - `invenio-cli services status` - can be also viewed in Docker Desktop UI
    - `invenio-cli services stop` - stop container services
    - `invenio-cli services destroy` - remove containers, will require setup again
    - `invenio-cli run` - start local dev server, exit with [CTRL+C]
        - `invenio-cli run --services` enable dockerized services
        - `invenio-cli run --no-services` disable dockerized services
        - `invenio-cli run --debug
- **Individual level application**
    - `invenio-cli packages install $HOME/projects/invenio/`
        - runs installation for pip packages of said project
    - `invenio-cli assets build` - injects variables and transpiles
    - `invenio-cli assets watch` - watch mode (can be run in a separate terminal), exit with [CTRL+C]
        - can only watch existing files, if creating a new file stop your server and `invenio-cli assets build` before watching again.
        - TODO: how different is this from `invenio-cli run`??

## Docker Commands

> InvenioCLI controls Docker and Docker Compose. If for any reason you want to modify the containers ultraviolet works on you can do it directly with Docker too.

- [docker CLI](https://docs.docker.com/engine/reference/commandline/cli/)
- [docker compose CLI](https://docs.docker.com/compose/reference/)
- Information and plugins
```sh
docker info
```
- Check running containers
  ```sh
  docker ps
  ```
- Stop a specific container
  ```sh
  docker stop CONTAINER-ID
  ```
- Delete a specific container
  ```sh
  docker rm CONTAINER-ID
  ```
- Check existing images
  ```sh
  docker images
  ```
- Delete an existing image (all containers which use the image must be deleted)
  ```sh
  docker rmi IMAGE-ID
  ```
- Delete all unused resources
  ```sh
  docker system prune -s
  ```
- Debug a docker-compose container
  ```sh
  docker logs --tail 50 --follow --timestamps CONTAINER-NAME
  ```
- Cleanup/clobber docker-compose to start over
  ```sh
  docker-compose down --rmi all --volumes  --remove-orphans
  ```
