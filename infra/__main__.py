"""A Google Cloud Python Pulumi program"""
from pulumi import export

from cluster import K8Cluster, provision_k8s_cluster
from deployment import provision_application_service


def execute():
    """Execute the program"""

    # Create a new cluster
    cluster: K8Cluster = provision_k8s_cluster()
    provision_application_service(cluster)


if __name__ == "__main__":
    execute()
