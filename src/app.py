from typing import Any, Callable

import panel as pn
import pandas as pd
from param import Parameterized, Selector

# Application is following class based design suitable for large projects
# https://panel.holoviz.org/explanation/api/examples/outliers_declarative.html

df = pd.read_csv(
    r"C:\Users\pmp07\code\panel-examples\assets\DP_LIVE_15102023130525039.csv"
)
df = df[["LOCATION", "TIME", "Value"]]
locations = ["ALL"] + df["LOCATION"].values.tolist()
times = df["TIME"].values.tolist()


def view_average_net_worth_tabulator(df: pd.DataFrame) -> Any:
    return pn.widgets.Tabulator(df, pagination="remote", page_size=10)


def view_average_net_worth_df(df: pd.DataFrame):
    return pn.widgets.DataFrame(df, name="Average Net Worth")


# https://panel.holoviz.org/how_to/profiling/profile.html
@pn.io.profile("clustering", engine="snakeviz")
def compute_average_networth(
    location: str,
    view_fn: Callable[[pd.DataFrame], Any] = view_average_net_worth_tabulator,
) -> Any:
    df_location = df if location == "ALL" else df[df["LOCATION"] == location]
    df_location = df_location.groupby("LOCATION")[["Value"]].sum().reset_index()
    return view_fn(df_location)


class Example(Parameterized):
    select_location = Selector(default="ALL", objects=list(locations))
    view_fn = Selector(
        default=view_average_net_worth_tabulator,
        objects=[view_average_net_worth_tabulator, view_average_net_worth_df],
    )

    def view(self):
        return compute_average_networth(self.select_location, self.view_fn)


if pn.state.served:
    pn.extension("tabulator")
    example = Example()

    example_param = pn.Param(
        example.param,
        widgets={
            "select_location": {
                "widget_type": pn.widgets.RadioButtonGroup,
                "button_type": "success",
            }
        },
        name="Average Net Worth",
    )

    pn.Column(example_param, example.view).servable()
