import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
import plotly.graph_objects as go
import numpy as np


#------ Approvals Dataframe ---------------------------
approvals = pd.read_csv('Data/approvals_test_data.csv', 
    parse_dates=['end_date'],
    dtype={
        'yes': float,
        'no': float
    }
)

#------ Lowess Smoothing Function ---------------------------
def get_lowess(result, col):
    fig_temp =px.scatter(
        result, x="end_date", y=col,
        trendline="lowess", 
        trendline_options=dict(frac=0.1)
    )

    trace = fig_temp.data[1]
    smoothed = np.round(trace.y, 2)
    residuals = result[col].values - smoothed
    std = residuals.std()
    upper = np.round(smoothed + 0.96 * std, 2)
    lower = np.round(smoothed - 0.96 * std, 2)

    return trace.x, smoothed, upper, lower

#------- Approval Chart Function ---------------------------
def approval_chart(result, theme='light', lines=None):
    if lines is None:
        lines = ['approve', 'disapprove', 'net']

    # --- Theme colors ---
    if theme == 'dark':
        bg_color = '#0d1117'
        grid_color = '#222222'
        font_color = 'white'
        hline_color = 'white'
    else:
        bg_color = 'white'
        grid_color = '#e0e0e0'
        font_color = '#111111'
        hline_color = 'black'

    # --- Calculate net ---
    result = result.copy()
    result['net'] = result['yes'] - result['no']

    
    x_yes, smoothed_yes, upper_yes, lower_yes = get_lowess(result, 'yes')
    x_no, smoothed_no, upper_no, lower_no = get_lowess(result, 'no')
    x_net, smoothed_net, upper_net, lower_net = get_lowess(result, 'net')

    fig = go.Figure()

    # --- Approve ---
    if 'approve' in lines:
        fig.add_trace(go.Scatter(x=x_yes, y=lower_yes, mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'))
        fig.add_trace(go.Scatter(x=x_yes, y=upper_yes, mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(0,128,128,0.08)', showlegend=False, hoverinfo='skip'))
        fig.add_trace(go.Scatter(x=x_yes, y=smoothed_yes, mode='lines', line=dict(color='teal', width=2), name='Approve'))

    # --- Disapprove ---
    if 'disapprove' in lines:
        fig.add_trace(go.Scatter(x=x_no, y=lower_no, mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'))
        fig.add_trace(go.Scatter(x=x_no, y=upper_no, mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(255,0,0,0.08)', showlegend=False, hoverinfo='skip'))
        fig.add_trace(go.Scatter(x=x_no, y=smoothed_no, mode='lines', line=dict(color='red', width=2), name='Disapprove'))

    # --- Net Approval ---
    if 'net' in lines:
        fig.add_trace(go.Scatter(x=x_net, y=lower_net, mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'))
        fig.add_trace(go.Scatter(x=x_net, y=upper_net, mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(128,128,128,0.08)', showlegend=False, hoverinfo='skip'))
        fig.add_trace(go.Scatter(x=x_net, y=smoothed_net, mode='lines', line=dict(color='gray', width=2), name='Net Approval'))

    # --- Annotations and end markers ---
    last_date = x_yes[-1]

    if 'approve' in lines:
        fig.add_annotation(x=last_date, y=smoothed_yes[-1], text=f"Approve<br>{smoothed_yes[-1]:.1f}%", showarrow=False, xanchor="left", xshift=10, font=dict(size=13, color="teal"))
        fig.add_trace(go.Scatter(x=[last_date], y=[smoothed_yes[-1]], mode="markers", marker=dict(size=8, color="teal"), showlegend=False, hoverinfo='skip'))

    if 'disapprove' in lines:
        fig.add_annotation(x=last_date, y=smoothed_no[-1], text=f"Disapprove<br>{smoothed_no[-1]:.1f}%", showarrow=False, xanchor="left", xshift=10, font=dict(size=13, color="red"))
        fig.add_trace(go.Scatter(x=[last_date], y=[smoothed_no[-1]], mode="markers", marker=dict(size=8, color="red"), showlegend=False, hoverinfo='skip'))

    if 'net' in lines:
        fig.add_annotation(x=last_date, y=smoothed_net[-1], text=f"Net<br>{smoothed_net[-1]:.1f}%", showarrow=False, xanchor="left", xshift=10, font=dict(size=13, color="gray"))
        fig.add_trace(go.Scatter(x=[last_date], y=[smoothed_net[-1]], mode="markers", marker=dict(size=8, color="gray"), showlegend=False, hoverinfo='skip'))

    # --- Layout ---
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Approval Rating %",
        showlegend=False,
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font=dict(color=font_color)
    )
    fig.update_xaxes(range=[result['end_date'].min(), last_date + pd.Timedelta(days=45)], gridcolor=grid_color)
    fig.update_yaxes(gridcolor=grid_color)
    fig.add_hline(y=50, line=dict(color=hline_color, dash="dash", width=1))

    return fig

