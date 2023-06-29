# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from azure.identity import (
    DeviceCodeCredential,
    InteractiveBrowserCredential,
    UsernamePasswordCredential)
from azure.identity.aio import (
    AuthorizationCodeCredential,
    ClientSecretCredential,
    CertificateCredential,
    OnBehalfOfCredential)
from kiota_authentication_azure.azure_identity_authentication_provider import (
    AzureIdentityAuthenticationProvider)
from msgraph import GraphRequestAdapter, GraphServiceClient

class CreateClients:
    @staticmethod
    def create_with_authorization_code() -> GraphServiceClient:
        # <AuthorizationCodeSnippet>
        scopes = ['User.Read']

        # Multi-tenant apps can use "common",
        # single-tenant apps must use the tenant ID from the Azure portal
        tenant_id = 'common'

        # Values from app registration
        client_id = 'YOUR_CLIENT_ID'
        client_secret = 'YOUR_CLIENT_SECRET'
        redirect_uri = 'YOUR_REDIRECT_URI'

        # For authorization code flow, the user signs into the Microsoft
        # identity platform, and the browser is redirected back to your app
        # with an authorization code in the query parameters
        authorization_code = 'AUTH_CODE_FROM_REDIRECT'

        # azure.identity.aio
        credential = AuthorizationCodeCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            authorization_code=authorization_code,
            redirect_uri=redirect_uri,
            client_secret=client_secret)

        # kiota_authentication_azure.azure_identity_authentication_provider
        auth_provider = AzureIdentityAuthenticationProvider(credential, scopes=scopes) # type: ignore

        adapter = GraphRequestAdapter(auth_provider)

        graph_client = GraphServiceClient(adapter)
        # </AuthorizationCodeSnippet>

        return graph_client

    @staticmethod
    def create_with_client_secret() -> GraphServiceClient:
        # <ClientSecretSnippet>
        # The client credentials flow requires that you request the
        # /.default scope, and pre-configure your permissions on the
        # app registration in Azure. An administrator must grant consent
        # to those permissions beforehand.
        scopes = ['https://graph.microsoft.com/.default']

        # Values from app registration
        tenant_id = 'YOUR_TENANT_ID'
        client_id = 'YOUR_CLIENT_ID'
        client_secret = 'YOUR_CLIENT_SECRET'

        # azure.identity.aio
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret)

        # kiota_authentication_azure.azure_identity_authentication_provider
        auth_provider = AzureIdentityAuthenticationProvider(credential, scopes=scopes) # type: ignore

        adapter = GraphRequestAdapter(auth_provider)

        graph_client = GraphServiceClient(adapter)
        # </ClientSecretSnippet>

        return graph_client

    @staticmethod
    def create_with_client_certificate() -> GraphServiceClient:
        # <ClientCertificateSnippet>
        # The client credentials flow requires that you request the
        # /.default scope, and pre-configure your permissions on the
        # app registration in Azure. An administrator must grant consent
        # to those permissions beforehand.
        scopes = ['https://graph.microsoft.com/.default']

        # Values from app registration
        tenant_id = 'YOUR_TENANT_ID'
        client_id = 'YOUR_CLIENT_ID'
        certificate_path = 'YOUR_CERTIFICATE_PATH'

        # azure.identity.aio
        credential = CertificateCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            certificate_path=certificate_path)

        # kiota_authentication_azure.azure_identity_authentication_provider
        auth_provider = AzureIdentityAuthenticationProvider(credential, scopes=scopes) # type: ignore

        adapter = GraphRequestAdapter(auth_provider)

        graph_client = GraphServiceClient(adapter)
        # </ClientCertificateSnippet>

        return graph_client

    @staticmethod
    def create_with_on_behalf_of() -> GraphServiceClient:
        # <OnBehalfOfSnippet>
        scopes = ['https://graph.microsoft.com/.default']

        # Multi-tenant apps can use "common",
        # single-tenant apps must use the tenant ID from the Azure portal
        tenant_id = 'common'

        # Values from app registration
        client_id = 'YOUR_CLIENT_ID'
        client_secret = 'YOUR_CLIENT_SECRET'

        # This is the incoming token to exchange using on-behalf-of flow
        obo_token = 'JWT_TOKEN_TO_EXCHANGE'

        # azure.identity.aio
        credential = OnBehalfOfCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
            user_assertion=obo_token)

        # kiota_authentication_azure.azure_identity_authentication_provider
        auth_provider = AzureIdentityAuthenticationProvider(credential, scopes=scopes) # type: ignore

        adapter = GraphRequestAdapter(auth_provider)

        graph_client = GraphServiceClient(adapter)
        # </OnBehalfOfSnippet>

        return graph_client

    @staticmethod
    def create_with_device_code() -> GraphServiceClient:
        # <DeviceCodeSnippet>
        scopes = ['User.Read']

        # Multi-tenant apps can use "common",
        # single-tenant apps must use the tenant ID from the Azure portal
        tenant_id = 'common'

        # Values from app registration
        client_id = 'YOUR_CLIENT_ID'

        # azure.identity
        credential = DeviceCodeCredential(
            tenant_id=tenant_id,
            client_id=client_id)

        # kiota_authentication_azure.azure_identity_authentication_provider
        auth_provider = AzureIdentityAuthenticationProvider(credential, scopes=scopes)

        adapter = GraphRequestAdapter(auth_provider)

        graph_client = GraphServiceClient(adapter)
        # </DeviceCodeSnippet>

        return graph_client

    @staticmethod
    def create_with_interactive() -> GraphServiceClient:
        # <InteractiveSnippet>
        scopes = ['User.Read']

        # Multi-tenant apps can use "common",
        # single-tenant apps must use the tenant ID from the Azure portal
        tenant_id = 'common'

        # Values from app registration
        client_id = 'YOUR_CLIENT_ID'
        redirect_uri = 'http://localhost:8000'

        # azure.identity
        credential = InteractiveBrowserCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            redirect_uri=redirect_uri)

        # kiota_authentication_azure.azure_identity_authentication_provider
        auth_provider = AzureIdentityAuthenticationProvider(credential, scopes=scopes)

        adapter = GraphRequestAdapter(auth_provider)

        graph_client = GraphServiceClient(adapter)
        # </InteractiveSnippet>

        return graph_client

    @staticmethod
    def create_with_username_password() -> GraphServiceClient:
        # <UserNamePasswordSnippet>
        scopes = ['User.Read']

        # Multi-tenant apps can use "common",
        # single-tenant apps must use the tenant ID from the Azure portal
        tenant_id = 'common'

        # Values from app registration
        client_id = 'YOUR_CLIENT_ID'

        # User name and password
        username = 'adelev@contoso.com'
        password = 'Password1!'

        # azure.identity
        credential = UsernamePasswordCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            username=username,
            password=password)

        # kiota_authentication_azure.azure_identity_authentication_provider
        auth_provider = AzureIdentityAuthenticationProvider(credential, scopes=scopes)

        adapter = GraphRequestAdapter(auth_provider)

        graph_client = GraphServiceClient(adapter)
        # </UserNamePasswordSnippet>

        return graph_client
