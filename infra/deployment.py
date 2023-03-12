from enum import Enum
from typing import List

import yaml
from pulumi import ResourceOptions, export, get_project, get_stack
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

from helper import list_files
from models import K8ConfigModel


class K8DefinationEnum(str, Enum):
    service = "Service"
    deployment = "Deployment"
    load_balancer = "LoadBalancer"
    cluster_ip = "ClusterIP"


def load_yaml(filpath):
    with open(filpath, "r") as f:
        return yaml.safe_load(f)


def load_config():
    config_paths = list_files("k8-configs")
    return [K8ConfigModel(**load_yaml(path)) for path in config_paths]


def init_service(model, k8s_provider) -> Service:
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


def init_loadbalancer(model, k8s_provider):
    labels = {}
    ingress = Service(
        model.metadata.name,
        spec=ServiceSpecArgs(
            type="LoadBalancer",
            selector=labels,
            ports=[ServicePortArgs(port=80)],
        ),
        opts=ResourceOptions(provider=k8s_provider),
    )
    return ingress


def init_deploy(model, k8s_provider):
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


def provision_application_service(cluster):
    # Create a canary deployment to test that this cluster works.
    k8_config_models: List[K8ConfigModel] = load_config()
    services = {}
    deployments = {}
    for model in k8_config_models:
        if model.kind == K8DefinationEnum.service.value:
            services[model.spec.type] = init_service(model, cluster.provider)
        if model.kind == K8DefinationEnum.deployment.value:
            deployments[model.kind] = init_deploy(model, cluster.provider)

    # export the kubeconfig so that the client can easily access the cluster.
    export("kubeconfig", cluster.config)
    if ingress := services.get(K8DefinationEnum.load_balancer.value):
        export(
            "ingress_ip",
            ingress.status.apply(lambda status: status.load_balancer.ingress[0].ip),
        )
