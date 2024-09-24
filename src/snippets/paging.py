# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import time
from kiota_abstractions.base_request_configuration import RequestConfiguration
from msgraph.generated.models.message import Message
from msgraph.generated.users.item.messages.messages_request_builder import MessagesRequestBuilder
from msgraph.graph_service_client import GraphServiceClient
from msgraph_core.tasks.page_iterator import PageIterator

class Paging:
    @staticmethod
    async def run_all_samples(graph_client: GraphServiceClient) -> None:
        # await Paging.iterate_all_messages(graph_client)
        await Paging.iterate_all_messages_with_pause(graph_client)
        # await Paging.manually_page_all_messages(graph_client)

    @staticmethod
    # <IterateCallbackSnippet>
    def message_callback(message: Message) -> bool:
        print(message.subject)

        # Return True to continue iterating
        return True
    # </IterateCallbackSnippet>

    @staticmethod
    async def iterate_all_messages(graph_client: GraphServiceClient) -> None:
        # <PagingSnippet>
        query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
            select=['sender', 'subject', 'body'],
            top=10
        )

        config = RequestConfiguration(
            query_parameters=query_params
        )

        config.headers.add('Prefer', 'outlook.body-content-type="text"')

        messages = await graph_client.me.messages.get(config)

        page_iterator = PageIterator(messages, graph_client.request_adapter) # type: ignore

        # Re-add the header to subsequent requests
        page_iterator.headers.add('Prefer', 'outlook.body-content-type="text"')

        await page_iterator.iterate(Paging.message_callback)
        # </PagingSnippet>


    # <IterateCallbackWithPauseSnippet>
    msg_count = 0

    @staticmethod
    def message_callback_with_pause(message: Message) -> bool:
        print(message.subject)
        Paging.msg_count += 1

        # Will return False after 25 messages,
        # stopping the iteration
        return Paging.msg_count < 25
    # </IterateCallbackWithPauseSnippet>

    @staticmethod
    async def iterate_all_messages_with_pause(graph_client: GraphServiceClient) -> None:
        # <ResumePagingSnippet>
        query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
            select=['sender', 'subject'],
            top=10
        )

        config = RequestConfiguration(
            query_parameters=query_params
        )

        messages = await graph_client.me.messages.get(config)

        page_iterator = PageIterator(messages, graph_client.request_adapter) # type: ignore

        while True:
            await page_iterator.iterate(Paging.message_callback_with_pause)

            # This is working in my specific case, but I'm not confident
            # it will work for all scenarios. Specifically, the pause_index
            # is winding up as 0 in my case, with the last page being only 4 messages
            # Yes, this will accurately detect there are no more pages, but
            # I can't be sure that I've iterated over the entire current page
            if (page_iterator.current_page.odata_next_link is None and
                page_iterator.current_page.value is not None and
                page_iterator.pause_index < len(page_iterator.current_page.value)):
                break

            time.sleep(5)

            # Reset the count
            Paging.msg_count = 0
        # </ResumePagingSnippet>

    @staticmethod
    async def manually_page_all_messages(graph_client: GraphServiceClient) -> None:
        # <ManualPagingSnippet>
        query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
            select=['sender', 'subject'],
            top=10
        )

        config = RequestConfiguration(
            query_parameters=query_params
        )

        messages = await graph_client.me.messages.get(config)

        while messages is not None and messages.value is not None:
            for message in messages.value:
                print(message.subject)

            if messages.odata_next_link is not None:
                messages = await graph_client.me.messages.with_url(messages.odata_next_link).get()
            else:
                break
        # </ManualPagingSnippet>
