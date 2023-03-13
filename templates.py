import json
import time


def games_template(data):
    """ This function making templates for games """
    dict_keys = [i for i in data.keys()]

    if len(dict_keys) > 3:
        if type(data.get(dict_keys[2])) != str:
            header = f"=== {dict_keys[1]} ===\n"
            body = '\n\n'.join([f"'''{key}''' {value}" for key, value in data.get(dict_keys[1]).items()])
            header2 = f'=== {dict_keys[2]} ===\n'
            body2 = '\n\n'.join([f"'''{key}''' {value}" for key, value in data.get(dict_keys[2]).items()])
            note = f"'''{dict_keys[3].upper()}''': {data.get(dict_keys[3]).strip('NOTE:')}"
            template = f'== Windows ==\n' \
                       f'{header}' \
                       f'{body}\n' \
                       f'{header2}' \
                       f'{body2}\n\n' \
                       f'{note}'
            return template
        else:
            header = f"=== {dict_keys[1]} ===\n"
            body = '\n\n'.join([f"'''{key}''' {value}" for key, value in data.get(dict_keys[1]).items()])
            note = f"'''{dict_keys[2].upper()}''': {data.get(dict_keys[2])}"
            note2 = f"'''{dict_keys[3].upper()}''': {data.get(dict_keys[3]).strip('NOTE:')}"
            template = f'== Windows ==\n' \
                       f'{header}' \
                       f'{body}\n\n' \
                       f'{note}\n\n' \
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
            note = f"'''{dict_keys[2].upper()}''': {data.get(dict_keys[2]).strip('NOTE:')}"
            template = f'== Windows ==\n' \
                       f'{header}' \
                       f'{body}\n\n' \
                       f'{note}'
            return template
    elif len(dict_keys) > 1:
        header = f"=== {dict_keys[1]} ===\n"
        body = '\n\n'.join([f"'''{key}''' {value}" for key, value in data.get(dict_keys[1]).items()])
        template = f'== Windows ==\n' \
                   f'{header}' \
                   f'{body}'
        return template
    else:
        print(f'Sorry, no any info yet')


def soft_template(data):
    """ This function making templates for soft """
    dict_keys = [i for i in data.keys()]

    header = f"=== {dict_keys[1]} ===\n"
    body = '\n\n'.join([f"'''{key}''': {value}" for key, value in data.get(dict_keys[1])[0].items()])
    #note = f"'''{dict_keys[3].upper()}''': {data.get(dict_keys[3]).strip('NOTE:')}"
    template = f'== Windows ==\n' \
               f'{header}' \
               f'{body}\n' \
               #f'{note}'
    return template
