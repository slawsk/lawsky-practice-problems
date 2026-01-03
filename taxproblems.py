import numpy as np
import plotly.graph_objects as go
import dash
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import json
import random
import pypandoc
import os
from datetime import datetime
import time
import base64
import pandas as pd
import io
from flask import send_from_directory, jsonify
# from celery.result import AsyncResult
# from celery_tasks import create_code_book_task

# from celery_tasks import celery

import faq
import functionmodules as fm
import basictaxproblems as bt
import partnershiptaxproblems as pt
import statutoryproblems as st
import problemtopics as top
import createCodeAndRegsImages as cc

MAX_QUIZ_QUESTIONS = fm.MAX_QUIZ_QUESTIONS


def generate_quiz_components():
    """Generate quiz problem and answer components dynamically"""
    quiz_components = []
    for i in range(1, MAX_QUIZ_QUESTIONS + 1):
        quiz_components.extend(
            [
                dcc.Markdown(id=f"quiz_problem_{i}", dangerously_allow_html=True),
                dcc.Dropdown(id=f"quiz_answers_{i}", style={"display": "none"}),
                html.Br(),
            ]
        )
    return quiz_components


def generate_output_list():
    """Generate the list of Output objects dynamically"""
    outputs = []
    for i in range(1, MAX_QUIZ_QUESTIONS + 1):
        outputs.extend(
            [
                Output(f"quiz_problem_{i}", "children"),
                Output(f"quiz_answers_{i}", "options"),
                Output(f"quiz_answers_{i}", "style"),
            ]
        )
    outputs.extend(
        [Output("quiz_submit_button", "style"), Output("correct-list", "children")]
    )
    return outputs


def generate_scoring_states():
    """Generate the State inputs for scoring dynamically"""
    states = []
    for i in range(1, MAX_QUIZ_QUESTIONS + 1):
        states.extend(
            [
                State(f"quiz_answers_{i}", "value"),
                State(f"quiz_problem_{i}", "children"),
            ]
        )
    states.extend(
        [State("correct-list", "children"), State("number-questions", "value")]
    )
    return states


app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {
            "name": "description",
            "content": "Free practice problems and quizzes for Federal Income Taxation law school classes.",
        },
        {
            "name": "google-site-verification",
            "content": "Cmw463c-ZgWSE_OZOraY3c4DGeppNfyb3MuTGLjFSGg",
        },
    ],
)


nav_item = dbc.Nav(
    [
        dbc.NavLink("Practice Problems", href="/"),
        dbc.NavLink("Rates", href="/ratespage"),
        dbc.NavLink("Statutes", href="/statutes"),
        dbc.NavLink("Quizzes", href="/quizzes"),
        dbc.NavLink("Code and Regs", href="/codeandregs"),
        dbc.NavLink("About", href="/about"),
        dbc.NavLink("Open Source", href="/otherprojects"),
    ],
    navbar=True,
)


navbar1 = dbc.NavbarSimple(
    children=[nav_item],
    brand="Lawsky Practice Problems",
    color="primary",
    dark=True,
    fluid=True,
)


navbar = html.Div([navbar1])

# main app
app.config.suppress_callback_exceptions = True
app.title = "Lawsky Practice Problems"

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Interval(
            id="interval-component", interval=1000, n_intervals=0, disabled=True
        ),
        dcc.Store(id="processing-flag",data=False),
        dcc.Store(id="task-input-store"),
        dcc.Store(id="reset-state", data=False),
        html.Div(
            id="page-content",
            style={
                "max-width": "1200px",
                "margin": "0 auto",
                "padding": "0 5%",
                "background-color": "#fff",
                "min-height": "100vh",
            },
        ),
    ],
    style={"background-color": "#95a5a6"},
)


fed_tax_layout = html.Div(
    children=[
        navbar,
        html.Br(),
        html.Div(
            [
                html.H3(
                    id="title-language",
                    children=["Federal Income Tax"],
                    style={"display": "inline-block", "margin-right": "10px"},
                ),
                html.H3("Practice Problems", style={"display": "inline-block"}),
            ]
        ),
        dbc.Button(
            children=["Switch to Partnership"],
            id="switch_problem_type_button",
            n_clicks=0,
        ),
        html.Br(),
        html.Br(),
        dcc.Markdown(faq.problem_page_intro),
        dcc.Markdown(
            faq.partnership_addl_info, id="partnership-info", style={"display": "none"}
        ),
        dcc.Dropdown(
            id="type-dropdown-id",
            options=[{"label": k, "value": k} for k in bt.functions_list],
            style={
                "width": f"{fm.dropdown_width(bt.functions_list)}em",
                "max-width": "90%",
            },
        ),
        html.Br(),
        dbc.Button("Submit Topic", id="submittype_button", n_clicks=0),
        html.Br(),
        html.Br(),
        dcc.Markdown(id="full_problem", dangerously_allow_html=True),
        dcc.Dropdown(id="possible-answers-dropdown-id", style={"display": "none"}),
        html.Br(),
        dbc.Button(
            "Submit Answer",
            id="submitanswer_button",
            n_clicks=0,
            style={"display": "none"},
        ),
        html.Br(),
        html.Br(),
        dcc.Markdown(id="judgement-explanation", dangerously_allow_html=True),
        html.Div(id="my-list", style={"display": "none"}),
        # this hidden button resets the explanation when someone picks a new type of problem
        dbc.Button(
            "Shhhh", id="hidden-counter-1", n_clicks=0, style={"display": "none"}
        ),
        html.Div(
            id="current-type-problem",
            children=["Federal Income Tax"],
            style={"display": "none"},
        ),
    ],
    style=fm.page_style_dict,
)

rates_layout = html.Div(
    [
        navbar,
        html.Br(),
        html.H3("Rates"),
        html.Div("What is the taxpayer's filing status?"),
        dcc.Dropdown(
            id="filing-status-pick",
            options=[{"label": k, "value": k} for k in fm.rates_dict.keys()],
            style={"width": "15em"},
            value="Single",
        ),
        html.Br(),
        html.Div("What is the taxpayer's taxable income?"),
        dbc.Input(
            id="taxable-income",
            type="number",
            style={"width": "15em", "maxwidth": "100%"},
        ),
        html.Br(),
        dbc.Button(
            "Submit Income",
            id="submitincome_button",
            n_clicks=0,
            style={"margin-bottom": "20px", "display": "block", "width": "140px"},
        ),
        dbc.Button(
            "Reset Income",
            id="resetincome_button",
            style={"display": "none"},
            n_clicks=0,
        ),
        html.Br(),
        dcc.Markdown(id="rates_answers"),
        html.Br(),
        html.Div(
            [
                dcc.Graph(
                    id="tax-rates-graph",
                )
            ],
            style={"width": "100%", "display": "inline-block", "padding": "0 20"},
        ),
        # this hidden button resets the explanation when someone picks a new type of problem
        dbc.Button(
            "Shhhh", id="hidden-counter-rates", n_clicks=0, style={"display": "none"}
        ),
        html.Div(id="page-3-content"),
    ],
    style=fm.page_style_dict,
)


faq_layout = html.Div(
    [
        navbar,
        html.Br(),
        html.H3("FAQ"),
        html.Div(html.H5("General Information and Questions")),
        dcc.Markdown(faq.general_faq, dangerously_allow_html=True),
        html.Hr(),
        html.Div(html.H5("Practice Problems")),
        dcc.Markdown(faq.practice_problems_faq, dangerously_allow_html=True),
        html.Hr(),
        html.Div(html.H5("Statutes")),
        dcc.Markdown(faq.statutes_faq, dangerously_allow_html=True),
        html.Hr(),
        html.Div(html.H5("Quizzes")),
        dcc.Markdown(faq.quizzes_faq, dangerously_allow_html=True),
        html.Br(),
        html.Div(id="page-4-content"),
    ],
    style=fm.page_style_dict,
)

code_and_regs_layout = html.Div(
    [
        navbar,
        html.Br(),
        html.H3("Create Code and Regs Book"),
        dcc.Markdown(faq.codeandregsdownload, dangerously_allow_html=True),
        html.Hr(),
        html.Div(html.H4("STEP 1: FORMAT YOUR SPREADSHEET OF CODE AND REG SECTIONS")),
        html.Div(
            [
                html.Img(
                    src="data:image/png;base64,{}".format(fm.encoded_image.decode()),
                    style={"width": "500px", "max-width": "90%"},
                )
            ]
        ),
        html.Br(),
        dcc.Markdown(faq.code_template_explanation),
        html.Br(),
        html.Div(html.H4("STEP 2 (OPTIONAL): PICK WHAT GOES INTO YOUR BOOK")),
        dcc.Markdown(faq.code_pick_explanation),
        html.Div(
            "Select the items you would like in your Selected Sections book, in the order you would like them. Make sure to pick the selected Code and Regs (assuming you want to include them)!"
        ),
        html.Br(),
        dcc.Dropdown(
            id="docs-dropdown",
            options=[{"label": k, "value": k} for k in cc.possible_files_list],
            style={
                "width": "90%",
                "max-width": f"{fm.dropdown_width(cc.possible_files_list)}em",
            },
            multi=True,
        ),
        html.Br(),
        dcc.Markdown("Decide whether to include page numbers."),
        html.Div(
            [
                html.Div(
                    id="page-numbers",
                    children=[
                        dbc.Checklist(
                            options=[{"label": "Page numbers off/on", "value": 1}],
                            value=[1],
                            id="page-number-input",
                            switch=True,
                        ),
                        html.Br(),
                    ],
                )
            ]
        ),
        html.Div(html.H4("STEP 3: UPLOAD YOUR SPREADSHEET")),
        dcc.Markdown(faq.code_upload_explanation),
        dcc.Upload(
            id="upload-data-all",
            children=dbc.Button("Upload File", id="submitfile-all", n_clicks=0),
            multiple=False,
        ),
        # dbc.Button('Upload File',id='submitfile-all',n_clicks=0),
        html.Br(),
        html.Div(html.H4("STEP 4: WAIT")),
        dcc.Markdown(faq.be_patient),
        html.Br(),
        html.Div([
    dcc.Loading(
        id="loading-book",
        type="default",  # or "circle", "dot", "cube"
        children=dcc.Markdown(id="upload-confirm-all", dangerously_allow_html=True)
    )
]),
        html.Br(),
        html.Br(),
        html.Div(
            [
                html.Div(
                    id="after-book-options",
                    children=[
                        html.Div(
                            "Click here to reset the page in order to upload a new set of desired sections and subsections.",
                            id="offer-reset-book",
                        ),
                        html.Br(),
                        dbc.Button("Reset Book", id="book_reset_button", n_clicks=0),
                        html.Br(),
                        html.Br(),
                    ],
                    style={"display": "none"},
                )
            ]
        ),
        html.Div(id="book-title", style={"display": "none"}),
        html.Br(),
        html.Hr(),
        dcc.Markdown(faq.codeandregs, dangerously_allow_html=True),
        html.Br(),
        html.Br(),
        html.Div(id="code-regs-content"),
    ],
    style=fm.page_style_dict,
)

statutes_layout = html.Div(
    children=[
        navbar,
        html.Br(),
        html.H3("Practicing Statutory Language"),
        dcc.Markdown(st.instruction_language, dangerously_allow_html=True),
        dbc.Button("Generate Problem", id="statute_button", n_clicks=0),
        html.Br(),
        html.Br(),
        dcc.Markdown(id="statute_problem", dangerously_allow_html=True),
        dbc.Input(
            id="statute_answer",
            type="number",
            style={"display": "none", "width": "10em", "maxwidth": "100%"},
        ),
        html.Br(),
        dbc.Button(
            "Submit Answer",
            id="submit_statute_answer_button",
            n_clicks=0,
            style={"display": "none"},
        ),
        html.Br(),
        html.Br(),
        dcc.Markdown(id="statute_explanation", dangerously_allow_html=True),
        html.Div(id="correct_statute_answer", style={"display": "none"}),
        html.Div(id="page-5-content"),
    ],
    style=fm.page_style_dict,
)

quiz_layout = html.Div(
    children=[
        navbar,
        html.Br(),
        html.Div(
            [
                html.H3(
                    id="quiz-title-language",
                    children=["Federal Income Tax"],
                    style={"display": "inline-block", "margin-right": "10px"},
                ),
                html.H3("Quizzes", style={"display": "inline-block"}),
            ]
        ),
        dbc.Button(
            children=["Switch to Partnership"],
            id="quiz-switch_problem_type_button",
            n_clicks=0,
        ),
        html.Br(),
        html.Br(),
        dcc.Markdown(faq.quiz_explanation),
        html.Hr(),
        html.Div(
            f"Enter the number of questions on the quiz, up to a maximum of {MAX_QUIZ_QUESTIONS}. If you do not enter a number, the quiz will have five questions."
        ),
        html.Br(),
        dbc.Input(
            id="number-questions",
            type="number",
            style={"width": "10em", "maxwidth": "100%"},
        ),
        html.Br(),
        html.Br(),
        html.Div(
            "Select one or more topics--as many as you would like. The problems will be drawn randomly (with replacement) from the list of topics you select. If you select no topics, all of the topics will be in play."
        ),
        html.Br(),
        dcc.Dropdown(
            id="quiz-type-dropdown-id",
            options=[{"label": k, "value": k} for k in bt.functions_list],
            style={
                "width": "90%",
                "max-width": f"{fm.dropdown_width(bt.functions_list)}em",
            },
            multi=True,
        ),
        html.Br(),
        dbc.Button("Generate Quiz", id="quiz_button", n_clicks=0),
        html.Br(),
        html.Br(),
        *generate_quiz_components(),
        html.Br(),
        dbc.Button(
            "Submit Answers",
            id="quiz_submit_button",
            n_clicks=0,
            style={"display": "none"},
        ),
        html.Br(),
        dcc.Markdown(id="return-score", dangerously_allow_html=True),
        html.Br(),
        html.Div(
            [
                html.Div(
                    id="after-quiz-options",
                    children=[
                        html.Div(
                            "To download these questions, answers, and explanations, click here.",
                            id="offer-download",
                        ),
                        dbc.Button(
                            "Download Answers", id="download_quiz_button", n_clicks=0
                        ),
                        dcc.Download(id="download-answer-key"),
                        html.Br(),
                        html.Br(),
                        html.Div(id="download-confirm-answer-key"),
                        html.Br(),
                        html.Div(
                            "To reset this quiz in order to take a new quiz, click here.",
                            id="offer-reset-quiz",
                        ),
                        dbc.Button("Reset Quiz", id="quiz_reset_button", n_clicks=0),
                        html.Br(),
                        html.Br(),
                    ],
                    style={"display": "none"},
                )
            ]
        ),
        html.Div(id="correct-list", style={"display": "none"}),
        html.Div(id="file-number", style={"display": "none"}),
        html.Div(id="page-7-content"),
        html.Div(
            id="quiz-current-type-problem",
            children=["Federal Income Tax"],
            style={"display": "none"},
        ),
    ],
    style=fm.page_style_dict,
)

other_projects_layout = html.Div(
    children=[
        navbar,
        html.Br(),
        html.H3("Open Source Projects"),
        dcc.Markdown(faq.other_projects_info),
        html.Hr(),
        dcc.Markdown(faq.other_projects_list),
    ],
    style=fm.page_style_dict,
)


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
)
def display_page(pathname):

    if pathname == "/":
        return fed_tax_layout
    elif pathname == "/ratespage":
        return rates_layout
    elif pathname == "/about":
        return faq_layout
    elif pathname == "/statutes":
        return statutes_layout
    elif pathname == "/quizzes":
        return quiz_layout
    elif pathname == "/codeandregs":
        return code_and_regs_layout
    elif pathname == "/otherprojects":
        return other_projects_layout


# basic page
@app.callback(
    [
        Output("type-dropdown-id", "options"),
        Output("title-language", "children"),
        Output("type-dropdown-id", "value"),
        Output("type-dropdown-id", "style"),
        Output("partnership-info", "style"),
        Output("submittype_button", "n_clicks"),
        Output("current-type-problem", "children"),
        Output("switch_problem_type_button", "children"),
    ],
    [Input("switch_problem_type_button", "n_clicks")],
    [State("current-type-problem", "children")],
)
def pick_type_problem(n_click, type_value):

    if n_click == 0:
        raise PreventUpdate

    else:

        if type_value[0] == "Federal Income Tax":
            new_type_value = "Partnership Tax"
            submit_button = "Switch to Fed Tax"

        elif type_value[0] == "Partnership Tax":
            new_type_value = "Federal Income Tax"
            submit_button = "Switch to Partnership"

        pick_dictionary = {
            "Federal Income Tax": [bt, {"display": "none"}],
            "Partnership Tax": [pt, {"display": "block"}],
        }
        fn = pick_dictionary[new_type_value][0]
        to_display = pick_dictionary[new_type_value][1]

        maxwidth = fm.dropdown_width(fn.functions_list)

        return (
            [{"label": k, "value": k} for k in fn.functions_list],
            new_type_value,
            "",
            {"width": "90%", "max-width": f"{maxwidth}em"},
            to_display,
            0,
            [new_type_value],
            [submit_button],
        )


@app.callback(
    [
        Output("full_problem", "children"),
        Output("possible-answers-dropdown-id", "options"),
        Output("possible-answers-dropdown-id", "value"),
        Output("my-list", "children"),
        Output("submitanswer_button", "n_clicks"),
        Output(component_id="possible-answers-dropdown-id", component_property="style"),
        Output(component_id="submitanswer_button", component_property="style"),
    ],
    [Input("submittype_button", "n_clicks")],
    [State("current-type-problem", "children"), State("type-dropdown-id", "value")],
)
def create_problem(n_clicks_submit_types, type_value, dropdown_id_value):

    pick_dictionary = {"Federal Income Tax": bt, "Partnership Tax": pt}

    return fm.create_problem(
        n_clicks_submit_types, dropdown_id_value, pick_dictionary[type_value[0]]
    )


@app.callback(
    Output("judgement-explanation", "children"),
    [Input("submitanswer_button", "n_clicks")],
    [
        State("hidden-counter-1", "value"),
        State("submittype_button", "n_clicks"),
        State("possible-answers-dropdown-id", "value"),
        State("my-list", "children"),
    ],
)
def create_explanation(n_clicks, hidden1, submit_type_reset, input1, list1):
    return fm.create_explanation(n_clicks, hidden1, submit_type_reset, input1, list1)


# Rates Page


@app.callback(
    [Output("rates_answers", "children"), Output("resetincome_button", "style")],
    [Input("submitincome_button", "n_clicks")],
    [State("filing-status-pick", "value"), State("taxable-income", "value")],
)
def rates_function(n_clickssubmit, filing_status, taxable_income):
    if filing_status is None:
        raise PreventUpdate

    if n_clickssubmit == 0:
        return "", {"display": "none"}

    else:
        return bt.rates_facts(filing_status, taxable_income), {
            "display": "block",
            "margin-top": "20px",
            "width": "140px",
        }


@app.callback(
    Output("tax-rates-graph", "figure"), [Input("filing-status-pick", "value")]
)
def update_graph(filing_status):

    status = fm.rates_dict.get(filing_status)
    if filing_status == "Married Filing Jointly":
        top_number = 1000000
    else:
        top_number = 700000

    x_data = np.concatenate(
        [
            np.arange(10, 500, 10),  # Fine grain at start
            np.arange(500, top_number, 1000),  # Larger steps after
        ]
    )
    y_data1 = [fm.rates_facts_average(status, income) for income in x_data]
    y_data2 = [fm.rates_facts_marginal(status, income) for income in x_data]
    # Create arrays for the stepped line
    x_stepped = []
    y_stepped = []

    x_stepped.append(0)
    y_stepped.append(y_data2[0])
    # Add first point
    x_stepped.append(x_data[0])
    y_stepped.append(y_data2[0])
    for i in range(len(x_data) - 1):
        if y_data2[i] != y_data2[i + 1]:
            # Add the end of current step
            x_stepped.append(x_data[i + 1])
            y_stepped.append(y_data2[i])
            # Add None to create discontinuity
            x_stepped.append(x_data[i + 1])
            y_stepped.append(None)
            # Add start of next step
            x_stepped.append(x_data[i + 1])
            y_stepped.append(y_data2[i + 1])

    # Add last point
    x_stepped.append(x_data[-1])
    y_stepped.append(y_data2[-1])
    x_data = np.concatenate(([1], x_data))  # Use 1 instead of 0
    y_data1 = [y_data1[0]] + y_data1

    return {
        "data": [
            (
                go.Scatter(
                    x=x_data,
                    y=y_data1,
                    mode="lines",
                    name="Average Rate",
                    line=dict(color="royalblue"),
                    connectgaps=False,  # Important: don't connect the None values
                )
            ),
            (
                go.Scatter(
                    x=x_stepped,
                    y=y_stepped,
                    mode="lines",
                    name="Marginal Rate",
                    line=dict(color="firebrick", dash="dot"),
                    connectgaps=False,  # Important: don't connect the None values
                )
            ),
        ],
        "layout": go.Layout(
            {
                "title": f"Tax Rates - {filing_status} - {fm.current_year}",
                "legend": {"traceorder": "reversed"},
            },
            xaxis={
                "title": "Taxable Income",
                "tickformat": "$,",
                "range": [0, top_number],
            },
            yaxis={
                "title": "Rate",
                "tickformat": ".0%",
                "range": [0, max(max(y_data1), max(y_data2)) * 1.1],
            },
        ),
    }


@app.callback(
    [Output("taxable-income", "value"), Output("submitincome_button", "n_clicks")],
    [Input("resetincome_button", "n_clicks")],
)
def reset_income(n_clicks):
    # if n_clicks != 0: #Don't clear options when loading page for the first time
    return "", 0


# statute page


@app.callback(
    [
        Output("statute_problem", "children"),
        Output("correct_statute_answer", "children"),
        Output(component_id="statute_answer", component_property="style"),
        Output(component_id="submit_statute_answer_button", component_property="style"),
    ],
    [Input("statute_button", "n_clicks")],
)
def display_statute_problem(clicks):
    if clicks == 0:
        return ["", "", {"display": "none"}, {"display": "none"}]

    else:

        (problem_language, correct_answer) = st.statute_problem()
        return [
            problem_language,
            correct_answer,
            {"display": "block", "width": "10em", "maxwidth": "100%"},
            {"display": "block"},
        ]


@app.callback(
    Output("statute_explanation", "children"),
    [Input("submit_statute_answer_button", "n_clicks")],
    [
        State("statute_button", "n_clicks"),
        State("statute_answer", "value"),
        State("correct_statute_answer", "children"),
    ],
)
def judge_statute_answer(submitclicks, langclicks, submittedanswer, rightanswer):
    if submittedanswer is None:
        raise PreventUpdate

    if submitclicks == 0 or langclicks == 0:
        explanation = ""

    elif submitclicks > 3 and submittedanswer != rightanswer:
        explanation = f"The correct answer is {rightanswer:,d}."

    else:
        if submittedanswer == rightanswer:
            explanation = "Correct."
        else:
            explanation = "Try again."

    return explanation


@app.callback(
    [
        Output("statute_answer", "value"),
        Output("submit_statute_answer_button", "n_clicks"),
    ],
    [Input("statute_button", "n_clicks")],
)
def reset_statute_prob(n_clicks):
    return "", 0


@app.callback(
    [
        Output("quiz-type-dropdown-id", "options"),
        Output("quiz-title-language", "children"),
        Output("quiz-type-dropdown-id", "value", allow_duplicate=True),
        Output("quiz-type-dropdown-id", "style"),
        Output("quiz-current-type-problem", "children"),
        Output("quiz-switch_problem_type_button", "children"),
    ],
    [Input("quiz-switch_problem_type_button", "n_clicks")],
    [State("quiz-current-type-problem", "children")],
    prevent_initial_call=True,
)
def pick_type_quiz(n_click, type_value):

    if n_click == 0:
        raise PreventUpdate

    else:

        if type_value[0] == "Federal Income Tax":
            new_type_value = "Partnership Tax"
            submit_button = "Switch to Fed Tax"

        elif type_value[0] == "Partnership Tax":
            new_type_value = "Federal Income Tax"
            submit_button = "Switch to Partnership"

        pick_dictionary = {"Federal Income Tax": bt, "Partnership Tax": pt}

        fn = pick_dictionary[new_type_value]

        maxwidth = fm.dropdown_width(fn.functions_list)

        return (
            [{"label": k, "value": k} for k in fn.functions_list],
            new_type_value,
            "",
            {"width": "90%", "max-width": f"{maxwidth}em"},
            [new_type_value],
            [submit_button],
        )


@app.callback(
    generate_output_list(),
    [Input("quiz_button", "n_clicks")],
    [
        State("quiz-current-type-problem", "children"),
        State("quiz-type-dropdown-id", "value"),
        State("number-questions", "value"),
    ],
)
def create_quiz(n_clicks, current_type, types_problem, number_questions):
    if n_clicks == 0:
        return ["", "", {"display": "none"}] * MAX_QUIZ_QUESTIONS + [
            {"display": "none"},
            "",
        ]

    else:
        if number_questions is None or number_questions == "":
            number_questions = 5
        else:
            number_questions = min(int(number_questions), MAX_QUIZ_QUESTIONS)
        return_list = []
        correct_dict = {}
        pick_dictionary = {"Federal Income Tax": bt, "Partnership Tax": pt}

        fn = pick_dictionary[current_type[0]]

        for n in range(number_questions):
            if types_problem is None or types_problem == "":
                problem_type = "a random type of problem"
            else:
                problem_type = random.choice(types_problem)

            [problemtext, cleananswers, json_dict, correct_answer] = fn.function_picker(
                problem_type
            )

            answerslist = [{"label": i, "value": i} for i in cleananswers]
            maxwidth = fm.dropdown_width(answerslist)
            correct_explanation_dict = json.loads(json_dict)

            correct_answer = fm.fancify_string(
                list(correct_explanation_dict.keys())[0], correct_answer
            )

            correct_explanation = correct_explanation_dict[correct_answer]
            correct_explanation = fm.clean_explanation(correct_explanation)

            problemtext = f"""
            
**Question {n+1}**
            
{problemtext}"""

            return_list.append(problemtext)
            return_list.append(answerslist)
            return_list.append(
                {"width": "90%", "max-width": f"{maxwidth}em", "display": "block"}
            )

            correct_dict[f"Problem {n+1}"] = {correct_answer: correct_explanation}

        for n in range(MAX_QUIZ_QUESTIONS - number_questions):
            return_list.append("")
            return_list.append("")
            return_list.append({"display": "none"})

        return_list.append({"display": "block"})
        return_list.append(json.dumps(correct_dict))

    return return_list


@app.callback(
    [
        Output("return-score", "children"),
        Output("after-quiz-options", "style"),
    ],
    [Input("quiz_submit_button", "n_clicks")],
    generate_scoring_states(),
)
def score_quiz(n_clicks, *args):
    if n_clicks == 0:
        return ["", {"display": "none"}]

    else:
        answer_problem_pairs = args[:-2]
        jsondict = args[-2]
        numberquestions = args[-1]

        # Process number of questions
        numberquestions = min(int(numberquestions or 5), MAX_QUIZ_QUESTIONS)

        # Split pairs into answers and problems
        completeanswerlist = answer_problem_pairs[::2]  # Even indices
        completeproblemlist = answer_problem_pairs[1::2]  # Odd indices

        # Process answers
        answer_dict = json.loads(jsondict)
        correct_answers = 0
        explanation_string = ""

        # Only process the number of questions actually used
        for n in range(numberquestions):
            answer = completeanswerlist[n]
            problem = fm.clean_explanation(completeproblemlist[n])
            correct_answer = list(answer_dict[f"Problem {n+1}"].keys())[0]
            correct_explanation = answer_dict[f"Problem {n+1}"][correct_answer]

            if answer == correct_answer:
                correct_answers += 1

            explanation_string += f"""

{problem}

Your answer: {answer}

Correct answer: {correct_answer}

Explanation: {correct_explanation}


"""

        full_string = (
            f"""You got {correct_answers} correct out of {numberquestions} questions.
        
        """
            + explanation_string
        )
        return [full_string, {"display": "block"}]


@app.callback(
    [
        Output("download-answer-key", "data"),
        Output("file-number", "children"),
        Output("download-confirm-answer-key", "children"),
    ],
    [Input("download_quiz_button", "n_clicks")],
    [State("return-score", "children")],
)
def download_answers(n_clicks, answerkeystring):

    if n_clicks == 0:
        return ["", "", ""]
    else:
        fm.remove_old_files("saved_files")
        now = datetime.timestamp(datetime.now())
        fm.create_answer_key(answerkeystring, now)
        exam_title = f"saved_files/taxquiz.{now}.docx"

        return [dcc.send_file(exam_title), f"{now}", "Your answer key has downloaded."]


@app.callback(
    [
        Output("quiz_button", "n_clicks"),
        Output("quiz_submit_button", "n_clicks"),
        Output("download_quiz_button", "n_clicks"),
        Output("quiz-type-dropdown-id", "value", allow_duplicate=True),
        Output("number-questions", "value"),
    ],
    [Input("quiz_reset_button", "n_clicks")],
    [State("file-number", "children")],
    prevent_initial_call=True,
)
def reset_quiz(n_clicks, titlenumberstring):
    if titlenumberstring:
        exam_title = f"saved_files/taxquiz.{titlenumberstring}"
        os.remove(f"{exam_title}.docx")
        os.remove(f"{exam_title}.md")
    return [0, 0, 0, "", ""]


def parse_contents(contents):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    return pd.ExcelFile(io.BytesIO(decoded))


def parse_contents_code_book(contents):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    return decoded


@app.server.route("/download/<path:path>")
def serve_file_in_dir(path):
    if not os.path.isfile(path):
        path = os.path.join("saved_code", path)

    return send_from_directory(os.path.dirname(path), os.path.basename(path))

@app.callback(
    [
        Output("upload-confirm-all", "children"),
        Output("after-book-options", "style"),
        Output("interval-component", "disabled", allow_duplicate=True),
        Output("processing-flag", "data", allow_duplicate=True),
    ],
    [Input("upload-data-all", "contents")],
    [
        State("submitfile-all", "n_clicks"),
        State("docs-dropdown", "value"),
        State("page-number-input", "value"),
    ],
    prevent_initial_call=True,
)
def create_code_regs(contents, nclicks, docsdropdown, pagenumbers):
    if contents is not None and contents != "" and nclicks > 0:
        fm.remove_old_files("saved_code")
        fm.remove_old_files("CodeRegs/FilesForBook")
        
        full_file = parse_contents_code_book(contents)
        full_file_b64 = base64.b64encode(full_file).decode("utf-8")
        now = datetime.timestamp(datetime.now())
        book_title = f"SelectedSections.{now}"
        
        with open(fm.counter_file, "a") as f:
            f.write(f"\n{now}")
        
        pagenumber = 1 in pagenumbers
        
        # Direct call instead of Celery task
        excel_file = io.BytesIO(base64.b64decode(full_file_b64))
        all_errors, footer_error = cc.create_code_book(
            book_title, excel_file, now, docsdropdown, pagenumber
        )

        if all_errors.startswith("ROW_LIMIT:"):
            return [f"Your request contains too many sections. For performance reasons, please limit requests to 250 total sections (Code and regulations combined) at a time.",  {"display": "block"}, True, False]
        
        download_link = f"/download/saved_code/{book_title}.pdf"
        
        if len(all_errors) > 3:
            reg_error = f"I could not find the following sections: {all_errors}."
        else:
            reg_error = ""
        
        if len(all_errors) > 3 or len(footer_error) > 1:
            message = f"Your file was mostly processed successfully. However, I encountered the following issues. {reg_error} {footer_error}\n\n[Download your Selected Sections book]({download_link})"
        else:
            message = f"Your file was processed successfully.\n\n[Download your Selected Sections book]({download_link})"
        
        return [message, {"display": "block"}, True, False]  # Stop interval, clear processing flag
    
    return ["", {"display": "none"}, True, False]

@app.callback(
    [
        Output("submitfile-all", "n_clicks"),
        Output("upload-confirm-all", "children", allow_duplicate=True),
        Output("docs-dropdown", "value"),
        Output("upload-data-all", "contents"),
        Output("reset-state", "data", allow_duplicate=True),
    ],
    [Input("book_reset_button", "n_clicks")],
    prevent_initial_call=True,
)
def reset_code_book(n_clicks):
    if n_clicks == 0:
        raise PreventUpdate
    else:
        return 0, "", "", "", True


if __name__ == "__main__":
    app.run_server(debug=False)
