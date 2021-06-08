import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import pyodbc
import os
import numpy as np
import pandas as pd
import pprint

#-----------------------------------------------------
#Databae connection

def get_database_connection():
    server = os.environ['DB_SERVER'] 
    database = os.environ['DB_NAME']
    username = os.environ['DB_USER']
    password = os.environ['DB_PASSWD']
    #print(os.environ['PATH'])
    cnxn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
    cnxn = pyodbc.connect(cnxn_string)
    cursor = cnxn.cursor()
    
    return cnxn, cursor

cnxn, cursor = get_database_connection()

#-------------------------------------------
# Databae functions

def get_page_list():
    
    query = 'SELECT * FROM [PAGES]'
    out =  np.asarray(pd.read_sql(query, cnxn)['TITLE'])
    return out



def get_page_tag_list(page):
    query = f"SELECT * FROM PAGE_TAG WHERE PAGE = '{page}'"
    out= np.asarray(pd.read_sql(query, cnxn)['TAG'])
    return out


def get_page_card_list(page):
    query = f"SELECT * FROM PAGE_CARD WHERE PAGE = '{page}'"
    out = np.asarray(pd.read_sql(query, cnxn)['CARD'])
    return out


def get_page_card_list_by_tag_list(page, tag_list):
     card_list = get_page_card_list(page, cnxn)
     if len(tag_list) == 1:
         tag_list.append('')
     query = f"SELECT * FROM CARD_TAG WHERE CARD IN {tuple(card_list)} AND TAG IN {tuple(tag_list)}"
     out =  np.asarray(pd.read_sql(query, cnxn)['CARD'].unique())
     return out
 
 
def get_cards_df_by_card_list(card_list):
    if len(card_list) in [0,1]:
        card_list = list(card_list)
        card_list.append('')
    query = f"SELECT * FROM CARDS WHERE TITLE IN {tuple(card_list)}"
    out =  pd.read_sql(query, cnxn)
    return out

#------------------------------------------------------------------
 #App initialization


FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"

app = dash.Dash(
    __name__,
    #requests_pathname_prefix="/Bio/",

            meta_tags=[
                {"name": "viewport", "content": "width=device-width, initial-scale=1"}
            ],
            external_stylesheets=[dbc.themes.FLATLY, FONT_AWESOME],
      )

#----------------------------------------------------------------
# Navbar

#TODO: Need to check if the navbar can collapse after clicking

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="Home")),
        dbc.NavItem(dbc.NavLink("Skills", href="Skills")),
        dbc.NavItem(dbc.NavLink("Experience", href="Experience")),
        dbc.NavItem(dbc.NavLink("Cetifications", href="Certifications")),
        dbc.NavItem(dbc.NavLink("Projects", href="Projects")),
        dbc.NavItem(dbc.NavLink("Demos", href="Demos")),
        dbc.NavItem(dbc.NavLink("Publications", href="Publications")),
        dbc.NavItem(dbc.NavLink("Resources", href="Resources")),
        dbc.NavItem(dbc.NavLink("Contact", href="Contact")),

    ],
        
    brand="Machines Do Learn",
    brand_href="home",
    color="primary",
    dark=True,
    sticky='top',
    fluid=True,
)

#---------------------------------------------------------------
# Main app footer

#TODO: Need to fix allignment of the icons make them centered

app_footer =  dbc.Row(
            [
                dbc.NavLink(href="https://www.linkedin.com/in/yadav-abhimanyu/", children=[html.I(className="fab fa-linkedin-in")]),
                dbc.NavLink(href="https://github.com/abhimanyu-yadav-1985", children=[html.I(className="fab fa-github")]),
                dbc.NavLink(href="https://yadav-manyu.medium.com/", children=[html.I(className="fab fa-medium")])
            ], align="center")

#---------------------------------------------------------------
# main app layout

app.layout= html.Div(
    [
        dcc.Location(id='url', refresh=False),
        navbar,
        html.Br(),
        html.Div(id='page-content'),
        html.Hr(),
        app_footer
    ]
)

#-------------------------------------------------------------
#TODO: ability to handle video cards
def make_card(title, header, description, footer, img, className, link_1_text, link_1, link_2_text, link_2, medium):
    children = []
    if header != 'NA':
        children.append(dbc.CardHeader(header))
    if img != 'NA':
        children.append(dbc.CardImg(src=img, top=True))
    
    children_cbody = []
    children_cbody.append(html.H4(title, className="card-title"))
    if description !='NA':
        children_cbody.append(html.P(description, className="card-text"))
        
    if link_1_text != 'NA':
        children_cbody.append(dbc.CardLink(link_1_text, href=link_1))
    
    if link_2_text!='NA':
        children_cbody.append(dbc.CardLink(link_2_text, href=link_2))
        
    children.append(dbc.CardBody(children=children_cbody))
    
    if footer!='NA':
        children.append(dbc.CardFooter(footer))
        
    card = dbc.Card(children=children, className = className)
    
    return card


def make_card_list(cards_df):
    card_list = []
    for _, row in cards_df.iterrows():
        title = row.TITLE
        header = row.HEADER
        description = row.DESCRIPTION
        img = row.IMAGE_NAME
        footer = row.FOOTER
        className = f'card text-black border-{row.STYLE} mb-3'
        link_1_text = row.LINK_1_NAME
        link_1 = row.LINK_1
        link_2_text = row.LINK_2_NAME
        link_2 = row.LINK_2
        medium = row.MEDIUM
        active = row.ACTIVE
        if active == 'y':
            card_list.append(make_card(
                title=title, header=header,
                footer=footer, img=img,
                description=description,
                className=className,
                link_1_text=link_1_text,
                link_1=link_1,
                link_2=link_2,
                link_2_text = link_2_text,
                medium=medium))
    
    return card_list


def get_card_layout(cards_df):
    return dbc.CardColumns(make_card_list(cards_df))


def get_page_content_without_filter(page):
    card_title_list = get_page_card_list(page)
    cards_df = get_cards_df_by_card_list(card_title_list)
    if len(cards_df) == 0:
        return html.H1('No Card Found')
    return get_card_layout(cards_df)


def get_page_content_with_filter():
    return html.Div('MaKe Filered page')

def get_home_page():
    return html.Div('MaKe Home to check')

def get_contact_page():
    return html.Div('Make Contact')



pages_with_filter = ['Resources']

def get_page_content(page):
    page_list = get_page_list()
    if page in page_list:
        if page in pages_with_filter:
            return get_page_content_with_filter(page)
        else:
            return get_page_content_without_filter(page)
    elif page == 'Home':
        return get_home_page()
    elif page == 'Contact':
        return get_contact_page()
    else:
        return html.H1('404 Page Not Found')
    

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    page = pathname.split('/')[1]
    #return get_page_content(page)
    return get_page_content(page)
    
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='80')