#!/usr/bin/env bash

autopep8 --in-place --aggressive --recursive .
isort -rc ./
autoflake --imports=django --in-place --recursive .
