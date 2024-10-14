import requests
from bs4 import BeautifulSoup
import pandas as pd

# Setting the headers and user string
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}

def product(url):
    # Sending a request to fetch HTML of the page
    response = requests.get(url, headers=headers)
    
    # Checking if the request was successful (status code 200)
    if response.status_code != 200:
        print('Sorry, cannot fetch data for this product right now!!')
        exit()
    
    # Creating the soup object
    soup = BeautifulSoup(response.content, 'html.parser')

    # Changing the encoding to utf-8
    soup.encode('utf-8')

    title = soup.find('span', attrs={'class': 'B_NuCI'}).get_text()
    price = soup.find('div', attrs={'class': '_30jeq3 _16Jk6d'}).get_text()

    th = ['Title', 'Price']
    td = [title, price]

    for td_elem in soup.find_all('td', attrs={'class': '_1hKmbr col col-3-12'}):
        th.append(td_elem.get_text())

    for t_elem in soup.find_all('li', attrs={'class': '_21lJbe'}):
        td.append(t_elem.get_text())

    if len(th) == 2:
        for i_elem in soup.find_all('div', attrs={'class': 'col col-3-12 _2H87wv'}):
            th.append(i_elem.get_text())

        for t_elem in soup.find_all('div', attrs={'class': 'col col-9-12 _2vZqPX'}):
            td.append(t_elem.get_text())

    if len(th) > len(td):
        th.pop(2)
    elif len(th) < len(td):
        td.pop(2)

    data = {"Features": th, "Details": td}
    df = pd.DataFrame(data=data)

    return df