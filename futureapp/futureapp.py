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

# import torch

# Introjs trial
# class IntroSteps(rx.Component):
#     library = "intro.js-react"
#     tag = "Steps"
#     initialStep: rx.Var[int]
#     initialStep: 0

#     @classmethod
#     def get_controlled_triggers(cls) -> dict[str, rx.Var]:
#         return {"on_change": rx.EVENT_ARG}

# Image API Server Check details
instance_id = "i-0b1fc05fd631f16c8"
import requests
import json
# API Gateway endpoint
url = "https://ubqbjs2b96.execute-api.ap-south-1.amazonaws.com/default/handleRAMInstance"

# Data to send in the request for starting the instance
data_start = {
    'action': 'start',
    'instance_id': instance_id
}

# # Data to send in the request for stopping the instance
data_stop = {
    'action': 'stop',
    'instance_id': instance_id
}

# Data to send in the request for checking the status of the instance
data_status = {
    'action': 'status',
    'instance_id': instance_id
}
headers = {
  'Content-Type': 'application/json',
#   'Access-Control-Allow-Origin' : '*'
}


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
            "background":"#a3ce55 !important",  
            "color": "#fff !important",
    },
#Tab selected color
    ".css-52dxnr[aria-selected=true], .css-52dxnr[data-selected]": {
            # "background_color": accent_color,
            "color": "#a3ce55 !important",
        },


    rx.ResponsiveGrid: {
        "animation": "fadeInAnimation ease 3s",
        "animation-iteration-count": "1",
        "animation-fill-mode": "forwards",
    },

    rx.Heading: {
        # "font_size": "32px",
        "font_family": "Candal",
        # "font_family": "'Ariel', sans-serif",
        "font_weight": "700",
        # "font_size": "32px",
        "color": "#333",
    },
    rx.Text: {
        "font_family": "Inter",
        # "line-height" : "1.7",
        # "font_weight": "100",
        "font_size": ["12px","12px","12px","16px","16px","22px"],
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
    rx.Tabs: {
        # "background" : "linear-gradient(45deg,#e6e4fc,#fceded) !important",
        "color" : "#333",
        "shadow" : "lg",
        "border-radius" : "16px",
        "box-shadow" : "6px 6px 12px #b8b9be,-6px -6px 12px #fff!important",

    },
    # rx.DataTable: {
    #     "background": "linear-gradient(45deg,#e6e4fc,#fceded)",
    # }
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
    ispositive = True
    issafe = "Safe"    
    sentiment_color = sentiment_empty_bg.split('.')[0]
    sentiment_value = 0
    sff1 = ""
    sentiment_disp_value = 0
    keyword_list = pd.DataFrame([[]])
    sentiment_pie = []     

    # keyword_list: List[str] = [["1"]]
    #Check Server Status
    # response = requests.post(url, headers=headers, data=json.dumps(data_status))  # Change data to data
    # print(response.text)
    # status = response.json()['message'].split('is ')[-1]
    # if status == 'running':
    #     print("Server is running")
    #     is_checked: bool = "Switch On!"
    #     checked: bool = True
    # else:
    #     is_checked: bool = "Switch off!"
    #     checked: bool = False

    # @rx.var
    # def checked(self):
    #     response = requests.post(url, headers=headers, data=json.dumps(data_status))  # Change data to data
    #     print(response.text)
    #     status = response.json()['message'].split('is ')[-1]
    #     if status == 'running':
    #         print("Server is running")
    #         is_checked: bool = "Switch On!"
    #         checked: bool = True
    #     else:
    #         is_checked: bool = "Switch off!"
    #         checked: bool = False
        
    #     return checked

    # def change_check(self, checked: bool):
    #     self.checked = checked
    #     if self.checked:
    #         self.is_checked = "Switch on!"
    #         response = requests.post(url, headers=headers, data=json.dumps(data_status))  # Change data to data
    #         print(response.text)
    #         status = response.json()['message'].split('is ')[-1]
    #         if status == 'running':
    #             print("Server is already running")
    #         else:
    #             print("Turning on the server")
    #             response = requests.post(url, headers=headers, data=json.dumps(data_start))  # Change data to data
    #             status = response.json()['message']
    #             print(status)

    #     else:
    #         self.is_checked = "Switch off!" 
    #         response = requests.post(url, headers=headers, data=json.dumps(data_status))  # Change data to data
    #         print(response.text)
    #         status = response.json()['message'].split('is ')[-1]
    #         if status != 'running':
    #             print("Server is already off")
    #         else:
    #             print("Turning Off the server")
    #             response = requests.post(url, headers=headers, data=json.dumps(data_stop))  # Change data to data
    #             status = response.json()['message']
    #             print(status)               

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
        screendata = {}
        global model
        global articles, article_data
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
        self.ispositive = True
        self.issafe = "Safe"
        self.sentiment_value = 0
        self.sff1 = ""
        self.sentiment_disp_value = 0  
        self.sentiment_pie = [1,1]
        for ac,article in enumerate(articles):
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
            # os.system(f"wget {article_image} -O downloads/mainimage.{imgpost}")
            # list_uploaded_file = wget.download(article_image)
            # list_uploaded_file = f"{downloads/mainimage.{imgpost}}"
            list_uploaded_file = f"{screendata['local_image']}"
            uploaded_file = list_uploaded_file    
            ui_uploaded_file = f'{screendata["local_image"].split("/")[-1]}'    
            # shutil.copy(uploaded_file,f'assets/{ui_uploaded_file}')
            # import pdb;pdb.set_trace()
            uploaded_file = "assets/articleimages/"+ui_uploaded_file
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

            try: 
                self.sff1 = screendata["sff1"]

                self.keyword_list = pd.DataFrame(screendata["keyword_list"])

                self.sentiment_disp_value = screendata["sentiment_disp_value"]

                self.sentiment_value = int(self.sentiment_disp_value * 10)
                piey = [self.sentiment_value,100-self.sentiment_value]
                # import pdb;pdb.set_trace()
                self.sentiment_pie = rx.data(
                                        "pie",
                                        x=["Positive", "Negative"],
                                        y=piey,
                                    )
                self.sentiment_disp_value = f"{self.sentiment_value}%"
                self.ispositive = True if "Positive" in self.sff1 else False
                self.issafe = "Safe" if self.ispositive else "Unsafe"
                # self.sentiment_filled_bg = screendata["sentiment_filled_bg"]
                self.sentiment_filled_bg = "rgb(163, 206, 85)" if "green" in screendata["sentiment_filled_bg"] else screendata["sentiment_filled_bg"]
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
            self.processing,self.complete = False,True
            yield                
        elif not os.path.exists(uploaded_file):
            self.alert_msg_header = "Error"
            self.alert_msg = "Failed to load image"
            self.alert_change()
            self.processing,self.complete = False,True
            yield
            # return rx.window_alert("Failed to load image")
            # st.error("Failed to load image")
        elif not article.title:
            self.alert_msg_header = "Error"
            self.alert_msg = "Failed to load data file"
            self.alert_change()
            self.processing,self.complete = False,True
            yield            
            # return rx.window_alert("Failed to load data file ")
            # st.error("Failed to load data file ") 
        else:
            self.alert_msg_header = "Error"
            self.alert_msg = "Unknown Error"
            self.alert_change()
            self.processing,self.complete = False,True
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

    colorval = ["#a3ce55","#991BE2"]
    return rx.badge(
            tag, variant="solid",
            background="#a3ce55",
            line_height="1.42",
            # bg="#fff",
            # color=f"{colorval[colindex]}",##991BE2
            color="#fff",
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

def navbar_logo(**style_props):
    """Create a Reflex logo component.

    Args:
        style_props: The style properties to apply to the component.
    """
    return rx.link(
        rx.image(
            src="https://www.futureflixmedia.com/images/logo.png",
            **style_props,
        ),
        href="/",
    )
hamburger_button_style_dict = {
    "margin_left": "5%",
    "margin_right": "5%",
    "font_family": "Candal",
    "position": "relative",
    "color": '#fff',
    "margin_bottom" : "-30px !important",
    "padding_bottom" : "10px",

}
menu_button_style_dict = {
    "margin_left": "5%",
    "margin_right": "5%",
    "font_family": "Candal",
    "position": "relative",
    "color": '#fff',
    "margin_bottom" : ["40px !important","40px !important","40px !important","150px !important","150px !important","150px !important"],
    "padding_bottom" : "10px",

}
menu_style_dict = {
    "margin_bottom" : "180px",
    "margin_left": ["40px","40px","70px","90px","90px","110px"],
}

PADDING_X = ["1em", "2em", "5em"]

logo_style = {
    # "height": "200px",
    # "margin_bottom" : "150px"
    "margin_top" : ["20px","20px","20px","-110px","-110px","-110px"]
}
logo = navbar_logo(**logo_style)



def navbar():
    return rx.box(
            rx.hstack(
                rx.hstack(
                    logo,
                    # rx.box(
                    #     rx.image(src="images/CitFlix_Logo-01.png", height="350px",margin_left="200px", padding_bottom="100px",margin_top="-60px"
                    #             ,on_click=rx.redirect("/"),_hover={"cursor": "pointer"}
                    #             ),
                    # ),
                    rx.link(
                        rx.heading("Home", size="sm",color="#fff"),
                        href="https://www.futureflixmedia.com/",
                        color="#fff",
                        display=["none", "none", "none", "flex", "flex", "flex"],
                        style=menu_button_style_dict,
                    ),
                    rx.link(
                        rx.heading("Who we are?", size="sm",color="#fff"),
                        href="https://www.futureflixmedia.com/who-we-are",
                        color="#fff",
                        display=["none", "none", "none", "flex", "flex", "flex"],
                        style=menu_button_style_dict,
                    ),
                    rx.link(
                        rx.heading("What we do?", size="sm",color="#fff"),
                        href="https://www.futureflixmedia.com/contextual",
                        color="#fff",
                        display=["none", "none", "none", "flex", "flex", "flex"],
                        style=menu_button_style_dict,
                    ),                    
                    # rx.menu(
                    #     rx.menu_button(
                    #         rx.hstack(
                    #             rx.heading("What we do?", size="l",color="#fff",style=menu_button_style_dict),
                    #             rx.icon(
                    #                 tag="chevron_down",color="#fff",style=menu_button_style_dict
                    #             ),
                    #             cursor="pointer",
                    #             display=["none", "none", "none", "flex", "flex", "flex"],
                    #         )
                    #     ),
                    #     rx.menu_list(
                    #         rx.link(
                    #             rx.menu_item(
                    #                 "Contextual",style=menu_button_style_dict
                    #             ),
                    #             href="/docs/gallery",
                    #         ),
                    #     ),
                    #     style=menu_button_style_dict,
                    # ),
                    rx.link(
                        rx.heading("How we Do?", size="sm",color="#fff"),
                        href="https://www.futureflixmedia.com/how-we-do",
                        color="#fff",
                        display=["none", "none", "none", "flex", "flex", "flex"],
                        style=menu_button_style_dict,
                    ),
                    rx.link(
                        rx.heading("Contact Us", size="sm",color="#fff"),
                        href="https://www.futureflixmedia.com/contact-us",
                        color="#fff",
                        display=["none", "none", "none", "flex", "flex", "flex"],
                        style=menu_button_style_dict,
                    ),
                    rx.hstack(
                        rx.vstack(
                            rx.hstack(
                                rx.html("""<a href='https://www.linkedin.com/company/future-flix-media/' style='color:white' target='_blank' title='Linkdin'><span class='icon socialicon text-white'><svg stroke='currentColor' fill='currentColor' stroke-width='0' viewBox='0 0 16 16' height='1em' width='1em' xmlns='http://www.w3.org/2000/svg'><path d='M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z'></path></svg></span></a>"""),
                                rx.html("""<a href='https://www.instagram.com/futureflixmedia/' style='color:white' target='_blank' title='Instagram'><span class='icon socialicon text-white'><svg stroke='currentColor' fill='currentColor' stroke-width='0' viewBox='0 0 16 16' height='1em' width='1em' xmlns='http://www.w3.org/2000/svg'><path d='M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.917 3.917 0 0 0-1.417.923A3.927 3.927 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.916 3.916 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.926 3.926 0 0 0-.923-1.417A3.911 3.911 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0h.003zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599.28.28.453.546.598.92.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.47 2.47 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.478 2.478 0 0 1-.92-.598 2.48 2.48 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233 0-2.136.008-2.388.046-3.231.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92.28-.28.546-.453.92-.598.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045v.002zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92zm-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217zm0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334z'></path></svg></span></a>"""),
                                rx.html("""<a href='https://www.facebook.com/futureflixmedia' style='color:white' target='_blank' title='Facebook'><span class='icon socialicon text-white'><svg stroke='currentColor' fill='currentColor' stroke-width='0' viewBox='0 0 16 16' height='1em' width='1em' xmlns='http://www.w3.org/2000/svg'><path d='M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951z'></path></svg></span></a>"""),
                                margin_top="20px",
                            ),
                            rx.html("""
                                    <button class='btn-101'>
                                    Join Us
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
                            style=menu_style_dict,
                            display=["none", "none", "none", "flex", "flex", "flex"],
                        ),                    
                        rx.icon(
                            tag="hamburger",
                            # on_click=NavbarState.toggle_sidebar,
                            width="2em",
                            height="2em",
                            _hover={
                                "cursor": "pointer",
                                "color": "#a3ce55",
                            },
                            style=hamburger_button_style_dict,
                            display=["flex", "flex", "flex", "none", "none", "none"],
                        ),
                        height="full",
                    ),
                    width="100%",
                    justify="space-between",
                    # spacing="2em",
                ),
                width="100%",
                # padding_left=["40px","40px","40px","80px","120px","150px"],
                padding_left=["2%","2%","2%","8%","8%","8%"],   
                padding_right=["2%","2%","2%","8%","8%","8%"],
                # padding=PADDING_X,
                # margin_bottom="150px"
            ),
            background_color="#333",
            height="120px",
            width="100%",
            # backdrop_filter="blur(10px)",
            # padding_y=["0.8em", "0.8em", "0.5em"],
            # border_bottom="1px solid #F4F3F6",
        )


def index() -> rx.Component:
    return rx.box(
        rx.hstack(
            # rx.image(src="https://citrusberry.biz/assets/img/menu_logo1.png", width="41px", height="auto"),
            navbar(),
            # columns=[1, 2, 3, 4, 5, 6],
            # rx.image(src="images/CitFlix_Logo-01.png", width="250px", height="auto"),
            # width="100%",
            # padding="10px",            
        ),
        rx.hstack(
            rx.center(
                rx.heading("Fusing Content With Context", size="xl",color="#fff"),
                width="100%",
            # margin_left="650px",margin_right="50px"            
            ),
        background_color="#a3ce55",
        height="150px",
        width="100%",
        margin_bottom="80px",
        ),        
        # Replicate the navbar as shown in the website on this url - https://www.futureflixmedia.com/#service,
        # Windows Cards
        rx.container(
            # rx.responsive_grid(
            rx.flex(
                rx.box(
                    rx.card(
                        rx.vstack(
                            # rx.center(
                            rx.image(src="images/Group_126.png", width=["100%","100%","100%","70%","70%","70%"],border_radius="0px",object_fit="cover"),
                            rx.vstack(
                                rx.text("81% of users prefer to watch ads relevant to their browsing experiences", size="sm",padding="0px"),
                                
                            ),
                            justify="space-between",
                            # padding_bottom="5%",

                        ),
                        footer=rx.button("Discover more",bg="#333",color="#fff",size="md",_hover={"cursor": "pointer","background-color":"#a3ce55"},bottom="0px"),#,on_click=State.run_analysis
                        border_color="rgba(163,206,85,.87)",
                        border_width="3px",
                        direction="column",                    
                        align="center",
                        width=["240px","240px","240px","240px","240px","300px"],
                        height=["320px","320px","320px","320px","320px","400px"],
                        margin="0px",
                        # margin_left="150px",
                    ),  
                    width="100%",
                    margin="5px",
                ),
                rx.box(
                    rx.card(
                        rx.vstack(
                            rx.image(src="images/Group_127.png", width=["90%","90%","90%","60%","60%","60%"],border_radius="0px",object_fit="cover"),
                            rx.vstack(
                                rx.text("Interactive contextual ads drive 3X more engagement", size="sm",padding="0px"),
                                rx.text(" ", size="sm",padding="8px"),
                            ),
                            justify="space-between",
                            # padding_bottom="5%",

                        ),
                        footer=rx.button("Discover more",bg="#333",color="#fff",size="md",_hover={"cursor": "pointer","background-color":"#a3ce55"},bottom="0px"),#,on_click=State.run_analysis
                        border_color="rgba(163,206,85,.87)",
                        border_width="3px",
                        direction="column",                    
                        align="center",  
                        width=["240px","240px","240px","240px","240px","300px"],
                        height=["320px","320px","320px","320px","320px","400px"],
                        margin="0px",
                        # width="100%",
                    ), 
                    width="100%",
                    margin="5px",
                ),                    
                rx.box(
                    rx.card(
                        rx.vstack(
                            rx.image(src="images/Group_128.png", width=["90%","90%","90%","60%","60%","60%"],border_radius="0px",object_fit="cover"),
                            rx.text("66% of consumer report being uncomfortable with personal data tracking", size="sm",padding="0px"),
                        ),
                        # header=rx.heading("X RAE", size="lg"),
                        footer=rx.button("Discover more",bg="#333",color="#fff",size="md",_hover={"cursor": "pointer","background-color":"#a3ce55"},bottom="0px"),#,on_click=State.run_analysis
                        # footer=rx.heading("Footer", size="sm"),
                        border_color="rgba(163,206,85,.87)",
                        border_width="3px",
                        direction="column",                    
                        align="center",
                        # width="240px",
                        # height="320px",                                    
                        width=["240px","240px","240px","240px","240px","300px"],
                        height=["320px","320px","320px","320px","320px","400px"],
                        margin="0px",
                        # width="100%",
                    ), 
                    width="100%",
                    margin="5px",
                ),                       
                rx.box(
                    rx.card(
                        rx.vstack(
                            rx.image(src="images/Group_129.png", width=["100%","100%","100%","65%","65%","65%"],border_radius="0px",object_fit="cover"),
                            rx.text("Hyper Contextual targeting capabilities with data privacy as a top priority", size="sm",padding="0px"),
                        ),
                        # header=rx.heading("X RAE", size="lg"),
                        footer=rx.button("Discover more",bg="#333",color="#fff",size="md",_hover={"cursor": "pointer","background-color":"#a3ce55"},bottom="0px"),#,on_click=State.run_analysis
                        border_color="rgba(163,206,85,.87)",
                        border_width="3px",
                        direction="column",                    
                        align="center",
                        # width="240px",
                        # height="320px",                                       
                        width=["240px","240px","240px","240px","240px","300px"],
                        height=["320px","320px","320px","320px","320px","400px"],
                        margin="0px",
                        # width="100%",
                    ), 
                    width="100%",
                    margin="5px",
                ),                       
            #     columns=[4],
            #     # spacing_x="10px",    
            #     width="100%",
            #     padding_top="50px",
                padding_bottom="80px",
            #     gap=4,
                flex_direction=["column", "column", "column", "row", "row"],
            ),  
            center_content=True,      
            # display=["none", "none", "none", "flex", "flex", "flex"],
        ),






        # Mobile Cards
        rx.container(
            # rx.responsive_grid(
            rx.vstack(
                rx.card(
                    rx.vstack(
                        # rx.center(
                        rx.image(src="images/Group_126.png", width=["100%","100%","100%","70%","70%","70%"],border_radius="0px",object_fit="cover"),
                        rx.vstack(
                            rx.text("81% of users prefer to watch ads relevant to their browsing experiences", size="sm",padding="0px"),
                            
                        ),
                        justify="space-between",
                        # padding_bottom="5%",

                    ),
                    footer=rx.button("Discover more",bg="#333",color="#fff",size="md",_hover={"cursor": "pointer","background-color":"#a3ce55"},bottom="0px"),#,on_click=State.run_analysis
                    border_color="rgba(163,206,85,.87)",
                    border_width="3px",
                    direction="column",                    
                    align="center",
                    width=["300px","300px","300px","300px","240px","300px"],
                    height=["400px","400px","400px","400px","320px","400px"],
                    margin="0px",
                    # margin_left="150px",
                ), 
                rx.card(
                    rx.vstack(
                        rx.image(src="images/Group_127.png", width=["90%","90%","90%","60%","60%","60%"],border_radius="0px",object_fit="cover"),
                        rx.vstack(
                            rx.text("Interactive contextual ads drive 3X more engagement", size="sm",padding="0px"),
                            rx.text(" ", size="sm",padding="8px"),
                        ),
                        justify="space-between",
                        # padding_bottom="5%",

                    ),
                    footer=rx.button("Discover more",bg="#333",color="#fff",size="md",_hover={"cursor": "pointer","background-color":"#a3ce55"},bottom="0px"),#,on_click=State.run_analysis
                    border_color="rgba(163,206,85,.87)",
                    border_width="3px",
                    direction="column",                    
                    align="center",  
                    width=["300px","300px","300px","300px","240px","300px"],
                    height=["400px","400px","400px","400px","320px","400px"],
                    margin="0px",
                    # width="100%",
                ), 
                rx.card(
                    rx.vstack(
                        rx.image(src="images/Group_128.png", width=["90%","90%","90%","60%","60%","60%"],border_radius="0px",object_fit="cover"),
                        rx.text("66% of consumer report being uncomfortable with personal data tracking", size="sm"),
                    ),
                    # header=rx.heading("X RAE", size="lg"),
                    footer=rx.button("Discover more",bg="#333",color="#fff",size="md",_hover={"cursor": "pointer","background-color":"#a3ce55"},bottom="0px"),#,on_click=State.run_analysis
                    # footer=rx.heading("Footer", size="sm"),
                    border_color="rgba(163,206,85,.87)",
                    border_width="3px",
                    direction="column",                    
                    align="center",
                    # width="240px",
                    # height="320px",                                    
                    width=["300px","300px","300px","300px","240px","300px"],
                    height=["400px","400px","400px","400px","320px","400px"],
                    # width="100%",
                ), 
                rx.card(
                    rx.vstack(
                        rx.image(src="images/Group_129.png", width=["100%","100%","100%","65%","65%","65%"],border_radius="0px",object_fit="cover"),
                        rx.text("Hyper Contextual targeting capabilities with data privacy as a top priority", size="sm"),
                    ),
                    # header=rx.heading("X RAE", size="lg"),
                    footer=rx.button("Discover more",bg="#333",color="#fff",size="md",_hover={"cursor": "pointer","background-color":"#a3ce55"},bottom="0px"),#,on_click=State.run_analysis
                    border_color="rgba(163,206,85,.87)",
                    border_width="3px",
                    direction="column",                    
                    align="center",
                    # width="240px",
                    # height="320px",                                       
                    width=["300px","300px","300px","300px","240px","300px"],
                    height=["400px","400px","400px","400px","320px","400px"],
                    # width="100%",
                ), 
            #     columns=[4],
            #     # spacing_x="10px",    
            #     width="100%",
            #     padding_top="50px",
                padding_bottom="80px",
            #     gap=4,

            ),  
            center_content=True,      
            display=["flex", "flex", "flex", "none", "none", "none"],
        ),


        rx.vstack(
            rx.tooltip(
                # rx.card(  
                    rx.center(
                        rx.image(src="images/logo-11.png", width="350px", height="auto",padding="0px",margin="0px"),
                    # #     rx.heading("X-Rae Output", size="xl", color="#fb5e78"),
                    # # border_radius="15px",
                    # # border_width="thick",
                    width="100%",
                    margin="-150px",
                    padding="-200px"
                    # # border_color="#fb5e78",
                    ), 
                # ),                       
                # background="linear-gradient(90deg, #ff5c72, #a485f2)",
            # rx.heading("Contextual AI Demo!", font_size="2em",color="#a3ce55",),
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
                            placeholder="Select an example.",
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
                # rx.button(
                #     "Analyze", on_click=State.run_analysis,is_loading=State.processing,width="100%",
                #     background_image="linear-gradient(90deg, #ff5c72, #a485f2)",
                # ),                

            ),
            rx.cond(
                State.complete,
                    rx.responsive_grid(        
                     rx.vstack(
                        # rx.divider(border_color="#a3ce55"),
                        rx.heading(State.article_title, size="lg",margin="30px",font_size="40px",font_weight="800"
                                   ),
                        # rx.hstack(
                        rx.responsive_grid(        
                            rx.card(
                                rx.center(
                                    rx.image(
                                    src=State.image_url,
                                    height="25em",
                                    width="37.5em",
                                    border_radius="10px",
                                    ), 
                                border_radius="10px",
                                border_width="2px",
                                border_color="#a3ce55",
                                width="100%",
                                ),
                                header=rx.heading("Article Image", size="lg",color="#fff"),
                                background_color="#a3ce55",
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
                        #     rx.divider(border_color="#a3ce55"),
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
                                rx.grid(
                                    rx.grid_item(
                                        rx.center(
                                            rx.vstack(
                                                rx.hstack(
                                                    rx.heading(State.model_caption, size="sm", color="grey" ),
                                                    padding="100px",
                                                    padding_top="10px",
                                                    padding_left="10px",
                                                    border="2px solid #d6d1d1",
                                                    border_radius="10px",
                                                ),
                                                rx.spacer(),                                            
                                                rx.hstack(
                                                    rx.foreach(State.model_tag_list,tag_list),rx.spacer(),
                                                    # is_inline=True,
                                                    wrap="wrap"
                                                ),
                                                padding_top="25%",
                                            ),
                                        ),
                                        col_span=1, 
                                        padding="0px",
                                    ),                                        
                                    rx.grid_item(
                                        rx.center(
                                            rx.image(src="images/Xray-01.png", width="80%",padding="0px",margin_left=["50px","100px","100px","130px","130px","200px"]),
                                        ),

                                        # rx.html("""
                                        #         <div class='phone' >
                                        #                 <iframe src='https://creatives.citrusberry.biz/mobile_inscreen_videodemo' class='phone-screen'></iframe>
                                        #             </div>
                                        # """),
                                        col_span=1, 
                                        padding="0px",
                                    ),  
                                    template_columns="repeat(2, 1fr)",
                                    width="100%",
                                    padding="0px",
                                ),
                                padding="0px",
                                background="#f2f2f2",
                                header=rx.heading("X RAE Image Analysis", size="lg",justify_content="center"),
                                
                            ),
                            columns=[1],
                            spacing="4",    
                            width="100%",
                        ),  
                        rx.responsive_grid(
                            # rx.divider(border_color="black"),
                            rx.card(  
                                rx.center(
                                    rx.hstack(
                                        rx.vstack(
                                            rx.vstack(
                                                rx.heading("Overall Sentiment", size="lg"),
                                                rx.hstack(
                                                    rx.heading(
                                                        State.sff1+State.sentiment_disp_value, color=State.sentiment_filled_bg,opacity="0.8"
                                                    ),
                                                    rx.cond(
                                                        State.ispositive,
                                                        rx.image(src="images/thumbs_up.png")
                                                    ),
                                                ),
                                                padding="0px",
                                            ),
                                            rx.vstack(
                                                rx.heading("Safety Parameter", size="lg"),
                                                rx.hstack(
                                                    rx.heading(
                                                        State.issafe, color=State.sentiment_filled_bg,opacity="0.8",
                                                    ),
                                                    rx.cond(
                                                        State.ispositive,                                                    
                                                        rx.image(src="images/Check.png"),
                                                    ),
                                                ),
                                                padding="0px",
                                            ), 
                                            padding="0px",
                                        ),                                       
                                        # rx.hstack(
                                        rx.container(
                                            rx.pie(
                                                data=State.sentiment_pie,
                                                color_scale=['#a3ce55','#333'],
                                                pad_angle=5.0,
                                                inner_radius=100.0,
                                                start_angle=0.0,
                                                # radius=100.0,
                                            )  ,   
                                            # center_content=True,
                                            bg="transparent",
                                        ),                                            
                                         
                                        # rx.progress(value=State.sentiment_value, width="100%",color_scheme=State.sentiment_color,height="15px",bg="#fff",opacity="0.8"),        
                                        # ),
                                        width="100%",
                                        justify="space-between",
                                        margin_left=["50px","50px","50px","50px","50px","130px"],
                                        margin_right=["50px","50px","50px","50px","50px","130px"],
                                    ),
                                ),
                                background="#fff",
                                # header=rx.heading("Overall Sentiment", size="lg"),
                                
                            ),
                            columns=[1],
                            spacing="4",    
                            width="100%",
                        ),                                                  
                        rx.tabs(
                            items=[
                                (
                                    "Targeting Metrics",
                                    rx.responsive_grid(  
                                        rx.card(
                                                rx.vstack(        
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
                                ),
                                (
                                    "Brands", 
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
                            ),
                            (
                                "Website Inventory",
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
                            ),
                            (
                                "News Inventory",
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
                            )
                            ],
                        ), 
                    ),
                    animation="fadeInAnimation ease 3s",

                    )
            ),            
            spacing="1.5em",
            font_size="1em",
            # padding="3%",
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
        "styles/citflexfontstyles.css","styles/center-simple.css","styles/introjs.min.css"  # This path is relative to assets/
    ],style=style,scripts="intro.js")
app.add_page(index,title="Contextual Demo",on_load=State.run_analysis)
app.add_page(about, route="/about")
app.compile()
