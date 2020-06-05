#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import os

PIN_LTE5V_EN=7  # LTE_BUF_OE
PIN_W_DISABLE=15
PIN_PWRKEY=18
PIN_RESET=22      # High reset
PIN_WAKEUP_IN=11
PIN_ANTENNA=16   # VDD_ANT_GNSS_EN
PIN_AP_READY=13
MODEM_TTY="/dev/ttyUSB3"

def quectel_poweronoff():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    GPIO.setup(PIN_LTE5V_EN, GPIO.OUT)
    GPIO.setup(PIN_W_DISABLE, GPIO.OUT)
    GPIO.setup(PIN_PWRKEY, GPIO.OUT)
    GPIO.setup(PIN_RESET, GPIO.OUT)
    GPIO.setup(PIN_WAKEUP_IN, GPIO.OUT)
    GPIO.setup(PIN_ANTENNA, GPIO.OUT)
    GPIO.setup(PIN_AP_READY, GPIO.OUT)

    # enable GNSS ANTENNA power
    GPIO.output(PIN_ANTENNA,GPIO.LOW)
    # enable  LTE 5V
    GPIO.setup(PIN_LTE5V_EN,GPIO.HIGH)
    time.sleep(0.2)
    # deassert RESET
    GPIO.output(PIN_RESET,GPIO.LOW)
    # disable Airplane mode
    GPIO.output(PIN_W_DISABLE,GPIO.HIGH)
    # stay in WAKEUP state
    GPIO.output(PIN_WAKEUP_IN,GPIO.LOW)

    # Power On
    GPIO.output(PIN_PWRKEY,GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(PIN_PWRKEY,GPIO.HIGH)
    time.sleep(0.6)
    GPIO.output(PIN_PWRKEY,GPIO.LOW)
    time.sleep(0.1)

def main():
    quectel_poweronoff()
    GPIO.output(PIN_AP_READY,GPIO.LOW)
    time.sleep(1)
    is_on = 0
    if not os.path.exists(MODEM_TTY):
        is_on = 1
    if not is_on == 0:
        print("Power on LTE module")
        while not os.path.exists(MODEM_TTY):
            pass
        print("OK")
        exit(0)
    print("Power off LTE module")
    while os.path.exists(MODEM_TTY):
        pass
    time.sleep(10)
    print("OK")
    exit(1)

if __name__ == "__main__":
    main()

