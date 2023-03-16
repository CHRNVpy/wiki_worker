import csv
import json
import os
import time
from pprint import pprint

import requests
from bs4 import BeautifulSoup


headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (X11;Ubuntu;Linuxx86_64;rv:109.0)Gecko/20100101 Firefox/110.0'
}


def get_games(path='Games_processed'):
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0-9']

    for letter in alphabet:
        print(f'Current letter {letter}')
        with open(f'Games/Games_{letter}.csv') as file:
            writer = csv.writer(file)
            for num in range(1, 11):
                url = f'https://gamesystemrequirements.com/database/{letter.lower()}/page/{num}'
                print(url)
                response = requests.get(url, headers=headers)
                print(response.status_code)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    games_list = soup.find_all(class_="gr_box")
                    for game in games_list:
                        game_name = game['title']
                        game_link = game['href']
                        print(game_name)
                        print(game_link)
                        writer.writerow([game_name, game_link])
                    time.sleep(5)
                else:
                    print(f'Page: {num} - not existing page')


def check_new_games():
    with open(f'Games_processed/Games_A.csv', newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        rows = [row for row in reader]
    list = []
    for row in rows:
        list.append(row[0])
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0-9']

    for letter in alphabet:
        print(f'Current letter {letter}')
        url = f'https://gamesystemrequirements.com/database/{letter.lower()}'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        pages = soup.find(class_="pagenav_d").find_all('a')[-2].text
        for num in range(1, int(pages)+1):
            url = f'https://gamesystemrequirements.com/database/{letter.lower()}/page/{num}'
            response = requests.get(url, headers=headers)
            print(response.status_code)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                games_list = soup.find_all(class_="gr_box")
                for game in games_list:
                    game_name = game['title']
                    game_link = game['href']
                    if game_name not in list:
                        print(f'{game_name} not in list')
                        #print(game_link)
                time.sleep(5)


def get_soft_categories():
    print(f'[+] parsing soft categories')
    url = 'https://getintopc.com/all-software-categories/'
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    soft_categories = soup.find(class_="vertical-menu").find_all('a')
    cat_name_list = []
    cat_url_list = []
    # with open(f'software_categories_links.csv', 'a') as file:
    #     writer = csv.writer(file)
    for category in soft_categories[1:]:
        cat_name = category.text.split('(')[0].strip(' ')
        cat_url = category['href']
        cat_name_list.append(cat_name)
        cat_url_list.append(cat_url)
    return cat_url_list


def get_software_links(start_url):
    links = []
    gen_response = requests.get(url=start_url, headers=headers)
    soup = BeautifulSoup(gen_response.text, 'html.parser')
    title = soup.find(class_="title archive-category").text
    print(f'[+] Parsing {title}')
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
                links.append(link)
                # writer.writerow([soft_name, link])
                print(f'Saving {soft_name}')
    else:
        names = soup.find_all('h2')
        for soft in names:
            soft_name = soft.text.strip('Free Download')
            link = soft.find('a')['href']
            links.append(link)
            print(f'Saving {soft_name}')
    return links


def get_game_requirement(url: str):
    requirements_dict = {}
    minimum_dict = {}
    recommend_dict = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find(class_="main-panel").find('h1').text
    requirements_dict['title'] = title.split(' System Requirements')[0]
    requirements = soup.find_all(class_="gsr_section")
    for index, section in enumerate(requirements):
        if index == 0 and len(section) > 1:
            min_header = requirements[index].find('h2').text
            rows = section.find_all(class_="gsr_row")
            for i in rows:
                param_name = i.find(class_="gsr_label").text
                param = i.find(class_="gsr_text").text.strip('\r\n')
                minimum_dict[param_name] = param
            requirements_dict[min_header] = minimum_dict
        elif index == 1:
            if len(section) > 1:
                rec_header = requirements[index].find('h2').text
                rows = section.find_all(class_="gsr_row")
                for i in rows:
                    param_name = i.find(class_="gsr_label").text
                    param = i.find(class_="gsr_text").text
                    recommend_dict[param_name] = param
                requirements_dict[rec_header] = recommend_dict
            elif len(section.find_all('br')) > 0:
                big_note = '\n'.join([sec.text for sec in section])
                requirements_dict['NOTE'] = big_note
            else:
                try:
                    param_name = section.find(class_="gsr_text").text.split(':')[0]
                    param = '\n'.join([sec for sec in section.find(class_="gsr_text").text.split(':')[1:]])
                    requirements_dict[param_name] = param
                except AttributeError:
                    rec_header = requirements[index].find('h2').text
                    requirements_dict[rec_header] = ''
        elif index == 2 and len(section) > 0:
            if len(section.find_all('br')) > 1:
                big_note = '\n'.join([sec.text for sec in section])
                requirements_dict['NOTE'] = big_note
            else:
                param_name = section.find(class_="gsr_text").text.split(':')[0]
                param = section.find(class_="gsr_text").text.split(':')[1]
                requirements_dict[param_name] = param
        elif index == 3 and len(section) > 0:
            if len(section.find_all('br')) > 0:
                big_note = '\n'.join([sec.text for sec in section])
                requirements_dict['NOTE'] = big_note
            else:
                param_name = section.find(class_="gsr_text").text.split(':')[0]
                param = section.find(class_="gsr_text").text.split(':')[1]
                requirements_dict[param_name] = param
    return requirements_dict


def get_soft_requirement(url: str):
    response = requests.get(url, headers=headers)
    info = {}
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find(class_="title").text.split(' Free Download')[0]
    info['title'] = title
    block = soup.find_all('h2')
    tags = []
    for h2 in block:
        if 'system requirements' in h2.text.lower():
            start_h2 = soup.find('h2', string=h2.text)
            while start_h2.findNextSibling() != start_h2.findNext('h2'):
                tags.append(start_h2.findNextSibling())
                start_h2 = start_h2.findNextSibling()
    p_list = []
    li_list = []
    for tag in tags:
        if tag.name == 'p':
            p_list.append(tag.text)
        if tag.name == 'ul':
            for li in tag:
                li_list.append(li.text)
    if len(p_list) > 0:
        p_list.pop(0)
    info['p'] = p_list
    info['li'] = li_list
    print(info)
    return info


def req_json_maker(path='Games', destination='Games_processed', function=get_game_requirement):
    # path = 'Games'
    # destination = 'Games_processed'
    file_list = os.listdir(path)
    for file in file_list:
        print(f'{file} processing')
        req_list = []
        with open(f'{path}/{file}', 'r') as f:
            data = csv.reader(f)
            for link in data:
                url = link[1]
                req_list.append(function(url))
                #time.sleep(3)
                print(f'Game/Soft: {link[0]} processed')
        if not os.path.exists(destination):
            os.makedirs(destination)
        with open(f'{destination}/{file.split(".")[0]}.json', 'w', encoding='utf-8') as j:
            json.dump(req_list, j, indent=4, ensure_ascii=False)
        os.rename(f'{path}/{file}', f'{destination}/{file}')
        print(f'{file.split(".")[0]} done')



def main():
    # data = get_soft_categories()
    # for i in data[15:]:
    #     get_software(i)
    #     time.sleep(3)
    #pprint(get_game_requirement('https://gamesystemrequirements.com/game/fear-combat'))
    # req_json_maker('Soft', 'Soft_processed', get_soft_requirement)
    get_soft_requirement('https://getintopc.com/softwares/dwkit-core-ultimate-free-download/')
    # check_new_games()



if __name__ == '__main__':
    main()
