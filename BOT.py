import asyncio
import json
import parser_bk
from keyboard import kb_client
import settings
from aiogram import Bot, Dispatcher, executor, types
from create_message import FORMAT

# инициализация бота
bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot)

# Идексация того, что бот начал работу
async def on_startup(_):
    print('Бот вышел в сеть')

# Команда запуска бота
@dp.message_handler(commands=['start', 'help'])
async def START(message: types.Message):
    # Сбор всех id пользователей, которые активировали бота
    with open('users.txt', 'r') as f:
        users = ''.join(f.readlines()).strip().split('\n')
    # Проверка, если пользователя нет в списке активировавших, то записываем его туда
    if not (str(message.from_user.id) in users):
        with open('users.txt', 'a') as f:
            f.write(f'{message.from_user.id}\n')

    await message.answer('Здравствуйте, чтобы получить список лиг, введите /liga или нажмите на кнопку', reply_markup= kb_client)

# Команда сбора и записи всех доступных лиг на попент активации данной команды
@dp.message_handler(commands=['liga'])
async def all_liga(message: types.Message):
    # Сбор всех лиг (названий и ссылок) и запись их в файл .json
    all_name_cat, all_href_cat = parser_bk.alls(parser_bk.URL_categorii)
    json_all_liga = {}
    for i in range(1,len(all_name_cat) + 1):
        json_all_liga[f'{i}'] = all_href_cat[i]
        # Отправка сообщения со всеми лигами с нумерацией
        await message.answer(f"{i} - {all_name_cat[i]}")

    with open("json_all_liga.json", "w") as file:
        json.dump(json_all_liga, file, indent=4, ensure_ascii=False)

    await message.answer(f"Чтобы начать мониторинг лиг введите /main_liga или нажмите на кнопку")

# Команда подсказки, как начать следить за лигами
@dp.message_handler(commands=['main_liga'])
async def main_liga(message: types.Message):
    await message.answer('Чтобы ввести новый список лиг или обновить старый введите NewLiga_ и далее номера лиг через запятую'
                         '\n(Пример NewLiga_2,3,5,13,19):')

# Функция мониторинга за всеми сообщениями, если попадается сообщение в котором имеется "NewLiga", то начинает выполняться алгоритм
@dp.message_handler()
async def main_liga(message: types.Message):
    if message.text.split('_')[0] == 'NewLiga':
        # Открываем, создаем и считываем необходимимые для работы бота бота файлы
        with open('DATA.json', 'w') as file:
            json.dump('', file, indent=4, ensure_ascii=False)

        with open("json_all_liga.json", "r") as file:
            json_all_liga = json.load(file)

        # Запись выбранных пользователем лиг, по номерам
        with open('main_liga.txt', 'w') as file:
            all_liga = message.text.split('_')[1].replace(' ', '').strip(',').split(',')
            for liga in all_liga:
                file.write(f'{json_all_liga[liga]}\n')
    # Запускаем бесконечный цикл работы бота
    while True:
        try:
            # Открываем список пользователей, которые активировали бота
            with open('users.txt', 'r') as f:
                users = ''.join(f.readlines()).strip().split('\n')

            print('RUN')
            ALL_INFO = []
            # Считывание лиг, которые необходимо собрать
            with open('main_liga.txt', 'r') as file:
                HREF_MAIN_LIGA = ''.join(file.readlines()).strip().split('\n')

            # Проврка того, что лиги были собраны
            if len(HREF_MAIN_LIGA) != 0:
                # print(len(HREF_MAIN_LIGA))
                # Заппуск парсера сайта и сбор всей необходмой информации
                ALL_DATA = parser_bk.Parser(HREF_MAIN_LIGA)

                print('read')
                # Чтение файла со всеми матчами последнего сбора бота
                with open('DATA.json', 'r') as file:
                    contr = json.load(file)

                print('for')
                # Запуск цикла обработки информации полученной из парсера
                for DATA in ALL_DATA:
                    for data in DATA:
                        # смотрим иметются данные которое были собраны до данного прохода цикла, есди да, то начиаем сравнение
                        if contr != '':
                            kk = 0
                            kontr = 0
                            # Цикл сравнения старого сбора матчей с текущим
                            for one_game in contr:
                                # проверка по id матчей, если id совпадают, то продолжаем
                                if one_game['evev'] == data['evev']:

                                    kontr += 1
                                    # print('111111')
                                    # смотрим, были ли изменения в данных матча, если были, продолжаем
                                    if len(one_game['stat']) != len(data['stat']) or len(one_game['aces']) != len(data['aces']) or len(one_game['double_errors']) != len(data['double_errors']):
                                        contr[kk] = data
                                        # т.к. были изменения, то по информации текущего сбора запускаем функцию сбора сообщения
                                        MS = FORMAT(data)
                                        # отпраавка собранного сообщения отправляем всем польхователям активировавшим бота
                                        for user in users:
                                            await bot.send_message(chat_id=user, text=MS)
                                        print('1')
                                        print(data)
                                        # ALL_INFO.append(data)
                                kk += 1
                            # Проверка на новизну сообщения, если матч нового сбора не совпал не с
                            # одним матчем из страого, то выполняем этот сценарий
                            if kontr == 0:
                                # по информации текущего сбора запускаем функцию сбора сообщения
                                MS = FORMAT(data)
                                print('2')
                                # отпраавка собранного сообщения отправляем всем польхователям активировавшим бота
                                for user in users:
                                    await bot.send_message(chat_id=user, text=MS)
                        # Если файл DATA.json был пуст, занчит бора не было и отправляем все игры, что были собраны
                        else:
                            MS = FORMAT(data)
                            # отпраавка собранного сообщения отправляем всем польхователям активировавшим бота
                            for user in users:
                                await bot.send_message(chat_id=user, text=MS)
                                # await message.answer(MS)
                            print('3')
                            print(data)
                        # await message.answer(MS)
                        # Формирование списка из всех матчей текущего сбора
                        ALL_INFO.append(data)

                print('write')
                # Обновление информации в DATA.json
                with open('DATA.json', 'w') as file:
                    json.dump(ALL_INFO, file, indent=4, ensure_ascii=False) #``````
            # Цикл засыпает на 5 сек.
            print('sleep')
            await asyncio.sleep(5)
            print()
        # Если произошла какя то ошибка, то цикл засыпает на 30 сек и начинается снова
        except:
            print('ERROR')
            await asyncio.sleep(30)

# Запуска бота
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

