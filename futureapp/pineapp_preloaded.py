"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config
from typing import List
import reflex as rx

import os, glob, json, shutil
from time import sleep
import subprocess
import re
import pandas as pd
from io import StringIO

import random
from PIL import Image
import urllib.request


# Introjs trial
# class IntroSteps(rx.Component):
#     library = "intro.js-react"
#     tag = "Steps"
#     initialStep: rx.Var[int]
#     initialStep: 0

#     @classmethod
#     def get_controlled_triggers(cls) -> dict[str, rx.Var]:
#         return {"on_change": rx.EVENT_ARG}




filename = f"{config.app_name}/{config.app_name}.py"
colindex = 0
accent_color = "#a883ed"
style = {

    "background" : "rgb(250, 250, 250)",
    # "font_family": "AirCerealMedium",
    # "font_family": "'Ariel', sans-serif",
    "font_size": "16px",
    # "font_weight": "",    
    "::selection": {
            "background_color": accent_color,
        },  
    "th" : {
            "background":"linear-gradient(45deg,#e6e4fc,#fceded)",  
    },
#Disco button


#Disco Button


    rx.ResponsiveGrid: {
        "animation": "fadeInAnimation ease 3s",
        "animation-iteration-count": "1",
        "animation-fill-mode": "forwards",
    },

    rx.Heading: {
        # "font_size": "32px",
        "font_family": "AirCereal",
        # "font_family": "'Ariel', sans-serif",
        "font_weight": "700",
        "color": "#a61d55",
    },
    rx.Text: {
        "font_family": "AirCerealNormalText",
        "line-height" : "1.7",
        # "font_weight": "100",
        "font_size": "16px",
        "font-weight": "normal",
        # "font-variant": "normal"
    },
    rx.Card: {
        "border-radius" : "16px",
        # "box-shadow" : "5px 10px",
        # "box-shadow" : "rgb(204, 219, 232) 3px 3px 6px 0px inset, rgba(255, 255, 255, 0.5) -3px -3px 6px 1px inset;"
        "box-shadow" : "6px 6px 12px #b8b9be,-6px -6px 12px #fff!important",
        "padding" : "10px 20px",
        "margin" : "10px 20px",
        # "background" : ""
    },
    rx.Badge: {
        "padding" : "10px 20px!important",
        "margin" : "10px 20px!important",   
        "text-transform" : "lowercase!important",
        "border-radius" : "5px!important",
        "box-shadow" : "5px 5px #000000!important",
    },
    rx.Slider: {
        "height": "5px",
        "overflow": "hidden",
        "background": "#fff",
        # "border" : "1px solid #29d",
    },

    rx.DataTable: {
        "background": "linear-gradient(45deg,#e6e4fc,#fceded)",
    }
    # rx.SliderFilledTrack: {
	# "position": "absolute",
	# "top": "0",
	# "right": "100%",
	# "height": "5px",
	# "width": "100%",
	# "background": "#29d",
    # }    
}


class ArticleData:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.data_file = os.path.join(self.data_dir, 'articles.json')
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump([], f)

    def store_article(self, article):
        """
        Store article data to json file
        """
        with open(self.data_file, 'r+') as f:
            articles = json.load(f)
            articles.append(article)
            f.seek(0)           # reset file position to the beginning.
            json.dump(articles, f, indent=4)

    def get_articles(self):
        """
        Fetch all articles from json file
        """
        with open(self.data_file, 'r') as f:
            articles = json.load(f)
            return articles
    def delete_articles(self,article_url):
        """
        Delete a specific article from json file
        """        
        with open(self.data_file, 'r+') as f:
            articles = json.load(f)
            articles = [article for article in articles if article['url'] != article_url]
            f.seek(0)           # reset file position to the beginning.
            f.truncate()        # remove existing file content.
            json.dump(articles, f, indent=4)        



article_data = ArticleData()
articles = article_data.get_articles()
a_options : List[str] = [datavalue['url'] for datavalue in articles]

b_options = []





class State(rx.State):
    # The colors to cycle through.
    global a_options
    colors: List[str] = [
        "black",
        "red",
        "green",
        "blue",
        "purple",
    ]
    # selected_option_a: str = "No selection yet."
    selected_option_a: str = a_options[0]
    text: str = "Enter Page url"
    processing = False
    complete = False
    error_occured = False
    image_url = ""
    model_tags = ""
    model_caption = ""
    alert_msg = ""
    alert_show: bool = False
    alert_msg_header = ""
    article_text = ""
    article_title = ""
    model_tag_list: List[str] = ['1','2']
    # The index of the current color.
    index: int = 0
    df = pd.DataFrame([[]])
    df1 = pd.DataFrame([[]])
    pff1 = ""
    pfl1 = ""
    df2 = pd.DataFrame([[]])
    pff2 = ""
    pfl2 = ""
    df3 = pd.DataFrame([[]])
    pff3 = ""
    pfl3 = ""
    df4 = pd.DataFrame([[]])
    pff4 = ""
    pfl4 = ""
    df5 = pd.DataFrame([[]])
    pff5 = ""
    pfl5 = ""
    df6 = pd.DataFrame([[]])
    pff6 = ""
    pfl6 = ""

    #Openai model outputs
    iab_safety_response_msg = ""
    iab_response_msg = ""
    global_brands_response_msg = ""
    indian_brands_response_msg = ""
    web_inventory_response_msg = ""
    ind_web_response_msg = ""
    news_response_msg = ""
    news_ind_response_msg = ""
    sentiment_filled_bg = "red"
    sentiment_empty_bg = "green.100"
    sentiment_color = sentiment_empty_bg.split('.')[0]
    sentiment_value = 0
    sff1 = ""
    sentiment_disp_value = 0
    keyword_list = pd.DataFrame([[]])
    # keyword_list: List[str] = [["1"]]
    

    def next_color(self):
        """Cycle to the next color."""
        self.index = (self.index + 1) % len(self.colors)

    @rx.var
    def color(self) -> str:
        return self.colors[self.index]
    
    def clear_text(self):
        # import pdb;pdb.set_trace()
        self.text = ""    

    def run_analysis(self):
        print("Start new analysis")
        screendata = {}
        global model
        global articles
        removestatus = [os.remove(file) for file in glob.glob('downloads/*')]
        removestatus = [os.remove(file) for file in glob.glob('assets/mainimage*')]
        self.processing,self.complete = False,False
        yield
        self.text = self.selected_option_a
        if self.text == "Select an example." or self.text == "No selection yet." or self.text == "":
            self.alert_msg_header = "Error"
            self.alert_msg = "Please select a url link"
            self.alert_change()
            self.processing,self.complete = False,False
            yield
            return   
        sleep(2)
        self.processing,self.complete = True,False
        self.iab_safety_response_msg = ""
        self.iab_safety_response_msg = ""
        self.iab_response_msg = ""
        self.global_brands_response_msg = ""
        self.indian_brands_response_msg = ""
        self.web_inventory_response_msg = ""
        self.ind_web_response_msg = ""
        self.news_response_msg = ""
        self.news_ind_response_msg = ""
        self.sentiment_filled_bg = "red"
        self.sentiment_empty_bg = "green.100"
        self.sentiment_value = 0
        self.sff1 = ""
        self.sentiment_disp_value = 0        
        for article in articles:
            if article['url'] == self.selected_option_a:
                screendata = article
                break
        # print(screendata) 
        article_image = screendata["image"]
        imgpost = article_image.split('.')[-1]
        article_title = screendata["title"]
        print(f"Article image file is - {article_image}")
        try:
            # urllib.request.urlretrieve(article_image,f"downloads/mainimage.{imgpost}")
            os.system(f"wget {article_image} -O downloads/mainimage.jpg")
            # list_uploaded_file = wget.download(article_image)
            list_uploaded_file = f"downloads/mainimage.{imgpost}"
            uploaded_file = list_uploaded_file    
            ui_uploaded_file = f'mainimage.{imgpost}'    
            shutil.move(uploaded_file,f'assets/{ui_uploaded_file}')
            uploaded_file = "assets/"+ui_uploaded_file
        except IndexError as error:
            print("Image file doesnt exist")
            uploaded_file = "doesntexist.txt"  
        except Exception as error:  
            print(error)
            uploaded_file = "doesntexist.txt"  
        if article_title and os.path.exists(uploaded_file):
            print("Main Execution")
            # image = Image.open(uploaded_file)
            
            # self.image_url = ui_uploaded_file 
            print(uploaded_file)
            self.processing,self.complete = False,True
            image = Image.open(uploaded_file)
            self.image_url = image 
            self.article_title = article_title
            self.article_text = screendata["text"]
    
            self.model_tag_list =  screendata["tags"]
            self.model_caption = screendata["caption"]
            # import pdb;pdb.set_trace()

            try: 
                self.sff1 = screendata["sff1"]

                self.keyword_list = pd.DataFrame(screendata["keyword_list"])

                self.sentiment_disp_value = screendata["sentiment_disp_value"]

                self.sentiment_value = int(self.sentiment_disp_value * 10)
                self.sentiment_disp_value = f"{self.sentiment_value}%"
                self.sentiment_filled_bg = screendata["sentiment_filled_bg"]
                self.sentiment_empty_bg = screendata["sentiment_empty_bg"]   
                self.sentiment_color = screendata["sentiment_empty_bg"].split('.')[0]
                print(f"Sentiment color is {self.sentiment_color}")

            except Exception as error:
                print(error)
                try:
                    self.iab_safety_response_msg = screendata["sff1"]
                except:
                    print(error)
            yield
            # st.info(f'X-rae Response -  {iab_response_msg["content"]}')

            print("Get IAB Categories")
            try:
                self.df = pd.DataFrame(screendata["df"])  
            except Exception as error:
                print(error)
                self.error_occured = True
                self.iab_response_msg = screendata["df"]
            # self.iab_response_msg = iab_response_msg["content"]
            yield

            print("Get Brands")
            try:
                self.pff1 = screendata["pff1"]

                self.df1 = pd.DataFrame(screendata["df1"]) 
                # screendata['df1'] =  data

                # Extract the last paragraph
                self.pfl1 = screendata["pfl1"]
            except Exception as error:
                print(error)
                self.pff1 = screendata["pff1"]
            yield    

            print("Indian Brands")
            try:
                self.pff2 = screendata["pff2"]
                self.df2 = pd.DataFrame(screendata["df2"]) 
                # screendata['df2'] =  data
                # Extract the last paragraph
                self.pfl2 = screendata["pfl2"]
            except Exception as error:
                print(error)
                self.pff2 = screendata["pff2"]
            yield

            print("Websites")
            try:
                # Extract the first paragraph
                self.pff3 = screendata["pff3"]

                # Extract the table content                          
                self.df3 = pd.DataFrame(screendata["df3"]) 
                # screendata['df3'] =  data

                # Extract the last paragraph
                self.pfl3 = screendata["pfl3"]
            except Exception as error:
                print(error)
                self.pff3 = screendata["pff3"]
            yield  

            print("Indian Websites")
            try:
                 # Extract the first paragraph
                self.pff4 = screendata["pff4"]

                self.df4 = pd.DataFrame(screendata["df4"]) 
                # screendata['df4'] =  data
                # Extract the last paragraph
                self.pfl4 = screendata["pfl4"]
            except Exception as error:
                print(error)
                self.pff4 = screendata["pff4"]
            yield

            print("News")
            try:
                # Extract the first paragraph
                self.pff5 = screendata["pff5"]

                # Extract the table content                       
                self.df5 = pd.DataFrame(screendata["df5"]) 
                # screendata['df5'] =  data

                # Extract the last paragraph
                self.pfl5 = screendata["pfl5"]
            except Exception as error:
                print(error)
                self.pff5 = screendata["pfl5"]
            yield

            print("News India")        
            try:
                # Extract the first paragraph
                self.pff6 = screendata["pff6"]

                # Extract the table content
                self.df6 = pd.DataFrame(screendata["df6"]) 
                # screendata['df6'] =  data

                # Extract the last paragraph
                self.pfl6 = screendata["pfl6"]        
            except Exception as error:
                print(error)
                self.pff6 = screendata["pff6"]
            yield
            return True               
            # st.info(f'X-rae Response -  {news_ind_response_msg["content"]}')        
                
        elif uploaded_file == "parisingerror":
            self.alert_msg_header = "Error"
            self.alert_msg = "Failed to parse url"
            self.alert_change()
            self.processing,self.complete = False,False
            yield                
        elif not os.path.exists(uploaded_file):
            self.alert_msg_header = "Error"
            self.alert_msg = "Failed to load image"
            self.alert_change()
            self.processing,self.complete = False,False
            yield
            # return rx.window_alert("Failed to load image")
            # st.error("Failed to load image")
        elif not article.title:
            self.alert_msg_header = "Error"
            self.alert_msg = "Failed to load data file"
            self.alert_change()
            self.processing,self.complete = False,False
            yield            
            # return rx.window_alert("Failed to load data file ")
            # st.error("Failed to load data file ") 
        else:
            self.alert_msg_header = "Error"
            self.alert_msg = "Unknown Error"
            self.alert_change()
            self.processing,self.complete = False,False
            yield            
            # return rx.window_alert("Failed to load data file ")
            # print(f"Files not found - {uploaded_file} - 'out.json'")      

    def alert_change(self):
        self.alert_show = not (self.alert_show)

def tag_list(tag: str):
#       display: inline-block;
#   margin: 6px;
#   font-size: inherit;
#   line-height: 1.42;
#   padding: 0.7em 1.4em;
#   font-weight: normal;
#   border-width: 1px;
#   border-style: solid;
#   background: transparent;
#   border-radius: 1.41em;
#   cursor: pointer;
#   font-family: "Booster Next FY", "Avenir Next", Avenir, sans-serif;
#   user-select: none;
#   vertical-align: bottom;
    # index = random.randint(0,4)
    global colindex
    # import pdb;pdb.set_trace()
    if colindex == 0:
        colindex = 1
    else:
        colindex = 0
    print(f"Color index is {colindex}")

    colorval = ["#a61d55","#991BE2"]
    return rx.badge(
            tag, variant="solid",
            background="transparent",
            line_height="1.42",
            # bg="#fff",
            color=f"{colorval[colindex]}",##991BE2
            border_color=f"{colorval[colindex]}",##991BE2
            border_width="1px",
            border_style= "solid",
            font_size="1em",
            font_weight="normal",
            text_transform = "lowercase",
            border_radius = "1.41em",
            cursor = "pointer",
            # box_shadow = "5px 5px #000000",
            margin = "6px",
            padding = "0.7em 1.4em"
        )

def colored_box(color: str):
    return rx.box(rx.text(color), bg=color)



def index() -> rx.Component:
    return rx.fragment(
        rx.hstack(
            rx.image(src="https://citrusberry.biz/assets/img/menu_logo1.png", width="41px", height="auto"),
            rx.image(src="https://citrusberry.biz/assets/img/menu_logo.png", width="90px", height="auto"),
            padding="10px",
            margin="5px",
        ),
        # rx.color_mode_button(rx.color_mode_icon(), float="right"),
        rx.vstack(
            rx.tooltip(
                rx.card(  
                    rx.center(
                        rx.image(src="logo-no-background.png", width="200px", height="auto"),
                    #     rx.heading("X-Rae Output", size="xl", color="#fb5e78"),
                    # border_radius="15px",
                    # border_width="thick",
                    width="100%",
                    # border_color="#fb5e78",
                    ), 
                ),                       
                # background="linear-gradient(90deg, #ff5c72, #a485f2)",
            # rx.heading("Contextual AI Demo!", font_size="2em",color="#a61d55",),
            label="Please select a link and Click on Analyze",
            ),         
            rx.alert_dialog(
                rx.alert_dialog_overlay(
                    rx.alert_dialog_content(
                        rx.alert_dialog_header(State.alert_msg_header),
                        rx.alert_dialog_body(
                            State.alert_msg
                        ),
                        rx.alert_dialog_footer(
                            rx.button(
                                "Close",
                                on_click=State.alert_change,
                            )
                        ),
                    )
                ),
                is_open=State.alert_show,
            ),            
            # rx.box("Get started by editing ", rx.code(filename, font_size="1em")),
                rx.center(
                    rx.tooltip(
                        rx.icon(
                                tag="link",margin_right="10px",on_click=rx.set_clipboard(State.selected_option_a),
                                ),
                    label="Copy Link",
                    ),      
                    rx.tooltip(
                        rx.select(
                            a_options,
                            # placeholder="Select an example.",
                            on_change=State.set_selected_option_a,
                        ),
                    label="Please select a link and Click on Analyze",
                    ),                      
                    width="1000px"    
                ),
                      
            rx.hstack(
                # rx.button(
                #     "Clear", on_click=State.clear_text,width="100%",
                # ),  
                rx.html("""
                        <button class='btn-101'>
                        Analyse
                        <svg>
                            <defs>
                            <filter id='glow'>
                                <fegaussianblur result='coloredBlur' stddeviation='5'></fegaussianblur>
                                <femerge>
                                <femergenode in='coloredBlur'></femergenode>
                                <femergenode in='coloredBlur'></femergenode>
                                <femergenode in='coloredBlur'></femergenode>
                                <femergenode in='SourceGraphic'></femergenode>
                                </femerge>
                            </filter>
                            </defs>
                            <rect />
                        </svg>
                        </button>                      
                        """,on_click=State.run_analysis),
                #rx.button(
                #    "Analyze", on_click=State.run_analysis,is_loading=State.processing,width="100%",
                #    background_image="linear-gradient(90deg, #ff5c72, #a485f2)",
                #),                

            ),
            rx.cond(
                State.complete,
                    rx.responsive_grid(        
                     rx.vstack(
                        # rx.divider(border_color="#a61d55"),
                        rx.heading(State.article_title, size="lg",margin="30px",
                                   ),
                        # rx.hstack(
                        rx.responsive_grid(        
                            rx.card(
                                rx.center(
                                    rx.image(
                                    src=State.image_url,
                                    height="25em",
                                    width="37.5em",
                                    ), 
                                border_radius="10px",
                                border_width="2px",
                                border_color="#a61d55",
                                width="100%",
                                ),
                                header=rx.heading("Article Image", size="lg"),
                                # footer=rx.heading("Footer", size="sm"),
                            ), 
                            rx.card(
                                rx.text(State.article_text),
      
                                header=rx.heading("Article Text", size="lg"),
                                # footer=rx.heading("Footer", size="sm"),
                            ), 
                            columns=[2],
                            spacing="4",                                                                 
                        ),
                        #Image caption output Card
                        # rx.responsive_grid(
                        #     rx.divider(border_color="#a61d55"),
                        #     rx.card(  
                        #         rx.center(
                        #             rx.hstack(
                        #                 rx.foreach(State.model_tag_list,tag_list),rx.spacer(),
                        #                 # rx.center(
                        #                 #     rx.divider(
                        #                 #         orientation="vertical", border_color="black"
                        #                 #     ),
                        #                 #     height="4em",
                        #                 # ),                            
                        #                 # rx.foreach(State.colors, colored_box),
                        #                 # rx.span(State.model_caption, font_weight="bold"),
                        #                 # rx.span(State.model_caption),
                        #             ),
                        #         ),
                        #         background="linear-gradient(45deg,#e4fcf2,#fceded)",
                        #     ),
                        #     # rx.divider(border_color="black"),
                        #     columns=[1],
                        #     spacing="4",    
                        #     width="100%",
                        # ),
                        rx.responsive_grid(
                            # rx.divider(border_color="black"),
                            rx.card(  
                                rx.center(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.foreach(State.model_tag_list,tag_list),rx.spacer(),
                                        ),
                                        rx.hstack(
                                            rx.heading(State.model_caption, size="lg", ),
                                        ),
                                    ),
                                ),
                                background="linear-gradient(45deg,#e6e4fc,#fceded)",
                                header=rx.heading("X RAE Image Analysis", size="lg"),
                                
                            ),
                            columns=[1],
                            spacing="4",    
                            width="100%",
                        ),  
                        rx.responsive_grid(
                            # rx.divider(border_color="black"),
                            rx.card(  
                                rx.center(
                                    rx.vstack(
                                        # rx.hstack(
                                        rx.heading(
                                            State.sff1+State.sentiment_disp_value, color=State.sentiment_filled_bg,opacity="0.8"
                                        ),
                                        # ),
                                        # rx.hstack(
                                        rx.progress(value=State.sentiment_value, width="100%",color_scheme=State.sentiment_color,height="15px",bg="#fff",opacity="0.8"),        
                                        # ),
                                        width="75%",
                                    ),
                                ),
                                background="linear-gradient(45deg,#e6e4fc,#fceded)",
                                header=rx.heading("Overall Sentiment", size="lg"),
                                
                            ),
                            columns=[1],
                            spacing="4",    
                            width="100%",
                        ),                                                  
                        rx.responsive_grid(  
                           rx.card(
                                rx.vstack(
                                    # rx.heading(State.sff1),        
                                    # rx.heading(
                                    #     State.sff1+State.sentiment_disp_value, color=State.sentiment_filled_bg
                                    # ),
                                    # rx.progress(value=State.sentiment_value, width="100%",color_scheme=State.sentiment_color,height="15px"),        
                                    # rx.slider(
                                    #     rx.slider_track(
                                    #         rx.slider_filled_track(bg=State.sentiment_filled_bg),
                                    #         bg=State.sentiment_empty_bg,
                                    #         height="5px",
                                    #     ),
                                    #     # rx.slider_thumb(
                                    #     #     rx.icon(tag="star", color="white"),
                                    #     #     box_size="1.5em",
                                    #     #     bg="tomato",
                                    #     # ),
                                    #     # on_change_end=SliderManual.set_end,
                                    #     value=State.sentiment_value,
                                    #     default_value=40,
                                    #     is_disabled=True,
                                    #     height="5px",

                                    # ),           
                                    rx.data_table(
                                        data=State.keyword_list,
                                        pagination=False,
                                        search=False,
                                        sort=False,
                                    ),      
                                    rx.text(State.iab_safety_response_msg),
                            

                                ),
                                header=rx.heading("Keywords", size="lg"),
                                # footer=rx.heading("Footer", size="sm"),
                            ), 

                            rx.card(
                                rx.cond(
                                    State.error_occured,
                                    rx.text(State.iab_response_msg),
                                    rx.data_table(
                                        data=State.df,
                                        # pagination=True,
                                        # search=True,
                                        # sort=True,
                                    ),      
                                ),                                    
                                header=rx.heading("IAB Categories", size="lg"),
                                # footer=rx.heading("Footer", size="sm"),
                            ), 
                            columns=[2],
                            spacing="4",               
                        ),
                        rx.responsive_grid(  
                           rx.card(
                                rx.vstack(
                                    rx.text(State.pff1),
                                    rx.data_table(
                                        data=State.df1,
                                        # pagination=True,
                                        # search=True,
                                        # sort=True,
                                    ),             
                                    rx.text(State.pfl1,font_style="italic"),
                                ),
                                header=rx.heading("Global Brands To Target", size="lg"),
                                # footer=rx.heading("Footer", size="sm"),
                            ), 
                            rx.card(
                                # rx.text(State.indian_brands_response_msg),
                                rx.vstack(
                                    rx.text(State.pff2),
                                    rx.data_table(
                                        data=State.df2,
                                        # pagination=True,
                                        # search=True,
                                        # sort=True,
                                    ),             
                                    rx.text(State.pfl2,font_style="italic"),
                                ),                                
      
                                header=rx.heading("Indian Brands To Target", size="lg"),
                                # footer=rx.heading("Footer", size="sm"),
                            ), 
                            columns=[2],
                            spacing="4",               
                        ),
                        rx.responsive_grid(  
                           rx.card(
                                # rx.text(State.web_inventory_response_msg),
                                rx.vstack(
                                    rx.text(State.pff3),
                                    rx.data_table(
                                        data=State.df3,
                                        # pagination=True,
                                        # search=True,
                                        # sort=True,
                                    ),             
                                    rx.text(State.pfl3,font_style="italic"),
                                ),                                
    
                                header=rx.heading("Website Inventory to target", size="lg"),
                                # footer=rx.heading("Footer", size="sm"),
                            ), 
                            rx.card(
                                # rx.text(State.ind_web_response_msg),
                                rx.vstack(
                                    rx.text(State.pff4),
                                    rx.data_table(
                                        data=State.df4,
                                        # pagination=True,
                                        # search=True,
                                        # sort=True,
                                    ),             
                                    rx.text(State.pfl4,font_style="italic"),
                                ),                                
      
                                header=rx.heading("Indian Website Inventory to target", size="lg"),
                                # footer=rx.heading("Footer", size="sm"),
                            ), 
                            columns=[2],
                            spacing="4",               
                        ),  
                        rx.responsive_grid(  
                           rx.card(
                                # rx.text(State.news_response_msg),
                                rx.vstack(
                                    rx.text(State.pff5),
                                    rx.data_table(
                                        data=State.df5,
                                        # pagination=True,
                                        # search=True,
                                        # sort=True,
                                    ),             
                                    rx.text(State.pfl5,font_style="italic"),
                                ),                                
    
                                header=rx.heading("News Website Inventory to target", size="lg"),
                                # footer=rx.heading("Footer", size="sm"),
                            ), 
                            rx.card(
                                # rx.text(State.news_ind_response_msg),
                                rx.vstack(
                                    rx.text(State.pff6),
                                    rx.data_table(
                                        data=State.df6,
                                        # pagination=True,
                                        # search=True,
                                        # sort=True,
                                    ),             
                                    rx.text(State.pfl6,font_style="italic"),
                                ),      
                                header=rx.heading("Indian News Website Inventory to target", size="lg"),
                                # footer=rx.heading("Footer", size="sm"),
                            ), 
                            columns=[2],
                            spacing="4",               
                        ),                                                
                     ),
                    animation="fadeInAnimation ease 3s",

                    )
            ),            
            spacing="1.5em",
            font_size="1em",
            padding="3%",
            shadow="lg",
            border_radius="lg",            
        ),
        width="100%",
        height="auto",
        #        
    )

def about():
    return rx.text("About Page")



# Add state and page to the app.
app = rx.App(state=State,stylesheets=[
        "styles/fontstyles.css","styles/center-simple.css","styles/introjs.min.css"  # This path is relative to assets/
    ],style=style,scripts="intro.js")
app.add_page(index,title="Contextual Demo",on_load=State.run_analysis)
app.add_page(about, route="/about")
app.compile()
