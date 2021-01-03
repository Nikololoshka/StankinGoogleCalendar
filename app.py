"""
Главный файл приложения для добавления расписаний в Google Calendar.

Google Calendar API docs:
https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/index.html
https://developers.google.com/calendar/v3/reference
"""

from config import CLIENT_SECRET, API_NAME, API_VERSION, SCOPES
from loader import create_service
from schedule.helper import *
from schedule.handler import *

if __name__ == '__main__':
    service = create_service(CLIENT_SECRET, API_NAME, API_VERSION, SCOPES)

    # r = get_all_calendars(service)
    # pretty_print(r)

    ids = '42d8qc3alsq0tb484rv5nhuilk@group.calendar.google.com'
    r = get_all_events(service, ids)
    pretty_print(r)

    for e in r:
        remove_event(service, ids, e['id'])

    r = get_all_events(service, ids)
    pretty_print(r)

    schedule = Schedule('test-data/ИДБ-17-09.json')
    for i, event in enumerate(schedule.events()):
        r = create_event(service, ids, event)
        print(i)
        # time.sleep(0.1)

    # delete calendar
    # response = service.calendars().delete(calendarId='thj9c06um55bmr51qat71dvabc@group.calendar.google.com').execute()
    # print(response)

    # request_body = {
    #     'summary': 'Тестовое расписание',
    #     'description': 'Расписание МГТУ "СТАНКИН" Весна-2021',
    #     'timeZone': 'Europe/Moscow'
    # }

    # insert calendar
    # response = service.calendars().insert(body=request_body).execute()
    # pretty_print(response)

    # for calendar in get_all_calendars(service):
    #    if 'Весна-2021' in calendar.get('description', ''):
    #        pretty_print(calendar)

    # export_to_google_calendar_dir(service, './test-data')
