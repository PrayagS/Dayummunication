#!/usr/bin/env python3


import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

import BPSK
import BFSK
import QPSK
import QFSK
import MPSK
import channel

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
            html.H1(children="Dayummunication", style={
                    "textAlign": "center", "margin": 10}),
            html.H5(children="Making digital communications look dayumm!", style={
                    "textAlign": "center", "margin": 10}),
            html.Hr(),
            html.Div(
                id="modulation-type",
                children=[
                    html.H2(
                        children="Modulation Scheme",
                        style={"margin": 5, "textAlign": "left"},
                    ),
                    dcc.Dropdown(
                        id="modulation-scheme",
                        options=[
                            {"label": "Binary Phase Shift Keying (BPSK)",
                             "value": "BPSK"},
                            {"label": "Binary Frequency Shift Keying (BFSK)",
                             "value": "BFSK"},
                            {"label": "Quadrature Phase Shift Keying (QPSK)",
                             "value": "QPSK"},
                            {"label": "Quadrature Frequency Shift Keying (QFSK)",
                             "value": "QFSK"},
                            {"label": "M'ary Phase Shift Keying (MPSK)",
                             "value": "MPSK"},
                        ],
                        placeholder="For eg. BPSK",
                        value="BPSK",
                        style={
                            "margin": 5
                        }
                    ),
                ]
            ),
            html.Div(
                id="modulation-params",
                children=[
                    html.Label("Energy of the signal"),
                    dcc.Input(
                        id="energy",
                        value=0.001,
                        type="number",
                        style={
                            "margin": 5
                        }),
                    html.Label("Bit time"),
                    dcc.Input(
                        id="bit-time",
                        value=0.01,
                        type="number",
                        style={
                            "margin": 5
                        }),
                    html.Label("Carrier Frequency"),
                    dcc.Input(
                        id="carrier-frequency",
                        value=100,
                        type="number",
                        style={
                            "margin": 5
                        }),
                    html.Label("Sampling Frequency"),
                    dcc.Input(
                        id="sampling-frequency",
                        value=10000,
                        type="number",
                        style={
                            "margin": 5
                        }),
                    html.Label("Noise Energy"),
                    dcc.Input(
                        id="noise-energy",
                        value=0.000004,
                        type="number",
                        style={
                            "margin": 5
                        }),
                ],
                style={
                    "columnCount": 3
                }
            ),
            html.Div(
                id="input",
                children=[
                    html.H2(
                        children="Input Signal",
                        style={"margin": 5, "textAlign": "left"},
                    ),
                    dcc.Input(
                        id="input-str",
                        value="0",
                        type="text",
                        style={
                            "margin": 5
                        }),
                    html.Button(
                        id="submit-button-state", n_clicks=0, children="Submit",
                        style={
                            "margin": 5
                        },
                    ),
                ],
            ),
            dcc.Graph(id="signal"),
            dcc.Graph(id="modulated-signal"),
            dcc.Graph(id="noise-signal"),
            dcc.Graph(id="signal-plus-noise"),
            dcc.Graph(id="demodulated-signal"),
        ]
    )

    @app.callback(
        [
            Output("signal", "figure"),
            Output("modulated-signal", "figure"),
            Output("noise-signal", "figure"),
            Output("signal-plus-noise", "figure"),
            Output("demodulated-signal", "figure"),
        ],
        [
            Input("submit-button-state", "n_clicks"),
            Input("modulation-scheme", "value"),
            Input("energy", "value"),
            Input("bit-time", "value"),
            Input("carrier-frequency", "value"),
            Input("sampling-frequency", "value"),
            Input("noise-energy", "value"),
        ],
        [State("input-str", "value")],
    )
    def conv(n_clicks: int,
             modulation_scheme: str, Eb: int, Tb: int, f_c: int, f_s: int, N0: str,
             input_str: str) -> None:
        if n_clicks >= 0:

            chars = []
            for i in input_str:
                b = bin(ord(i))[2:]
                b = "0" + b if len(b) == 7 else "00" + b
                chars.append(b)

            chars = [int(i) for i in list("".join(chars))]
            modulated_signal = None
            noise_signal = None
            signal_plus_noise = None
            demodulated_signal = None
            t = None

            if modulation_scheme == "BPSK":
                modulated_signal = BPSK.modulate(chars, Eb, Tb, f_c, f_s)
                noise_signal = channel.generate_noise(
                    modulated_signal, N0, f_s)
                signal_plus_noise = modulated_signal + noise_signal
                demodulated_signal = BPSK.demodulate(
                    signal_plus_noise, Tb, f_c, f_s)
                t = np.linspace(0, len(chars) * Tb, int(len(chars) * Tb * f_s))

            if modulation_scheme == "BFSK":
                modulated_signal = BFSK.modulate(chars, Eb, Tb, f_c, f_s)
                noise_signal = channel.generate_noise(
                    modulated_signal, N0, f_s)
                signal_plus_noise = modulated_signal + noise_signal
                demodulated_signal = BFSK.demodulate(
                    signal_plus_noise, Tb, f_c, f_s)
                t = np.linspace(0, len(chars) * Tb, int(len(chars) * Tb * f_s))

            if modulation_scheme == "QPSK":
                modulated_signal = QPSK.modulate(chars, Eb, Tb, f_c, f_s)
                noise_signal = channel.generate_noise(
                    modulated_signal, N0, f_s)
                signal_plus_noise = modulated_signal + noise_signal
                demodulated_signal = QPSK.demodulate(
                    signal_plus_noise, Tb, f_c, f_s)
                symbols = np.array([chars[0::2], chars[1::2]])
                t = np.linspace(
                    0, np.size(symbols, axis=1) *
                    Tb, int(np.size(symbols, axis=1) * Tb * f_s)
                )

            if modulation_scheme == "QFSK":
                modulated_signal = QFSK.modulate(chars, Eb, Tb, f_c, f_s)
                noise_signal = channel.generate_noise(
                    modulated_signal, N0, f_s)
                signal_plus_noise = modulated_signal + noise_signal
                demodulated_signal = QFSK.demodulate(
                    signal_plus_noise, Tb, f_c, f_s)
                t = np.linspace(0, len(chars) * Tb, int(len(chars) * Tb * f_s))

            binary_signal_figure = go.Figure()
            binary_signal_figure.add_trace(go.Scatter(x=list(range(len(chars))), y=chars,
                                                      mode="lines+markers"))
            binary_signal_figure.update_layout(title="Binary Signal")

            modulated_signal_figure = go.Figure()
            modulated_signal_figure.add_trace(
                go.Scatter(x=t, y=modulated_signal))
            modulated_signal_figure.update_layout(title="Modulated Signal")

            noise_signal_figure = go.Figure()
            noise_signal_figure.add_trace(go.Scatter(x=t, y=noise_signal))
            noise_signal_figure.update_layout(title="Noise Signal")

            signal_plus_noise_figure = go.Figure()
            signal_plus_noise_figure.add_trace(
                go.Scatter(x=t, y=signal_plus_noise))
            signal_plus_noise_figure.update_layout(
                title="Modulated Signal + Noise Signal")

            demodulated_signal_figure = go.Figure()
            demodulated_signal_figure.add_trace(
                go.Scatter(x=t, y=demodulated_signal))
            demodulated_signal_figure.update_layout(title="Demodulated Signal")

            return (
                binary_signal_figure,
                modulated_signal_figure,
                noise_signal_figure,
                signal_plus_noise_figure,
                demodulated_signal_figure
            )

    return app


if __name__ == "__main__":
    dashboard().run_server(debug=True)
