"""
Главный файл приложения для управления расписаниями в Google Calendar.

Google Calendar API docs:
https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/index.html
https://developers.google.com/calendar/v3/reference
"""
from commands import export_command, create_parser

if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()

    cmd = namespace.command
    if cmd == 'export':
        export_command(namespace)

    # service = create_service(CLIENT_SECRET, API_NAME, API_VERSION, SCOPES)
    #
    # # r = get_all_calendars(service)
    # # pretty_print(r)
    #
    # ids = '42d8qc3alsq0tb484rv5nhuilk@group.calendar.google.com'
    # r = get_all_events(service, ids)
    # pretty_print(r)
    #
    # for e in r:
    #     remove_event(service, ids, e['id'])
    #
    # r = get_all_events(service, ids)
    # pretty_print(r)
    #
    # schedule = Schedule('test-data/ИДБ-17-09.json')
    # for i, event in enumerate(schedule.events()):
    #     r = create_event(service, ids, event)
    #     print(i)
    #     # time.sleep(0.1)
