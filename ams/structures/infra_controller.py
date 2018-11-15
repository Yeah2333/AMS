#!/usr/bin/env python
# coding: utf-8

from ams import get_namedtuple_from_dict, get_structure_superclass
from ams.structures.event_loop import const as event_loop_const
from ams.structures import Target, Targets, Cycle, Schedules, MessageHeader, EventLoop


topic = {
    "CATEGORIES": {}
}
topic["CATEGORIES"].update(event_loop_const["TOPIC"]["CATEGORIES"])
topic["CATEGORIES"].update({
    "CONFIG": ["config"],
    "STATUS": ["status"],
    "CYCLE": ["cycle"],
    "SCHEDULES": ["schedules"]
})

const = {}
const.update(event_loop_const)
const.update({
    "NODE_NAME": "infra_controller",
    "ROLE_NAME": "infra_controller",
    "TOPIC": topic
})

CONST = get_namedtuple_from_dict("CONST", const)


config_template = EventLoop.Config.get_template()
config_template.update({
    "targets": Targets.get_template()
})

config_schema = EventLoop.Config.get_schema()
config_schema.update({
    "targets": Targets.get_schema()
})


class Config(get_structure_superclass(config_template, config_schema)):
    Targets = Targets


status_template = EventLoop.Status.get_template()

status_schema = EventLoop.Status.get_schema()


class Status(get_structure_superclass(status_template, status_schema)):
    pass


config_message_template = {
    "header": MessageHeader.get_template(),
    "body": Config.get_template()
}

config_message_schema = {
    "header": {
        "type": "dict",
        "schema": MessageHeader.get_schema(),
        "required": True,
        "nullable": False
    },
    "body": {
        "type": "dict",
        "schema": Config.get_schema(),
        "required": True,
        "nullable": False
    }
}


class ConfigMessage(get_structure_superclass(config_message_template, config_message_schema)):
    pass


status_message_template = {
    "header": MessageHeader.get_template(),
    "body": Status.get_template()
}

status_message_schema = {
    "header": {
        "type": "dict",
        "schema": MessageHeader.get_schema(),
        "required": True,
        "nullable": False
    },
    "body": {
        "type": "dict",
        "schema": Status.get_schema(),
        "required": True,
        "nullable": False
    }
}


class StatusMessage(get_structure_superclass(status_message_template, status_message_schema)):
    pass


cycle_message_template = {
    "header": MessageHeader.get_template(),
    "body": {
        "target": Target.get_template(),
        "schedules": Cycle.get_template()
    }
}

cycle_message_schema = {
    "header": {
        "type": "dict",
        "schema": MessageHeader.get_schema(),
        "required": True,
        "nullable": False
    },
    "body": {
        "type": "dict",
        "schema": {
            "target": {
                "type": "dict",
                "schema": Target.get_schema(),
                "required": True,
                "nullable": False
            },
            "cycle": {
                "type": "dict",
                "schema": Cycle.get_schema(),
                "required": True,
                "nullable": False
            }
        },
        "required": True,
        "nullable": False
    }
}


class CycleMessage(
        get_structure_superclass(cycle_message_template, cycle_message_schema)):
    pass


schedules_message_template = {
    "header": MessageHeader.get_template(),
    "body": {
        "target": Target.get_template(),
        "schedules": Schedules.get_template()
    }
}

schedules_message_schema = {
    "header": {
        "type": "dict",
        "schema": MessageHeader.get_schema(),
        "required": True,
        "nullable": False
    },
    "body": {
        "type": "dict",
        "schema": {
            "target": {
                "type": "dict",
                "schema": Target.get_schema(),
                "required": True,
                "nullable": False
            },
            "schedules": Schedules.get_schema()
        },
        "required": True,
        "nullable": False
    }
}


class SchedulesMessage(
        get_structure_superclass(schedules_message_template, schedules_message_schema)):
    pass


class Message(EventLoop.Message):
    Config = ConfigMessage
    Status = StatusMessage
    Cycle = CycleMessage
    Schedules = SchedulesMessage


class InfraController(EventLoop):
    CONST = CONST
    Config = Config
    Status = Status
    Message = Message
