# функия формирования сообщения, принимает словарь данных о игре и отдает свормированное сообщение в виде строки
def FORMAT(data):
    MS = f"{data['name_team_1']} - {data['name_team_2']}\n" \
         f"{data['name_liga']}\n" \
         f"{data['time_game']}\n\n"
    try:
        MS += f"П1 {round(float(data['win_team_1']), 2)} П2 {round(float(data['win_team_2']), 2)}\n"
    except:
        MS += f"П1 {data['win_team_1']} П2 {data['win_team_2']}\n"
    try:
        MS += f"Ф1 {data['fora_1'].split(' ')[0].replace('()', '')} @ {round(float(data['fora_1'].split(' ')[1]), 2)}\n"
    except:
        MS += f"Ф1 {data['fora_1'].split(' ')[0].replace('()', '')} @ {data['fora_1'].split(' ')[1]}\n"
    try:
        MS += f"Ф1 {data['fora_2'].split(' ')[0].replace('()', '')} @ {round(float(data['fora_2'].split(' ')[1]), 2)}\n"
    except:
        MS += f"Ф2 {data['fora_2'].split(' ')[0].replace('()', '')} @ {data['fora_2'].split(' ')[1]}\n"
    try:
        MS += f"ТОТ {data['total_1'].split(' ')[0].replace('()', '')} Over {round(float(data['total_2'].split(' ')[1]), 2)} Under {round(float(data['total_1'].split(' ')[1]), 2)}"
    except:
        MS += f"ТОТ {data['total_1'].split(' ')[0].replace('()', '')} Over {data['total_2'].split(' ')[1]} Under {data['total_1'].split(' ')[1]}"

    # Проверка на вкладку СТАТИСТИКА
    if data['stat'] != {}:
        for key, val in data['stat'].items():
            if key == f"{data['name_team_1']}_1":
                MS += '\n\nБрейкпойнты\n\n'

                MS += f"{data['name_team_1']} - {data['name_team_2']}\n" \
                      f"{data['name_liga']}\n" \
                      f"{data['time_game']}"

                MS += f'\n\nП1 {round(float(val), 2)}'
            elif key == f"Поровну_1":
                MS += f' X {round(float(val), 2)}'
            elif key == f"{data['name_team_2']}_1":
                MS += f' П2 {round(float(val), 2)}'
            elif key == f"{data['name_team_1']}_2":
                MS += f'\nФ1 {val.split(" ")[0].replace("()", "")} @ {round(float(val.split(" ")[1]), 2)}'
            elif key == f"{data['name_team_2']}_2":
                MS += f'\nФ2 {val.split(" ")[0].replace("()", "")} @ {round(float(val.split(" ")[1]), 2)}'
            elif key == 'Меньше_12':
                MS += f'\nТОТ {val.split(" ")[0].replace("()", "")} Over {round(float(data["stat"]["Больше_12"].split(" ")[1]), 2)} Under {round(float(val.split(" ")[1]), 2)}'
            elif key == "Меньше_13":
                MS += f'\nИТ1 {val.split(" ")[0].replace("()", "")} Over {round(float(data["stat"]["Больше_13"].split(" ")[1]), 2)} Under {round(float(val.split(" ")[1]), 2)}'
            elif key == "Меньше_14":
                MS += f'\nИТ2 {val.split(" ")[0].replace("()", "")} Over {round(float(data["stat"]["Больше_14"].split(" ")[1]), 2)} Under {round(float(val.split(" ")[1]), 2)}'

            elif key == 'Кто совершит больше брейков':
                MS += '\n\nБрейки\n\n'

                MS += f"{data['name_team_1']} - {data['name_team_2']}\n" \
                      f"{data['name_liga']}\n" \
                      f"{data['time_game']}"
            elif key == f"{data['name_team_1']}_3":
                MS += f'\n\nП1 {round(float(val), 2)}'
            elif key == f"Поровну_3":
                MS += f' X {round(float(val), 2)}'
            elif key == f"{data['name_team_2']}_3":
                MS += f' П2 {round(float(val), 2)}'
            elif key == f"{data['name_team_1']}_4":
                MS += f'\nФ1 {val.split(" ")[0].replace("()", "")} @ {round(float(val.split(" ")[1]), 2)}'
            elif key == f"{data['name_team_2']}_4":
                MS += f'\nФ2 {val.split(" ")[0].replace("()", "")} @ {round(float(val.split(" ")[1]), 2)}'
            elif key == 'Меньше_5':
                MS += f'\nТОТ {val.split(" ")[0].replace("()", "")} Over {round(float(data["stat"]["Больше_5"].split(" ")[1]), 2)} Under {round(float(val.split(" ")[1]), 2)}'
            elif key == "Меньше_15":
                MS += f'\nИТ1 {val.split(" ")[0].replace("()", "")} Over {round(float(data["stat"]["Больше_15"].split(" ")[1]), 2)} Under {round(float(val.split(" ")[1]), 2)}'
            elif key == "Меньше_16":
                MS += f'\nИТ2 {val.split(" ")[0].replace("()", "")} Over {round(float(data["stat"]["Больше_16"].split(" ")[1]), 2)} Under {round(float(val.split(" ")[1]), 2)}'


    # ПРОВЕРКА НА ВКЛАДУ ЭЙСЫ
    if data['aces'] != {}:
        MS += '\n\nЭйсы\n\n'

        MS += f"{data['name_team_1']} - {data['name_team_2']}\n" \
              f"{data['name_liga']}\n" \
              f"{data['time_game']}\n\n"
        for key, val in data['aces'].items():
            if key == f"{data['name_team_1']}_9":
                MS += f'П1 {round(float(val), 2)}'
            elif key == f"Поровну_9":
                MS += f' X {round(float(val), 2)}'
            elif key == f"{data['name_team_2']}_9":
                MS += f' П2 {round(float(val), 2)}\n'
            elif key == f"{data['name_team_1']}_10":
                MS += f'Ф1 {val.split(" ")[0].replace("()", "")} @ {round(float(val.split(" ")[1]), 2)}\n'
            elif key == f"{data['name_team_2']}_10":
                MS += f'Ф2 {val.split(" ")[0].replace("()", "")} @ {round(float(val.split(" ")[1]), 2)}\n'
            elif key == 'Меньше_11':
                MS += f'ТОТ {val.split(" ")[0].replace("()", "")} Over {round(float(data["aces"]["Больше_11"].split(" ")[1]), 2)} Under {round(float(val.split(" ")[1]), 2)}\n'
            elif key == "Меньше_17":
                MS += f'ИТ1 {val.split(" ")[0].replace("()", "")} Over {round(float(data["aces"]["Больше_17"].split(" ")[1]), 2)} Under {round(float(val.split(" ")[1]), 2)}\n'
            elif key == "Меньше_18":
                MS += f'ИТ2 {val.split(" ")[0].replace("()", "")} Over {round(float(data["aces"]["Больше_18"].split(" ")[1]), 2)} Under {round(float(val.split(" ")[1]), 2)}'
    # ПРОВЕРКА НА ВКЛАДКУ ДВОЙНЫЕ ООШИБКИ
    if data['double_errors'] != {}:
        MS += '\n\nДвойные ошибки\n\n'

        MS += f"{data['name_team_1']} - {data['name_team_2']}\n" \
              f"{data['name_liga']}\n" \
              f"{data['time_game']}\n\n"
        for key, val in data['double_errors'].items():
            if key == f"{data['name_team_1']}_6":
                MS += f'П1 {round(float(val), 2)}'
            elif key == f"Поровну_6":
                MS += f' X {round(float(val), 2)}'
            elif key == f"{data['name_team_2']}_6":
                MS += f' П2 {round(float(val), 2)}\n'
            elif key == f"{data['name_team_1']}_7":
                MS += f'Ф1 {val.split(" ")[0].replace("()", "")} @ {round(float(val.split(" ")[1]), 2)}\n'
            elif key == f"{data['name_team_2']}_7":
                MS += f'Ф2 {val.split(" ")[0].replace("()", "")} @ {round(float(val.split(" ")[1]), 2)}\n'
            elif key == 'Меньше_8':
                MS += f'ТОТ {val.split(" ")[0].replace("()", "")} Over {round(float(data["double_errors"]["Больше_8"].split(" ")[1]), 2)} Under {round(float(val.split(" ")[1]), 2)}\n'
            elif key == "Меньше_19":
                MS += f'ИТ1 {val.split(" ")[0].replace("()", "")} Over {round(float(data["double_errors"]["Больше_19"].split(" ")[1]), 2)} Under {round(float(val.split(" ")[1]), 2)}\n'
            elif key == "Меньше_20":
                MS += f'ИТ2 {val.split(" ")[0].replace("()", "")} Over {round(float(data["double_errors"]["Больше_20"].split(" ")[1]), 2)} Under {round(float(val.split(" ")[1]), 2)}'
    return MS
