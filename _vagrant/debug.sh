#!/bin/sh -x

if test -z "$1"
then
  echo "USAGE: ./debug.sh COMMAND"
else
  VAGRANT_LOG=INFO vagrant $1 $2
fi
