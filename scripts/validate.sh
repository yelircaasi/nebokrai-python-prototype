#!/bin/env bash

# should be run in root of nebokrai package if executed without root path passed as an argument

if [[ -n $1 ]]; then
  NEBOKRAI_ROOT="$1"
else
  NEBOKRAI_ROOT="$PWD"
fi

check-jsonschema --schemafile $NEBOKRAI_ROOT/schemata/declaration/calendar-schema.json $NEBOKRAI_ROOT/data/declaration/calendar.json --verbose
check-jsonschema --schemafile $NEBOKRAI_ROOT/schemata/declaration/config-schema.json   $NEBOKRAI_ROOT/data/declaration/config.json   --verbose
check-jsonschema --schemafile $NEBOKRAI_ROOT/schemata/declaration/roadmaps-schema.json $NEBOKRAI_ROOT/data/declaration/roadmaps.json --verbose
check-jsonschema --schemafile $NEBOKRAI_ROOT/schemata/declaration/routines-schema.json $NEBOKRAI_ROOT/data/declaration/routines.json --verbose
check-jsonschema --schemafile $NEBOKRAI_ROOT/schemata/declaration/tracking-schema.json $NEBOKRAI_ROOT/data/declaration/tracking.json --verbose
check-jsonschema --schemafile $NEBOKRAI_ROOT/schemata/derivation/plan-schema.json      $NEBOKRAI_ROOT/data/derivation/plan.json      --verbose
check-jsonschema --schemafile $NEBOKRAI_ROOT/schemata/derivation/schedules-schema.json $NEBOKRAI_ROOT/data/derivation/schedules.json --verbose
