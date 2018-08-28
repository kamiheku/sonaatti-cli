#!/bin/sh

# quick and dirty helper script used to get the restaurant ids

for restaurant in \
  "libri" \
  "lozzi" \
  "syke" \
  "tilia" \
  "kvarkki" \
  "ylisto" \
  "piato" \
  "wilhelmiina" \
  "uno" \
  "normaalikoulu" \
  "novelli"
  do
    echo -n "$restaurant "
    curl -sq "http://www.sonaatti.fi/$restaurant/" | sed -n 's/.*div ng-init="init(\([0-9]*\).*/\1/p'
  done
