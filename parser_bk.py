import requests
from bs4 import BeautifulSoup as BS4
import lxml

URL_categorii = 'https://www.marathonbet.ru/su/betting/Tennis+-+2398?cpcids=all'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}

# Функция запроса на сайт
def get_html(url):
    r = requests.get(url, headers=HEADERS) #{'User-Agent': UserAgent().chrome}
    soup = BS4(r.text, 'lxml')
    return soup

# Функция сбора всех лиг, а именно их названий и ссылок
def ALL_categorii(soup):
    all_categorii = soup.find('div', class_='sport-category-content').find_all('td', class_='category-label-td')

    all_name_cat = {}
    all_href_cat = {}
    ALLS = []
    i = 1
    # цикл обработки лиг
    for categoriya in all_categorii:
        name_cat_list = categoriya.find('h2', class_='category-label').text.split('/')
        # Формирования название лиги
        if len(name_cat_list) != 1:
            cat = name_cat_list[0].split('.')
            del cat[-1]
            name_cat = cat[0]
            name_cat.strip('.')
        else:
            name_cat = name_cat_list[0]
        # Получение ссылки на лигу
        href_cat_list = f"https://www.marathonbet.ru{categoriya.find('a', class_='category-label-link').get('href')}".split(
            '/')
        href_cat = ''
        for cat in range(7): href_cat += f'{href_cat_list[cat]}/'
        # Фильтруем от лишних лиг и формируем списки названий и ссылок
        if (href_cat not in ALLS) and ('Турнир ITF' not in name_cat) and ('Серия Про Матч UTR' not in name_cat):
            all_name_cat[i] = f'{name_cat}'
            all_href_cat[i] = f'{href_cat}'
            ALLS.append(href_cat)
            i += 1

    return all_name_cat, all_href_cat

# Функция вызова сбора лиг
def alls(URL_categorii):
    soup = get_html(URL_categorii)

    all_name_cat, all_href_cat = ALL_categorii(soup)
    return all_name_cat, all_href_cat

# функция сбора ссылок на все матчи, принимает код страницы лиги, отдает спиок ссылок на все матчи
def ALL_game_in_one_liga(soup):
    all_game = soup.find_all('div', class_='bg coupon-row')#.find('div', class_='category-content')
    All_hrefs_in_game = []
    for game in all_game:
        href_in_game = f"https://www.marathonbet.ru/su/betting/{game.get('data-event-path')}"
        All_hrefs_in_game.append(href_in_game)
    return All_hrefs_in_game

# Функция по сбору данных, получает список ссылок на лиги, отдает список словарей со всеми необходимыми данными
def INFO_in_one_game(all_hrefs_in_game_one_liga):
    ALL_DATA = []
    for one_game in all_hrefs_in_game_one_liga:
        # print(one_game)
        soup = get_html(one_game)
        name_liga = soup.find('table', class_='category-header').find('h1', class_='category-label').text.strip()
        # print(name_liga)

        even = soup.find('div', class_='bg coupon-row').get('data-event-treeid')

        soup_head_info = soup.find_all('table', class_='coupon-row-item')[1]

        # Сбор основной информации
        names = soup_head_info.find('table', class_='member-area-content-table').find_all('a', class_='member-link')
        name_team_1 = names[0].text.strip()
        name_team_2 = names[1].text.strip()

        try:
            date_game = soup_head_info.find('td', class_='date date-short').text.strip()
        except:
            date_game = soup_head_info.find('td', class_='date date-with-month').text.strip()
        # print(date_game)

        try:
            time_game = soup_head_info.find('td', class_='date date-short').text.strip()
        except:
            time_game = soup_head_info.find('td', class_='date date-with-month').text.strip()

        all_head_info = soup_head_info.find('tr', class_='sub-row').find_all('td', class_='price')
        try:
            win_team_1 = all_head_info[0].text.strip()
            win_team_2 = all_head_info[1].text.strip()
        except:
            win_team_1 = '- -'
            win_team_2 = '- -'

        try:
            fora_1 = all_head_info[2].text.strip()
            fora_2 = all_head_info[3].text.strip()
        except:
            fora_1 = '- -'
            fora_2 = '- -'

        try:
            total_1 = all_head_info[4].text.strip()
            total_2 = all_head_info[5].text.strip()
        except:
            total_1 = '- -'
            total_2 = '- -'

        # print(f'{name_team_1} - {name_team_2} \nWIN {win_team_1} - {win_team_2} \nFORA {fora_1} - {fora_2}  \nTOTAL >{total_1} - <{total_2}')

        blocks_market = soup.find_all('div', class_='block-market-wrapper hidden')
        # Объявляем списки с подробной информацией
        statistika = {}
        double_errors = {}
        aces = {}
        # Запуска цикла по просмотре основных блоков
        for block in blocks_market:
            # Получаем имя блока
            name_block = block.find('div', class_='name-field').text.strip()

            # Проверка блока со СТАТИСТИКОЙ
            if name_block == 'Статистика':
                podblocki = block.find_all('div',class_='market-inline-block-table-wrapper')

                # Сбор информации из блока СТАТИСТИКА
                for podblock in podblocki:
                    name_podblock = podblock.find('div', class_='name-field').text.strip()
                    if name_podblock == 'У кого будет больше брейк-поинтов':
                        # print()
                        # print(name_podblock)
                        statistika['У кого будет больше брейк-поинтов'] = ''
                        results_left = podblock.find_all('div', class_='result-left')
                        results_right = podblock.find_all('div', class_='result-right')
                        for i in range(len(results_left)):
                            left = results_left[i].text.strip()
                            right = results_right[i].find("span").text.strip()
                            if left == name_team_1 or left == 'Поровну' or left == name_team_2:
                                statistika[f"{left}_1"] = right
                            # print(f'{left} - {right}')
                    elif name_podblock == 'У кого будет больше брейк-поинтов с учетом форы':
                        # print()
                        # print(name_podblock)
                        statistika['У кого будет больше брейк-поинтов с учетом форы'] = ''
                        ths = podblock.find_all('th')
                        tds = podblock.find_all('td', class_='price height-column-with-price $this.getStyle()')
                        for i in range(len(ths)):
                            if ths[i].text.strip() == name_team_1 or ths[i].text.strip() == name_team_2:
                                statistika[f"{ths[i].text.strip()}_2"] = tds[i].text.strip().replace('\n', '')
                            # print(ths[i].text.strip().replace('\n', ''))
                            # print(tds[i].text.strip().replace('\n', ''))
                    elif name_podblock == 'Тотал брейк-поинтов':
                        # print()
                        # print(name_podblock)
                        statistika['Тотал брейк-поинтов'] = ''
                        ths = podblock.find_all('th')
                        tds = podblock.find_all('td', class_='price height-column-with-price')
                        for i in range(len(ths)):
                            th = ths[i].text.strip().replace('\n', '')
                            td = tds[i].text.strip().replace('\n', '')
                            if th == 'Меньше' or th == 'Больше':
                                statistika[f"{th}_12"] = td
                            # print(ths[i].text.strip().replace('\n', ''))
                            # print(tds[i].text.strip().replace('\n', ''))

                    elif name_podblock.replace(' ', '') == f'Тотал брейк-поинтов ({name_team_1})'.replace(' ', ''):
                        # print()
                        # print(name_podblock)
                        statistika[f'Тотал брейк-поинтов ({name_team_1})'] = ''
                        ths = podblock.find_all('th')
                        tds = podblock.find_all('td', class_='price height-column-with-price')
                        for i in range(len(ths)):
                            th = ths[i].text.strip().replace('\n', '')
                            td = tds[i].text.strip().replace('\n', '')
                            if th == 'Меньше' or th == 'Больше':
                                statistika[f"{th}_13"] = td
                            # print(ths[i].text.strip().replace('\n', ''))
                            # print(tds[i].text.strip().replace('\n', ''))

                    elif name_podblock.replace(' ', '') == f'Тотал брейк-поинтов ({name_team_2})'.replace(' ', ''):
                        # print()
                        # print(name_podblock)
                        statistika[f'Тотал брейк-поинтов ({name_team_2})'] = ''
                        ths = podblock.find_all('th')
                        tds = podblock.find_all('td', class_='price height-column-with-price')
                        for i in range(len(ths)):
                            th = ths[i].text.strip().replace('\n', '')
                            td = tds[i].text.strip().replace('\n', '')
                            if th == 'Меньше' or th == 'Больше':
                                statistika[f"{th}_14"] = td
                            # print(ths[i].text.strip().replace('\n', ''))
                            # print(tds[i].text.strip().replace('\n', ''))

                    elif name_podblock == 'Кто совершит больше брейков':
                        # print()
                        # print(name_podblock)
                        statistika['Кто совершит больше брейков'] = ''
                        results_left = podblock.find_all('div', class_='result-left')
                        results_right = podblock.find_all('div', class_='result-right')
                        for i in range(len(results_left)):
                            if results_left[i].text.strip() == name_team_1 or results_left[i].text.strip() == 'Поровну' or results_left[i].text.strip() == name_team_2:
                                statistika[f"{results_left[i].text.strip()}_3"] = results_right[i].text.strip()
                            # print(f'{results_left[i].text.strip()} - {results_right[i].text.strip()}')
                    elif name_podblock == 'Кто совершит больше брейков с учетом форы':
                        # print()
                        # print(name_podblock)
                        statistika['Кто совершит больше брейков с учетом форы'] = ''
                        ths = podblock.find_all('th')
                        tds = podblock.find_all('td', class_='price height-column-with-price $this.getStyle()')
                        for i in range(len(ths)):
                            if ths[i].text.strip() == name_team_1 or ths[i].text.strip() == name_team_2:
                                statistika[f"{ths[i].text.strip()}_4"] = tds[i].text.strip().replace('\n', '')
                            # print(ths[i].text.strip().replace('\n', ''))
                            # print(tds[i].text.strip().replace('\n', ''))
                    elif name_podblock == 'Тотал брейков':
                        # print()
                        # print(name_podblock)
                        statistika['Тотал брейков'] = ''
                        ths = podblock.find_all('th')
                        tds = podblock.find_all('td', class_='price height-column-with-price')
                        for i in range(len(ths)):
                            if ths[i].text.strip() == 'Меньше' or ths[i].text.strip() == 'Больше':
                                statistika[f"{ths[i].text.strip()}_5"] = tds[i].text.strip().replace('\n', '')
                            # print(ths[i].text.strip().replace('\n', ''))
                            # print(tds[i].text.strip().replace('\n', ''))

                    elif name_podblock.replace(' ', '') == f'Тотал брейков ({name_team_1})'.replace(' ', ''):
                        # print()
                        # print(name_podblock)
                        statistika[f'Тотал брейков ({name_team_1})'] = ''
                        ths = podblock.find_all('th')
                        tds = podblock.find_all('td', class_='price height-column-with-price')
                        for i in range(len(ths)):
                            th = ths[i].text.strip().replace('\n', '')
                            td = tds[i].text.strip().replace('\n', '')
                            if th == 'Меньше' or th == 'Больше':
                                statistika[f"{th}_15"] = td
                            # print(ths[i].text.strip().replace('\n', ''))
                            # print(tds[i].text.strip().replace('\n', ''))

                    elif name_podblock.replace(' ', '') == f'Тотал брейков ({name_team_2})'.replace(' ', ''):
                        # print()
                        # print(name_podblock)
                        statistika[f'Тотал брейков ({name_team_2})'] = ''
                        ths = podblock.find_all('th')
                        tds = podblock.find_all('td', class_='price height-column-with-price')
                        for i in range(len(ths)):
                            th = ths[i].text.strip().replace('\n', '')
                            td = tds[i].text.strip().replace('\n', '')
                            if th == 'Меньше' or th == 'Больше':
                                statistika[f"{th}_16"] = td
                            # print(ths[i].text.strip().replace('\n', ''))
                            # print(tds[i].text.strip().replace('\n', ''))
            # Проверка блока ДВОЙНЫЕ ОШИБКИ
            elif name_block == 'Двойные ошибки':
                podblocki = block.find_all('div', class_='market-inline-block-table-wrapper')

                # цикл сбора информации по двойным ошибкам
                for podblock in podblocki:
                    name_podblock = podblock.find('div', class_='name-field').text.strip()
                    if name_podblock == 'Кто совершит больше двойных ошибок':
                        double_errors['Кто совершит больше двойных ошибок'] = ''
                        # print()
                        # print(name_podblock)
                        results_left = podblock.find_all('div', class_='result-left')
                        results_right = podblock.find_all('div', class_='result-right')
                        for i in range(len(results_left)):
                            if results_left[i].text.strip() == name_team_1 or results_left[i].text.strip() == 'Поровну' or results_left[i].text.strip() == name_team_2:
                                double_errors[f'{results_left[i].text.strip()}_6'] = results_right[i].text.strip()
                            # print(f'{results_left[i].text.strip()} - {results_right[i].text.strip()}')
                    elif name_podblock == 'Кто совершит больше двойных ошибок с учетом форы':
                        double_errors['Кто совершит больше двойных ошибок с учетом форы'] = ''
                        # print()
                        # print(name_podblock)
                        ths = podblock.find_all('th')
                        tds = podblock.find_all('td', class_='price height-column-with-price $this.getStyle()')
                        for i in range(len(ths)):
                            th = ths[i].text.strip().replace('\n', '')
                            td = tds[i].text.strip().replace('\n', '')
                            if th == name_team_1 or th == name_team_2:
                                double_errors[f"{th}_7"] = td
                            # print(ths[i].text.strip().replace('\n', ''))
                            # print(tds[i].text.strip().replace('\n', ''))
                    elif name_podblock == 'Тотал двойных ошибок':
                        double_errors['Тотал двойных ошибок'] = ''
                        # print()
                        # print(name_podblock)
                        ths = podblock.find_all('th')
                        tds = podblock.find_all('td', class_='price height-column-with-price')
                        for i in range(len(ths)):
                            th = ths[i].text.strip().replace('\n', '')
                            td = tds[i].text.strip().replace('\n', '')
                            if th == 'Меньше' or th == 'Больше':
                                double_errors[f"{th}_8"] = td
                            # print(ths[i].text.strip().replace('\n', ''))
                            # print(tds[i].text.strip().replace('\n', ''))
                    elif name_podblock.replace(' ', '') == f'Тотал двойных ошибок ({name_team_1})'.replace(' ', ''):
                        # print()
                        # print(name_podblock)
                        double_errors[f'Тотал двойных ошибок ({name_team_1})'] = ''
                        ths = podblock.find_all('th')
                        tds = podblock.find_all('td', class_='price height-column-with-price')
                        for i in range(len(ths)):
                            th = ths[i].text.strip().replace('\n', '')
                            td = tds[i].text.strip().replace('\n', '')
                            if th == 'Меньше' or th == 'Больше':
                                double_errors[f"{th}_19"] = td
                            # print(ths[i].text.strip().replace('\n', ''))
                            # print(tds[i].text.strip().replace('\n', ''))
                    elif name_podblock.replace(' ', '') == f'Тотал двойных ошибок ({name_team_2})'.replace(' ', ''):
                        # print()
                        # print(name_podblock)
                        double_errors[f'Тотал двойных ошибок ({name_team_2})'] = ''
                        ths = podblock.find_all('th')
                        tds = podblock.find_all('td', class_='price height-column-with-price')
                        for i in range(len(ths)):
                            th = ths[i].text.strip().replace('\n', '')
                            td = tds[i].text.strip().replace('\n', '')
                            if th == 'Меньше' or th == 'Больше':
                                double_errors[f"{th}_20"] = td
                            # print(ths[i].text.strip().replace('\n', ''))
                            # print(tds[i].text.strip().replace('\n', ''))

            # Проверка блока ЭЙСЫ
            elif name_block == 'Эйсы':
                podblocki = block.find_all('div', class_='market-inline-block-table-wrapper')
                # запуск сбора информации по эйсам
                for podblock in podblocki:
                    name_podblock = podblock.find('div', class_='name-field').text.strip()
                    if name_podblock == 'Кто подаст больше эйсов':
                        aces['Кто подаст больше эйсов'] = ''
                        # print()
                        # print(name_podblock)
                        results_left = podblock.find_all('div', class_='result-left')
                        results_right = podblock.find_all('div', class_='result-right')
                        for i in range(len(results_left)):
                            if results_left[i].text.strip() == name_team_1 or results_left[i].text.strip() == 'Поровну' or results_left[i].text.strip() == name_team_2:
                                aces[f"{results_left[i].text.strip()}_9"] = results_right[i].text.strip()
                            # print(f'{results_left[i].text.strip()} - {results_right[i].text.strip()}')
                    elif name_podblock == 'Кто подаст больше эйсов с учетом форы':
                        aces['Кто подаст больше эйсов с учетом форы'] = ''
                        # print()
                        # print(name_podblock)
                        ths = podblock.find_all('th')
                        tds = podblock.find_all('td', class_='price height-column-with-price $this.getStyle()')
                        for i in range(len(ths)):
                            th = ths[i].text.strip().replace('\n', '')
                            td = tds[i].text.strip().replace('\n', '')
                            if th == name_team_1 or th == name_team_2:
                                aces[f"{th}_10"] = td
                            # print(ths[i].text.strip().replace('\n', ''))
                            # print(tds[i].text.strip().replace('\n', ''))
                    elif name_podblock == 'Тотал эйсов':
                        aces['Тотал эйсов'] = ''
                        # print()
                        # print(name_podblock)
                        ths = podblock.find_all('th')
                        tds = podblock.find_all('td', class_='price height-column-with-price')
                        for i in range(len(ths)):
                            th = ths[i].text.strip().replace('\n', '')
                            td = tds[i].text.strip().replace('\n', '')
                            if th == 'Меньше' or th == 'Больше':
                                aces[f"{th}_11"] = td
                            # print(ths[i].text.strip().replace('\n', ''))
                            # print(tds[i].text.strip().replace('\n', ''))
                    elif name_podblock.replace(' ', '') == f'Тотал эйсов ({name_team_1})'.replace(' ', ''):
                        # print()
                        # print(name_podblock)
                        aces[f'Тотал эйсов ({name_team_1})'] = ''
                        ths = podblock.find_all('th')
                        tds = podblock.find_all('td', class_='price height-column-with-price')
                        for i in range(len(ths)):
                            th = ths[i].text.strip().replace('\n', '')
                            td = tds[i].text.strip().replace('\n', '')
                            if th == 'Меньше' or th == 'Больше':
                                aces[f"{th}_17"] = td
                            # print(ths[i].text.strip().replace('\n', ''))
                            # print(tds[i].text.strip().replace('\n', ''))
                    elif name_podblock.replace(' ', '') == f'Тотал эйсов ({name_team_2})'.replace(' ', ''):
                        # print()
                        # print(name_podblock)
                        aces[f'Тотал эйсов ({name_team_2})'] = ''
                        ths = podblock.find_all('th')
                        tds = podblock.find_all('td', class_='price height-column-with-price')
                        for i in range(len(ths)):
                            th = ths[i].text.strip().replace('\n', '')
                            td = tds[i].text.strip().replace('\n', '')
                            if th == 'Меньше' or th == 'Больше':
                                aces[f"{th}_18"] = td
        #                     print(ths[i].text.strip().replace('\n', ''))
        #                     print(tds[i].text.strip().replace('\n', ''))

        # Создание списка со словарями, в которых находятся все данные
        ALL_DATA.append({
            'evev': even,
            'name_liga': name_liga,
            'name_team_1': name_team_1,
            'name_team_2': name_team_2,
            'date_game': date_game,
            'time_game': time_game,
            'win_team_1': win_team_1,
            'win_team_2': win_team_2,
            'fora_1': fora_1,
            'fora_2': fora_2,
            'total_1': total_1,
            'total_2': total_2,
            'stat': statistika,
            'double_errors': double_errors,
            'aces': aces
        })
    return ALL_DATA

# Основная фунция парсинга сайта, собирает все необходимые данные и отдает их в обработку
def Parser(all_liga):#all_liga
    ALL_DATA = []
    # Цикл обработки каждой лиги
    for href_liga in all_liga: # len(all_href_cat) + 1
        # Проверка того, что ссылка на лиги еще действительна
        if href_liga.strip('/') == requests.get(href_liga.strip('/')).url.strip('/'):
        # href_liga = all_href_cat[i]
            # Отправка запроса на сайт и получение кода страницы
            soup_liga = get_html(href_liga)
            # Вызов функции сбора ссылок на все матчи
            all_hrefs_in_game_one_liga = ALL_game_in_one_liga(soup_liga)
            # print(all_hrefs_in_game_one_liga)
            # Вызов функции сбора необходимых данных
            ALL_DATA.append(INFO_in_one_game(all_hrefs_in_game_one_liga))

    return ALL_DATA

# if __name__ == '__main__':
#     Parser()