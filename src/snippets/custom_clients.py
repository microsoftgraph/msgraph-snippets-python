# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from typing import List
from azure.core.credentials import TokenCredential
from msgraph import GraphServiceClient, GraphRequestAdapter
from msgraph_core import GraphClientFactory
from kiota_authentication_azure.azure_identity_authentication_provider import (
    AzureIdentityAuthenticationProvider)
from httpx import AsyncClient
from middleware.custom_middleware import CustomMiddleware

class CustomClients:
    @staticmethod
    def create_with_custom_middleware(
        credential: TokenCredential, scopes: List[str]) -> GraphServiceClient:
        # <CustomMiddlewareSnippet>
        # Create an authentication provider
        # credential is one of the credential classes from azure.identity
        # scopes is an array of permission scope strings
        auth_provider = AzureIdentityAuthenticationProvider(credential, scopes=scopes)

        # Get default middleware
        # msgraph_core.GraphClientFactory
        middleware = GraphClientFactory.get_default_middleware(options=None)

        # Add custom middleware
        # Implement a custom middleware by extending the BaseMiddleware class
        # https://github.com/microsoft/kiota-http-go/blob/main/kiota_http/middleware/middleware.py
        middleware.append(CustomMiddleware())

        # Create an HTTP client with the middleware
        http_client = GraphClientFactory.create_with_custom_middleware(middleware)

        # Create a request adapter with the HTTP client
        adapter = GraphRequestAdapter(auth_provider, http_client)

        # Create the Graph client
        graph_client = GraphServiceClient(request_adapter=adapter)
        # </CustomMiddlewareSnippet>

        return graph_client

    @staticmethod
    def create_with_proxy(
        credential: TokenCredential, scopes: List[str]) -> GraphServiceClient:
        # <ProxySnippet>
        # Create an authentication provider
        # credential is one of the credential classes from azure.identity
        # scopes is an array of permission scope strings
        auth_provider = AzureIdentityAuthenticationProvider(credential, scopes=scopes)

        # Proxy URLs
        proxies = {
            'http://': 'http://proxy-url',
            'https://': 'http://proxy-url',
        }

        # Create a custom HTTP client with the proxies
        # httpx.AsyncClient
        http_client = AsyncClient(proxies=proxies) # type: ignore

        # Apply the default Graph middleware to the HTTP client
        http_client = GraphClientFactory.create_with_default_middleware(client=http_client)

        # Create a request adapter with the HTTP client
        adapter = GraphRequestAdapter(auth_provider, http_client)

        # Create the Graph client
        graph_client = GraphServiceClient(request_adapter=adapter)
        # </ProxySnippet>

        return graph_client
