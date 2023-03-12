""" Module for taking care of cluster provisioning """

from enum import Enum
from typing import Any

from constants import (
    CERTIFICATE,
    MASTER_VERSION,
    NODE_COUNT,
    NODE_MACHINE_TYPE,
    OUTH_SCOPES,
    PROJECT,
    ZONE,
)
from pulumi import Output
from pulumi_gcp.container import Cluster, ClusterNodeConfigArgs
from pulumi_kubernetes import Provider
from pydantic import BaseModel


class ClusterEnum(str, Enum):
    CLUSTER = "cluster"
    CONFIG = "config"
    INFO = "info"
    PROVIDER = "provider"


class K8Cluster(BaseModel):
    """Model class for cluster provisioning"""

    cluster: Any
    config: Any
    info: Any
    provider: Any


def cluster_auth(k8s_info: Output) -> None:
    """Auth cluster with certificate"""
    info_callable = lambda info: CERTIFICATE.format(
        info[2]["cluster_ca_certificate"],
        info[1],
        "{0}_{1}_{2}".format(PROJECT, ZONE, info[0]),
    )

    k8s_config = k8s_info.apply(info_callable)
    return k8s_config


def provision_k8s_cluster() -> K8Cluster:
    """Provision Cluster K8Cluster Object"""
    k8s_cluster: Cluster = Cluster(
        "gke-cluster",
        initial_node_count=NODE_COUNT,
        node_version=MASTER_VERSION,
        min_master_version=MASTER_VERSION,
        node_config=ClusterNodeConfigArgs(
            machine_type=NODE_MACHINE_TYPE,
            oauth_scopes=OUTH_SCOPES,
        ),
    )
    k8s_info: Output = Output.all(
        k8s_cluster.name,
        k8s_cluster.endpoint,
        k8s_cluster.master_auth,
    )
    k8s_config: Output = cluster_auth(k8s_info)
    # Make a Kubernetes provider instance that uses our cluster from above.
    k8s_provider: Provider = Provider("gke_k8s", kubeconfig=k8s_config)
    return K8Cluster(
        **{
            ClusterEnum.CLUSTER.value: k8s_cluster,
            ClusterEnum.CONFIG.value: k8s_config,
            ClusterEnum.INFO.value: k8s_info,
            ClusterEnum.PROVIDER.value: k8s_provider,
        },
    )
