#!/usr/bin/env bash

# activate
source .venv/bin/activate

# install
pip install -r requirements.txt

# edit
nvim .

# venv created via `ptython -m venv .venv`
# if new requirements added then `pip freeze > requirements.txt` within venv
