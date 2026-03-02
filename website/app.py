from dash import Dash, html, dcc, callback, Input, Output
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import statsmodels.api as sm



df = pd.read_csv('../Data/approvals_test_data.csv', 
    parse_dates=['end_date'],
    dtype={
        'yes': float,
        'no': float
    }
)

app = Dash()

#print("hi")

approval_fig = px.scatter(
        df, 
        x="end_date", 
        y="yes", 
        labels={"end_date" : "Date", "yes" : "Approval Rating %"},
        color_discrete_sequence=['limegreen'],
        trendline="lowess",
        trendline_options=dict(frac=0.2)
    )

approval_fig.update_layout(width=1000, height=600)
approval_fig.update_traces(marker=dict(opacity=0.5))
approval_fig.add_hline(y=50, line=dict(color="black", dash="dash", width=2))

dissaproval_fig = px.scatter(
        df, 
        x="end_date", 
        y="no", 
        labels={"end_date" : "Date", "no" : "Dissaproval Rating %"},
        color_discrete_sequence=['red'],
        trendline="lowess",
        trendline_options=dict(frac=0.2)
    )

dissaproval_fig.update_layout(width=1000, height=600)
dissaproval_fig.update_traces(marker=dict(opacity=0.5))
dissaproval_fig.add_hline(y=50, line=dict(color="black", dash="dash", width=2))

app.layout = [
    html.Div(children=['Approval Ratings']),
    html.Hr(),
    dcc.RadioItems(options=['Approval', 'Disapproval'], value='Approval', id='controls-and-radio-item'),
    dcc.Graph(figure = {}, id='controls-and-graph'),
        dag.AgGrid(
        rowData=df.to_dict('records'),
        columnDefs=[{"field": i} for i in df.columns]
    )
]

@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    if col_chosen == 'Approval':
        return approval_fig
    else:
        return dissaproval_fig


if __name__ == "__main__":
    app.run(debug=True)