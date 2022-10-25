from encodings import utf_8
from pickle import TRUE
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pyparsing import col
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import time
from time import strptime
import pandas as pd
import csv
from pywebio.output import put_html
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts

put_image(open('nfl.jpeg', 'rb').read(), width = '100px')
put_markdown("# Welcome!")
put_text("This is a website designed to portray data on the top players you select based on URL. Credits to pro football reference.")

def check_form(info):
    try:
        val = strptime(info['birthday'], "%m/%d/%Y")
    except:
        return ('birthday', "Invalid birthday!")
    
    if info['fname'].isdigit():
        return('fname', 'Invalid first name!')
    if info['lname'].isdigit():
        return('lname', 'Invalid last name!')
info = input_group("Before we get on to the fun, I'd like you to fill out the form:", [
     input('First Name', name='fname', required = True, placeholder = "Ex: Tom"),
     input('Last Name', name='lname', required = True, placeholder = "Ex: Brady"),
     input("Date of Birth", name = "birthday", required = True, placeholder = "Ex: mm/dd/yyyy")], validate = check_form)
popup("Your Details",
      f"First Name: {info['fname']} \nLast Name: {info['lname']}\
      \nBirthday: {info['birthday']}",
      closable=True)
link = input("Enter a valid URL you want to use from pro-football-reference to generate the data.", type = URL, placeholder = "Ex: https://www.pro-football-reference.com/years/2021/passing.htm")
html = urlopen(link)
soup = BeautifulSoup(html, features="html.parser")
headers = [th.getText() for th in soup.findAll('tr')[0].findAll('th')]
headers = headers[1:]
rows = soup.findAll('tr', class_ = lambda table_rows: table_rows != "thead")
player_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
player_stats = player_stats[1:]
df = pd.DataFrame(player_stats, columns = headers)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
put_html(df)

lis = list()
lis.append(info)

path_deploy()



