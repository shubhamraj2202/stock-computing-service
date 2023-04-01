"""A Google Cloud Python Pulumi program"""
from __future__ import annotations

from typing import Dict

from pulumi import export
from pulumi_kubernetes.core.v1 import Service
from src.cluster import K8Cluster, provision_k8s_cluster
from src.deployment_service import K8DefinationEnum, provision_application_service

KUBECONFIG: str = "kubeconfig"
INGRESS_IP: str = "ingress_ip"


def export_config(cluster: K8Cluster, services: Dict[str, Service]) -> None:
    """Export the kubeconfig so that the client can easily access the cluster.
    Args:
        cluster (K8Cluster): Cluster
        services (Dict[str, Service]): Dict containing service name and its k8 object
    """

    export(KUBECONFIG, cluster.config)
    for service_name, service in services.items():
        if service_name == services.get(K8DefinationEnum.load_balancer.value):
            export(
                INGRESS_IP,
                service.status.apply(lambda status: status.load_balancer.ingress[0].ip),
            )


def execute() -> None:
    """Executes Infrastructure as Code"""
    cluster: K8Cluster = provision_k8s_cluster()
    _, services = provision_application_service(cluster)
    export_config(cluster, services)


if __name__ == "__main__":
    execute()
