""" Model class for IaC GKE"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Labels(BaseModel):
    name: str
    app: Optional[str]


class Metadata(BaseModel):
    name: str
    labels: Labels


class MatchLabels(BaseModel):
    name: str
    app: Optional[str]


class Selector(BaseModel):
    matchLabels: Optional[MatchLabels]


class Port(BaseModel):
    containerPort: Optional[int]


class SpecPort(BaseModel):
    port: Optional[int]
    targetPort: Optional[int] = Field(alis="target_port")


class EnvItem(BaseModel):
    name: Optional[str]
    value: Optional[str]


class Container(BaseModel):
    name: str
    image: str
    ports: Optional[List[Port]]
    env: Optional[List[EnvItem]]


class TemplateSpec(BaseModel):
    containers: Optional[List[Container]]


class Template(BaseModel):
    metadata: Metadata
    spec: Optional[TemplateSpec]


class Spec(BaseModel):
    type: Optional[str]
    replicas: Optional[int] = 1
    selector: Optional[Selector]
    template: Optional[Template] = None
    containers: Optional[List[Container]]
    ports: Optional[List[SpecPort]]


class K8ConfigModel(BaseModel):
    apiVersion: str  # add validation for API Kind
    kind: str  # add validation for kind
    metadata: Metadata
    spec: Spec
