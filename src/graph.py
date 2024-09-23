# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from configparser import SectionProxy
from azure.identity import DeviceCodeCredential
from msgraph.graph_service_client import GraphServiceClient

# pylint: disable=too-few-public-methods
class Graph:
    settings: SectionProxy

    def __init__(self, config: SectionProxy) -> None:
        self.settings = config

    def get_client_for_user(self) -> GraphServiceClient:
        client_id = self.settings['clientId']
        tenant_id = self.settings['tenantId']
        graph_scopes = self.settings['graphUserScopes'].split(' ')

        credential = DeviceCodeCredential(client_id, tenant_id = tenant_id)
        client = GraphServiceClient(credential, graph_scopes)
        return client
