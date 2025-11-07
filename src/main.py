# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import asyncio
import configparser
from msgraph.generated.models.o_data_errors.o_data_error import ODataError
from graph import Graph
from snippets.batch_requests import BatchRequests
from snippets.create_requests import CreateRequests

async def main():
    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)
    # user_client = graph.get_client_for_user()
    user_client = graph.get_debug_client_for_user()

    #user = await user_client.me.get()
    #if user:
    #    print('Hello', user.display_name)

    choice = -1

    while choice != 0:
        print('Please choose one of the following options:')
        print('0. Exit')
        print('1. Run batch samples')
        print('2. Run request samples')

        try:
            choice = int(input())
        except ValueError:
            choice = -1

        try:
            match choice:
                case 0:
                    print('Goodbye...')
                case 1:
                    await BatchRequests.run_all_samples(user_client)
                case 2:
                    await CreateRequests.run_all_samples(user_client)
                case _:
                    print('Invalid choice!\n')

        except ODataError as odata_error:
            print('Error:')
            if odata_error.error:
                print(odata_error.error.code, odata_error.error.message)

# Run main
asyncio.run(main())
