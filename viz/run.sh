#!/bin/bash

pydeps ../src/planager --noshow -x planager.util -T svg --show-deps > pydeps.txt
pydeps ../src/planager/util --noshow -T svg --show-deps > util-pydeps.txt
