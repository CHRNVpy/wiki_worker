import csv
import json
import os
import time
from pprint import pprint

import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp

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
    url = 'https://getintopc.com/all-software-categories/'
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    soft_categories = soup.find(class_="vertical-menu").find_all('a')
    cat_name_list = []
    cat_url_list = []
    with open(f'software_categories_links.csv', 'a') as file:
        writer = csv.writer(file)
        for category in soft_categories[1:]:
            cat_name = category.text.split('(')[0].strip(' ')
            cat_url = category['href']
            cat_name_list.append(cat_name)
            cat_url_list.append(cat_url)
            writer.writerow([cat_name, cat_url])
    return cat_url_list


def get_software_links(start_url):
    links = []
    #start_url = 'https://getintopc.com/softwares/3d-printing/'
    gen_response = requests.get(url=start_url, headers=headers)
    soup = BeautifulSoup(gen_response.text, 'html.parser')
    title = soup.find(class_="title archive-category").text
    # path = 'Soft'
    # if not os.path.exists(path):
    #     os.makedirs(path)
    # with open(f'Soft/{title}.csv', 'a') as file:
    #     writer = csv.writer(file)
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
                # print(f'Saving {soft_name}')
    else:
        names = soup.find_all('h2')
        for soft in names:
            soft_name = soft.text.strip('Free Download')
            link = soft.find('a')['href']
            links.append(link)
            # writer.writerow([soft_name, link])
            # print(f'Saving {soft_name}')
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
    if len(requirements) > 0:
        minimum_header = requirements[0].find('h2').text
        if len(requirements[0].find_all(class_="gsr_label")) > 0:
            param_1 = requirements[0].find_all(class_="gsr_label")[0].text
            param_1_req = requirements[0].find_all(class_="gsr_text")[0].text
            minimum_dict[param_1] = param_1_req
            requirements_dict[minimum_header] = minimum_dict
        if len(requirements[0].find_all(class_="gsr_label")) > 1:
            param_2 = requirements[0].find_all(class_="gsr_label")[1].text
            param_2_req = requirements[0].find_all(class_="gsr_text")[1].text
            minimum_dict[param_2] = param_2_req
            requirements_dict[minimum_header] = minimum_dict
        if len(requirements[0].find_all(class_="gsr_label")) > 2:
            param_3 = requirements[0].find_all(class_="gsr_label")[2].text
            param_3_req = requirements[0].find_all(class_="gsr_text")[2].text
            minimum_dict[param_3] = param_3_req
            requirements_dict[minimum_header] = minimum_dict
        if len(requirements[0].find_all(class_="gsr_label")) > 3:
            param_4 = requirements[0].find_all(class_="gsr_label")[3].text
            param_4_req = requirements[0].find_all(class_="gsr_text")[3].text
            minimum_dict[param_4] = param_4_req
            requirements_dict[minimum_header] = minimum_dict
        if len(requirements[0].find_all(class_="gsr_label")) > 4:
            param_5 = requirements[0].find_all(class_="gsr_label")[4].text
            param_5_req = requirements[0].find_all(class_="gsr_text")[4].text
            minimum_dict[param_5] = param_5_req
            requirements_dict[minimum_header] = minimum_dict
        if len(requirements[0].find_all(class_="gsr_label")) > 5:
            param_6 = requirements[0].find_all(class_="gsr_label")[5].text
            param_6_req = requirements[0].find_all(class_="gsr_text")[5].text
            minimum_dict[param_6] = param_6_req
            requirements_dict[minimum_header] = minimum_dict
        if len(requirements[0].find_all(class_="gsr_label")) > 6:
            param_7 = requirements[0].find_all(class_="gsr_label")[6].text
            param_7_req = requirements[0].find_all(class_="gsr_text")[6].text
            minimum_dict[param_7] = param_7_req
            requirements_dict[minimum_header] = minimum_dict

    if len(requirements) > 1:
        try:
            recommend_header = requirements[1].find('h2').text
            if len(requirements[1].find_all(class_="gsr_label")) > 0:
                rec_param_1 = requirements[1].find_all(class_="gsr_label")[0].text
                rec_param_1_req = requirements[1].find_all(class_="gsr_text")[0].text
                recommend_dict[rec_param_1] = rec_param_1_req
            if len(requirements[1].find_all(class_="gsr_label")) > 1:
                rec_param_2 = requirements[1].find_all(class_="gsr_label")[1].text
                rec_param_2_req = requirements[1].find_all(class_="gsr_text")[1].text
                recommend_dict[rec_param_2] = rec_param_2_req
            if len(requirements[1].find_all(class_="gsr_label")) > 2:
                rec_param_3 = requirements[1].find_all(class_="gsr_label")[2].text
                rec_param_3_req = requirements[1].find_all(class_="gsr_text")[2].text
                recommend_dict[rec_param_3] = rec_param_3_req
            if len(requirements[1].find_all(class_="gsr_label")) > 3:
                rec_param_4 = requirements[1].find_all(class_="gsr_label")[3].text
                rec_param_4_req = requirements[1].find_all(class_="gsr_text")[3].text
                recommend_dict[rec_param_4] = rec_param_4_req
            if len(requirements[1].find_all(class_="gsr_label")) > 4:
                rec_param_5 = requirements[1].find_all(class_="gsr_label")[4].text
                rec_param_5_req = requirements[1].find_all(class_="gsr_text")[4].text
                recommend_dict[rec_param_5] = rec_param_5_req
                requirements_dict[recommend_header] = recommend_dict
            if len(requirements[1].find_all(class_="gsr_label")) > 5:
                rec_param_6 = requirements[1].find_all(class_="gsr_label")[5].text
                rec_param_6_req = requirements[1].find_all(class_="gsr_text")[5].text
                recommend_dict[rec_param_6] = rec_param_6_req
                requirements_dict[recommend_header] = recommend_dict
            if len(requirements[1].find_all(class_="gsr_text")) > 6:
                rec_param_7 = requirements[1].find_all(class_="gsr_label")[6].text
                rec_param_7_req = requirements[1].find_all(class_="gsr_text")[6].text
                recommend_dict[rec_param_7] = rec_param_7_req
                requirements_dict[recommend_header] = recommend_dict
        except AttributeError:
            recommend_header = requirements[1].find_all(class_="gsr_text")[0].text
            requirements_dict[recommend_header.split(':')[0]] = recommend_header.split(':')[1]
    if len(requirements) > 2:
        note = requirements[2].find(class_="gsr_text").text
        requirements_dict['note'] = note
    return requirements_dict


def get_soft_requirement(url: str):
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    block = soup.find_all('h2')
    info = {}
    soft_requirement = {}
    for index, i in enumerate(block):
        if block[index].text.lower().split(' for')[0] == 'system requirements':
            sys_req_block = block[index].text.lower().split(' for')
            header = sys_req_block[0].capitalize()
            if len(sys_req_block) > 1:
                soft_name = sys_req_block[1].strip(' ').capitalize()
                info['title'] = soft_name
            else:
                soft_name = soup.find('h1').text.lower().split(' free download')[0].capitalize()
                info['title'] = soft_name
            reqs = block[index].findNext('ul').find_all('li')
            params = {}
            params_list = []
            for ind, j in enumerate(reqs):
                parameter = reqs[ind].text
                if len(parameter.split(':')) > 1:
                    param_name = parameter.split(':')[0]
                    param_param = parameter.split(':')[1].strip()
                    params[param_name] = param_param
                else:
                    params['*'] = parameter
            params_list.append(params)
            info[header] = params_list
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


#def main():
    # data = get_soft_categories()
    # for i in data[15:]:
    #     get_software(i)
    #     time.sleep(3)
    # pprint(get_game_requirement('https://gamesystemrequirements.com/game/shootmania-storm'))
    #req_json_maker('Soft', 'Soft_processed', get_soft_requirement)
    #print(get_soft_requirement('https://getintopc.com/softwares/video-editing/vsdc-video-editor-for-windows-free-download/'))
    #check_new_games()


# if __name__ == '__main__':
#     main()
