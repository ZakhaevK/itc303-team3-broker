#!/bin/bash

sleep 500
influx auth list --hide-headers | awk '{print $4}' >/shared/token
infx test
