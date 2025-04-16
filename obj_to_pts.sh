#!/bin/bash

cat $1 | sed -ne "s/^v \(.*\)/p \1/gp" >$2
