from typing import Any, List, Optional

import dlt
from dlt.sources.rest_api import (
    RESTAPIConfig,
    check_connection,
    rest_api_resources,
)


def get_interested_leagues() -> List[str]:
    return [741068]


@dlt.source(name="fpl")
def fpl_source(
    access_token: Optional[str] = dlt.secrets.value,
) -> Any:
    # Create a REST API configuration for the GitHub API
    # Use RESTAPIConfig to get autocompletion and type checking
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://fantasy.premierleague.com/api/",
            # we add an auth config if the auth token is present
            "auth": (
                {
                    "type": "bearer",
                    "token": access_token,
                }
                if access_token
                else None
            ),
        },
        # The default configuration for all resources and their endpoints
        "resource_defaults": {
            "write_disposition": "replace",
            "endpoint": {
                "params": {
                    "per_page": 100,
                },
            },
        },
        "resources": [
            # This is a simple resource definition,
            # that uses the endpoint path as a resource name:
            # "pulls",
            # Alternatively, you can define the endpoint as a dictionary
            # {
            #     "name": "pulls", # <- Name of the resource
            #     "endpoint": "pulls",  # <- This is the endpoint path
            # }
            # Or use a more detailed configuration:
            {
                "name": "standings",
                "endpoint": {
                    "path": "bootstrap-static/",
                    # Query parameters for the endpoint
                },
            },
            {
                "name": "elements",
                "endpoint": {
                    "path": "bootstrap-static/",
                    # Query parameters for the endpoint
                },
            },
            # The following is an example of a resource that uses
            # a parent resource (`issues`) to get the `issue_number`
            # and include it in the endpoint path:
            # {
            #     "name": "issue_comments",
            #     "endpoint": {
            #         # The placeholder {issue_number} will be resolved
            #         # from the parent resource
            #         "path": "issues/{issue_number}/comments",
            #         "params": {
            #             # The value of `issue_number` will be taken
            #             # from the `number` field in the `issues` resource
            #             "issue_number": {
            #                 "type": "resolve",
            #                 "resource": "issues",
            #                 "field": "number",a
            #             }
            #         },
            #     },
            #     # Include data from `id` field of the parent resource
            #     # in the child data. The field name in the child data
            #     # will be called `_issues_id` (_{resource_name}_{field_name})
            #     "include_from_parent": ["id"],
            # },
        ],
    }

    yield from rest_api_resources(config)


def check_network_and_authentication() -> None:
    (can_connect, error_msg) = check_connection(
        fpl_source,
        "not_existing_endpoint",
    )
    if not can_connect:
        pass  # do something with the error message


pipeline = dlt.pipeline(
    pipeline_name="fpl",
    destination="duckdb",
    dataset_name="fpl_data",
)

load_info = pipeline.run(fpl_source())
print(load_info)  # noqa: T201
