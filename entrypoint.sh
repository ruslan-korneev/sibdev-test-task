#!/bin/bash

sibdev collectstatic --noinput
sibdev migrate
"$@"