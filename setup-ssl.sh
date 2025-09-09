#!/bin/bash

# Install certbot
apt install certbot python3-certbot-nginx -y

# Stop nginx container temporarily
docker compose stop frontend

# Get SSL certificate
certbot certonly --standalone -d your-domain.com -d www.your-domain.com

# Update nginx config for SSL
# You'll need to modify nginx.conf to include SSL configuration

# Restart containers
docker compose up -d
