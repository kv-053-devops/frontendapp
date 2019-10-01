#!/bin/bash

# frontend app http://frontendapp.dev.svc
# uncomment this line to use APP_ADDRESS as cript argument
APP_ADDRESS=$1

# get status code from app
result=$(curl --connect-timeout 10 -s -o /dev/null -w "%{http_code}" ${APP_ADDRESS})

# check is APP status code is equal to "200" OK
if [ $result == "200" ]; then
  echo "Connection succeeded!"
fi