from dash import Dash, html, dcc, callback, Input, Output
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
from figures import approval_graph, dissaproval_graph
from figures import black_approval_chart, white_approval_chart


df = pd.read_csv('../Data/approvals_test_data.csv', 
    parse_dates=['end_date'],
    dtype={
        'yes': float,
        'no': float
    }
)

app = Dash()


dark_chart = black_approval_chart(df)
light_chart = white_approval_chart(df)



app.layout = [
    html.Div(children=['President Approval Ratings']),
    html.Hr(),
    html.Button('Switch Theme', id='toggle-btn', n_clicks=0),
    dcc.Graph(id='approval-chart', style={'width': '1000px', 'height': '600px'}),

]

@callback(
    Output('approval-chart', 'figure'),
    Input('toggle-btn', 'n_clicks')
)
def toggle_theme(n_clicks):
    if n_clicks % 2 == 0:
        return light_chart
    else:
        return dark_chart



if __name__ == "__main__":
    app.run(debug=True)