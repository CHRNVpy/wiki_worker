import time

import mwclient
import requests
import schedule as schedule
from bs4 import BeautifulSoup

from functions import get_game_requirement, get_soft_categories, get_software_links, get_soft_requirement
from templates import games_template, soft_template

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (X11;Ubuntu;Linuxx86_64;rv:109.0)Gecko/20100101 Firefox/110.0'
}


def check_new_games():
    """ This function checking new games """
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0-9']
    links = []
    for letter in alphabet:
        print(f'[!] Checking games with letter {letter}')
        url = f'https://gamesystemrequirements.com/database/{letter.lower()}'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        pages = soup.find(class_="pagenav_d").find_all('a')[-2].text

        for num in range(1, int(pages)+1):
            url = f'https://gamesystemrequirements.com/database/{letter.lower()}/page/{num}'
    #url = 'https://gamesystemrequirements.com/database/g/page/2'
            response = requests.get(url, headers=headers)
            print(response.status_code)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                games_list = soup.find_all(class_="gr_box")
                for game in games_list:
                    game_name = game['title']
                    game_link = game['href']
                    wiki_response = requests.get(f"https://systemrequirements.wiki/{game_name.replace(' ', '_')}",
                                                 headers=headers)
                    if wiki_response.status_code != 200:
                        time.sleep(2)
                        links.append(game_link)
    return links


def check_new_soft(start_url):
    """ This function checking new soft """
    links = []
    gen_response = requests.get(url=start_url, headers=headers)
    soup = BeautifulSoup(gen_response.text, 'html.parser')
    #title = soup.find(class_="title archive-category").text
    if soup.find(class_='page-navi pagination numbers clear-block'):
        pages = soup.find(class_='page-navi pagination numbers clear-block').find_all('a')[-2].text
        for i in range(1, int(pages) + 1):
            url = start_url + f'page/{i}/'
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            names = soup.find_all('h2', {'class': "title"})
            for soft in names:
                soft_name = soft.text.strip('Free Download')
                link = soft.find('a')['href']
                wiki_response = requests.get(f"https://systemrequirements.wiki/{soft_name.replace(' ', '_')}",
                                             headers=headers)
                if wiki_response.status_code != 200:
                    time.sleep(2)
                    links.append(link)
    else:
        names = soup.find_all('h2')
        for soft in names:
            soft_name = soft.text.strip('Free Download')
            link = soft.find('a')['href']
            wiki_response = requests.get(f"https://systemrequirements.wiki/{soft_name.replace(' ', '_')}",
                                         headers=headers)
            if wiki_response.status_code != 200:
                time.sleep(2)
                links.append(link)
    return links



def loader(template: dict, title: str):
    """ This function loading game and soft templates to Wiki """
    # Set up the site object with your MediaWiki website's URL and API endpoint.
    site = mwclient.Site('meta.wikimedia.org', path='/w/')  # , scheme='https')

    # Log in with your admin credentials.
    site.login('YOUR_USERNAME', 'YOUR_PASSWORD')

    # Define the username and content for the user page.
    username = 'YOUR_USERNAME'
    userpage_content = template

    # Create the user page.
    userpage_title = title
    userpage = site.pages[userpage_title]
    result = userpage.save(userpage_content, summary=f'Creating new page {title}')
    print(f'{result["result"]} template loaded')


def main():
    """ This function include all logic which scrapes data from both game and soft websites, creating templates
     and loading templates to Wiki website """
    # loading game links
    game_links = check_new_games()
    #print('[+] loading game links')
    for game_link in game_links:
        # getting game requirements from game web page
        game_info = get_game_requirement(game_link)
        title = game_info.get('title')
        #print(f'[+] getting {title} info')
        # creating game template for loading to wiki
        game_template = games_template(game_info)
        #print(game_template)
        #print(f'[+] loading {title} template to Wiki')
        # loading game template to wiki
        loader(game_template, title)
    # getting soft categories links
    soft_categories = get_soft_categories()
    #print('[+] loading soft links')
    for link in soft_categories:
        # getting soft links from category
        soft_links = check_new_soft(link)
        for url in soft_links:
            # getting soft requirements from soft web page
            soft_info = get_soft_requirement(url)
            title = soft_info.get('title')
            #print(f'[+] getting {title} info')
            # creating soft template for loading to wiki
            soft_templ = soft_template(soft_info)
            print(f'[+] loading {title} template to Wiki')
            # loading soft template to wiki
            loader(soft_templ, title)


if __name__ == '__main__':
    # scheduler will start every 7 days
    schedule.every(7).days.do(main())