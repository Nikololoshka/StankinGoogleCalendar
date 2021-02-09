"""
Вспомогательный модуль для работы с Google Calendar API.
"""

from datetime import datetime
import json


def get_all_calendars(service):
    """
    Возвращает список всех текущих календарей.
    """
    page_token = None

    while True:
        response = service.calendarList().list(pageToken=page_token).execute()
        for calendar in response['items']:
            if 'МГТУ "СТАНКИН"' in calendar.get('description', ''):
                yield calendar

        page_token = response.get('nextPageToken')
        if not page_token:
            break


def create_calendar(service, name: str, description: str = None, time_zone: str = None):
    """
    Создает новый календарь с заданным именем.
    """
    request_body = {
        'summary': name,
        'description': auto_description() if description is None else description,
        'timeZone': default_time_zone() if time_zone is None else time_zone
    }
    return service.calendars().insert(body=request_body).execute()


def update_calendar(service, calendar_id: str, body: dict):
    """
    Обновляет данные о календаре
    """
    return service.calendars().update(calendarId=calendar_id, body=body).execute()


def remove_calendar(service, calendar_id: str):
    """
    Удаляетт календаль и все его события.
    """
    return service.calendars().delete(calendarId=calendar_id).execute()


def create_event(service, calendar_id: str, event: dict):
    """
    Создает новое событие в календаре.
    """
    return service.events().insert(calendarId=calendar_id, body=event).execute()


def remove_event(service, calendar_id: str, event_id: str):
    """
    Удаляет событие из календаря.
    """
    return service.events().delete(calendarId=calendar_id, eventId=event_id).execute()


def get_all_events(service, calendar_id: str):
    """
    Возвращает список всех событий календаря.
    """
    page_token = None

    while True:
        response = service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
        for event in response['items']:
            yield event

        page_token = response.get('nextPageToken')
        if not page_token:
            break


def find_calendar(calendars: list, name: str):
    """
    Возвращает необходимый календарь из списка. Если такого нет, то None.
    """
    for calendar in calendars:
        if name in calendar['summary']:
            return calendar

    return None


def auto_description():
    """
    Генерирует описание для Google календарей в формате 'Расписание МГТУ "СТАНКИН" на #Весна-2021'.
    """
    now = datetime.now().today()
    semester = 'Весна' if now.month < 6 else 'Осень'
    return f'Расписание МГТУ "СТАНКИН" на #{semester}-{now.year}'


def default_time_zone():
    """
    Возвращает временную зону по умолчанию
    """
    return 'Europe/Moscow'


# def convert_to_rfc_datetime(year=1900, month=1, day=1, hour=0, minute=0):
#     """
#     Конвертор даты в формат для Google Calendar API.
#     """
#     return datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'


def convert_to_rfc_datetime(date, time):
    """
    Конвертор даты в формат для Google Calendar API.
    """
    return datetime.strptime(f'{date} {time}', '%Y.%m.%d %H:%M').isoformat()


def convert_to_rfc_until_date(date: datetime):
    """
    Конвертор даты в формат для Google Calendar API.
    """
    return date.strftime('%Y%m%dT%H%M%S') + 'Z'


def pretty_print(obj):
    """
    Красивый вывод объекта в консоль.
    """
    print(json.dumps(obj, ensure_ascii=False, indent=4))
