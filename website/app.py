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


approval_fig = approval_graph
dissaproval_fig = dissaproval_graph

black_chart = black_approval_chart(df)
white_chart = white_approval_chart(df)



app.layout = [
    html.Div(children=['Approval Ratings from Linux']),
    html.Hr(),
    dcc.Graph(figure=black_chart, style={'width': '1000px', 'height': '600px'}),
    dcc.Graph(figure=white_chart, style={'width': '1000px', 'height': '600px'})
]




if __name__ == "__main__":
    app.run(debug=True)