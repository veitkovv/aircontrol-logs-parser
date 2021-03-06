import os
import re
import glob
import logging
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from functools import wraps

from datetime import datetime, timedelta
from time import time as get_current_time

from .models import Roll


def file_is_old(filename):
    return os.path.basename(filename).startswith('asrun')


def get_previous_day_filename(filename):
    """Берет предыдущую дату и возвращает имя файла в формате Cinegy"""
    date_minus_one_day = get_date_from_filename(filename) - timedelta(days=1)
    return f"activity_0_{date_minus_one_day.strftime('%d-%m-%Y')}.txt"


def get_date_from_filename(filename):
    """Ищет в имени файла дату и возвращает объект date"""
    re_pattern = "([0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9])"
    return datetime.strptime(re.search(re_pattern, filename).group(0), '%d-%m-%Y').date()


def crop_numbers(fn):
    """Полный С полем общий пн 22.45 16+ 10:00:00:00.1 => Полный С полем общий пн 22.45 16+"""

    @wraps(fn)
    def wrapped(*args, **kwargs):
        return re.sub(r'\d\d:\d\d:\d\d:\d.+', '', fn(*args, **kwargs))

    return wrapped


def crop_prefix(fn):
    """Полный С полем общий пн 22.45 16+ => С полем общий пн 22.45 16+"""

    @wraps(fn)
    def wrapped(*args, **kwargs):
        return re.sub(r'(^Полный )', '', fn(*args, **kwargs))

    return wrapped


@crop_prefix
@crop_numbers
def format_roll_name(roll_name):
    return roll_name.strip()


def process_log_file(filename: str):
    """
    Для нового формата
    "11/01/2016","08:31:15.385","VIDEO","START","{1B0855B9-17D6-4585-887E-46968ED006F8}","Утро 01.11.2016 ГОТОВО","","","","10:01:13:02","29.335",""
    Функция открывает на чтение файл, и считывает построчно, формируя словарь со значениями
    :return: генератор словарей
    """
    logging.debug(f'processing new file {filename}')
    with open(filename, 'r', encoding="utf-16") as f:
        for line in f.readlines():
            line_dict = {  # Стандартизированный словарь, который функция заполняет значениями из строк
                "datetime": "",
                "category": "",
                "is_start": "",
                "uuid": "",
                "name": "",
                "description": "",
            }

            log_entry = line.split('","')

            date = log_entry[0].strip('"')
            time = log_entry[1]
            line_dict["datetime"] = datetime.strptime(date + time, '%m/%d/%Y%H:%M:%S.%f')

            category = log_entry[2]
            line_dict["category"] = category
            if category == "ENGINE":
                # категория engine не имеет других параметров, кроме START - END
                logging.debug(f'ENGINE MESSAGE DETECTED: {line}')
                yield line_dict
            else:
                line_dict["is_start"] = log_entry[3] == "START"
                line_dict["uuid"] = log_entry[4].strip('{}')
                line_dict["name"] = format_roll_name(log_entry[5])
                line_dict["description"] = log_entry[6].strip()
                yield line_dict


def scan_logs(source_path: str) -> list:
    """
    Функция получает список файлов *.txt по входному пути, и многопоточно вызывает функцию process_new_file,
     которая обрабатывает содержимое файлов
    :param source_path: Путь где лежат логи
    :return: список со всеми строками всех файлов в виде словарей
    """
    filenames = glob.glob(source_path + f'/*.txt')
    filenames.sort(key=os.path.getmtime)  # имена файлов по возрастанию даты создания

    all_events = []

    with PoolExecutor(max_workers=4) as executor:
        t0 = get_current_time()
        logging.info(f'start scanning at {datetime.now()}')
        for result in executor.map(process_log_file, [f for f in filenames if not file_is_old(f)]):
            all_events.extend(result)
    all_events.sort(key=lambda x: x["datetime"])  # сортировка всего списка по дате, ролики идут подряд
    logging.info(f'all files scanned and sorted. Total lines: {len(all_events)}, total time: {get_current_time() - t0}')
    return all_events


def start_roll_fabric(event_list: list) -> None:
    """
    функция-фабрика объектов Roll, создает объекты и вностит в базу данных
    :param event_list: список словарей из лога
    :return:
    """
    parsed_rolls = []
    buff = []
    for roll in event_list:
        if roll["is_start"]:
            r = Roll()
            r.start = roll["datetime"]
            r.category = roll["category"]
            r.uuid = roll["uuid"]
            r.name = roll["name"]
            r.description = roll["description"]
            buff.append(r)
        else:
            for item in buff:
                if item.uuid == roll["uuid"] and not item.end:
                    pos = buff.index(item)
                    finish_roll = buff.pop(pos)
                    finish_roll.end = roll["datetime"]
                    parsed_rolls.append(finish_roll)
    parsed_rolls.extend(buff)  # Добавляем роллы, которые по какой-то причине без времени окончания
    Roll.objects.bulk_create(parsed_rolls, ignore_conflicts=True)
    logging.info('Done with creating new rolls')
