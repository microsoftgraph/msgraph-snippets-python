# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import asyncio
import configparser
from graph import Graph

async def main():
    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)
    user_client = graph.get_client_for_user()

    user = await user_client.me.get()
    if user:
        print('Hello', user.display_name)

# Run main
asyncio.run(main())
