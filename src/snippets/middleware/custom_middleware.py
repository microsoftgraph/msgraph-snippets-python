# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# <CustomMiddlewareSnippet>
from kiota_http.middleware.middleware import BaseMiddleware
from httpx import Request, Response, AsyncBaseTransport

class CustomMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def send(self, request: Request, transport: AsyncBaseTransport) -> Response:
        print(request.method, request.url)
        response = await super().send(request, transport)
        return response
# </CustomMiddlewareSnippet>
