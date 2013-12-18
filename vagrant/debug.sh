#!/bin/sh -x

if test -z "$1"
then
  echo "USAGE: ./v COMMAND"
else
  VAGRANT_LOG=INFO vagrant $1 $2
fi
