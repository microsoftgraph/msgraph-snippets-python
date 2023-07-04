# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from azure.identity import InteractiveBrowserCredential
from kiota_authentication_azure.azure_identity_authentication_provider import (
    AzureIdentityAuthenticationProvider)
from msgraph import GraphServiceClient, GraphRequestAdapter
from msgraph_core import GraphClientFactory, NationalClouds

# pylint: disable=too-few-public-methods
class NationalCloudClients:
    @staticmethod
    def create_client_for_us_gov() -> GraphServiceClient:
        # <NationalCloudSnippet>
        scopes = ['https://graph.microsoft.us/.default']

        credential = InteractiveBrowserCredential(
            tenant_id='YOUR_TENANT_ID',
            client_id='YOUR_CLIENT_ID',
            redirect_uri='YOUR_REDIRECT_URI')

        auth_provider = AzureIdentityAuthenticationProvider(credential, scopes=scopes)

        # Create the HTTP client using
        # the Microsoft Graph for US Government L4 endpoint
        http_client = GraphClientFactory.create_with_default_middleware(
            host=NationalClouds.US_GOV)

        adapter = GraphRequestAdapter(auth_provider, http_client)

        graph_client = GraphServiceClient(request_adapter=adapter)
        # </NationalCloudSnippet>

        return graph_client
