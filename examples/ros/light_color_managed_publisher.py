#!/usr/bin/env python
# coding: utf-8

from argparse import ArgumentParser
from ams.ros import LightColorManagedPublisher


parser = ArgumentParser()
parser.add_argument("-H", "--host", type=str, default="localhost", help="host")
parser.add_argument("-P", "--port", type=int, default=1883, help="port")
parser.add_argument("-N", "--name", type=str, default="sim_car 1", help="name")
args = parser.parse_args()


if __name__ == '__main__':
    lightColorManagedPublisher = LightColorManagedPublisher(name=args.name)

    print("lightColorManagedPublisher {} on {}".format(
        lightColorManagedPublisher.event_loop_id, lightColorManagedPublisher.get_pid()))

    lightColorManagedPublisher.start(host=args.host, port=args.port)