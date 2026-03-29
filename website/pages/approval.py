import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
from figures import black_approval_chart, white_approval_chart

dash.register_page(__name__, path='/', name='Approval Ratings')

df = pd.read_csv('Data/approvals_test_data.csv',
    parse_dates=['end_date'],
    dtype={'yes': float, 'no': float}
)

dark_chart = black_approval_chart(df)
light_chart = white_approval_chart(df)

layout = html.Div(className='page-content', children=[
    html.Div(className='chart-card', children=[
        html.H2('Presidential Approval Ratings', className='chart-title'),
        html.P('Smoothed polling average • Updated daily', className='chart-subtitle'),
        html.Button('Switch Theme', id='toggle-btn', n_clicks=0, className='toggle-btn'),
        dcc.Graph(id='approval-chart', style={'height': '550px'}),
    ])
])

@callback(
    Output('approval-chart', 'figure'),
    Input('toggle-btn', 'n_clicks')
)
def toggle_theme(n_clicks):
    if n_clicks % 2 == 0:
        return light_chart
    else:
        return dark_chart