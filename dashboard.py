#!/usr/bin/env python3

import base64

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input, Output

import MPSK

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


def dashboard() -> dash.Dash:
    """Loading the model and application"""

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    msg = np.array(
        [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0]
    )  # 8PSK demo signal
    # msg = np.array([0, 1, 0, 0, 1, 1, 0, 1, 1, 0])  # QPSK demo signal
    # msg = np.random.randint(low=0, high=2, size=int(1e3))
    M = 8
    k = int(np.log2(M))

    x = MPSK.modulate(msg, k, M)

    app.layout = html.Div(
        children=[
            html.H1(children="Title", style={"textAlign": "center", "margin": 20}),
            html.Div(
                id="input",
                children=[
                    html.H2(
                        children="Input",
                        style={"marginBottom": 0, "textAlign": "left"},
                    ),
                    dcc.Input(id="input-str", value="0", type="text"),
                ],
            ),
            html.Div(
                id="output",
                children=[
                    html.H2(
                        children="Bit Array",
                        style={"marginBottom": 0, "textAlign": "left"},
                    ),
                    dcc.Input(id="output-str", value="0", type="text"),
                ],
            ),
            dcc.Graph(id="QPSK", figure={"data": [{"x": x[0], "y": x[0]}]}),
        ]
    )

    @app.callback(Output("output-str", "value"), [Input("input-str", "value")])
    def conv(input_str: str) -> None:
        return "".join(format(ord(i), "b") for i in input_str)

    return app


if __name__ == "__main__":
    dashboard().run_server(debug=True)
