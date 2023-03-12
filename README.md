# Summary
1. This project to Extract/Transform/Load Data from ree API provider named [AlphaVantage](https://www.alphavantage.co/documentation/) in to a Database
2. Provides API service to sync the data, also retrieve from database and get statistic 

# Tech Stack
- Python for backend
- FastAPI for runnning api services
- Sql lite as Database
- Docker to set up image for deployment and local development

# Setup project for development:
`source setup.sh`

# Run using command line:
`uvicorn financial.main:app --host 0.0.0.0 --port 8000`
- Go to Browser: http://0.0.0.0:8000/docs to test the APIs

# Build Docker Image
`docker image build -t stock-computing-service .`
`docker buildx build --platform linux/amd64 -f ./Dockerfile -t image .`

# Run via Docker using any of the below options:
1. `docker run stock-computing-service`
2. `docker-compose up`

# Upload to docker hub
`docker tag stock-computing-service-app shubhamraj2202/stock-computing-service-app:latest`

`docker push shubhamraj2202/stock-computing-service-app:latest`

# Maintaining API key
For local development, the API key can be accessed via environment variable `FINANCIAL_KEY`
- Run `export FINANCIAL_KEY="YourAPIKEY"` on shell.  

For production environment, the API key should be stored in a secret management service like Vault, GCP Secret Manager /AWS


# Deployment:
Install Google Cloud CLI https://cloud.google.com/sdk/docs/install
gcloud init
gcloud auth login
pulumi new gcp-python
gcloud auth application-default login
pulumi config set gcp:project stock-computing-service
export GOOGLE_PROJECT=stock-computing-service
pulumi config set gcp:region us-west1
gcloud components install gke-gcloud-auth-plugin
gcloud container clusters get-credentials gke-cluster-f0853e1 --zone us-west1-a
