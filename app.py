import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_trich_components as dtc

from dash.dependencies import Output, Input

import yaml
import urllib
import os

CARD_PATH = os.environ['CARD_PATH']
STACK_PATH = os.environ['STACK_PATH']
ABOUT_PATH = os.environ['ABOUT_PATH']

card_data = yaml.safe_load(urllib.request.urlopen(CARD_PATH))
stacks_data = yaml.safe_load(urllib.request.urlopen(STACK_PATH))
about_data = yaml.safe_load(urllib.request.urlopen(ABOUT_PATH))

external_stylesheets = [
    dbc.themes.FLATLY,
    'https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick.css',
    'https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;700&display=swap',
    'https://fonts.googleapis.com/css2?family=Squada+One&display=swap',
    'https://use.fontawesome.com/releases/v5.8.1/css/all.css']

external_scripts = [
    'https://code.jquery.com/jquery-3.5.1.min.js',
    'https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick.min.js']

meta_tags = [
    {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, maximum-scale=1",
    }]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    meta_tags=meta_tags)

app.title = "Machines Do Learn"

server = app.server

#---------------------------------------------------------------------------------
def About():
    about = html.Div([
        html.Div([
            html.H4(
                "Abhimanyu",
                className="font-xl bold letter_spac8 default_inverse"
            ),
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                                about_data['para1'], 
                                html.Br(), 
                                html.Br(),
                                about_data['para2']
                            ],
                            className="font-sm",
                        )
                    ], lg=12, sm=12),
                ]),
            ], className="about_content padding32")
        ], className="terciary_bg radius8 relative about")
    ], className="padding16")
    return about
#---------------------------------------------------------------------------------
def Stacks():
    stacks = html.Div([
        dtc.Carousel([
            html.Div(
                html.Img(alt=i['name'], src=i['image']),
                className="item padding16 margin16 radius8 white_bg"
            ) for i in stacks_data
        ],
            slides_to_scroll=1,
            swipe_to_slide=True,
            autoplay=True,
            speed=2000,
            variable_width=True,
            center_mode=True,
            responsive=[
            {
                'breakpoint': 991,
                'settings': {
                    'arrows': False
                }
            }
        ])
    ], className="stacks padding16")

    return stacks
#---------------------------------------------------------------------------------
def Card(image, title, description, link, badge, git):

    card = dbc.Col(
        html.Div([
            html.A(
                html.Div(
                    html.Img(src=image, alt=title),
                    className="bottom16 portfolio_card_img"),
                href=link, target="_blank"
            ),
            html.Div([
                html.H4(title, className="font-sm bold uppercase"),
                html.P(description, className="font-xs"),
            ], className="portfolio_card_text bottom16"),
            html.Div([
                html.Div([
                    html.Div(
                        dbc.Badge(
                            i, className="mr-1 self_center default_inverse primary_bg"),
                        className="inline-block"
                    ) for i in badge
                ]),
                html.A(
                    html.I(className="fab fa-github font-sm terciary"),
                    href=git, target="_blank"),
            ], className="font-xs flex_row_btw portfolio_card_footer")
        ], className="second_bg padding16 radius8 portfolio_card"),
        className="padding16", lg=4, md=6, sm=6, xs=12
    )
    return card
#---------------------------------------------------------------------------------
def Footer():
    app_footer =  dbc.Row(
            [
                dbc.NavLink(href="https://www.linkedin.com/in/yadav-abhimanyu/", children=[html.I(className="fab fa-linkedin-in")]),
                dbc.NavLink(href="https://github.com/abhimanyu-yadav-1985", children=[html.I(className="fab fa-github")]),
                dbc.NavLink(href="https://yadav-manyu.medium.com/", children=[html.I(className="fab fa-medium")])
            ])

    footer = html.Div(
        html.Div(
            dbc.Row([
                dbc.Col([
                    html.Div(
                        'Contact', className="uppercase bold font-xs padding4"),
                    html.Div(
                        html.A(
                            'yadav.manyu@gmail.com',
                            href="mailto:yadav.manyu@gmail.com",
                            target="_blank"
                        ), className="padding4"),
                ], lg=12, width=12),
                app_footer
            ], className="padding16"),
            className="terciary_bg radius8"),
        className="padding32 default_inverse footer font-sm")

    return footer
#---------------------------------------------------------------------------------
def NavBar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="Home")),
            dbc.NavItem(dbc.NavLink("Projects", href="Projects")),
            dbc.NavItem(dbc.NavLink("Articles", href="Articles")),
        ],
            
        brand="Machines Do Learn",
        brand_href="home",
        color="primary",
        dark=True,
        sticky='top',
        fluid=True)
    return navbar
#---------------------------------------------------------------------------------
app.layout= html.Div(
    [
        dcc.Location(id='url', refresh=False),
        NavBar(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div(id='page-content'),
        html.Hr(),
        Footer()
    ])
#---------------------------------------------------------------------------------
def make_cards(card_list):
    portfolio = html.Div([
        dbc.Row([
            Card(i['image'], i['title'], i['description'], i['link'], i['badges'], i['git']) for i in card_list
        ], className="portfolio")
    ])
    return portfolio

def make_home_page():
    portfolio_cards = []
    for card in card_data:
        if card['feature'] == 1:
            portfolio_cards.append(card)
            
    featured = make_cards(portfolio_cards)
    
    body = dbc.Container(
        [
            About(),
            Stacks(),
            featured,
        ], className="top32")

    return body

def make_porfolio_page(page):
    portfolio_cards = []
    for card in card_data:
        if card['page'] == page:
            portfolio_cards.append(card)
            
    featured = make_cards(portfolio_cards)
    
    body = dbc.Container(
        [
            dbc.Row(
            [
             html.H4(page)
            ], justify="center", align="center", className="h-50"
            ),
            html.Hr(),
            featured,
        ], className="top32")

    return body
    
def get_page_content(page):
    
    if page in ['','Home']:
        return make_home_page()
    elif page == 'Projects':
        return make_porfolio_page('Projects')
    elif page == 'Articles':
        return make_porfolio_page('Articles')
    else:
        return html.H1('404 Page Not Found')
    
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    page = pathname.split('/')[1]
    #return get_page_content(page)
    return get_page_content(page)

if __name__ == "__main__":
    app.run_server(debug=True)
