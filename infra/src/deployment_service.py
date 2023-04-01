""" Module for taking care of deployments/service provisioning """
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List

import yaml
from pulumi import ResourceOptions
from pulumi_kubernetes import Provider
from pulumi_kubernetes.apps.v1 import Deployment, DeploymentSpecArgs
from pulumi_kubernetes.core.v1 import (
    ContainerArgs,
    PodSpecArgs,
    PodTemplateSpecArgs,
    Service,
    ServicePortArgs,
    ServiceSpecArgs,
)
from pulumi_kubernetes.meta.v1 import LabelSelectorArgs, ObjectMetaArgs

from .cluster import K8Cluster
from .constants import K8_DEFINATION_PATH
from .misc import list_files
from .models import K8ConfigModel


class K8DefinationEnum(str, Enum):
    service = "Service"
    deployment = "Deployment"
    load_balancer = "LoadBalancer"
    cluster_ip = "ClusterIP"


def load_yaml(filpath: str) -> Dict[str, Any]:
    """Load yaml file"""
    with open(filpath, "r") as f:
        return yaml.safe_load(f)


def load_config() -> List[K8ConfigModel]:
    """Load K8 Definations config"""
    config_paths = list_files(K8_DEFINATION_PATH)
    return [K8ConfigModel(**load_yaml(path)) for path in config_paths]


def init_service(model: K8ConfigModel, k8s_provider: Provider) -> Service:
    """Initializes K8 Service"""
    ports: List[ServicePortArgs] = [
        ServicePortArgs(port=port.port, target_port=port.targetPort)
        for port in model.spec.ports
    ]
    service: Service = Service(
        model.metadata.name,
        spec=ServiceSpecArgs(
            type=model.spec.type,
            selector=model.spec.selector.matchLabels.dict(),
            ports=ports,
        ),
        opts=ResourceOptions(provider=k8s_provider),
    )
    return service


def init_deploy(model: K8ConfigModel, k8s_provider: Provider) -> Deployment:
    """Initializes K8 Deployment"""
    containers: List[ContainerArgs] = [
        ContainerArgs(**cont.dict()) for cont in model.spec.template.spec.containers
    ]
    deployment = Deployment(
        model.metadata.name,
        spec=DeploymentSpecArgs(
            selector=LabelSelectorArgs(
                match_labels=model.spec.selector.matchLabels.dict(),
            ),
            replicas=model.spec.replicas,
            template=PodTemplateSpecArgs(
                metadata=ObjectMetaArgs(
                    labels=model.spec.template.metadata.labels.dict(),
                ),
                spec=PodSpecArgs(containers=containers),
            ),
        ),
        opts=ResourceOptions(provider=k8s_provider),
    )
    return deployment


def provision_application_service(cluster: K8Cluster) -> None:
    """Loads Yaml k8 definationa and create services/deployments accordingly
    Args:
        cluster (K8Cluster): Cluster Model
    """
    k8_config_models: List[K8ConfigModel] = load_config()
    services: Dict[str, Service] = {}
    deployments: Dict[str, Deployment] = {}
    for model in k8_config_models:
        if model.kind == K8DefinationEnum.service.value:
            services[model.metadata.name] = init_service(model, cluster.provider)
        if model.kind == K8DefinationEnum.deployment.value:
            deployments[model.metadata.name] = init_deploy(model, cluster.provider)

    return (deployments, services)
