import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
import plotly.graph_objects as go
import numpy as np


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

#---------- Both Figures
def black_approval_chart(result):
    
    fig_yes = px.scatter(
    result, x="end_date", y="yes",
    color_discrete_sequence=['teal'],
    trendline="lowess",
    trendline_options=dict(frac=0.1)
    )
    yes_trace = fig_yes.data[1]
    smoothed_yes = np.round(yes_trace.y, 2)
    residuals_yes = result['yes'].values - smoothed_yes
    std_yes = residuals_yes.std()
    upper_yes = np.round(smoothed_yes + 0.96 * std_yes, 2)
    lower_yes = np.round(smoothed_yes - 0.96 * std_yes, 2)

    # --- Disapproval (no) ---
    fig_no = px.scatter(
        result, x="end_date", y="no",
        color_discrete_sequence=['red'],
        trendline="lowess",
        trendline_options=dict(frac=0.1)
    )
    no_trace = fig_no.data[1]
    smoothed_no = np.round(no_trace.y, 2)
    residuals_no = result['no'].values - smoothed_no
    std_no = residuals_no.std()
    upper_no = np.round(smoothed_no + 0.96 * std_no, 2)
    lower_no = np.round(smoothed_no - 0.96 * std_no, 2)

    # --- Combine into one figure ---
    fig = go.Figure()

    # Approval band
    fig.add_trace(go.Scatter(x=yes_trace.x, y=lower_yes, mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=yes_trace.x, y=upper_yes, mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(0,128,128,0.08)', showlegend=False, hoverinfo='skip'))

    # Disapproval band
    fig.add_trace(go.Scatter(x=no_trace.x, y=lower_no, mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=no_trace.x, y=upper_no, mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(255,0,0,0.08)', showlegend=False, hoverinfo='skip'))

    

    # Smooth lines
    fig.add_trace(go.Scatter(x=yes_trace.x, y=smoothed_yes, mode='lines', line=dict(color='teal', width=2), name='Approve'))
    fig.add_trace(go.Scatter(x=no_trace.x, y=smoothed_no, mode='lines', line=dict(color='red', width=2), name='Disapprove'))

    # End point annotations and markers
    last_date = yes_trace.x[-1]
    fig.add_annotation(x=last_date, y=smoothed_yes[-1], text=f"Approve<br>{smoothed_yes[-1]:.1f}%", showarrow=False, xanchor="left", xshift=10, font=dict(size=13, color="teal"))
    fig.add_annotation(x=last_date, y=smoothed_no[-1], text=f"Disapprove<br>{smoothed_no[-1]:.1f}%", showarrow=False, xanchor="left", xshift=10, font=dict(size=13, color="red"))
    fig.add_trace(go.Scatter(x=[last_date], y=[smoothed_yes[-1]], mode="markers", marker=dict(size=8, color="teal"), showlegend=False, hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=[last_date], y=[smoothed_no[-1]], mode="markers", marker=dict(size=8, color="red"), showlegend=False, hoverinfo='skip'))

    # Layout
    fig.update_layout(
        width=1000, height=600,
        xaxis_title="Date",
        yaxis_title="Approval Rating %",
        showlegend=False,
        paper_bgcolor='#0d1117',
        plot_bgcolor='#0d1117',
        font=dict(color='white')
    )

    fig.update_xaxes(range=[result['end_date'].min(), last_date + pd.Timedelta(days=30)])
    fig.add_hline(y=50, line=dict(color="black", dash="dash", width=1))
    fig.update_xaxes(gridcolor='#222222')
    fig.update_yaxes(gridcolor='#222222')

    return fig

#---------- Build White Chart Function ---------------------------
def white_approval_chart(result):
    
    fig_yes = px.scatter(
    result, x="end_date", y="yes",
    color_discrete_sequence=['teal'],
    trendline="lowess",
    trendline_options=dict(frac=0.1)
    )
    yes_trace = fig_yes.data[1]
    smoothed_yes = np.round(yes_trace.y, 2)
    residuals_yes = result['yes'].values - smoothed_yes
    std_yes = residuals_yes.std()
    upper_yes = np.round(smoothed_yes + 0.96 * std_yes, 2)
    lower_yes = np.round(smoothed_yes - 0.96 * std_yes, 2)

    # --- Disapproval (no) ---
    fig_no = px.scatter(
        result, x="end_date", y="no",
        color_discrete_sequence=['red'],
        trendline="lowess",
        trendline_options=dict(frac=0.1)
    )
    no_trace = fig_no.data[1]
    smoothed_no = np.round(no_trace.y, 2)
    residuals_no = result['no'].values - smoothed_no
    std_no = residuals_no.std()
    upper_no = np.round(smoothed_no + 0.96 * std_no, 2)
    lower_no = np.round(smoothed_no - 0.96 * std_no, 2)

    # --- Combine into one figure ---
    fig = go.Figure()

    # Approval band
    fig.add_trace(go.Scatter(x=yes_trace.x, y=lower_yes, mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=yes_trace.x, y=upper_yes, mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(0,128,128,0.08)', showlegend=False, hoverinfo='skip'))

    # Disapproval band
    fig.add_trace(go.Scatter(x=no_trace.x, y=lower_no, mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=no_trace.x, y=upper_no, mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(255,0,0,0.08)', showlegend=False, hoverinfo='skip'))

    

    # Smooth lines
    fig.add_trace(go.Scatter(x=yes_trace.x, y=smoothed_yes, mode='lines', line=dict(color='teal', width=2), name='Approve'))
    fig.add_trace(go.Scatter(x=no_trace.x, y=smoothed_no, mode='lines', line=dict(color='red', width=2), name='Disapprove'))

    # End point annotations and markers
    last_date = yes_trace.x[-1]
    fig.add_annotation(x=last_date, y=smoothed_yes[-1], text=f"Approve<br>{smoothed_yes[-1]:.1f}%", showarrow=False, xanchor="left", xshift=10, font=dict(size=13, color="teal"))
    fig.add_annotation(x=last_date, y=smoothed_no[-1], text=f"Disapprove<br>{smoothed_no[-1]:.1f}%", showarrow=False, xanchor="left", xshift=10, font=dict(size=13, color="red"))
    fig.add_trace(go.Scatter(x=[last_date], y=[smoothed_yes[-1]], mode="markers", marker=dict(size=8, color="teal"), showlegend=False, hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=[last_date], y=[smoothed_no[-1]], mode="markers", marker=dict(size=8, color="red"), showlegend=False, hoverinfo='skip'))

    # Layout
    fig.update_layout(
        width=1000, height=600,
        xaxis_title="Date",
        yaxis_title="Approval Rating %",
        showlegend=False
    )

    fig.update_xaxes(range=[result['end_date'].min(), last_date + pd.Timedelta(days=30)])
    fig.add_hline(y=50, line=dict(color="black", dash="dash", width=1))
    
    return fig