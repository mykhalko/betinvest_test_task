from __future__ import annotations
from typing import Dict, List, Union

from .schemas import EventInputSchema, SectionInputSchema


class ResultsBoard:
    """
    Class for keeping parsed results
    Should be created via class methods <input_from_web> / <input_from_db>

    Class attributes for navigation in data dicts

    for raw web json:
        ORIGIN_EVENT_KEY - events block key in
        ORIGIN_SECTIONS_KEY - sections block key

    for processed data:
        SECTION_EVENTS_KEY - events block key for each section
        SECTION_ID_KEY - section id key
        EVENT_NAME_KEY - event name key
        EVENT_ID_KEY - event id key
    """
    # for raw json
    ORIGIN_EVENTS_KEY = "events"
    ORIGIN_SECTIONS_KEY = "sections"

    # for processed json
    SECTION_EVENTS_KEY = "events"
    SECTION_ID_KEY = "id"
    EVENT_NAME_KEY = "name"
    EVENT_ID_KEY = "id"

    def __init__(self, data: Union[Dict, List], raw: bool = True):
        if raw:
            data = self.parse(data)
        self._data = data

    @classmethod
    def init_from_web(cls, data: Dict) -> ResultsBoard:
        """
        Use this constructor method for initiating ResultsBoard from raw web json

        :param data: raw data
        :return: class instance
        """
        return cls(data=data, raw=True)

    @classmethod
    def init_from_db(cls, data: List) -> ResultsBoard:
        """
        Use this constructor method for initiating ResultsBoard from db data

        :param data: db data
        :return: class instance
        """
        return cls(data=data, raw=False)

    @classmethod
    def parse(cls, data: Dict) -> List[Dict]:
        """
        Transform data from raw web json to application data

        :param data: raw web json
        :return: application data
        """
        sections = SectionInputSchema().load(data[cls.ORIGIN_SECTIONS_KEY], many=True)
        events = EventInputSchema().load(data[cls.ORIGIN_EVENTS_KEY], many=True)
        for section in sections:
            section_events_ids = section[cls.SECTION_EVENTS_KEY]
            section[cls.SECTION_EVENTS_KEY] = [events[event_id - 1] for event_id in section_events_ids]
        return sections

    @property
    def sections(self) -> List[Dict]:
        """
        Get results sections
        :return:
        """
        return self._data

    @property
    def events(self) -> List[Dict]:
        """
        Get all events
        :return:
        """
        return [section[self.SECTION_EVENTS_KEY] for section in self.sections]

    def filter(self, search: str = "") -> List[Dict]:
        """
        Filter events by name
        Filter is case insensitive, filter for values that starts with search expression
        If no events in section, section won't be included in results

        :param search: search expression
        :return: filtered section
        """
        # Lets make case insensitive
        search = search.lower()
        filtered_sections = []
        for section in self.sections:
            events = section[self.SECTION_EVENTS_KEY]
            filtered_events = [
                event for event in events
                if event[self.EVENT_NAME_KEY].lower().startswith(search)
            ]
            # include section only if it contains events that satisfies filter expr
            if filtered_events:
                filtered_sections.append({**section, self.SECTION_EVENTS_KEY: filtered_events})
        return filtered_sections

    def sort(self) -> None:
        """
        Sort data to origin representation
        :return:
        """
        self._data.sort(key=lambda item: item[self.SECTION_ID_KEY])
        for section in self._data:
            section[self.SECTION_EVENTS_KEY].sort(key=lambda item: item[self.EVENT_ID_KEY])
