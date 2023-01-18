#!/bin/bash

cat $1 | sed -ne "s/^v //gp" | nl | sed -e 's/^/Vertex /' >$2
cat $1 | sed -ne "s/^f //gp" | nl | sed -e 's/^/Face /' >>$2
