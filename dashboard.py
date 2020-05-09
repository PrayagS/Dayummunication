#!/usr/bin/env python3


import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input, Output, State

import QPSK

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


def dashboard() -> dash.Dash:
    """Loading the model and application"""

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    # msg = np.array(
    #     [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0]
    # )  # 8PSK demo signal
    # msg = np.array([0, 1, 0, 0, 1, 1, 0, 1, 1, 0])  # QPSK demo signal
    # msg = np.random.randint(low=0, high=2, size=int(1e3))
    # M = 8
    # k = int(np.log2(M))
    t_csd = np.linspace(0.0, 2.0 * np.math.pi, 100)
    f_c = 100.0
    t_c = 1.0 / f_c

    # Sampling rate
    f_s = 10000.0
    t_s = 1.0 / f_s

    # MPSK Parameters
    Tb = 0.01
    Eb = 0.001

    app.layout = html.Div(
        children=[
            html.H1(children="Title", style={
                    "textAlign": "center", "margin": 20}),
            html.Div(
                id="input",
                children=[
                    html.H2(
                        children="Input",
                        style={"marginBottom": 0, "textAlign": "left"},
                    ),
                    dcc.Input(id="input-str", value="0", type="text"),
                    html.Button(
                        id="submit-button-state", n_clicks=0, children="Submit"
                    ),
                ],
            ),
            dcc.Graph(id="signal"),
            dcc.Graph(id="modulated-signal"),
            dcc.Graph(id="modulated-signal-with-noise"),
            dcc.Graph(id="demodulated-signal")
        ]
    )

    @app.callback(
        [Output("signal", "figure"), Output("modulated-signal", "figure"),
         Output("modulated-signal-with-noise", "figure"), Output("demodulated-signal", "figure")],
        [Input("submit-button-state", "n_clicks")],
        [State("input-str", "value")],
    )
    def conv(n_clicks: int, input_str: str) -> None:
        if n_clicks >= 0:
            chars = []
            for i in input_str:
                b = bin(ord(i))[2:]
                b = "0" + b if len(b) == 7 else "00" + b
                chars.append(b)

            chars = [int(i) for i in list("".join(chars))]

            symbols, mod_signal = QPSK.modulate(chars)
            t_sym, signal = QPSK.plot_signal(mod_signal, symbols)
            mod_signal_with_noise, N0 = QPSK.add_noise(mod_signal)
            demod_chars = QPSK.demodulate(mod_signal_with_noise)
            return (
                {
                    "data": [dict(x=list(range(len(chars))), y=chars)],
                    "layout": {
                        "display": "block",
                        "margin-left": "auto",
                        "margin-right": "auto",
                    },
                },
                {
                    "data": [dict(x=t_sym, y=signal)],
                    "layout": {
                        "display": "block",
                        "margin-left": "auto",
                        "margin-right": "auto",
                    },
                },
                {
                    "data": [dict(x=t_sym, y=mod_signal_with_noise)],
                    "layout": {
                        "display": "block",
                        "margin-left": "auto",
                        "margin-right": "auto",
                    },
                },
                {
                    "data": [dict(x=list(range(len(demod_chars))), y=demod_chars)],
                    "layout": {
                        "display": "block",
                        "margin-left": "auto",
                        "margin-right": "auto",
                    },
                }
            )

    return app


if __name__ == "__main__":
    dashboard().run_server(debug=True)
