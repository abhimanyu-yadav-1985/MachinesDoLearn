import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, state
import pyodbc
import os



FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"

app = dash.Dash(
    __name__,
    #requests_pathname_prefix="/Bio/",

            meta_tags=[
                {"name": "viewport", "content": "width=device-width, initial-scale=1"}
            ],
            external_stylesheets=[dbc.themes.FLATLY, FONT_AWESOME],
      )

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="home")),
        dbc.NavItem(dbc.NavLink("Skills", href="skills")),
        dbc.NavItem(dbc.NavLink("Experience", href="experience")),
        dbc.NavItem(dbc.NavLink("Cetifications", href="certifications")),
        dbc.NavItem(dbc.NavLink("Projects", href="projects")),
        dbc.NavItem(dbc.NavLink("Demos", href="projects")),
        dbc.NavItem(dbc.NavLink("Articles", href="articles")),
        dbc.NavItem(dbc.NavLink("Education", href="education")),
        dbc.NavItem(dbc.NavLink("Contact", href="#")),

    ],
        
    brand="Machines Do Learn",
    brand_href="home",
    color="primary",
    dark=True,
    sticky='top',
    fluid=True,
)

layout= html.Div(
    [
        dcc.Location(id='url', refresh=False),
        navbar,
        html.Br(),
        html.Div(id='page-content')
    ]
)

def make_card(title, header, description, footer, img, className):
    if img=='':
        img = 'test.jpg'

    card = dbc.Card(
            [
                dbc.CardHeader(header),
                dbc.CardImg(src=app.get_asset_url(img), top=True),
                dbc.CardBody(
                    [
                        html.H4(title, className="card-title"),
                        html.P(description, className="card-text"),
                    ]
                ),
                dbc.CardFooter(footer),
            ], className = className
        )
    
    return card


def make_card_list(card_dict):
    card_list = []
    titles = list(card_dict.keys())
    for title in titles:
        content = card_dict[title]
        header = content['header']
        description = content['description']
        footer = content['footer']
        img = content['img']
        className = content['className']
        card_list.append(make_card(
            title=title, header=header,
            footer=footer, img=img,
            description=description,
            className=className))
    
    return card_list


def get_card_layout(cards):
    return dbc.CardColumns(make_card_list(cards))

def get_page_cards(page):
    pass

def get_page_tags(page):
    pass

def make_tag_drop_down(tags):
    pass

def get_page_content(page):
    page_tags = get_page_tags(page)
    page_cards = get_page_cards(page)
    layout = html.Div(children = [
        dbc.Row([dbc.Col(make_tag_drop_down(page_tags))]),
        dbc.Row([dbc.Col(get_card_layout(page_cards))])
    ])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    page = pathname.split('/')[1]
    return get_page_content(page)
    


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='8080')