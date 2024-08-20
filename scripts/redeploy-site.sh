#!/bin/bash

# Change dir in to MLH Portfolio and fetch branch
cd ~/autoresume
# git fetch && git reset origin/main --hard

# Take down currently running containers
sudo docker compose -f docker-compose.prod.yml down

# Push new containers up
sudo -E docker compose -f docker-compose.prod.yml up -d --build