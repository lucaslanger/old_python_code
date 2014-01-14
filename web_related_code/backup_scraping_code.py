'''
Created on Jan 11, 2014

@author: Lucas
'''
import requests
import sqlite3
import os
from bs4 import BeautifulSoup
import re


connection = sqlite3.connect('articles.db')
curs = connection.cursor()

def getYahooData(url):
    content = requests.get(url).content
    soup = BeautifulSoup(content)
    stories = soup.find_all('div',{"class" : 'story'})
    listories = []
    for s in stories:
        try:
            img = re.findall("url\('(.+)'\);", str(s.find_all('div', {'class' : 'img'})[0].find_all('img')[0]) )[0]
            a_tag = s.find_all('a')[0]
            title = a_tag.get('alt').split('(')[0]
            href = 'http://ca.news.yahoo.com' + a_tag.get('href')
            listories.append({'img':img, 'title':title, 'href':href, 'content':''})
        except:
            continue
    return listories

def getArticles():
    yahoo_urls = ['http://ca.news.yahoo.com/science--most-popular/most-popular/' + str(i)+ '.html' for i in range(1,3)]
    for a in yahoo_urls:   
        yd = getYahooData(a)
        for s in yd:
            addArticle(s)
        
   
    
def addArticle(article): 
    curs.execute('''INSERT INTO articles (url, title, img, content) VALUES(?,?,?,?)''',(article['href'],article['title'],article['img'],article['content']))

def updateArticles(li_articles):
    for article in li_articles:
        addArticle(article)
      
def updateDb():      
    curs.execute('''CREATE TABLE if not exists articles (id INTEGER PRIMARY KEY, url TEXT, title TEXT, img TEXT, content TEXT)''') 
    getArticles()
    connection.commit()
    #database = open('articles.csv','w')
    d = open('articles.py', 'w')
    d.write("article_array = ")
    d.write("[")
    
    curs.execute('SELECT * FROM articles')
    for i in curs:
        d.write(str([str(i[j]) for j in range(len(i)-1)]))
        d.write(',')   
        #database.write(','.join([str(j) for j in i]))  
        #database.write('\n')
    d.seek(-1, os.SEEK_END)
    d.truncate()
    d.write("]")
    d.close()
    curs.close()  
            
def testDb():
    curs.execute('''CREATE TABLE if not exists articles (id INTEGER PRIMARY KEY, url TEXT, title TEXT, img TEXT, content TEXT)''') 
    getArticles()
    connection.commit()
    
    curs.execute('SELECT * FROM articles')
    for i in curs:
        for j in i:
            print j     
    curs.close()     
 
updateDb()
