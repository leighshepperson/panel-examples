from typing import Any, Callable

import panel as pn
import pandas as pd
import param
from param import Parameterized, Selector
import plotly.express as px

# Application is following class based design suitable for large projects
# https://panel.holoviz.org/explanation/api/examples/outliers_declarative.html

df = pd.read_csv(
    r"C:\Users\pmp07\code\panel-examples\assets\DP_LIVE_15102023130525039.csv"
)
df = df[["LOCATION", "TIME", "Value"]]
locations = ["ALL"] + df["LOCATION"].values.tolist()
times = df["TIME"].values.tolist()
sub_regions = {
    'ALL': locations,
    'EUROPE': ['ALL', 'GBR', 'FIN', 'FRA', 'ITA'],
    "ASIA": ['ALL', 'JPN']
}


def view_tabulator(df: pd.DataFrame) -> Any:
    return pn.widgets.Tabulator(df, pagination="remote", page_size=10)


def view_scatter_plot(df: pd.DataFrame):
    fig = px.bar(df, x="LOCATION", y="Value")
    return pn.pane.Plotly(fig)


def view_pie_chart(df: pd.DataFrame):
    fig = px.pie(df, names="LOCATION", values="Value")
    return pn.pane.Plotly(fig)


# https://panel.holoviz.org/how_to/profiling/profile.html
@pn.io.profile("clustering", engine="snakeviz")
def compute_net_worth_aggregate(
        location: str,
        region: str,
        aggregator: str,
        view_fn: Callable[[pd.DataFrame], Any] = view_tabulator,
) -> Any:
    possible_locations = sub_regions.get(region)
    df_location = df[df['LOCATION'].isin(possible_locations)]
    df_location = df_location if location == "ALL" else df_location[df_location["LOCATION"] == location]
    df_location = df_location.groupby("LOCATION")[["Value"]].aggregate(aggregator).reset_index()
    return view_fn(df_location)


class Example(Parameterized):
    region = Selector(default="ALL", objects=["ALL", "EUROPE", "ASIA"])
    location = Selector(default="ALL", objects=list(locations))
    aggregator = Selector(default="sum", objects=["sum", "max", "min", "mean", "median"])

    view_fn = Selector(
        default=view_tabulator,
        objects=[view_tabulator, view_scatter_plot, view_pie_chart],
    )

    @param.depends("region", watch=True)
    def _filter_regions(self):
        new_locations = sub_regions.get(self.region, locations)
        self.param['location'].objects = new_locations
        self.location = new_locations[0]
        self.param.trigger('location')

    @param.depends("location", "aggregator", "view_fn")
    def view(self):
        return compute_net_worth_aggregate(self.location, self.region, self.aggregator, self.view_fn)


if pn.state.served:
    pn.extension(sizing_mode="stretch_width")
    pn.extension("tabulator")
    pn.extension('plotly')
    example = Example()

    example_param = pn.Param(
        example.param,
        widgets={
            "location": {
                "widget_type": pn.widgets.RadioButtonGroup,
                "button_type": "success",
            }
        },
        name="Net Worth",
    )

    pn.Column(example_param, example.view).servable()
