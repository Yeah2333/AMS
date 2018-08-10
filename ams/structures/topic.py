#!/usr/bin/env python
# coding: utf-8

from ams import get_namedtuple_from_dict


TOPIC = get_namedtuple_from_dict("CONST", {
    "DOMAIN": "ams",
    "DELIMITER": "/",
    "ANY": "*",
    "DOMAIN_INDEX": 1,
    "FROM_GROUP_INDEX": 2,
    "FROM_ID_INDEX": 3,
    "TO_GROUP_INDEX": 4,
    "TO_ID_INDEX": 5,
    "CATEGORIES_HEAD_INDEX": 6,
    "REQUEST_CATEGORIES_HEAD": "request",
    "RESPONSE_CATEGORIES_HEAD": "response"
})
