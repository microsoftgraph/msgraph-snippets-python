# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import asyncio
import configparser
from msgraph.generated.models.o_data_errors.o_data_error import ODataError
from graph import Graph
from snippets.create_requests import CreateRequests
from snippets.large_file_upload import LargeFileUpload

async def main():
    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    azure_settings = config['azure']

    large_file_settings = config['large_file']

    graph: Graph = Graph(azure_settings)
    user_client = graph.get_client_for_user()

    user = await user_client.me.get()
    if user:
        print('Hello', user.display_name)

    choice = -1

    while choice != 0:
        print('Please choose one of the following options:')
        print('0. Exit')
        print('1. Run create request samples')
        print('2. Run upload samples')

        try:
            choice = int(input())
        except ValueError:
            choice = -1

        try:
            if choice == 0:
                print('Goodbye...')
            elif choice == 1:
                await CreateRequests.run_all_samples(user_client)
            elif choice == 2:
                await LargeFileUpload.run_all_samples(user_client, large_file_settings['largeFilePath'])
            else:
                print('Invalid choice!\n')
        except ODataError as odata_error:
            print('Error:')
            if odata_error.error:
                print(odata_error.error.code, odata_error.error.message)

# Run main
asyncio.run(main())
