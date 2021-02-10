"""
Файл с функциями для работы с расписаниями в Google Calendar.
"""

import os
import time

from tqdm import tqdm
from .helper import get_all_calendars, find_calendar, create_calendar, create_event, give_public_access
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

    current_calendars = get_all_calendars(service)

    for i, file in enumerate(files):
        name = os.path.basename(file)[:-5]
        export_to_google_calendar_file(service, file, name, current_calendars)


def export_to_google_calendar_file(service, file: str, name: str, current_calendars: list):
    """
    Экспортирует расписание в Google Calendar
    """
    calendar = find_calendar(current_calendars, name)
    exist = calendar is not None

    progress_tqdm = tqdm(total=100, position=0, desc=f'Экспорт расписания {name}')

    if not exist:
        schedule = Schedule(file)
        calendar = create_calendar(service, name)
        for i, event in enumerate(schedule.events()):
            create_event(service, calendar['id'], event)
            progress_tqdm.update(i)

        give_public_access(service, calendar['id'])

    progress_tqdm.update(progress_tqdm.total)
