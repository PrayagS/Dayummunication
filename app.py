#!/usr/bin/env python3

from typing import Tuple

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots

import BFSK
import BPSK
import channel
import Coding
import MPSK
import QFSK
import QPSK

external_stylesheets = [dbc.themes.BOOTSTRAP,
                        "https://codepen.io/chriddyp/pen/bWLwgP.css"]
colors = {"background": "#0e0e0e", "text": "#4ecca3", "options": "#fc7e2f"}

palatte = {
    "A": "#101010",
    "B": "#33415c",
    "C": "#5c677d",
    "D": "#7d8597",
    "E": "#f4f4f4",
    "F": "#2f2f2f",
}
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)


server = app.server


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
    style={"backgroundColor": colors["background"]},
    children=[
        dbc.Container(
            [
                html.H1(
                    children="Dayummunication",
                    style={"textAlign": "center",
                           "mt": 10, "mb": 10, "color": colors["text"]},
                ),
                html.H5(
                    children="Making digital communications look dayumm!",
                    style={"textAlign": "center",
                           "mt": 10, "mb": 10, "color": colors["text"]},
                ),
                html.Hr(),
                html.Div(
                    id="modulation-type",
                    children=[
                        html.H2(
                            children="Modulation Scheme",
                            style={"mt": 10, "mb": 10, "textAlign": "left",
                                   "color": colors["text"], },
                        ),
                        dcc.Dropdown(
                            id="modulation-scheme",
                            options=[
                                {"label": "Binary Phase Shift Keying (BPSK)",
                                 "value": "BPSK", },
                                {
                                    "label": "Binary Frequency Shift Keying (BFSK)",
                                    "value": "BFSK",
                                },
                                {
                                    "label": "Quadrature Phase Shift Keying (QPSK)",
                                    "value": "QPSK",
                                },
                                {
                                    "label": "Quadrature Frequency Shift Keying (QFSK)",
                                    "value": "QFSK",
                                },
                                # {
                                #     "label": "M'ary Phase Shift Keying (MPSK)",
                                #     "value": "MPSK",
                                # },
                            ],
                            placeholder="For eg. BPSK",
                            value="BPSK",
                            style={"mt": 10, "mb": 10, "color": "white"},
                        ),
                    ],
                ),

            ], fluid=True
        ),
        dbc.Container(
            id="modulation-params",
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(children=[
                            html.Label("Energy of the signal", style={
                                "color": colors["options"]}),
                            dcc.Input(
                                id="energy",
                                value=0.001,
                                type="number",
                                style={"color": "white"},
                                min=0.001,
                                max=10,
                            ),
                        ], sm=6, md=4, lg=3
                        ),
                        dbc.Col([html.Label("Bit time", style={"color": colors["options"]}),
                                 dcc.Input(
                            id="bit-time",
                            value=0.01,
                            type="number",
                            style={"color": "white"},
                            min=0.001,
                            max=5,
                        ),
                        ], sm=6, md=4, lg=3
                        ),
                        dbc.Col([html.Label("Carrier Frequency", style={
                            "color": colors["options"]}),
                            dcc.Input(
                            id="carrier-frequency",
                            value=100,
                            type="number",
                            style={"color": "white"},
                            min=10,
                            max=500,
                        ),
                        ], sm=6, md=4, lg=3
                        ),
                        dbc.Col([html.Label("Sampling Frequency", style={
                            "color": colors["options"]}),
                            dcc.Input(
                            id="sampling-frequency",
                            value=10000,
                            type="number",
                            style={"color": "white"},
                            min=1000,
                            max=20000,
                        ),
                        ], sm=6, md=4, lg=3
                        ),
                        dbc.Col([html.Label("Noise Energy", style={"color": colors["options"]}),
                                 dcc.Input(
                            id="noise-energy",
                            value=0.000004,
                            type="number",
                            style={"color": "white"},
                            min=0.00000000000000000001,
                            max=10,
                        ),
                        ], sm=6, md=4, lg=3
                        ),
                    ]
                ),
                # dbc.Row(
                #     children=[
                #     ],
                # ),
            ], fluid=True
            # style={"columnCount": 3},
        ),
        dbc.Container([
            html.Div(
                id="input",
                className="align-middle",
                children=[
                    html.H2(
                        children="Input Signal",
                        style={"mt": 10, "mb": 10, "textAlign": "left",
                               "color": colors["text"], },
                    ),
                    dcc.Input(
                        id="input-str",
                        value="0",
                        type="text",
                        style={"mt": 10, "mb": 10, "color": "white"},
                    ),
                    html.Button(
                        id="submit-button-state",
                        n_clicks=0,
                        children="Submit",
                        style={"mt": 10, "mb": 10, "color": "white",
                               "pb": 5},
                    ),
                    dcc.Checklist(
                        id="coding-flag",
                        options=[
                            {"label": "Encode", "value": "True"},
                        ],
                        labelStyle={
                            "font-size": 16
                        },
                        style={
                            "margin-left": 5
                        },
                    )
                ],
            ),
            html.Hr(),
            dcc.Graph(id="signal",),
            dcc.Graph(id="modulated-signal"),
            dbc.Row(children=[
                dbc.Col(dcc.Graph(id="noise"), md=12, lg=6),
                dbc.Col(dcc.Graph(id="noise-signal"),
                        md=12, lg=6),
            ]),
            dcc.Graph(id="demodulated-signal"),
        ], fluid=True
        ),
    ],
)


@app.callback(
    [
        Output("signal", "figure"),
        Output("modulated-signal", "figure"),
        Output("noise", "figure"),
        Output("noise-signal", "figure"),
        Output("demodulated-signal", "figure"),
    ],
    [
        Input("submit-button-state", "n_clicks"),
        Input("coding-flag", "value"),
        Input("modulation-scheme", "value"),
        Input("energy", "value"),
        Input("bit-time", "value"),
        Input("carrier-frequency", "value"),
        Input("sampling-frequency", "value"),
        Input("noise-energy", "value"),
    ],
    [State("input-str", "value")],
)
def conv(
    n_clicks: int,
    coding_flag: str,
    modulation_scheme: str,
    Eb: int,
    Tb: int,
    f_c: int,
    f_s: int,
    N0: str,
    input_str: str,
) -> tuple:
    if n_clicks >= 0:

        chars = []
        for i in input_str:
            b = bin(ord(i))[2:]
            b = "0" + b if len(b) == 7 else "00" + b
            chars.append(b)

        chars = [int(i) for i in list("".join(chars))]
        try:
            if coding_flag[0] == "True":
                chars = Coding.encodebits(chars)
        except (TypeError, IndexError):
            pass
        modulated_signal = None
        noise_signal = None
        signal_plus_noise = None
        demodulated_signal = None
        t = None

        try:
            if coding_flag[0] == "True":
                chars = Coding.encodebits(chars)
        except (TypeError, IndexError):
            pass

        if modulation_scheme == "BPSK":
            modulated_signal = BPSK.modulate(chars, Eb, Tb, f_c, f_s)
            noise_signal = channel.generate_noise(modulated_signal, N0, f_s)
            signal_plus_noise = modulated_signal + noise_signal
            demodulated_signal = BPSK.demodulate(
                signal_plus_noise, Tb, f_c, f_s)
            t = np.linspace(0, len(chars) * Tb, int(len(chars) * Tb * f_s))

        if modulation_scheme == "BFSK":
            modulated_signal = BFSK.modulate(chars, Eb, Tb, f_c, f_s)
            noise_signal = channel.generate_noise(modulated_signal, N0, f_s)
            signal_plus_noise = modulated_signal + noise_signal
            demodulated_signal = BFSK.demodulate(
                signal_plus_noise, Tb, f_c, f_s)
            t = np.linspace(0, len(chars) * Tb, int(len(chars) * Tb * f_s))

        if modulation_scheme == "QPSK":
            modulated_signal = QPSK.modulate(chars, Eb, Tb, f_c, f_s)
            noise_signal = channel.generate_noise(modulated_signal, N0, f_s)
            signal_plus_noise = modulated_signal + noise_signal
            demodulated_signal = QPSK.demodulate(
                signal_plus_noise, Tb, f_c, f_s)
            symbols = np.array([chars[0::2], chars[1::2]])
            t = np.linspace(
                0,
                np.size(symbols, axis=1) * Tb,
                int(np.size(symbols, axis=1) * Tb * f_s),
            )

        if modulation_scheme == "QFSK":
            modulated_signal = QFSK.modulate(chars, Eb, Tb, f_c, f_s)
            noise_signal = channel.generate_noise(modulated_signal, N0, f_s)
            signal_plus_noise = modulated_signal + noise_signal
            demodulated_signal = QFSK.demodulate(
                signal_plus_noise, Tb, f_c, f_s)
            t = np.linspace(0, len(chars) * Tb, int(len(chars) * Tb * f_s))

        try:
            if coding_flag[0] == "True":
                demodulated_signal = Coding.decodebits(demodulated_signal)
        except (TypeError, IndexError):
            pass

        binary_signal_figure = go.Figure()
        binary_signal_figure.add_trace(
            go.Scatter(
                x=list(range(len(chars))),
                y=chars,
                mode="lines+markers",
                marker=dict(color="#4ecca3"),
            )
        )
        binary_signal_figure.update_layout(
            title="Binary Signal",
            paper_bgcolor=palatte["A"],
            font=dict(color=palatte["E"], size=14),
            template="plotly_dark",
        )

        modulated_signal_figure = go.Figure()
        modulated_signal_figure.add_trace(
            go.Scatter(x=t, y=modulated_signal, marker=dict(color="#fc7e2f")),
        )
        modulated_signal_figure.update_layout(
            title="Modulated Signal",
            paper_bgcolor=palatte["A"],
            font=dict(color=palatte["E"], size=14),
            template="plotly_dark",
        )

        noise_figure = go.Figure()
        noise_figure.add_trace(
            go.Scatter(x=t, y=noise_signal, marker=dict(color="#4ecca3")),
        )
        noise_figure.update_layout(
            title="Noise Signal",
            paper_bgcolor=palatte["A"],
            font=dict(color=palatte["E"], size=14),
            template="plotly_dark",
        )

        noise_signal_figure = go.Figure()
        noise_signal_figure.add_trace(
            go.Scatter(x=t, y=signal_plus_noise, marker=dict(color="#fc7e2f")),
        )

        # noise_signal_figure = make_subplots(rows=1, cols=2)
        # noise_signal_figure.add_trace(
        #     go.Scatter(x=t, y=noise_signal, marker=dict(color="#4ecca3")), row=1, col=1,
        # )
        # noise_signal_figure.add_trace(
        #     go.Scatter(x=t, y=signal_plus_noise, marker=dict(color="#fc7e2f")), row=1, col=2,
        # )
        noise_signal_figure.update_layout(
            title="Modulation Signal + Noise Signal",
            paper_bgcolor=palatte["A"],
            font=dict(color=palatte["E"], size=14),
            template="plotly_dark",
        )

        demodulated_signal_figure = go.Figure()
        demodulated_signal_figure.add_trace(
            go.Scatter(x=t, y=demodulated_signal,
                       marker=dict(color="#4ecca3")),
        )
        demodulated_signal_figure.update_layout(
            title="Demodulated Signal",
            paper_bgcolor=palatte["A"],
            font=dict(color=palatte["E"], size=14),
            template="plotly_dark",
        )

        return (
            binary_signal_figure,
            modulated_signal_figure,
            noise_figure,
            noise_signal_figure,
            demodulated_signal_figure,
        )


if __name__ == "__main__":
    app.run_server(debug=True)
