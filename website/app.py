from dash import Dash, html, dcc
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

app.layout = [
    html.Div(children=['Approval Ratings']),
    dag.AgGrid(
        rowData=df.to_dict('records'),
        columnDefs=[{"field": i} for i in df.columns]
    ),
    dcc.Graph(figure = approval_fig)
]



if __name__ == "__main__":
    app.run(debug=True)