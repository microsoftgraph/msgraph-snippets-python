# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# <CustomMiddlewareSnippet>
from kiota_http.middleware.middleware import BaseMiddleware
from httpx import Request, Response, AsyncBaseTransport

# pylint: disable=too-few-public-methods
class CustomMiddleware(BaseMiddleware):
    async def send(self, request: Request, transport: AsyncBaseTransport) -> Response:
        print(request.method, request.url)
        response = await super().send(request, transport)
        return response
# </CustomMiddlewareSnippet>
