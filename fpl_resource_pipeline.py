import dlt
from dlt.sources.helpers.rest_client import RESTClient

# api url
base_url = "https://fantasy.premierleague.com/api/"
bootstrap_url = base_url + "bootstrap-static/"


fpl_client = RESTClient(base_url)


def load_bootstrap_event(key: str):
    response = fpl_client.get(bootstrap_url)
    response.raise_for_status()
    return response.json()[key]


# Define a resource for the first key
@dlt.resource(
    # primary_key="id",
    table_name="events",
    write_disposition="replace",
    max_table_nesting=0,
)
def events():
    yield load_bootstrap_event("events")


# Define a resource for the second key
@dlt.resource(
    # primary_key="id",
    table_name="phases",
    write_disposition="replace",
    max_table_nesting=0,
)
def phases():
    yield load_bootstrap_event("phases")


# create resources for [teams, total_players, elements, element_stats, element_types]
@dlt.resource(
    # primary_key="id",
    table_name="teams",
    write_disposition="replace",
    max_table_nesting=0,
)
def teams():
    yield load_bootstrap_event("teams")


@dlt.resource(
    # primary_key="id",
    table_name="total_players",
    write_disposition="replace",
    max_table_nesting=0,
)
def total_players():
    yield load_bootstrap_event("total_players")


@dlt.resource(
    # primary_key="id",
    table_name="elements",
    write_disposition="replace",
    max_table_nesting=0,
)
def elements():
    yield load_bootstrap_event("elements")


@dlt.resource(
    # primary_key="id",
    table_name="element_stats",
    write_disposition="replace",
    max_table_nesting=0,
)
def element_stats():
    yield load_bootstrap_event("element_stats")


@dlt.resource(
    # primary_key="id",
    table_name="element_types",
    write_disposition="replace",
    max_table_nesting=0,
)
def element_types():
    yield load_bootstrap_event("element_types")


# Create a pipeline and run it
pipeline = dlt.pipeline(
    pipeline_name="fpl",
    destination="duckdb",
    dataset_name="fpl_data",
)

@dlt.resource(
    # primary_key="id",
    table_name="standings",
    write_disposition="replace",
    max_table_nesting=0,
)
def standings():
    response = fpl_client.get(bootstrap_url)
    response.raise_for_status() 

load_info = pipeline.run(
    [
        events(),
        phases(),
        teams(),
        total_players(),
        elements(),
        element_stats(),
        element_types(),
    ]
)
print(load_info)  # noqa: T201


# @dlt.resource(table_name=lambda event: event["events"])
# def load_events():
