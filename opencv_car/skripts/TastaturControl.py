from pynput import keyboard
import RPi.GPIO as GPIO
import time, sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

INT1 = 11                    #ENA
INT2 = 12                    #ENB
servoPIN = 33                    
GPIO.setup(INT1,GPIO.OUT)
GPIO.setup(INT2,GPIO.OUT)
GPIO.setup(servoPIN, GPIO.OUT)

pwm1 = GPIO.PWM(INT1, 500)
pwm2 = GPIO.PWM(INT2, 500)
pwm_servo = GPIO.PWM(servoPIN, 50)

pwm1.start(0)
pwm2.start(0)
pwm_servo.start(7.5)

# 定义向前
def go():
    pwm1.ChangeDutyCycle(10)
    pwm2.ChangeDutyCycle(0)
    pwm_servo.ChangeDutyCycle(7.5)
    GPIO.output(INT1, GPIO.HIGH)
    GPIO.output(INT2, GPIO.LOW)
    # gpio.output(in3, gpio.HIGH)
    # gpio.output(in4, gpio.LOW)


# 定义向右
def right():
    pwm1.ChangeDutyCycle(15)
    pwm2.ChangeDutyCycle(0)
    pwm_servo.ChangeDutyCycle(10.5)
    
    # gpio.output(in1, gpio.HIGH)
    # gpio.output(in2, gpio.LOW)
    # gpio.output(in3, gpio.LOW)
    # gpio.output(in4, gpio.HIGH)


# 定义向左
def left():
    pwm1.ChangeDutyCycle(15)
    pwm2.ChangeDutyCycle(0)
    pwm_servo.ChangeDutyCycle(4.5)
    # gpio.output(in2, gpio.HIGH)
    # gpio.output(in3, gpio.HIGH)
    # gpio.output(in4, gpio.LOW)


# 定义向后
def back():
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(10)
    pwm_servo.ChangeDutyCycle(7.5)
    GPIO.output(INT1, GPIO.LOW)
    GPIO.output(INT2, GPIO.HIGH)
    # gpio.output(in3, gpio.LOW)
    # gpio.output(in4, gpio.HIGH)


# 定义停止
def stop():
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)
    #pwm_servo.ChangeDutyCycle(7.5)
    # gpio.output(in1, gpio.LOW)
    # gpio.output(in2, gpio.LOW)
    # gpio.output(in3, gpio.LOW)
    # gpio.output(in4, gpio.LOW)
def on_press(key):
    try:
        if key.char == 'w':
            go()
            print('towards')
        if key.char == 'a':
            left()
            print('left')
        if key.char == 's':
            back()
            print('back')
        if key.char == 'd':
            right()
            print('right')
    except AttributeError:
        print('special key {0} pressed'.format(key))


def on_release(key):
    stop()
    if key == keyboard.Key.esc:
        return False

# 键盘监听

with keyboard.Listener(
        on_press=on_press, on_release=on_release) as listener:
    listener.join()

pwm1.stop()
pwm2.stop()
pwm_servo.stop()

GPIO.cleanup()