from datetime import datetime
from typing import Any

from marshmallow import fields, Schema


class EventInputSchema(Schema):
    """
    Input schema for data received from web
    """
    id = fields.Integer(data_key="id")
    comment1 = fields.Str(data_key="comment1")
    comment2 = fields.Str(data_key="comment2")
    comment3 = fields.Str(data_key="comment3")
    goal_order = fields.Str(data_key="goalOrder")
    name = fields.Str(data_key="name")
    score = fields.Str(data_key="score")
    start_time = fields.Integer(data_key="startTime")
    status = fields.Integer(data_key="status")


class SectionInputSchema(Schema):
    """
    Input schema for data received from web
    """
    id = fields.Integer(data_key="id")
    events = fields.List(fields.Integer(), data_key="events")
    fonbet_sport_id = fields.Integer(data_key="fonbetSportId")
    name = fields.Str(data_key="name")
    sport = fields.Str(data_key="sport")


class EventDatetime(fields.Integer):
    """
    Custom field to translate datetime from seconds to human-readable string value
    """
    FORMAT = "%m/%d, %H:%M"

    def _serialize(self, value: Any, attr: str, obj: Any, **kwargs) -> str:
        value = super()._serialize(value, attr, obj, **kwargs)
        return datetime.fromtimestamp(value).strftime(self.FORMAT)


class EventStatus(fields.Integer):
    """
    Custom field for translating numeric status value to human-readable string status value
    """
    DEFAULT = "Неизвестно"
    MAPPING = {
        2: "LIVE",
        3: "ЗАВЕРШЕН",
        4: "ОТМЕНЕН",
    }

    def _serialize(self, value: Any, attr: str, obj: Any, **kwargs) -> str:
        value = super()._serialize(value, attr, obj, **kwargs)
        return self.MAPPING.get(value, self.DEFAULT)


class EventOutputSchema(Schema):
    """
    Schema for preparing values from db to template data
    """
    id = fields.Integer()
    comment1 = fields.Str()
    comment2 = fields.Str()
    comment3 = fields.Str()
    goal_order = fields.Str()
    name = fields.Str()
    score = fields.Str()
    start_time = EventDatetime()
    status = EventStatus()


class SectionOutputSchema(Schema):
    """
    Schema for preparing values from db to template data
    """
    events = fields.List(fields.Nested(EventOutputSchema))
    name = fields.Str()
    sport = fields.Str()
