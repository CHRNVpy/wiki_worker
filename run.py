import csv
import time

import mwclient
import requests
import schedule as schedule
from bs4 import BeautifulSoup

from functions import get_game_requirement, get_soft_categories, get_software_links, get_soft_requirement
from templates import games_template, soft_template


def check_new_games(letter: str):
    """ This function checking new games """
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (X11;Ubuntu;Linuxx86_64;rv:109.0)Gecko/20100101 Firefox/110.0'
    }

    info = {}
    links = []
    games = []

    print(f'[!] Checking games with letter {letter}')
    url = f'https://gamesystemrequirements.com/database/{letter.lower()}'
    res = requests.get(url, headers=headers)
    # print(res.status_code)
    soup = BeautifulSoup(res.text, 'html.parser')
    if soup.find(class_="pagenav_d"):
        pages = soup.find(class_="pagenav_d").find_all('a')[-2].text

        for num in range(1, int(pages) + 1):
            print(f'[+] checking page {num} of {pages}')
            url = f'https://gamesystemrequirements.com/database/{letter.lower()}/page/{num}'
            # url = 'https://gamesystemrequirements.com/database/g/page/2'
            response = requests.get(url, headers=headers)
            # print(response.status_code)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                games_list = soup.find_all(class_="gr_box")
                for game in games_list:
                    game_name = game['title'].replace('[', '(').replace(']', ')').strip('#')
                    game_link = game['href']
                    games.append(game_name)
                    wiki_response = requests.get(f"https://systemrequirements.wiki/{game_name.replace(' ', '_')}",
                                                 headers=headers)
                    # print(wiki_response.status_code)
                    if wiki_response.status_code != 200:
                        print(f'[+] new game found {game_name}')
                        #time.sleep(2)
                        links.append(game_link)
        info['links'] = links
        info['games'] = games
        return info
    else:
        url = f'https://gamesystemrequirements.com/database/{letter.lower()}'
        # url = 'https://gamesystemrequirements.com/database/g/page/2'
        response = requests.get(url, headers=headers)
        # print(response.status_code)
        if response.status_code == 200:
            print('one page')
            soup = BeautifulSoup(response.text, 'html.parser')
            games_list = soup.find_all(class_="gr_box")
            for game in games_list:
                game_name = game['title'].replace('[', '(').replace(']', ')').strip('#')
                game_link = game['href']
                games.append(game_name)
                wiki_response = requests.get(f"https://systemrequirements.wiki/{game_name.replace(' ', '_')}",
                                             headers=headers)
                if wiki_response.status_code != 200:
                    print(f'[+] new game found {game_name}')
                    # time.sleep(2)
                    links.append(game_link)
        info['links'] = links
        info['games'] = games
        return info


def check_new_soft(start_url):
    """ This function checking new soft """
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (X11;Ubuntu;Linuxx86_64;rv:109.0)Gecko/20100101 Firefox/110.0'
    }
    info = {}
    links = []
    soft_names = []
    raw_soft_names = []
    gen_response = requests.get(url=start_url, headers=headers)
    soup = BeautifulSoup(gen_response.text, 'html.parser')
    # title = soup.find(class_="title archive-category").text
    if soup.find(class_='page-navi pagination numbers clear-block'):
        pages = soup.find(class_='page-navi pagination numbers clear-block').find_all('a')[-2].text
        for i in range(1, int(pages) + 1):
            url = start_url + f'page/{i}/'
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            names = soup.find_all('h2', {'class': "title"})
            for soft in names:
                soft_name = soft.text.split('Free Download')[0].strip()
                raw_soft_name = soft.text
                url_name = soft_name.replace(' ', '_').replace('`', '').replace('[', '(').replace(']', ')')
                link = soft.find('a')['href']
                soft_names.append(soft_name)
                raw_soft_names.append(raw_soft_name)
                print(url_name)
                wiki_response = requests.get(url=f"http://systemrequirements.wiki/{url_name}", headers=headers)
                if wiki_response.status_code != 200:
                    # print(f"https://systemrequirements.wiki/{url_name}")
                    print(wiki_response.status_code)
                    print(f'[+] parsing {soft_name} info')
                    time.sleep(2)
                    links.append(link)
        info['soft'] = soft_names
        info['links'] = links
        return info
    else:
        names = soup.find_all('h2')
        for soft in names:
            soft_name = soft.text.split('Free Download')[0].strip()
            raw_soft_name = soft.text
            url_name = soft_name.replace(' ', '_').replace('`', '').replace('[', '(').replace(']', ')')
            link = soft.find('a')['href']
            soft_names.append(soft_name)
            raw_soft_names.append(raw_soft_name)
            wiki_response = requests.get(f"https://systemrequirements.wiki/{url_name}", headers=headers)
            if wiki_response.status_code != 200:
                # print(wiki_response.status_code)
                # print(f"https://systemrequirements.wiki/{url_name}")
                print(f'[+] parsing {soft_name} info')
                time.sleep(2)
                links.append(link)
        info['soft'] = soft_names
        info['links'] = links
    with open('all_raw_names.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(raw_soft_names)
    return info


def loader(template: dict, title: str):
    """ This function loading game and soft templates to Wiki """
    # Set up the site object with your MediaWiki website's URL and API endpoint.
    site = mwclient.Site('systemrequirements.wiki', path='/', scheme='https')

    # Log in with your admin credentials.
    site.login('LOGIN', 'PASSWORD')

    # Define the username and content for the user page.
    username = 'LOGIN'
    userpage_content = template

    # Create the user page.
    userpage_title = title.replace('[', '(').replace(']', ')').strip('#')
    userpage = site.pages[userpage_title]
    result = userpage.save(userpage_content, summary=f'Creating new page {title}')
    print(f'{result["result"]} {title} template loaded')


def games_index_loader(games_list: list, letter: str):
    """ This function loading game indexes to Wiki """
    # Set up the site object with your MediaWiki website's URL and API endpoint.
    site = mwclient.Site('systemrequirements.wiki', path='/', scheme='https')

    # Log in with your admin credentials.
    site.login('LOGIN', 'PASSWORD')

    # Define the username and content for the user page.
    username = 'LOGIN'
    userpage_content = '\n\n'.join([f'[[{name}]]' for name in games_list])

    # Create the user page.
    userpage_title = f'Games beginning with {letter}'
    userpage = site.pages[userpage_title]
    result = userpage.save(userpage_content, summary=f'Creating new page for {letter}')
    print(f'{result["result"]} indexes loaded')


def soft_index_loader(some_list: list, letter: str):
    """ This function loading soft indexes to Wiki """
    # Set up the site object with your MediaWiki website's URL and API endpoint.
    site = mwclient.Site('systemrequirements.wiki', path='/', scheme='https')

    # Log in with your admin credentials.
    site.login('LOGIN', 'PASSWORD')

    # Define the username and content for the user page.
    username = 'LOGIN'
    userpage_content = '\n\n'.join([f'[[{name}]]' for name in some_list])

    # Create the user page.
    userpage_title = f'Software beginning with {letter}'
    userpage = site.pages[userpage_title]
    result = userpage.save(userpage_content, summary=f'Creating new index page for {userpage_title}')
    print(f'{result["result"]} soft indexes for {letter} loaded')


def soft_names_sorter(some_data: list):
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    clear_data = []
    for item in some_data:
        # name = name.split('Download')[0]
        clear_data.append(item.replace('[', '(').replace(']', ')').replace('Download', '').replace
                          ('Portable', '').replace('+', '').replace('Free Download', '').replace('Free', '').replace
                          ('for Mac OS', '').replace('for Mac OS X', '').replace('For Mac OS', '').replace
                          ('Mac OSX', '').replace('Mac OS X', '').replace('for Mac', '').replace('For Mac', '').replace
                          ('\u200b', '').replace('\xa0', '').strip(',\n '))
    sorted_data = sorted(set(clear_data))

    for letter in alphabet:
        letter_list = [elem for elem in sorted_data if elem.lower().startswith(letter.lower())]
        # print(letter_list)
        soft_index_loader(letter_list, letter)
    non_alpha_list = [elem for elem in sorted_data if not elem[0].isalpha()]
    # print(non_alpha_list)
    soft_index_loader(non_alpha_list, '0-9')


def games_processor():
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0-9']
    for letter in alphabet:
        info = check_new_games(letter)
        games = info.get('games')
        # loading game links
        game_links = info.get('links')
        print('[+] loading game links')
        for game_link in game_links:
            # getting game requirements from game web page
            game_info = get_game_requirement(game_link)
            title = game_info.get('title')
            print(f'[+] getting {title} info')
            # creating game template for loading to wiki
            game_template = games_template(game_info)
            print(f'[+] loading {title} template to Wiki')
            # loading game template to wiki
            loader(game_template, title)
        games_index_loader(games, letter)


def soft_processor():
    # getting soft categories links
    soft_categories = get_soft_categories()
    data = []
    for link in soft_categories:
        category = link.split('/')[-2]
        print(f'[+] loading {category} soft links')
        # getting soft links from category
        new_soft = check_new_soft(link)
        soft_links = new_soft.get('links')
        for url in soft_links:
            # getting soft requirements from soft web page
            soft_info = get_soft_requirement(url)
            title = soft_info.get('title').replace('Download', '')
            print(f'[+] getting {title} info')
            # creating soft template for loading to wiki
            soft_templ = soft_template(soft_info)
            print(f'[+] loading {title} template to Wiki')
            # loading soft template to wiki
            loader(soft_templ, title)
    with open('all_raw_names.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for name in reader:
            data.append(name)
    data = data[0]
    soft_names_sorter(data)


def main():
    """ This function runs all logic processors which scrapes data from both game and soft websites, creating templates
     and loading templates to Wiki website """
    games_processor()
    # soft_processor()


if __name__ == '__main__':
    ''' scheduler will start every 7 days or run main() manually'''
    # schedule.every(7).days.do(main()) # uncomment this string to run it manually
    main()  # uncomment this string to run it manually
