import csv
import time

import mwclient
import requests
import schedule as schedule
from bs4 import BeautifulSoup

from functions import get_game_requirement, get_soft_categories, get_software_links, get_soft_requirement, name
from templates import games_template, soft_template

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (X11;Ubuntu;Linuxx86_64;rv:109.0)Gecko/20100101 Firefox/110.0'
}


def check_new_games(letter: str):
    """ This function checking new games """
    info = {}
    links = []
    games = []

    print(f'[!] Checking games with letter {letter}')
    url = f'https://gamesystemrequirements.com/database/{letter.lower()}'
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    pages = soup.find(class_="pagenav_d").find_all('a')[-2].text

    for num in range(1, int(pages)+1):
        print(f'[+] checking page {num} of {pages}')
        url = f'https://gamesystemrequirements.com/database/{letter.lower()}/page/{num}'
#url = 'https://gamesystemrequirements.com/database/g/page/2'
        response = requests.get(url, headers=headers)
        #print(response.status_code)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            games_list = soup.find_all(class_="gr_box")
            for game in games_list:
                game_name = game['title']
                game_link = game['href']
                games.append(game_name)
                wiki_response = requests.get(f"https://systemrequirements.wiki/{game_name.replace(' ', '_')}",
                                             headers=headers)
                if wiki_response.status_code != 200:
                    time.sleep(2)
                    links.append(game_link)
    info['links'] = links
    info['games'] = games
    return info


def check_new_soft(start_url):
    """ This function checking new soft """
    info = {}
    links = []
    soft_names = []
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
                soft_names.append(soft_name)
                wiki_response = requests.get(f"https://systemrequirements.wiki/{soft_name.replace(' ', '_')}",
                                             headers=headers)
                if wiki_response.status_code == 200:
                    time.sleep(2)
                    links.append(link)
        info['soft'] = soft_names
        info['links'] = links
        return info
    else:
        names = soup.find_all('h2')
        for soft in names:
            soft_name = soft.text.strip('Free Download')
            link = soft.find('a')['href']
            soft_names.append(soft_name)
            wiki_response = requests.get(f"https://systemrequirements.wiki/{soft_name.replace(' ', '_')}",
                                         headers=headers)
            if wiki_response.status_code == 200:
                time.sleep(2)
                links.append(link)
        info['soft'] = soft_names
        info['links'] = links
        return info



def loader(template: dict, title: str):
    """ This function loading game and soft templates to Wiki """
    # Set up the site object with your MediaWiki website's URL and API endpoint.
    site = mwclient.Site('systemrequirements.wiki', path='/', scheme='https')

    # Log in with your admin credentials.
    site.login('sreqsadmin', '9u)$(WTG_9rg8GR')

    # Define the username and content for the user page.
    username = 'sreqsadmin'
    userpage_content = template

    # Create the user page.
    userpage_title = title
    userpage = site.pages[userpage_title]
    result = userpage.save(userpage_content, summary=f'Creating new page {title}')
    print(f'{result["result"]} {title} template loaded')


def games_index_loader(games_list: list, letter: str):
    """ This function loading game indexes to Wiki """
    # Set up the site object with your MediaWiki website's URL and API endpoint.
    site = mwclient.Site('systemrequirements.wiki', path='/', scheme='https')

    # Log in with your admin credentials.
    site.login('sreqsadmin', '9u)$(WTG_9rg8GR')

    # Define the username and content for the user page.
    username = 'sreqsadmin'
    userpage_content = '\n\n'.join([f'[[{name}]]' for name in games_list])

    # Create the user page.
    userpage_title = f'Games beginning with {letter}'
    userpage = site.pages[userpage_title]
    result = userpage.save(userpage_content, summary=f'Creating new page for {letter}')
    print(f'{result["result"]} indexes loaded')


def soft_index_loader(some_list: list, letter: str, index_title: str):
    """ This function loading soft indexes to Wiki """
    # Set up the site object with your MediaWiki website's URL and API endpoint.
    site = mwclient.Site('systemrequirements.wiki', path='/', scheme='https')

    # Log in with your admin credentials.
    site.login('sreqsadmin', '9u)$(WTG_9rg8GR')

    # Define the username and content for the user page.
    username = 'sreqsadmin'
    userpage_content = '\n\n'.join([f'[[{name}]]' for name in some_list])

    # Create the user page.
    userpage_title = f'{index_title} {letter}'
    userpage = site.pages[userpage_title]
    userpage.append(userpage_content)
    result = userpage.save(f'Editing page info for {letter}')
    print(f'{result["result"]} indexes loaded')


def names_sorter(raw_data, alphabet, index_title):
    clear_data = []
    for name in raw_data:
        # name = name.split('Download')[0]
        clear_data.append(name.strip(' \n-,.\u200b\xa0').replace('[', '(').replace(']', ')'))
    sorted_data = sorted(set(clear_data))

    for letter in alphabet:
        letter_list = [elem for elem in sorted_data if elem.startswith(letter)]
        print(letter_list)
        soft_index_loader(letter_list, letter, index_title)
        return f'Page for {letter} edited'


def games_processor():
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0-9']
    for letter in alphabet:
        info = check_new_games(letter)
        games = info.get('games')
        # loading game links
        game_links = info.get('links')
        # print('[+] loading game links')
        for game_link in game_links:
            # getting game requirements from game web page
            game_info = get_game_requirement(game_link)
            title = game_info.get('title')
            # print(f'[+] getting {title} info')
            # creating game template for loading to wiki
            game_template = games_template(game_info)
            # print(f'[+] loading {title} template to Wiki')
            # loading game template to wiki
            loader(game_template, title)
            games_index_loader(games, letter)


def soft_processor():
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0-9']
    # getting soft categories links
    soft_categories = get_soft_categories()
    all_names = []
    new_names = []
    for link in soft_categories:
        print('[+] loading soft links')
        # getting soft links from category
        new_soft = check_new_soft(link)
        names = new_soft.get('soft')
        all_names.append(names)
        soft_links = new_soft.get('links')
        for url in soft_links:
            # getting soft requirements from soft web page
            soft_info = get_soft_requirement(url)
            title = soft_info.get('title')
            new_names.append(title)
            # print(f'[+] getting {title} info')
            # creating soft template for loading to wiki
            soft_templ = soft_template(soft_info)
            print(f'[+] loading {title} template to Wiki')
            # loading soft template to wiki
            loader(soft_templ, title)
            names_sorter(new_names, alphabet, 'Software beginning with')


def main():
    """ This function runs all logic processors which scrapes data from both game and soft websites, creating templates
     and loading templates to Wiki website """
    #games_processor()
    soft_processor()


if __name__ == '__main__':
    # scheduler will start every 7 days
    #schedule.every(7).days.do(main())
    main() # to run it manually