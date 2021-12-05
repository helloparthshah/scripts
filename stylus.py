#!/usr/bin/python3
import evdev
import math
import autopy
from evdev import UInput, AbsInfo, ecodes as e
import argparse
import os

if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

debug = 0

parser = argparse.ArgumentParser(description='workaround for stylus')
parser.add_argument('-d', '--debug', action='store_true',
                    help='start with debug mode')
parser.add_argument('-e', '--event', type=int, help='specify the event number')

args = parser.parse_args()
debug = args.debug

p = 0
devices = evdev.list_devices()

if not args.event:
    for dev in devices:
        print('%-12i%s' % (p, evdev.InputDevice(dev).name))
        p += 1

    i = int(input("Enter number: "))
else:
    i = args.event
device = evdev.InputDevice(devices[i])
# mouse = evdev.InputDevice('/dev/input/event15')

print(device)

# print(mouse.capabilities(verbose=True))

device.grab()

x, y = 0, 0
for event in device.read_loop():
    code, val = event.code, event.value

    # ui = evdev.UInput()

    if code == 59:
        if debug == 1:
            print('press', val)
        # device.write(e.EV_ABS, e.ABS_MT_DISTANCE, val)
        if val == 0:
            # mouse.write(e.EV_KEY, e.BTN_TOUCH, 1)
            # mouse.write(e.EV_KEY, e.BTN_TOOL_FINGER, 1)
            autopy.mouse.toggle(down=True)
        else:
            # mouse.write(e.EV_KEY, e.BTN_TOUCH, 0)
            # mouse.write(e.EV_KEY, e.BTN_TOOL_FINGER, 0)
            autopy.mouse.toggle(down=False)

    if code == 53:
        # val = math.floor(val*3211/5760)
        val = val*1919.5/5760
        if debug == 1:
            print('x', val)
        x = val
        # device.write(e.EV_ABS, e.ABS_MT_POSITION_X, val)
        # mouse.write(e.EV_ABS, e.ABS_MT_POSITION_X, val)
        # mouse.write(e.EV_ABS, e.ABS_X, val)
        # autopy.mouse.move(val, None)

    if code == 54:
        # val = math.floor(val*2431/3240)
        val = val*1079.5/3240
        if debug == 1:
            print('y', val)
        y = val
        # device.write(e.EV_ABS, e.ABS_MT_POSITION_Y, val)
        # mouse.write(e.EV_ABS, e.ABS_MT_POSITION_Y, val)
        # mouse.write(e.EV_ABS, e.ABS_Y, val)
        # autopy.mouse.move(None, val, duration=0)

    ''' if code == 57:
        print('tid', val)
        # device.write(e.EV_ABS, e.ABS_MT_TRACKING_ID, val)
        mouse.write(e.EV_ABS, e.ABS_MT_TRACKING_ID, val) '''

    if event.type == 0:
        if debug == 1:
            print("sync")
        # mouse.write(e.EV_MSC, e.MSC_TIMESTAMP, 0)
        # device.write(e.EV_SYN, 0, 0)
        # mouse.write(e.EV_SYN, 0, 0)
        autopy.mouse.move(x, y)

device.ungrab()
