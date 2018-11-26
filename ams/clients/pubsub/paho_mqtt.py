#!/usr/bin/env python
# coding: utf-8

from copy import copy
from pprint import pformat
import json
from multiprocessing import Manager
from _ssl import PROTOCOL_TLSv1_2
from time import sleep

from paho.mqtt.client import Client

from ams import AttrDict, logger
from ams.helpers import Topic
from ams.structures import CLIENT


class ArgsSetters(object):

    CONST = CLIENT.PUBSUB.BASE_CLIENTS.PAHO_MQTT

    def __init__(self):
        self.args = AttrDict()

    def set_args_of_Client(
            self, client_id="", clean_session=True, userdata=None,
            protocol=CONST.DEFAULT_PROTOCOL, transport="tcp"):
        self.args.client = copy(locals())
        self.args.client.pop("self")

    def set_args_of_tls_set(
            self, ca_certs=None, certfile=None, keyfile=None, cert_reqs=None, tls_version=PROTOCOL_TLSv1_2,
            ciphers=None):
        self.args.tls_set = copy(locals())
        self.args.tls_set.pop("self")

    def set_args_of_tls_insecure_set(self, value):
        self.args.tls_insecure_set = copy(locals())
        self.args.tls_insecure_set.pop("self")

    def set_args_of_will_set(self, topic, payload=None, qos=0, retain=False):
        self.args.will_set = copy(locals())
        self.args.will_set.pop("self")

    def set_args_of_connect(self, host, port=1883, keepalive=60, bind_address=""):
        self.args.connect = copy(locals())
        self.args.connect.pop("self")

    def set_args_of_username_pw_set(self, username, password=None):
        self.args.username_pw_set = copy(locals())
        self.args.username_pw_set.pop("self")


def set_on_message_and_connect(client, args, subscribers, subscribers_lock):
    def on_message(_client, _userdata, message_data):
        subscribers_lock.acquire()
        for topic, subscriber in subscribers.items():
            try:
                if Topic.compare_topics(topic, message_data.topic):
                    subscriber["callback"](_client, subscriber["user_data"], message_data.topic, message_data.payload)
            except ValueError as e:
                logger.exception("ValueError is raised in paho mqtt client. Cause: %s", e.message)
            except Exception as e:
                logger.exception("UnkownError is raised in paho mqtt client. Cause: %s", e.message)
        subscribers_lock.release()

    client.on_message = on_message
    client.connect(**args.connect)


class PubSubClient(ArgsSetters):
    def __init__(self):
        super(PubSubClient, self).__init__()
        self.__manager = Manager()
        self.__subscribers = {}
        self.__subscribers_lock = self.__manager.Lock()
        self.__client = None
        self.__dumps = json.dumps
        self.__loads = json.loads

    def __delete__(self):
        self.disconnect()
        self.__manager.shutdown()

    def set_dumps(self, dumps):
        self.__dumps = dumps

    def set_loads(self, loads):
        self.__loads = loads

    def subscribe(self, topic, callback, qos=0, user_data=None, structure=None, rate=None):
        logger.info("subscribe {} topic. qos: {}, structure: {}".format(topic, qos, structure))
        loads = self.__loads

        def wrapped_callback(_client, _user_data, _topic, _payload):
            message = Topic.deserialize(_payload, structure, loads)
            callback(_client, _user_data, _topic, message)

        self.__subscribers_lock.acquire()
        self.__subscribers[topic] = {
            "topic": topic,
            "callback": wrapped_callback,
            "qos": qos,
            "user_data": user_data
        }
        self.__subscribers_lock.release()

        if self.__client is not None:
            set_on_message_and_connect(
                self.__client, self.args, self.__subscribers, self.__subscribers_lock)

    def connect(self):
        def on_connect(client, _userdata, _flags, response_code):
            if response_code == 0:
                for topic, subscriber in self.__subscribers.items():
                    client.subscribe(topic=topic, qos=subscriber["qos"])
            else:
                logger.warning('connect status {0}'.format(response_code))

        self.__client = Client(**self.args.client)

        if "tls_set" in self.args.keys():
            self.__client.tls_set(**self.args.tls_set)

        if "tls_insecure_set" in self.args.keys():
            self.__client.tls_insecure_set(**self.args.tls_insecure_set)

        if "will_set" in self.args.keys():
            self.__client.will_set(**self.args.will_set)

        if "username_pw_set" in self.args.keys():
            self.__client.username_pw_set(**self.args.username_pw_set)

        self.__client.on_connect = on_connect
        set_on_message_and_connect(
            self.__client, self.args, self.__subscribers, self.__subscribers_lock)

        self.__client.loop_start()

    def publish(self, topic, message, structure=None, qos=0, retain=False, wait=False):
        if structure is not None:
            if not structure.validate_data(message):
                logger.error(pformat({"errors": structure.get_errors(), "message": message}))
                raise ValueError

        payload = Topic.serialize(message, self.__dumps)
        info = self.__client.publish(topic, payload, qos, retain)
        if wait:
            info.wait_for_publish()

    def unsubscribe(self, topic):
        self.__client.unsubscribe(topic)
        self.__subscribers_lock.acquire()
        self.__subscribers.pop(topic)
        self.__subscribers_lock.release()

    @staticmethod
    def loop(sleep_time):
        while True:
            sleep(sleep_time)

    def disconnect(self):
        self.__client.disconnect()
