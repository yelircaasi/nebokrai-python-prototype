#!/bin/bash

pydeps ../src/nebokrai --noshow -x nebokrai.util -T svg --show-deps > pydeps.txt
pydeps ../src/nebokrai/util --noshow -T svg --show-deps > util-pydeps.txt
