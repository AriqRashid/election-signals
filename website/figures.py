import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
import plotly.graph_objects as go


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
        trendline_options=dict(frac=0.2),
        opacity=0
    )

trendline_trace = approval_graph.data[1]
trendline_trace.line.width = 3

last_date = trendline_trace.x[-1]
last_val = trendline_trace.y[-1]

approval_graph.add_annotation(
    x=last_date,
    y=last_val,
    text=f"Approve<br>{last_val:.1f}%",
    showarrow=False,
    xanchor="left",
    xshift=10,
    font=dict(size=13, color="limegreen"),
    align="left",
    bgcolor="white", borderpad=4
)

approval_graph.add_trace(go.Scatter(
    x=[last_date],
    y=[last_val],
    mode="markers",
    marker=dict(size=8, color="limegreen"),
    showlegend=False
))

approval_graph.update_xaxes(range=[approvals['end_date'].min(), last_date + pd.Timedelta(days=30)])

approval_graph.add_hline(y=50, line=dict(color="black", dash="dash", width=2))

approval_graph.update_layout(
    width=1000, height=600,
    plot_bgcolor="white"
)



#------- Dissaproval Figure ---------------------------
dissaproval_graph = px.scatter(
        approvals, 
        x="end_date", 
        y="no", 
        labels={"end_date" : "Date", "no" : "Dissaproval Rating %"},
        color_discrete_sequence=['red'],
        trendline="lowess",
        trendline_options=dict(frac=0.2),
        opacity=0
    )

trendline_trace = dissaproval_graph.data[1]
trendline_trace.line.width = 3

last_date = trendline_trace.x[-1]
last_val = trendline_trace.y[-1]

dissaproval_graph.add_annotation(
    x=last_date,
    y=last_val,
    text=f"Disapprove<br>{last_val:.1f}%",
    showarrow=False,
    xanchor="left",
    xshift=10,
    font=dict(size=13, color="red"),
    align="left"
)

dissaproval_graph.add_trace(go.Scatter(
    x=[last_date],
    y=[last_val],
    mode="markers",
    marker=dict(size=8, color="red"),
    showlegend=False
))

dissaproval_graph.update_xaxes(range=[approvals['end_date'].min(), last_date + pd.Timedelta(days=30)])

dissaproval_graph.update_layout(width=1000, height=600)
dissaproval_graph.add_hline(y=50, line=dict(color="black", dash="dash", width=2))

dissaproval_graph.update_layout(
    width=1000, height=600,
    plot_bgcolor="white"
)


