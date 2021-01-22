from django.shortcuts import render
# import csv
import pandas as pd
import requests
# import sqlite3
from bs4 import BeautifulSoup
# import pyttsx3 as pt
# import speech_recognition as sr
from polls.models import *

# information = []


def scrape(data):
    main_list = []  # this is the main list where every list will be appended
    main_list_1 = ["TITLE"]
    main_list_2 = ['AUTHOR']
    main_list_3 = ['WEBSITE']
    main_list_4 = ['DATE']
    main_list_5 = ['LINK']
    main_list_6 = ['DURATION']
    title_list = []  # this is the where all the title_2 contents will be
    # title_2 = []  # this is the list where all the iterated titles will be
    detail_list = []  # this is the list where all the author details will be
    detail_2 = []  # this is the list where all the iterated author details will be
    link_list = []  # this is the list where all the link_2 items will be
    # link_2 = []  # this is the list where all the iterated links will be
    duration_list = []  # this is the list where all the duration_2 contents will be
    # duration_2 = []  # this is where all the iterated reading time content will be

    url = 'https://medium.com/search?q=' + str(data)
    r = requests.get(url)
    html_content = r.content
    # print(html_content)

    soup = BeautifulSoup(html_content, 'html.parser')
    # print(soup.prettify())

    titles = soup.find_all('h3', class_='graf--title')  # here all titles will be iterated
    details = soup.find_all('a', class_='link')  # here all authors will be iterated
    links = soup.find_all('div', class_='postArticle-content')  # here all links will be iterated
    durations = soup.find_all('span', class_='readingTime')  # here all the reading time will be iterated
    for title in titles:
        t = title.text
        # print(title.text)
        # title_2 = [t]
        title_list.append(t)
    for detail in details:
        a = detail.text
        # print(detail.text)
        detail_2 = [a]
        detail_list.append(detail_2)
    for link in links:
        l = link.a['href']
        # print(link.a['href'])
        # link_2 = [l]
        link_list.append(l)
    for duration in durations:
        d = duration['title']
        # print(duration['title'])
        # duration_2 = [d]
        duration_list.append(d)

    # code for extracting author's names

    indices_to_access_authors = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27]
    a_series_authors = pd.Series(detail_list)
    accessed_series_author = a_series_authors[indices_to_access_authors]
    accessed_list_authors = list(accessed_series_author)

    # code for extracting dates

    indices_to_access_dates = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29]
    a_series_dates = pd.Series(detail_list)
    accessed_series_dates = a_series_dates[indices_to_access_dates]
    accessed_list_dates = list(accessed_series_dates)

    # code for extracting websites on which author wrote

    indices_to_access_websites = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28]
    a_series_websites = pd.Series(detail_list)
    accessed_series_websites = a_series_websites[indices_to_access_websites]
    accessed_list_websites = list(accessed_series_websites)
    # print(detail_list)
    # print(title_list)
    # print(link_list)
    # # print(duration_list)
    # print(accessed_list_authors)
    # print(accessed_list_dates)
    # print(accessed_list_websites)

    main_list_1.append(title_list)
    main_list_2.append(accessed_list_authors)
    main_list_3.append(accessed_list_websites)
    main_list_4.append(accessed_list_dates)
    main_list_5.append(link_list)
    main_list_6.append(duration_list)
    # print(main_list)
    main_list.append(main_list_1)
    main_list.append(main_list_2)
    main_list.append(main_list_3)
    main_list.append(main_list_4)
    main_list.append(main_list_5)
    main_list.append(main_list_6)
    # print(main_list_1)
    # print(main_list_2)
    # print(main_list_3)
    # print(main_list_4)
    # print(main_list_5)
    # print(main_list_6)
    n_1 = len(title_list)
    # # # Creating a Database
    # conn = sqlite3.connect('scraped_data_1.bd')
    # c = conn.cursor()
    #
    # # # #  Creating a Table
    #
    # c.execute('''CREATE TABLE contents(Title TEXT, Author TEXT, Website TEXT, Date TEXT, Link TEXT, Duration Text)''')
    # #
    # # # Since data here is in form os lists, so I cannot add them directly to the columns of the table, hence we have
    # # # to iterate within the list or say we have to fetch the length of the list


    # for i in range(n_1):
    #     c.execute('''INSERT INTO contents VALUES(?,?,?,?,?,?)''', (
    #         title_list[i][0], accessed_list_authors[i][0], accessed_list_websites[i][0], accessed_list_dates[i][0],
    #         link_list[i][0], duration_list[i][0]))
    # conn.commit()
    #
    # # Conversion in the form of .csv file
    # with open('medium_data_1.csv', 'w') as file:
    #     writer = csv.writer(file)
    #     for item_1 in main_list:
    #         writer.writerow(item_1)
    #
    # with open('medium_data_1.csv', 'r') as file:
    #     reader = csv.reader(file)
    #     rows = list(reader)
    #     # print(rows[2])
    return [title_list, accessed_list_authors, accessed_list_dates, accessed_list_websites, duration_list, link_list, n_1]


def index(request):
    return render(request, 'index.html')


def scrape_data(request):
    data_1 = []
    data = request.POST.get('query')
    if data == "":
        return render(request, 'index.html', {"data_1": data_1})
    else:
        title_list, accessed_list_authors, accessed_list_dates, accessed_list_websites, duration_list, link_list, n_1 = scrape(
            data)
        # for i in accessed_list_authors:
        #     if accessed_list_authors[i] == "nan":
        #         accessed_list_authors[i] = "not found"
        for i in range(n_1):
            # print(accessed_list_authors[i])
            data_1.append({
                            'Title': title_list[i],
                            'Author': accessed_list_authors[i][0],
                            'Date': accessed_list_dates[i][0],
                            'Website': accessed_list_websites[i][0],
                            'Duration': duration_list[i],
                            'Link': link_list[i]
                           })
        for item in data_1:
            titans(item)
        # print(title_list, accessed_list_authors, accessed_list_dates, accessed_list_websites, duration_list, link_list)
        # global information
        # information = data_1
        # print(data)
        # print(information)
        return render(request, 'index.html', {"data_1": data_1})


# def renew(request):
#     return information

def titans(item):
    all_details = details()
    all_details.title = item["Title"]
    all_details.author = item["Author"]
    all_details.date = item["Date"]
    all_details.website = item["Website"]
    all_details.duration = item["Duration"]
    all_details.link = item["Link"]
    all_details.save()