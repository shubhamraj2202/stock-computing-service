Reference: https://github.com/pulumi/examples/blob/master/gcp-py-gke/README.md

1. `pulumi stack init dev`
2. 


# Upload to docker hub
`docker tag stock-computing-service-app shubhamraj2202/stock-computing-service-app:latest`
`docker push shubhamraj2202/stock-computing-service-app:latest-v1`

# Delete from docker hub
`docker rmi shubhamraj2202/stock-computing-service-app:latest-v1`
