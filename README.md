# InTheNou-Backend
Developed by @TheParodicts and @diego-amador

# Overview
This repo contains the bulk of the InTheNou Flask API, SQL Database schema, and related Docker Container initializations to deploy the InTheNou Backend solution on a Linux Server.

## Deployment
The deployment strategy is as follows:
1. Clone the `Master` branch to the desired server.
2. Manually add the required credential and environment variable files that are not hosted on GitHub.
3. Run the `db_setup.sh` script if this is the first time deploying.
4. Use Docker-Compose to create and run the Docker containers outlined in `docker-compose.yml`.

For a more detailed walkthrough of deployment, consult the Non-API Documentation available to Administrators.

## Flask API
The Flask API code is located under `flask/app/` and subdivided into:
  * routes
  * handlers
  * DAOs
