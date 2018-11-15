#!/usr/bin/env python
# coding: utf-8

from time import time, sleep

from ams.helpers import Hook, Condition, Publisher, Subscriber
from ams.helpers import StateMachine as StateMachineHelper
from ams.nodes.event_loop import EventLoop
from ams.structures import TrafficSignal as Structure
from ams.structures import InfraController


class TrafficSignal(EventLoop):

    CONST = Structure.CONST
    Config = Structure.Config
    Status = Structure.Status
    Message = Structure.Message

    def __init__(self, config, status, state_machine_path=None):
        super(TrafficSignal, self).__init__(config, status)

        self.user_data["target_traffic_signal"] = self.config.target_self

        topic = Subscriber.get_traffic_signal_cycle_topic(
            self.config.target_infra_controller, self.config.target_self)
        self.subscribers[topic] = {
            "topic": topic,
            "callback": Subscriber.on_traffic_signal_cycle_message,
            "structure": InfraController.Message.Cycle,
            "user_data": self.user_data
        }

        topic = Subscriber.get_traffic_signal_schedules_topic(
            self.config.target_infra_controller, self.config.target_self)
        self.subscribers[topic] = {
            "topic": topic,
            "callback": Subscriber.on_traffic_signal_schedules_message,
            "structure": InfraController.Message.Schedules,
            "user_data": self.user_data
        }

        self.state_machine_path = state_machine_path

    def loop(self):
        resource = StateMachineHelper.load_resource(self.state_machine_path)
        state_machine_data = StateMachineHelper.create_data(resource)
        StateMachineHelper.attach(
            state_machine_data,
            [
                Hook.update_traffic_signal_color,
                Hook.generate_traffic_signal_schedules,
                Hook.update_traffic_signal_schedules,
                Publisher.publish_traffic_signal_status,
                Condition.schedules_exists,
                Condition.on_schedule_close_to_the_end
            ],
            self.user_data
        )

        while True:
            start_time = time()

            status = Hook.get_status(self.user_data["kvs_client"], self.user_data["target_traffic_signal"], self.Status)
            event = status.event
            updated_flag = False
            if event is not None:
                updated_flag = StateMachineHelper.update_state(state_machine_data, event)

            if not updated_flag:
                StateMachineHelper.update_state(state_machine_data, None)

            status.state = StateMachineHelper.get_state(state_machine_data)
            Hook.set_status(self.user_data["kvs_client"], self.user_data["target_traffic_signal"], status)

            sleep(max(0, self.dt - (time()-start_time)))
