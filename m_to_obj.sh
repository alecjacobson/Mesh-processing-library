#!/bin/bash

cat $1 | sed -e "s/Vertex [0-9]* /v /g" | sed -e "s/Face [0-9]* /f /g" | grep "^[fv]" >$2
