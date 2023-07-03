# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from msgraph import GraphServiceClient
from msgraph.generated.users.item.user_item_request_builder import UserItemRequestBuilder
from msgraph.generated.users.item.messages.messages_request_builder import MessagesRequestBuilder
from msgraph.generated.users.item.messages.item.message_item_request_builder import MessageItemRequestBuilder
from msgraph.generated.users.item.events.events_request_builder import EventsRequestBuilder
from msgraph.generated.users.item.calendar_view.calendar_view_request_builder import CalendarViewRequestBuilder
from msgraph.generated.groups.groups_request_builder import GroupsRequestBuilder
from msgraph.generated.models.user import User
from msgraph.generated.models.message import Message
from msgraph.generated.models.calendar import Calendar
from msgraph.generated.models.team import Team
from msgraph.generated.models.team_fun_settings import TeamFunSettings
from msgraph.generated.models.giphy_rating_type import GiphyRatingType
from msgraph.generated.models.message_collection_response import MessageCollectionResponse
from msgraph.generated.models.event_collection_response import EventCollectionResponse

class CreateRequests:
    @staticmethod
    async def run_all_samples(graph_client: GraphServiceClient) -> None:
        # Create a new message
        message = Message()
        message.subject = 'Temporary'

        temp_message = await graph_client.me.messages.post(message)
        if temp_message and temp_message.id:
            message_id = temp_message.id
        else:
            raise RuntimeError('Could not create a temporary message')

        # Get a team to update
        query_params = GroupsRequestBuilder.GroupsRequestBuilderGetQueryParameters(
            filter='resourceProvisioningOptions/Any(x:x eq \'Team\')'
        )

        config = GroupsRequestBuilder.GroupsRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )

        teams = await graph_client.groups.get(config)
        if teams and teams.value and teams.value[0].id:
            team_id = teams.value[0].id
        else:
            raise RuntimeError('Could not get a team')

        await CreateRequests.make_read_request(graph_client)
        await CreateRequests.make_select_request(graph_client)
        await CreateRequests.make_list_request(graph_client)
        await CreateRequests.make_item_by_id_request(graph_client, message_id)
        await CreateRequests.make_expand_request(graph_client, message_id)
        await CreateRequests.make_delete_request(graph_client, message_id)
        await CreateRequests.make_create_request(graph_client)
        await CreateRequests.make_update_request(graph_client, team_id)
        await CreateRequests.make_headers_request(graph_client)
        await CreateRequests.make_query_parameters_request(graph_client)

    @staticmethod
    async def make_read_request(graph_client: GraphServiceClient) -> User | None:
        # <ReadRequestSnippet>
        # GET https://graph.microsoft.com/v1.0/me
        user = await graph_client.me.get()
        # </ReadRequestSnippet>

        return user

    @staticmethod
    async def make_select_request(graph_client: GraphServiceClient) -> User | None:
        # <SelectRequestSnippet>
        # GET https://graph.microsoft.com/v1.0/me?$select=displayName,jobTitle

        # msgraph.generated.users.item.user_item_request_builder
        query_params = UserItemRequestBuilder.UserItemRequestBuilderGetQueryParameters(
            select=['displayName', 'jobTitle']
        )

        config = UserItemRequestBuilder.UserItemRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )

        user = await graph_client.me.get(config)
        # </SelectRequestSnippet>

        return user

    @staticmethod
    async def make_list_request(graph_client: GraphServiceClient) -> MessageCollectionResponse | None:
        # <ListRequestSnippet>
        # GET https://graph.microsoft.com/v1.0/me/messages?
        # $select=subject,sender&$filter=subject eq 'Hello world'

        # msgraph.generated.users.item.messages.messages_request_builder.MessagesRequestBuilder
        query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
            select=['subject', 'sender'],
            filter='subject eq \'Hello world\''
        )

        config = MessagesRequestBuilder.MessagesRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )

        messages = await graph_client.me.messages.get(config)
        # </ListRequestSnippet>

        return messages

    @staticmethod
    async def make_item_by_id_request(graph_client: GraphServiceClient, message_id: str) -> Message | None:
        # <ItemByIdRequestSnippet>
        # GET https://graph.microsoft.com/v1.0/me/messages/{message-id}
        # message_id is a string containing the id property of the message
        message = await graph_client.me.messages.by_message_id(message_id).get()
        # </ItemByIdRequestSnippet>

        return message

    @staticmethod
    async def make_expand_request(graph_client: GraphServiceClient, message_id: str) -> Message | None:
        # <ExpandRequestSnippet>
        # GET https://graph.microsoft.com/v1.0/me/messages/{message-id}?$expand=attachments
        # message_id is a string containing the id property of the message

        # msgraph.generated.users.item.messages.item.message_item_request_builder.MessageItemRequestBuilder
        query_params = MessageItemRequestBuilder.MessageItemRequestBuilderGetQueryParameters(
            expand=['attachments']
        )

        config = MessageItemRequestBuilder.MessageItemRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )

        message = await graph_client.me.messages.by_message_id(message_id).get(config)
        # </ExpandRequestSnippet>

        return message

    @staticmethod
    async def make_delete_request(graph_client: GraphServiceClient, message_id: str) -> None:
        # <DeleteRequestSnippet>
        # DELETE https://graph.microsoft.com/v1.0/me/messages/{message-id}
        # message_id is a string containing the id property of the message
        await graph_client.me.messages.by_message_id(message_id).delete()
        # </DeleteRequestSnippet>

    @staticmethod
    async def make_create_request(graph_client: GraphServiceClient) -> Calendar | None:
        # <CreateRequestSnippet>
        # POST https://graph.microsoft.com/v1.0/me/calendars

        # msgraph.generated.models.calendar.Calendar
        calendar = Calendar()
        calendar.name = 'Volunteer'

        new_calendar = await graph_client.me.calendars.post(calendar)
        # </CreateRequestSnippet>

        return new_calendar

    @staticmethod
    async def make_update_request(graph_client: GraphServiceClient, team_id: str) -> None:
        # <UpdateRequestSnippet>
        # PATCH https://graph.microsoft.com/v1.0/teams/{team-id}

        # msgraph.generated.models.team_fun_settings.TeamFunSettings
        fun_settings = TeamFunSettings()
        fun_settings.allow_giphy = True
        # msgraph.generated.models.giphy_rating_type.GiphyRatingType
        fun_settings.giphy_content_rating = GiphyRatingType.Strict

        # msgraph.generated.models.team.Team
        team = Team()
        team.fun_settings = fun_settings

        # team_id is a string containing the id property of the team
        await graph_client.teams.by_team_id(team_id).patch(team)
        # </UpdateRequestSnippet>

    @staticmethod
    async def make_headers_request(graph_client: GraphServiceClient) -> EventCollectionResponse | None:
        # <HeadersRequestSnippet>
        # GET https://graph.microsoft.com/v1.0/me/events

        # msgraph.generated.users.item.events.events_request_builder.EventsRequestBuilder
        config = EventsRequestBuilder.EventsRequestBuilderGetRequestConfiguration(
            headers={ 'Prefer': 'outlook.timezone="Pacific Standard Time"' }
        )

        events = await graph_client.me.events.get(config)
        # </HeadersRequestSnippet>

        return events

    @staticmethod
    async def make_query_parameters_request(graph_client: GraphServiceClient) -> EventCollectionResponse | None:
        # <QueryParametersRequestSnippet>
        # GET https://graph.microsoft.com/v1.0/me/calendarView?
        # startDateTime=2023-06-14T00:00:00Z&endDateTime=2023-06-15T00:00:00Z

        # msgraph.generated.users.item.calendar_view.calendar_view_request_builder.CalendarViewRequestBuilder
        query_params = CalendarViewRequestBuilder.CalendarViewRequestBuilderGetQueryParameters(
            start_date_time='2023-06-14T00:00:00Z',
            end_date_time='2023-06-15T00:00:00Z'
        )

        config = CalendarViewRequestBuilder.CalendarViewRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )

        events = await graph_client.me.calendar_view.get(config)
        # </QueryParametersRequestSnippet>

        return events
