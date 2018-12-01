#!/usr/bin/env awk -f
{ sum += $1 }
END { print sum }
