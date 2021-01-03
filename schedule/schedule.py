"""
Классы и функции для работы с расписанием.
"""

import json

from schedule.helper import convert_to_rfc_datetime, default_time_zone


class Schedule:
    """
    Класс расписания для экспорта.
    """

    def __init__(self, filename: str):
        self._pairs: list = []

        with open(filename, 'r', encoding='utf-8') as file:
            pairs = json.load(file)
            for pair in pairs:
                self._pairs.append(Pair(pair))

    def events(self) -> dict:
        """
        Возвращает все события расписания для Google Calendar.
        """
        for pair in self._pairs:
            for event in pair.events():
                yield event


class Pair:
    """
    Класс пары в расписании.
    """

    def __init__(self, pair: dict):
        self.title: str = pair['title']
        self.lecturer: str = pair['lecturer']
        self.type: str = pair['type']
        self.subgroup: str = pair['subgroup']
        self.classroom: str = pair['classroom']

        self.time_start: str = pair['time']['start']
        self.time_end: str = pair['time']['end']

        self.dates = []
        for date in pair['dates']:
            self.dates.append(Date(date))

    def events(self) -> dict:
        """
        Возвращает все события пары для Google Calendar.
        """
        for date in self.dates:
            event = {
                'summary': self.title,
                'location': self.classroom,
                'start': {
                    'dateTime': convert_to_rfc_datetime(date.start_date(), self.time_start),
                    'timeZone': default_time_zone()
                },
                'end': {
                    'dateTime': convert_to_rfc_datetime(date.start_date(), self.time_end),
                    'timeZone': default_time_zone()
                },
                'recurrence': date.recurrence()
            }
            yield event


class Date:
    """
    Класс даты  в расписании.
    """

    def __init__(self, date: dict):
        self.date: str = date['date']
        self.frequency: str = date['frequency']

    def start_date(self):
        """
        Возвращает дату начала события.
        """
        if self.frequency == 'once':
            return self.date
        else:
            return self.date.split('-')[0]

    def recurrence(self):
        """
        Возвращает переодичность события для календаря.
        """
        pass
