# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from datetime import datetime, timedelta
from msgraph.generated.models.date_time_time_zone import DateTimeTimeZone
from msgraph.generated.models.event import Event
from msgraph.generated.users.item.calendar_view.calendar_view_request_builder import CalendarViewRequestBuilder
from msgraph.graph_service_client import GraphServiceClient
from msgraph_core.requests.batch_request_builder import BatchRequestBuilder
from msgraph_core.requests.batch_request_content import BatchRequestContent
from msgraph_core.requests.batch_request_content_collection import BatchRequestContentCollection
from msgraph_core.requests.batch_request_item import BatchRequestItem

class BatchRequests:
    @staticmethod
    async def run_all_samples(graph_client: GraphServiceClient) -> None:
        await BatchRequests.simple_batch(graph_client)
        await BatchRequests.dependent_batch(graph_client)

    @staticmethod
    async def simple_batch(graph_client: GraphServiceClient) -> None:
        # <SimpleBatchSnippet>
        # Use the request builder to generate a regular
        # request to /me
        user_request = graph_client.me.to_get_request_information()

        today = datetime.now().replace(hour=0,minute=0,second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)

        # Use the request builder to generate a regular
        # request to /me/calendarview?startDateTime="start"&endDateTime="end"
        query_params = CalendarViewRequestBuilder.CalendarViewRequestBuilderGetQueryParameters(
            start_date_time=today.isoformat(timespec='seconds'),
            end_date_time=tomorrow.isoformat(timespec='seconds')
        )

        config = CalendarViewRequestBuilder.CalendarViewRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )
        events_request = graph_client.me.calendar_view.to_get_request_information(config)

        # Build the batch
        user_batch_item = BatchRequestItem(request_information=user_request)
        events_batch_item = BatchRequestItem(request_information=events_request)
        batch_request_content = BatchRequestContentCollection()
        batch_request_content.add_batch_request_item(user_batch_item)
        batch_request_content.add_batch_request_item(events_batch_item)

        # Create batch request builder (temporary?)
        batch_request_builder = BatchRequestBuilder(request_adapter=graph_client.request_adapter)

        batch_response = await batch_request_builder.post(batch_request_content)

        # Deserialize response based on known return type
        # TODO
        # </SimpleBatchSnippet>
        return

    @staticmethod
    async def dependent_batch(graph_client: GraphServiceClient) -> None:
        # <DependentBatchSnippet>
        today = datetime.now().replace(hour=0,minute=0,second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)

        new_event = Event(
            subject= "File end-of-day report",
            start=DateTimeTimeZone(
                date_time=(today + timedelta(hours=17)).isoformat(timespec='seconds'),
                time_zone='Pacific Standard Time'
            ),
            end=DateTimeTimeZone(
                date_time=(today + timedelta(hours=17, minutes=30)).isoformat(timespec='seconds'),
                time_zone='Pacific Standard Time'
            )
        )

        # Use the request builder to generate a regular
        # POST request to /me/events
        add_event_request = graph_client.me.events.to_post_request_information(new_event)

        # Use the request builder to generate a regular
        # request to /me/calendarview?startDateTime="start"&endDateTime="end"
        query_params = CalendarViewRequestBuilder.CalendarViewRequestBuilderGetQueryParameters(
            start_date_time=today.isoformat(timespec='seconds'),
            end_date_time=tomorrow.isoformat(timespec='seconds')
        )

        config = CalendarViewRequestBuilder.CalendarViewRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )
        events_request = graph_client.me.calendar_view.to_get_request_information(config)

        # Build the batch
        add_event_batch_item = BatchRequestItem(request_information=add_event_request)
        events_batch_item = BatchRequestItem(request_information=events_request, depends_on=[add_event_batch_item])
        batch_request_content = BatchRequestContentCollection()
        batch_request_content.add_batch_request_item(add_event_batch_item)
        batch_request_content.add_batch_request_item(events_batch_item)

        # Create batch request builder (temporary?)
        batch_request_builder = BatchRequestBuilder(request_adapter=graph_client.request_adapter)

        batch_response = await batch_request_builder.post(batch_request_content)

        # Deserialize response based on known return type
        # TODO
        # </DependentBatchSnippet>
        return
