from __future__ import annotations

import re
from typing import List

import pydantic
import requests
import simpleregistry

from simrail_sdk import base

RE_REMARKS = re.compile(r"\[([\w ]+)\]", re.UNICODE)
RE_GROUP_NAME = re.compile(r"\((\w+)\)", re.UNICODE)


def get_servers_from_api() -> List:
    response = requests.get(f"https://panel.simrail.eu:8084/servers-open")
    return response.json()["data"]


class ServerRegistry(simpleregistry.Registry):
    def from_api(self):
        for server in get_servers_from_api():
            response_server = ServerResponse(**server)
            server = Server.from_server_response(response_server)
            self.register(server)


class ServerGroupRegistry(simpleregistry.Registry):
    def from_server_registry(self, server_registry: ServerRegistry):
        for server in server_registry:
            groups = RE_GROUP_NAME.search(server.name)
            if groups is None:
                continue
            name = groups.group(1)
            server_group = ServerGroup(code=server.group, name=name)
            self.register(server_group)

    def get_available_codes(self):
        return set(s.code for s in self)


server_registry = ServerRegistry("servers")
server_group_registry = ServerGroupRegistry("server_groups")


class ServerResponse(pydantic.BaseModel):
    ServerCode: str
    ServerName: str
    ServerRegion: str
    IsActive: bool
    id: str


@simpleregistry.register(server_group_registry)
class ServerGroup(base.BasePydanticModel):
    code: str
    name: str

    class Config:
        pk_fields = ["code"]


@simpleregistry.register(server_registry)
class Server(base.BasePydanticModel):
    active: bool
    group: str
    code: str
    name: str
    remarks: str = ""

    class Config:
        pk_fields = ["code"]

    @classmethod
    def from_server_response(cls, server_response: ServerResponse) -> Server:
        group = server_response.ServerCode[:2]
        remarks = ""
        if match := RE_REMARKS.findall(server_response.ServerName):
            remarks = match[0]
        return cls(
            group=group,
            code=server_response.ServerCode,
            name=server_response.ServerName,
            active=server_response.IsActive,
            remarks=remarks,
        )


server_registry.from_api()
server_group_registry.from_server_registry(server_registry)
