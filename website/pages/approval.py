import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
from figures import approval_chart

dash.register_page(__name__, path='/', name='Approval Ratings')

df = pd.read_csv('Data/approvals_test_data.csv',
    parse_dates=['end_date'],
    dtype={'yes': float, 'no': float}
)

layout = html.Div(className='page-content', children=[
    html.Div(className='chart-card', children=[
        html.H2('Presidential Approval Ratings', className='chart-title'),
        html.P('Smoothed polling average • Updated daily', className='chart-subtitle'),
        html.Div(className='controls', children=[
            dcc.Checklist(
                id='line-toggle',
                options=[
                    {'label': 'Approve', 'value': 'approve'},
                    {'label': 'Disapprove', 'value': 'disapprove'},
                    {'label': 'Net Approval', 'value': 'net'},
                ],
                value=['approve', 'disapprove'],
                inline=True
            ),
            html.Button('☀️ Switch Theme', id='toggle-btn', n_clicks=0, className='toggle-btn'),
        ]),
        dcc.Graph(id='approval-chart', style={'height': '700px'}),
    ])
])

@callback(
    Output('approval-chart', 'figure'),
    Output('toggle-btn', 'children'),  
    Input('toggle-btn', 'n_clicks'),
    Input('line-toggle', 'value')
)
def update_chart(n_clicks, selected_lines): 
    theme = 'dark' if n_clicks % 2 != 0 else 'light'
    
    btn_label = '☀️ Light' if theme == 'dark' else '🌙 Dark'  
    
    return approval_chart(df, theme=theme, lines=selected_lines), btn_label  