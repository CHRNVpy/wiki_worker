import json
import time
from functions import get_game_requirement, get_soft_requirement


def games_template(data):
    """ This function making templates for games """
    dict_keys = [i for i in data.keys()]
    print(dict_keys)

    if len(dict_keys) > 4:
        if type(data.get(dict_keys[1])) != str:
            header = f"=== {dict_keys[1]} ===\n"
            body = '\n\n'.join([f"'''{key}''' {value}" for key, value in data.get(dict_keys[1]).items()])
            header2 = f'=== {dict_keys[2]} ===\n'
            body2 = '\n\n'.join([f"'''{key}''' {value}" for key, value in data.get(dict_keys[2]).items()])
            note = f"'''{dict_keys[3]}''': {data.get(dict_keys[3])}" #.strip('NOTE:')}"
            note2 = f"'''{dict_keys[4]}''': {data.get(dict_keys[4]).strip('NOTE:')}"
            template = f'== Windows ==\n' \
                       f'{header}' \
                       f'{body}\n' \
                       f'{header2}' \
                       f'{body2}\n\n' \
                       f'=== Additional details ===\n' \
                       f'{note}\n\n' \
                       f'{note2}'
            return template
    if len(dict_keys) > 3:
        if type(data.get(dict_keys[2])) != str:
            header = f"=== {dict_keys[1]} ===\n"
            body = '\n\n'.join([f"'''{key}''' {value}" for key, value in data.get(dict_keys[1]).items()])
            header2 = f'=== {dict_keys[2]} ===\n'
            body2 = '\n\n'.join([f"'''{key}''' {value}" for key, value in data.get(dict_keys[2]).items()])
            note = f"'''{dict_keys[3]}''': {data.get(dict_keys[3]).strip('NOTE:')}"
            template = f'== Windows ==\n' \
                       f'{header}' \
                       f'{body}\n' \
                       f'{header2}' \
                       f'{body2}\n\n' \
                       f'=== Additional details ===\n' \
                       f'{note}'
            return template
        else:
            header = f"=== {dict_keys[1]} ===\n"
            body = '\n\n'.join([f"'''{key}''' {value}" for key, value in data.get(dict_keys[1]).items()])
            note = f"'''{dict_keys[2]}''': {data.get(dict_keys[2])}"
            note2 = f"'''{dict_keys[3]}''': {data.get(dict_keys[3]).strip('NOTE:')}"
            template = f'== Windows ==\n' \
                       f'{header}' \
                       f'{body}\n' \
                       f'=== Additional details ===\n' \
                       f'{note}\n' \
                       f'{note2}'
            return template
    elif len(dict_keys) > 2:
        if type(data.get(dict_keys[2])) != str:
            header = f"=== {dict_keys[1]} ===\n"
            body = '\n\n'.join([f"'''{key}''' {value}" for key, value in data.get(dict_keys[1]).items()])
            header2 = f'=== {dict_keys[2]} ===\n'
            body2 = '\n\n'.join([f"'''{key}''' {value}" for key, value in data.get(dict_keys[2]).items()])
            template = f'== Windows ==\n' \
                       f'{header}' \
                       f'{body}\n' \
                       f'{header2}' \
                       f'{body2}'
            return template
        else:
            header = f"=== {dict_keys[1]} ===\n"
            body = '\n\n'.join([f"'''{key}''' {value}" for key, value in data.get(dict_keys[1]).items()])
            note = f"'''{dict_keys[2]}''': {data.get(dict_keys[2]).strip('NOTE:')}"
            if dict_keys[2] == 'Recommended system requirements:':
                template = f'== Windows ==\n' \
                           f'{header}' \
                           f'{body}\n' \
                           f'=== {dict_keys[2]} ==='
                return template
            else:
                template = f'== Windows ==\n' \
                           f'{header}' \
                           f'{body}\n' \
                           f'=== Additional details ===\n' \
                           f'{note}'
                return template
    elif len(dict_keys) > 1:
        body = '\n\n'.join([f"'''{key}''' {value}" for key, value in data.get(dict_keys[1]).items()])
        template = f'== Windows ==\n' \
                   f'{dict_keys[1]}\n' \
                   f'{body}'
        return template
    else:
        template = f" "
        return template


def soft_template(data):
    """ This function making templates for soft """

    if len(data.get('p')) > 0 and len(data.get('li')) > 0:
        new_list_p = []
        for p in data.get('p'):
            if ':' in p:
                new_p = f"'''{p.split(':')[0]}''': {p.split(':')[1]}"
                new_list_p.append(new_p)
            else:
                new_list_p.append(p)
        p = '\n\n'.join([el.strip() for el in new_list_p])
        new_list_li = []
        for li in data.get('li'):
            if ':' in li:
                new_li = f"'''{li.split(':')[0]}''': {li.split(':')[1]}"
                new_list_li.append(new_li)
            else:
                new_list_li.append(li)
        li = '\n\n'.join([el.strip() for el in new_list_li])
        template = f'== Windows ==\n' \
                   f'=== Minimum system requirements ===' \
                   f'{p}\n\n' \
                   f'{li}'
        return template
    elif len(data.get('p')) == 1:
        p = data.get('p')
        template = f'== Windows ==\n' \
                   f'=== Minimum system requirements ===\n' \
                   f'{p}'
        return template
    elif len(data.get('p')) > 1:
        new_list = []
        for p in data.get('p'):
            if ':' in p:
                new_p = f"'''{p.split(':')[0]}''': {p.split(':')[1]}"
                new_list.append(new_p)
            else:
                new_list.append(p)
        p = '\n\n'.join([el.strip() for el in new_list])
        template = f'== Windows ==\n' \
                   f'=== Minimum system requirements ===\n' \
                   f"{p}"
        return template
    elif len(data.get('li')) > 0:
        new_list = []
        for li in data.get('li'):
            if ':' in li:
                new_li = f"'''{li.split(':')[0]}''': {li.split(':')[1]}"
                new_list.append(new_li)
            else:
                new_list.append(li)
        li = '\n\n'.join([el.strip() for el in new_list])
        template = f'== Windows ==\n' \
                   f'=== Minimum system requirements ===\n' \
                   f'{li}'
        return template



# data = get_game_requirement('https://gamesystemrequirements.com/game/fear-combat')
# print(games_template(data))

# data = get_soft_requirement('https://getintopc.com/softwares/3d-analysis/mentor-graphics-hyperlynx-vx-2020-free-download/')
# print(soft_template(data))
