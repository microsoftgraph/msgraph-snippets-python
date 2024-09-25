# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import msgraph.generated.users.item.messages.item.attachments.create_upload_session.create_upload_session_post_request_body as attachment_upload
import msgraph.generated.drives.item.items.item.create_upload_session.create_upload_session_post_request_body as drive_item_upload
from kiota_abstractions.api_error import APIError
from msgraph.generated.models.attachment_item import AttachmentItem
from msgraph.generated.models.attachment_type import AttachmentType
from msgraph.generated.models.drive_item import DriveItem
from msgraph.generated.models.drive_item_uploadable_properties import DriveItemUploadableProperties
from msgraph.generated.models.file_attachment import FileAttachment
from msgraph.generated.models.message import Message
from msgraph.graph_service_client import GraphServiceClient
from msgraph_core.tasks.large_file_upload import LargeFileUploadTask

class LargeFileUpload:
    @staticmethod
    async def run_all_samples(graph_client: GraphServiceClient, file_path: str) -> None:
        item_path = 'Documents/vacation.gif'
        await LargeFileUpload.upload_file_to_onedrive(graph_client, file_path, item_path)
        await LargeFileUpload.upload_attachment_to_message(graph_client, file_path)

    @staticmethod
    async def upload_file_to_onedrive(graph_client: GraphServiceClient, file_path: str, item_path: str) -> None:
        # <LargeFileUploadSnippet>
        file_stream = open(file_path, 'rb')

        # Use properties to specify the conflict behavior
        upload_properties = DriveItemUploadableProperties(
            additional_data={'@microsoft.graph.conflictBehavior': 'replace'}
        )

        # import msgraph.generated.drives.item.items.item.create_upload_session.create_upload_session_post_request_body as drive_item_upload
        upload_session_body = drive_item_upload.CreateUploadSessionPostRequestBody(
            item=upload_properties
        )

        # Create the upload session
        # item_path does not need to be a path to an existing item
        item_path_id = 'root:/' + item_path + ':'
        my_drive = await graph_client.me.drive.get()
        if my_drive is None or my_drive.id is None: return
        upload_session = await graph_client.drives.by_drive_id(
            my_drive.id).items.by_drive_item_id(
                item_path_id).create_upload_session.post(upload_session_body)

        if upload_session is None: return

        # Max slice size must be a multiple of 320 KiB
        max_slice_size = 320 * 1024
        file_upload_task = LargeFileUploadTask(
            upload_session=upload_session,
            request_adapter=graph_client.request_adapter,
            stream=file_stream, # type: ignore
            max_chunk_size=max_slice_size,
            parsable_factory=DriveItem #type:ignore
        )

        total_length = os.path.getsize(file_path)

        # Create a callback that is invoked after each slice is uploaded
        def progress_callback(uploaded_byte_range: tuple[int,int]):
            print(f'Uploaded {uploaded_byte_range[0]} bytes of {total_length} bytes\n')

        try:
            upload_result = await file_upload_task.upload(progress_callback)
            if upload_result.upload_succeeded and upload_result.item_response is not None:
                drive_item: DriveItem = upload_result.item_response
                print(f'Upload complete, item ID: {drive_item.id}')
            else:
                print('Upload failed')
        except APIError as ex:
            print(f'Error uploading file: {ex.message}')
        # </LargeFileUploadSnippet>

    @staticmethod
    async def resume_upload(file_upload_task: LargeFileUploadTask) -> None:
        # <ResumeSnippet>
        await file_upload_task.resume()
        # </ResumeSnippet>

    @staticmethod
    async def upload_attachment_to_message(graph_client: GraphServiceClient, file_path: str) -> None:
        # <UploadAttachmentSnippet>
        # Create message
        draft_message = Message(
            subject="Large attachment"
        )

        saved_draft = await graph_client.me.messages.post(draft_message)
        if saved_draft is None or saved_draft.id is None: return

        file_stream = open(file_path, 'rb')
        total_length = os.path.getsize(file_path)

        large_attachment = AttachmentItem(
            attachment_type=AttachmentType.File,
            name=os.path.basename(file_path),
            size=total_length
        )

        # import msgraph.generated.users.item.messages.item.attachments.create_upload_session.create_upload_session_post_request_body as attachment_upload
        upload_session_body = attachment_upload.CreateUploadSessionPostRequestBody(
            attachment_item=large_attachment
        )

        upload_session = await graph_client.me.messages.by_message_id(
            saved_draft.id).attachments.create_upload_session.post(upload_session_body)

        if upload_session is None: return

        # Max slice size must be a multiple of 320 KiB
        max_slice_size = 320 * 1024
        file_upload_task = LargeFileUploadTask(
            upload_session=upload_session,
            request_adapter=graph_client.request_adapter,
            stream=file_stream, # type: ignore
            max_chunk_size=max_slice_size,
            parsable_factory=FileAttachment #type:ignore
        )

        # Create a callback that is invoked after each slice is uploaded
        def progress_callback(uploaded_byte_range: tuple[int,int]):
            print(f'Uploaded {uploaded_byte_range[0]} bytes of {total_length} bytes\n')

        try:
            upload_result = await file_upload_task.upload(progress_callback)
            if upload_result.upload_succeeded and upload_result.item_response is not None:
                file_attachment: FileAttachment = upload_result.item_response
                print(f'Upload complete, attachment ID: {file_attachment.id}')
            else:
                print('Upload failed')
        except APIError as ex:
            print(f'Error uploading attachment: {ex.message}')
        # </UploadAttachmentSnippet>
