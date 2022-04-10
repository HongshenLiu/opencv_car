# -*- coding: utf-8 -*-                 #通过声明可以在程序中书写中文
import RPi.GPIO as GPIO                 #引入RPi.GPIO库函数命名为GPIO
import time                             #引入计时time函数
GPIO.setwarnings(False)
# BOARD编号方式，基于插座引脚编号
GPIO.setmode(GPIO.BOARD)                #将GPIO编程方式设置为BOARD模式

#接口定义
INT1 = 11                    #将L298 INT1口连接到树莓派Pin11
INT2 = 12

GPIO.setup(INT1,GPIO.OUT)
GPIO.setup(INT2,GPIO.OUT)

GPIO.output(INT1,GPIO.HIGH)
GPIO.output(INT2,GPIO.LOW)

time.sleep(1)

GPIO.cleanup()