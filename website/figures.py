import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import statsmodels.api as sm


#------ Approvals Dataframe ---------------------------
approvals = pd.read_csv('../Data/approvals_test_data.csv', 
    parse_dates=['end_date'],
    dtype={
        'yes': float,
        'no': float
    }
)

#------- Approval Figure ---------------------------
approval_graph = px.scatter(
        approvals, 
        x="end_date", 
        y="yes", 
        labels={"end_date" : "Date", "yes" : "Approval Rating %"},
        color_discrete_sequence=['limegreen'],
        trendline="lowess",
        trendline_options=dict(frac=0.2)
    )
approval_graph.update_layout(width=1000, height=600)
approval_graph.update_traces(marker=dict(opacity=0.5))
approval_graph.add_hline(y=50, line=dict(color="black", dash="dash", width=2))

