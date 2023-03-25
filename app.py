import random
import numpy as np

from dash import Dash, dcc, html, ctx
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px

from Birthday import Birthday, WeightedBirthdays

NUM_PEOPLE = 23
MIN_NUM_PEOPLE = 2
MAX_NUM_PEOPLE = 30
ks = range(MIN_NUM_PEOPLE, MAX_NUM_PEOPLE + 1)
NUM_POSSIBLE_BIRTHDAYS = 365
NUM_TRIALS = 100

app = Dash(__name__)

app.layout = html.Div([
        html.H1(children="Birthday Plus Problem"),
        html.H2(children="ISYE 6644"),
        html.H2(children="Authors: Stacey Helcher, Brian Collins"),
        html.Br(),
        dcc.Input(id="input_seed", 
                    type="number", 
                    placeholder="Add Seed Value", 
                    style={'marginRight':'10px'}),
        dcc.Input(id="num-share-bday", 
                    type="number", 
                    placeholder="Number Shared Birthdays", 
                    style={'marginRight':'20px'}),
        dcc.Input(id="num-people",
                    type="number",
                    placeholder="Number of People",
                    style={'marginRight':'20px'}),
        html.Br(),
        html.Div(id="seed_output"),
        html.Div(id="shared-bday"),
        html.Div(id="num-people-output"),
        html.Br(),
        html.Button('Run', id='run-button', n_clicks=0),
        html.Div(id='container-button-timestamp'),
        dcc.Graph(id='graph'),
        html.Br(),
        html.Br(),
        html.Button('Run Weights', id='run-weights-button', n_clicks=0),
        html.Div(id='container-button'),
        dcc.Graph(id='bday-heatmap'),
        dcc.Graph(id='graph-weights')
        ]
)


@app.callback(
    Output("seed_output", "children"),
    Input("input_seed", "value"),
)
def update_output(input_seed):
    return u'''Random Seed Set: {}'''.format(input_seed)
@app.callback(
    Output("shared-bday", "children"),
    Input("num-share-bday", "value"),
)
def update_output(n_shared):
    return u'''The Number of People to share a birthday: {}'''.format(n_shared)

@app.callback(
    Output("num-people-output", "children"),
    Input("num-people", "value"),
)
def update_output(num_people):
    return u'''Number of Participants {}'''.format(num_people)

@app.callback(
    Output('container-button-timestamp', 'children'),
    Output('graph', 'figure'),
    Input('run-button', 'n_clicks'),
    Input('input_seed', 'value'),
    Input('num-share-bday', 'value'),
    Input('num-people', 'value')
)
def run(run_button, seed, n_share_bday, num_people):
    msg = "None of the buttons have been clicked yet"
    fig = go.Figure()
    if n_share_bday == None:
        n_share_bday = 2
    if "run-button" == ctx.triggered_id:
        bday = Birthday(seed, NUM_TRIALS, MIN_NUM_PEOPLE, num_people, n_share_bday)
        np.random.seed(bday.seed)
        for idx, _ in enumerate(range(bday.num_trials)):
            bday.estimate_p_coincidence(idx=idx)
            bday.trial_list.append(idx)
            p_coincidence = bday.probability[-1]
        fig = px.scatter(x=bday.trial_list, y=bday.probability, 
                            labels={"x": "Trial Number", "y": "Probability"},
                            title=f'Probability of Shared Birthday with {NUM_TRIALS} trials')
            
        msg = f"""
                Probability {n_share_bday} people sharing a birthday 
                from a of pool of {num_people} is {p_coincidence}
               """
    return html.Div(msg), fig


@app.callback(
    Output('container-button', 'children'),
    Output('bday-heatmap', 'figure'),
    Output('graph-weights', 'figure'),
    Input('run-weights-button', 'n_clicks'),
    Input('input_seed', 'value'),
    Input('num-share-bday', 'value'),
    Input('num-people', 'value')
)
def run(run_button, seed, n_share_bday, num_people):
    msg = "None of the buttons have been clicked yet"
    fig_heatmap = go.Figure()
    fig_weights = go.Figure()
    if n_share_bday == None:
        n_share_bday = 2
    if "run-weights-button" == ctx.triggered_id:
        bday = WeightedBirthdays(seed, NUM_TRIALS, MIN_NUM_PEOPLE, num_people, n_share_bday)
        bday.create_df()
        bday.group_bday_by_day()
        bday.create_bday_weight()
        fig_heatmap = bday.create_heat_map()
        np.random.seed(bday.seed)
        for idx, _ in enumerate(range(bday.num_trials)):
            bday.estimate_p_coincidence(idx=idx)
            bday.trial_list.append(idx)
            p_coincidence = bday.probability[-1]
        fig_weights = px.scatter(x=bday.trial_list, y=bday.probability, 
                            labels={"x": "Trial Number", "y": "Probability"},
                            title=f'Probability of Shared Birthday with {NUM_TRIALS} trials')
            
        msg = f"""
                Probability {n_share_bday} people sharing a birthday 
                from a of pool of {num_people} is {p_coincidence}
               """
    return html.Div(msg), fig_heatmap, fig_weights


if __name__ == "__main__":
    app.run_server(debug=True)