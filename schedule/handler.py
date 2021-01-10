"""
Файл с функциями для работы с расписаниями в Google Calendar.
"""

import os
import time

from tqdm import tqdm
from .helper import get_all_calendars, find_calendar, create_calendar, create_event
from .schedule import Schedule


def export_to_google_calendar_dir(service, files_dir: str):
    """
    Экспортирует папку с файлами расписаний в Google Calendar.
    """
    files = []
    for dirpath, _, filenames in os.walk(files_dir):
        for filename in filenames:
            if filename.endswith('.json'):
                files.append(os.path.join(dirpath, filename))

    export_to_google_calendar_files(service, files)


def export_to_google_calendar_files(service, files: list):
    """
    Экспортирует список расписаний в Google Calendar.
    """

    progress_tqdm = tqdm(total=len(files), position=0)
    current_calendars = get_all_calendars(service)

    for i, file in enumerate(files):
        name = os.path.basename(file)[:-5]
        progress_tqdm.set_description(f'Экспорт расписания {name}')
        progress_tqdm.update(i)

        export_to_google_calendar_file(service, file, name, current_calendars)

    progress_tqdm.update(progress_tqdm.total)


def export_to_google_calendar_file(service, file: str, name: str, current_calendars: list):
    """
    Экспортирует расписание в Google Calendar
    """
    calendar = find_calendar(current_calendars, name)
    exist = calendar is not None

    schedule = Schedule(file)

    if not exist:
        calendar = create_calendar(service, name)
        for event in schedule.events():
            create_event(service, calendar['id'], event)
