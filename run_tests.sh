#!/usr/bin/env bash
#Usage:        ./run-tests.sh <path to test>
#Example:      ./run_tests.sh tests/ui


#check that pipenv is installed
if ! command -v pipenv &> /dev/null
then
    echo "pipenv could not be found"
    exit 1
fi

#check if pytest and fixtures are installed
if ! command -v pipenv run pytest --version&> /dev/null
then
    echo "pytest is not installed"
    exit 1
fi

#make sure pytest.ini is present
if ! test -f pytest.ini
then
    echo "pytest.ini does not exists. Are you in the right directory ?"
    exit 1
fi

#check that requirements are met if we are doing E2E testing
if [ "${E2E}" == 'yes' ]
then
   #check that chromedriver is installed
   if ! command -v  chromedriver &> /dev/null
   then
      echo "Chromedriver could not be found. You can not run e2e testing"
      exit 1
   fi
   #check that selenium client is installed
   if ! pipenv graph | grep 'selenium'
   then
      echo "Selenium client is not installed. You can not run e2e testing"
      exit 1
   fi
fi

#run tests
#if path to test is provided check that it is valid and use it
#otherwise run tests from test directory defined in  pytest.ini
if [ $# -eq 0 ]
then
    pipenv run pytest -p no:cacheprovider
else
    if ! [ -e "$1" ]
    then
       echo "Path to test(s) is invalid"
       exit 1
    fi
       pipenv run pytest -p no:cacheprovider "$1"
fi
