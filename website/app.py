import dash
from dash import html, dcc

app = dash.Dash(__name__, use_pages=True)



app.layout = html.Div([
    html.Nav(className='navbar', children=[
        html.H1('Election Signals'),
        html.Div(className='nav-links', children=[
            dcc.Link('Approval Ratings', href='/approval'),
        ])
    ]),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)