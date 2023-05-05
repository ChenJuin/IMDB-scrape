import requests
from bs4 import BeautifulSoup
import sqlite3
import csv

conn = sqlite3.connect('movierank.db')
c = conn.cursor()

#c.execute('''CREATE TABLE imdbmovie(rank INTERGER, name TEXT, year INTEGER, star_cast TEXT, rating REAL, link BLOB)''')
#c.execute('''DROP TABLE imdbmovie''')

url = "https://www.imdb.com/chart/top/"
source = requests.get(url).text

soup = BeautifulSoup(source,'html.parser')

csv_file = open('movie.csv','w',newline='',encoding='utf-8')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Rank','Name','Year','Cast','Rating','Link'])

full_details = soup.find('tbody', class_ = 'lister-list').find_all('tr')


def movie_details(a,b):
    
    details = full_details[a:b]
    #loop through 250 movie details
    for detail in details:
        
        #scrape all the details like rank, name, year, rating, star cast and the video link
        rank = detail.find('td', class_ = 'titleColumn').get_text(strip=True).split('.')[0]
        name = detail.find('td', class_ = 'titleColumn').a.text
        year = detail.find('td', class_ = 'titleColumn').span.text.strip('()')
        star_cast = detail.find('td', class_ = 'titleColumn').a.get('title')
        rating = detail.find('td', class_ = 'ratingColumn imdbRating').get_text(strip=True)
        link = 'www.imdb.com' + detail.find('td', class_ = 'titleColumn').a.get('href')
        
        #create csv file
        csv_writer.writerow([rank,name,year,star_cast,rating,link])

        #insert data into database
        c.execute('''INSERT INTO imdbmovie VALUES(?,?,?,?,?,?)''',(rank, name, year, star_cast, rating, link))

        #print out the details
        #print(rank,name,year,star_cast,rating,link)

        
   
#can start with any rank of movie details just replace the a and b with numbers
#movie_details(0,250)

#close csv file
csv_file.close()

conn.commit()

#c.execute('''DELETE from imdbmovie''')
c.execute('''SELECT * from imdbmovie''')
result = c.fetchall()
print(result)

conn.close()