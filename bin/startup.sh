#!/bin/bash

echo "process start"

#sudo python3 /home/pi/LEDs/src/ledsAgent.py --led-cols 255 --led-rows 32
sudo python3 /home/pi/LEDs/src/ledsAgent.py --led-cols 64 --led-rows 32 --led-slowdown-gpio=2 &
