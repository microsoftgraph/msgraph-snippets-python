# Microsoft Graph Python SDK Snippets

[![Pylint](https://github.com/microsoftgraph/msgraph-snippets-python/actions/workflows/pylint.yml/badge.svg)](https://github.com/microsoftgraph/msgraph-snippets-python/actions/workflows/pylint.yml) ![License.](https://img.shields.io/badge/license-MIT-green.svg)

This repository contains sample snippets for the [Microsoft Graph Python SDK](https://github.com/microsoftgraph/msgraph-sdk-python). These snippets are referenced in the [Microsoft Graph SDK documentation](https://learn.microsoft.com/graph/sdks/sdks-overview).

## Prerequisites

- [Python 3](https://www.python.org)

## Register an app in Azure Active Directory

1. Open a browser and navigate to the [Microsoft Entra admin center](https://entra.microsoft.com) and login using a **Work or School Account**.

1. Expand **Azure Active Directory** in the left-hand navigation, then expand **Applications**, then select **App registrations**.

1. Select **New registration**. Enter a name for your application, for example, `Graph Snippets`.

1. Set **Supported account types** as desired. The options are:

    | Option | Who can sign in? |
    |--------|------------------|
    | **Accounts in this organizational directory only** | Only users in your Microsoft 365 organization |
    | **Accounts in any organizational directory** | Users in any Microsoft 365 organization (work or school accounts) |
    | **Accounts in any organizational directory ... and personal Microsoft accounts** | Users in any Microsoft 365 organization (work or school accounts) and personal Microsoft accounts |

1. Leave **Redirect URI** empty.

1. Select **Register**. On the application's **Overview** page, copy the value of the **Application (client) ID** and save it, you will need it in the next step. If you chose **Accounts in this organizational directory only** for **Supported account types**, also copy the **Directory (tenant) ID** and save it.

1. Select **Authentication** under **Manage**. Locate the **Advanced settings** section and change the **Allow public client flows** toggle to **Yes**, then choose **Save**.

## Configuring the sample

You can set these values directly in [config.cfg](src/config.cfg), or you can create a copy of **config.cfg** named **config.dev.cfg** and set the values there.

1. Set `clientId` to the **Application (client) ID** from your app registration.
1. If you chose **Accounts in this organizational directory only** for **Supported account types**, set `tenantId` to your **Directory (tenant) ID**.

## Code of conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

```json
[
    {
        "id": "cbd979a7-60cf-400a-a1e4-d298cf3603c4",
        "url": "https://graph.microsoft.com/v1.0/me",
        "depends_on": []
    },
    {
        "id": "756960d4-3b04-431b-958f-3d7130f2d323",
        "url": "https://graph.microsoft.com/v1.0/me/calendarView?endDateTime=2024-10-05T00%3A00%3A00&startDateTime=2024-10-04T00%3A00%3A00",
        "depends_on": []
    }
]
```
