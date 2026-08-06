#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# obdonuds.py: A simple OBD client tool
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2026/08/06 v0.1 blush up
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# TODO:
#   * Support DoIP
#   * Support J1979 (Legacy OBD)
import time
import argparse

import threading
import can
import isotp
#import obd


def get_did(rx_payload):
    return '%04X' %(int.from_bytes(rx_payload[1:3], 'big'))

def dump_msg(rx_payload):
    msg = ' '.join('%02X' % rx_payload[idx]for idx in range(0, len(rx_payload)))
    return msg

def scan_obd_protocol():
    bus = can.interface.Bus(interface='socketcan',
                            channel=args.interface, bitrate=500000)
    bus.set_filters([{"can_id": 0x7E8, "can_mask": 0x7F8, "extended": False}])

    if args.debug:
        print("=== Start Supported OBD spec. (J1979/J1979-2) ===")

    # J1979-2 (OBD on UDS) can be checked if  SID=0x22, DID=0xF810 is supported
    # Use single frame of ISO-TP (top 0x02 is data len(2) [22 F8 10])
    req_data = [0x03, 0x22, 0xF8, 0x10] #, 0x00, 0x00, 0x00, 0x00]
    msg = can.Message(
        arbitration_id=0x7DF,
        data=req_data,
        is_extended_id=False
    )

    try:
        if args.debug:
            print(f"Sending (0x7DF): {' '.join(f'{b:02X}' for b in req_data)}")

        bus.send(msg)

        captured_responses = []
        start_time = time.time()
        while (time.time() - start_time) < 2.0:
            # busy poll using timeout = 0.1s
            rx_msg = bus.recv(timeout=0.1)
            if rx_msg is not None:
                captured_responses.append(rx_msg)

        print(f"Received {len(captured_responses)} messages")

        j1979_2_detected = False
        detected_ecus = []

        for rx in captured_responses:
            data_str = ' '.join(f'{b:02X}' for b in rx.data)
            print(f"  [Receive] ID: 0x{rx.arbitration_id:03X} | Data: {data_str}")
            # Record CAN ID of responded ECUs (dedupe)
            if rx.arbitration_id not in detected_ecus:
                detected_ecus.append(rx.arbitration_id)

            # Check positive responses (top 0x04 means data length(4bytes),
            # 0x22 means successful response, 0xF810 is DID)
            if len(rx.data) >= 5 and rx.data[1] == 0x62 and rx.data[2] == 0xF8 and rx.data[3] == 0x10:
                j1979_2_detected = True
                version = rx.data[4]
                print(f"Detected a positive response of J1979-2 (OBD on UDS) (Version: 0x{version:02X})")

        # 6. Show Summary
        print("=== Summary ===")
        print(f"Response ID of detected ECU: {[f'0x{ecu:03X}' for ecu in sorted(detected_ecus)]}")

    except can.CanError as e:
        print(f"CAN Communication Errror: {e}")
    finally:
        bus.shutdown()

def send_tester_present(socket):
    rx_payload = None
    try:
        # send Tester Present with response request
        socket.send(bytes([0x3E, 0x00]))
        rx_payload = socket.recv()
        print(dump_msg(rx_payload), '/', 'Tester Present Positive Response')
    except TimeoutError:
        if args.debug:
            print(time.time(), 'timeout: %s %3X' % (args.interface, rx_id))

def send_get_vin(socket):
    rx_payload = None
    try:
        # get VIN / 03 22 F8 02
        socket.send(bytes([0x22, 0xF8, 0x02]))
        rx_payload = socket.recv()
        print(dump_msg(rx_payload), '/', rx_payload[3:].decode('utf-8'))
    except TimeoutError:
        if args.debug:
            print(time.time(), 'timeout: %s %3X' % (args.interface, rx_id))
        print(type(rx_payload), rx_payload)

def send_get_ecu_name(socket):
    rx_payload = None
    try:
        # get VIN / 03 22 F8 0A
        socket.send(bytes([0x22, 0xF8, 0x0A]))
        rx_payload = socket.recv()
        print(dump_msg(rx_payload), '/', rx_payload[3:].decode('utf-8'))
    except TimeoutError:
        if args.debug:
            print(time.time(), 'timeout: %s %3X' % (args.interface, rx_id))
        print(type(rx_payload), rx_payload)

def send_get_sw_version(socket):
    rx_payload = None
    try:
        socket.send(bytes([0x22, 0xF1, 0x89]))
        rx_payload = socket.recv()
        print(dump_msg(rx_payload), '/', rx_payload[3:].decode('utf-8'))
    except TimeoutError:
        if args.debug:
            print(time.time(), 'timeout: %s %3X' % (args.interface, rx_id))
        print(type(rx_payload), rx_payload)

def send_get_rpm(socket):
    rx_payload = None
    try:
        # get RPM  F40C
        socket.send(bytes([0x22, 0xF4, 0x0C]))
        rx_payload = socket.recv()
        print(dump_msg(rx_payload), '/', (rx_payload[3] * 256 + rx_payload[4])/4)
    except TimeoutError:
        if args.debug:
            print(time.time(), 'timeout: %s %3X' % (args.interface, rx_id))

def send_get_speed(socket):
    rx_payload = None
    try:
        # get SPEED  F40C
        socket.send(bytes([0x22, 0xF4, 0x0D]))
        rx_payload = socket.recv()
        print(dump_msg(rx_payload), '/', rx_payload[3])
    except TimeoutError:
        if args.debug:
            print(time.time(), 'timeout: %s %3X' % (args.interface, rx_id))
        print(type(rx_payload), rx_payload)

def send_get_throttle(socket):
    rx_payload = None
    try:
        # get SPEED  F40C
        socket.send(bytes([0x22, 0xF4, 0x11]))
        rx_payload = socket.recv()
        print(dump_msg(rx_payload), '/', rx_payload[3] * 100 / 255)
    except TimeoutError:
        if args.debug:
            print(time.time(), 'timeout: %s %3X' % (args.interface, rx_id))
        print(type(rx_payload), rx_payload)

def send_get_ambient_temp(socket):
    rx_payload = None
    try:
        # get SPEED  F40C
        socket.send(bytes([0x22, 0xF4, 0x46]))
        rx_payload = socket.recv()
        print(dump_msg(rx_payload), '/', rx_payload[3])
    except TimeoutError:
        if args.debug:
            print(time.time(), 'timeout: %s %3X' % (args.interface, rx_id))
        print(type(rx_payload), rx_payload)

def send_get_all_dtcs(socket):
    rx_payload = None
    try:
        # 7E0  8  03 19 02 0F 00 00 00 00 (SID: 19, SF: 02, mask: 0F)
        #   02: reportDTCByStatusMask
        socket.send(bytes([0x19, 0x02, 0x0F]))
        rx_payload = socket.recv()
        #print(dump_msg(rx_payload), '/', '%d DTCs' % (len(rx_payload[3:]) / 3))
        count = int(len(rx_payload[3:]) / 3)
        dtcs = list()
        offset = 3
        for i in range(0, count):
            dtcs.append(int.from_bytes(rx_payload[offset+i*3:offset+(i*3)+3], 'big'))
        return dtcs
    except TimeoutError:
        if args.debug:
            print(time.time(), 'timeout: %s %3X' % (args.interface, rx_id))
        print(type(rx_payload), rx_payload)

def send_get_dtc_count(socket):
    rx_payload = None
    try:
        socket.send(bytes([0x19, 0x01, 0x0F]))
        rx_payload = socket.recv()
        # NOTE: rx_payload[4:6] means byte 4 and 5.
        print(dump_msg(rx_payload), '/', '%d DTCs' % (int.from_bytes(rx_payload[4:6], byteorder='big')))
    except TimeoutError:
        if args.debug:
            print(time.time(), 'timeout: %s %3X' % (args.interface, rx_id))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="obdonuds.py")
    parser.add_argument("--poll_timeout", type=float, default=0.1)
    parser.add_argument("-i", "--interface", default='vcan0')
    parser.add_argument("-b", "--broadcast", default=0x7DF)
    parser.add_argument("-m", "--mode", default='J1979-2')
    parser.add_argument("--scan", action="store_true")
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--ecus", nargs='*', type=lambda x: int(x, 16), default=[0x7E0, 0x7E1, 0x7E2])
    args = parser.parse_args()

    if args.scan:
        scan_obd_protocol()

    socket = isotp.socket()
    tx_id = 0x7E0
    rx_id = tx_id + 0x8
    socket.bind(args.interface, isotp.Address(rxid=rx_id, txid=tx_id))
    #
    socket.settimeout(10.0)
    #
    print('Checking...: %03X' % (tx_id))
    # 0x02, 0x7E, 0x00
    send_tester_present(socket)
    #
    # 0x22, 0xF8, 0x02
    send_get_vin(socket)

    send_get_ecu_name(socket)
    send_get_sw_version(socket)

    send_get_rpm(socket)
    send_get_speed(socket)
    send_get_throttle(socket)
    send_get_ambient_temp(socket)
    send_get_dtc_count(socket)
    send_get_all_dtcs(socket)

    for canid in args.ecus[1:]:
        print('Checking...: %03X' % (canid))
        s = isotp.socket()
        tx_id = canid
        rx_id = tx_id + 0x8
        s.bind(args.interface, isotp.Address(rxid=rx_id, txid=tx_id))
        s.settimeout(10.0)
        send_get_ecu_name(s)
        send_get_sw_version(s)
        send_get_dtc_count(s)
        send_get_all_dtcs(s)
        s.close()

    socket.close()
