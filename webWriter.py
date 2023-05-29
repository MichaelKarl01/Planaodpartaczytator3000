import os
import re
import requests
import pandas as pd
from urllib.request import urlopen
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

def get_title(html_page, title = "title"):
    for i in range(len(html_page)):
        if "<title>" in html_page[i]:
            return(html_page[i].split('-')[0].strip()[7:])

def Read_subj_page(url):
    print(url+'\n\n')
    html = urlopen(url).read().decode("utf-8").splitlines()
    page_title = get_title(html)

    classes_links = []
    classes_names = []
    
    df = pd.read_html(requests.get(url).content)[-1]
    classes_names = df[1][1].split('more information')
    for i in range(len(classes_names)):
        classes_names[i] = page_title+' '+classes_names[i].strip(" ").split(',')[0]
    for i in range(len(html)-1, -1, -1):
        if "Class type" in html[i]:
            for j in range(i,len(html)):
                if 'href' in html[j]:
                    classes_links.append(re.search("(?P<url>https?://[^\s]+)", html[j]).group("url"))
                if 'Coordinators' in html[j]:
                    break
            break
    return classes_names, classes_links

def Read_website(url, subject=True):
    classes_names, classes_links = Read_subj_page(url)
    classes = []
    for u in range(len(classes_links)):
        classes.append([])
        df = pd.read_html(requests.get(classes_links[u]).content)[-1]
        groups = df.values.tolist()[:-1]
        for i in groups:
            classes[-1].append([])
            group = i[1].split(',')
            for zaj in range(0,len(group),2):
                for j in range(len(days)):
                    if days[j] in group[zaj]:
                        hours = group[zaj+1]
                        classes[-1][-1].append(str(j+1)+hours)
                        zaj += 2
                        break
    return classes, classes_names

def get_hours(directory):
    ReadOrWrite = input('Read/Write/Append [R/W/A]: ')
    if  ReadOrWrite.upper() == 'W' or ReadOrWrite.upper() == 'A':
        if ReadOrWrite.upper() == 'W':
            group_file = open(directory, "w+", encoding="utf-8")
        else:
            group_file = open(directory, "a+", encoding="utf-8")
        token = False
        while True:
            if token == False:
                Url = input("Link to the subject page (or END):\n")
            if Url == 'END':
                break
            a, b = Read_website(Url,not token)
            for i in range(len(a)):
                if a[i] == [[]]:
                    print('No hours in the group '+b[i])
                else:
                    group_file.write('"'+b[i]+'"\n')
                    for j in a[i]:
                        if_was = False
                        for k in j:
                            if if_was == True:
                                group_file.write(', ')
                            group_file.write(k)
                            if_was = True
                        group_file.write('\n')
                    group_file.write('\n')
            group_file.flush()

        group_file.close()
