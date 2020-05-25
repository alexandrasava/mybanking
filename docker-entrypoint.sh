#!/usr/bin/env bash

flask db upgrade

cd /docker_dir
flask run --host 0.0.0.0
