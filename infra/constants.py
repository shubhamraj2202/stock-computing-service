from pulumi import Config
from pulumi_gcp.config import project, zone
from pulumi_random import RandomPassword

config = Config(None)

PROJECT = project if project else "stock-computing-service"
ZONE = zone if zone else "us-central1"
NODE_COUNT = config.get_int("node_count") or 2
NODE_MACHINE_TYPE = config.get("node_machine_type") or "n1-standard-1"
MASTER_VERSION = config.get("master_version")
OUTH_SCOPES = [
    "https://www.googleapis.com/auth/compute",
    "https://www.googleapis.com/auth/devstorage.read_only",
    "https://www.googleapis.com/auth/logging.write",
    "https://www.googleapis.com/auth/monitoring",
]
CERTIFICATE = """apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: {0}
    server: https://{1}
  name: {2}
contexts:
- context:
    cluster: {2}
    user: {2}
  name: {2}
current-context: {2}
kind: Config
preferences: {{}}
users:
- name: {2}
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1beta1
      command: gke-gcloud-auth-plugin
      installHint: Install gke-gcloud-auth-plugin for use with kubectl by following
        https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke
      provideClusterInfo: true
"""

# username is the admin username for the cluster.
# USERNAME = config.get("username") or "admin"
# # password is the password for the admin user in the cluster.
# PASSWORD = (
#     config.get_secret("password")
#     or RandomPassword("password", length=20, special=True).result
# )
