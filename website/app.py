from dash import Dash, html, dcc, callback, Input, Output
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
from figures import approval_graph, dissaproval_graph
from figures import build_approval_chart


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

chart = build_approval_chart(df)



app.layout = [
    html.Div(children=['Approval Ratings']),
    html.Hr(),
    #dcc.RadioItems(options=['Approval', 'Disapproval'], value='Approval', id='controls-and-radio-item'),
    # dcc.Graph(figure=approval_fig, id='controls-and-graph', style={'width': '1000px', 'height': '600px'}),
    dcc.Graph(figure=chart, style={'width': '1000px', 'height': '600px'}),
    dag.AgGrid(rowData=df.to_dict('records'),columnDefs=[{"field": i} for i in df.columns]
    )
]

# @callback(
#     Output(component_id='controls-and-graph', component_property='figure'),
#     Input(component_id='controls-and-radio-item', component_property='value')
# )
# def update_graph(col_chosen):
#     if col_chosen == 'Approval':
#         return approval_fig
#     else:
#         return dissaproval_fig


if __name__ == "__main__":
    app.run(debug=True)