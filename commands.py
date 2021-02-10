"""
Файл с обработчиком команд консоли.
"""
import argparse
import json

from config import CLIENT_SECRET, API_NAME, API_VERSION, SCOPES
from loader import create_service
from schedule.helper import *
from schedule.handler import *


def create_parser():
    """
    Создает парсер команд из консоли.
    """
    # главный парсер
    main_parser = argparse.ArgumentParser(
        prog='StankinGoogleCalender',
        description='Экспортер расписаний в Google Calendar',
        epilog='StankinGoogleCalender 0.1 beta (c) Январь 2021.'
               'Автор программы, как всегда, не несет никакой ответственности ни за что',
        add_help=False
    )
    main_parser_group = main_parser.add_argument_group(title='Параметры')
    main_parser_group.add_argument('-h', '--help', action='help', help='Справка по использованию')
    main_parser_group.add_argument('-v', '--version', action='version', help='Версия программы', version='0.1 beta')

    subparsers = main_parser.add_subparsers(
        dest='command',
        title='Возможные команды',
        description='Команды, которые должны быть в качестве первого параметра'
    )

    # эксорт расписаний
    export_parser = subparsers.add_parser('export', add_help=False)
    export_parser_group = export_parser.add_argument_group(title='Параметры')
    export_parser_group.add_argument('-h', '--help', action='help', help='Справка по использованию')
    export_parser_group.add_argument('-p', '--paths', help='Путь (-и) к расписаниям',
                                     required=True, nargs='+', metavar='ПУТЬ')
    export_parser_group.add_argument('-r', '--recursive', help='Рекурсивный поиск расписаний',
                                     action='store_true')

    # просмотр расписаний
    list_parser = subparsers.add_parser('ls', add_help=False)
    list_parser_group = list_parser.add_argument_group(title='Параметры')
    list_parser_group.add_argument('-h', '--help', action='help', help='Справка по использованию')
    list_parser_group.add_argument('-j', '--json', help='Экспортирует список расписаний в json')

    return main_parser


def export_command(namespace):
    """
    Экспорт расписаний в Google Calendar.
    """
    service = create_service(CLIENT_SECRET, API_NAME, API_VERSION, SCOPES)
    paths = []
    for path in namespace.paths:
        if os.path.isfile(path) and path.endswith('.json'):
            paths.append(path)
        elif namespace.recursive:
            for directory, _, filenames in os.walk(path):
                for filename in filenames:
                    if filename.endswith('.json'):
                        paths.append(os.path.join(directory, filename))
        else:
            for filename in os.listdir(path):
                if filename.endswith('.json'):
                    paths.append(os.path.join(path, filename))

    export_to_google_calendar_files(service, paths)


def list_command(namespace):
    """
    Выводит список всех расписаний в Google Calendar.
    """
    service = create_service(CLIENT_SECRET, API_NAME, API_VERSION, SCOPES)

    if namespace.json is not None:
        with open(namespace.json, 'w', encoding='utf-8') as output:
            schedules = []
            for schedule in get_all_calendars(service):
                schedules.append({
                    'name': schedule['summary'],
                    'link': create_shared_link(schedule['id'])
                })

            json.dump(schedules, output, ensure_ascii=False, indent=4)

    else:
        for schedule in get_all_calendars(service):
            print(f"Расписание: '{schedule['summary']}', id: '{schedule['id']}'")


def test():
    service = create_service(CLIENT_SECRET, API_NAME, API_VERSION, SCOPES)
    r = get_all_calendars(service)

    for s in r:
        pretty_print(s)
        ids = s['id']
        #pretty_print(acl_remove(service, ids, 'default'))

        #rr = create_acl(service, s['id'])
        #pretty_print(rr)

        #
        # calendar_list_entry = {
        #     'id': ids
        # }
        # cr = service.calendarList().insert(body=calendar_list_entry).execute()
        # print(cr)

        # acls = acl_list(service, ids)['items']
        # pretty_print(acls)
        #
        # print(f'https://calendar.google.com/calendar/embed?src={ids}')

