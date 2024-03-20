'''
# This app creates a simple sidebar layout using inline style arguments and the
# dbc.Nav component.
# dcc.Location is used to track the current location, and a callback uses the
# current location to render the appropriate page content. The active prop of
# each NavLink is set automatically according to the current pathname. To use
# this feature you must install dash-bootstrap-components >= 0.11.0.
# For more details on building multi-page Dash applications, check out the Dash
# documentation: https://dash.plot.ly/urls
# Source: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
# @ Create Time: 2024-03-20 07:23:11.828730
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
'''
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(
    title="testdoctor",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("PDPrognosis", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

patients = [
    {"name": "Patient 1", "score": 80},
    {"name": "Patient 2", "score": 75},
    {"name": "Patient 3", "score": 90},
    # إضافة بيانات المرضى الأخرى هنا
]

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content,
    html.Div(id="patient-details")  # تخصيص مكان لعرض تفاصيل المريض
])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the content of the home page!")
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(Output("patient-details", "children"), [Input("url", "pathname")])
def show_patient_details(pathname):
    if pathname == "/page-1":
        return html.Div([
            html.H3("Patient Details"),
            # عرض مربعات المرضى وتفاصيلهم
            *[html.Div([
                html.H5(patient["name"]),
                html.Button(f"Score: {patient['score']}", id={"type": "score-button", "index": index}),
                html.Div(id={"type": "score-output", "index": index})
            ]) for index, patient in enumerate(patients)]
        ])


@app.callback(Output({"type": "score-output", "index": "children"}, [Input({"type": "score-button", "index": "n_clicks"})]))
def show_patient_score(n_clicks):
    if n_clicks is None:
        return ""
    else:
        button_id = dash.callback_context.triggered[0]['prop_id']
        index = button_id.split('.')[0]["index"]
        score = patients[int(index)]["score"]
        return f"Patient {int(index) + 1} score: {score}"


if __name__ == "__main__":
    app.run_server(port=8050)
