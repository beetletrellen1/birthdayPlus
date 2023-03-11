import random

from dash import Dash, dcc, html, ctx
from dash.dependencies import Input, Output

from Birthday import Birthday

NUM_PEOPLE = 23
MIN_NUM_PEOPLE = 2
MAX_NUM_PEOPLE = 30
ks = range(MIN_NUM_PEOPLE, MAX_NUM_PEOPLE + 1)
NUM_POSSIBLE_BIRTHDAYS = 365
NUM_TRIALS = 1000

app = Dash(__name__)

app.layout = html.Div([
        html.H1(children="Birthday Plus Problem"),
        html.H2(children="ISYE 6644"),
        html.H2(children="Authors: Stacey Helcher, Brian Collins"),
        dcc.Input(id="input_seed", 
                    type="number", 
                    placeholder="Add Seed Value", 
                    style={'marginRight':'10px'}),
        dcc.Input(id="num-share-bday", 
                    type="number", 
                    placeholder="Number Shared Birthdays", 
                    style={'marginRight':'20px'}),
        html.Div(id="seed_output"),
        html.Button('Run', id='run-button', n_clicks=0),
        html.Div(id='container-button-timestamp')
        ]
)


@app.callback(
    Output("seed_output", "children"),
    inputs = [Input("input_seed", "value"),
              Input("num-share-bday", "value")],
)
def update_output(input_seed, n_shared):
    return u'Random Seed Set: {}'.format(input_seed)

@app.callback(
    Output('container-button-timestamp', 'children'),
    Input('run-button', 'n_clicks'),
    Input('input_seed', 'value'),
    Input('num-share-bday', 'value')
)
def run(run_button, seed, n_share_bday):
    msg = "None of the buttons have been clicked yet"
    if n_share_bday == None:
        n_share_bday = 2
    if "run-button" == ctx.triggered_id:
        bday = Birthday(seed, NUM_TRIALS, MIN_NUM_PEOPLE, MAX_NUM_PEOPLE, n_share_bday)
        p_coincidence = bday.estimate_p_coincidence()
        msg = f"""
                Probability {n_share_bday} people sharing a birthday 
                from a of pool of {MAX_NUM_PEOPLE} is {p_coincidence}
               """
    return html.Div(msg)

if __name__ == "__main__":
    app.run_server(debug=True)