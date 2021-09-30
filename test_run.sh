#!/usr/bin/env bash

#check that pipenv is installed
if ! command -v pipenv &> /dev/null
then
    echo "pipenv could not be found"
    exit
fi

#check if pytest and fixtures are installed
if ! command -v pipenv run pytest --version&> /dev/null
then
    echo "pytest is not installed"
    exit
fi

#make sure pytest.ini is present
if ! test -f pytest.ini
then
    echo "pytest.ini does not exists."
    exit
fi
if [ "${E2E}" == 'yes' ]
then
   #check that chromedriver is installed
   if ! command -v  chromedriver &> /dev/null
   then
      echo "Chromedriver could not be found. You can not run e2e testing"
      exit
   fi
   #check that selenium client is installed
   if ! pipenv graph | grep 'selenium'
   then
      echo "Selenium client is not installed. You can not run e2e testing"
      exit
   fi
fi

#run tests
pipenv run pytest -p no:cacheprovider
