import cv2
import numpy as np
import math
import RPi.GPIO as GPIO
import time



class Carctrl(object):
    
    def __init__(self):

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
            
        self.INT1 = 11                    #ENA
        self.INT2 = 12                    #ENB
        self.servoPIN = 33
            
        GPIO.setup(self.INT1,GPIO.OUT)
        GPIO.setup(self.INT2,GPIO.OUT)
        GPIO.setup(self.servoPIN, GPIO.OUT)

        self.pwm1 = GPIO.PWM(self.INT1, 500)
        self.pwm2 = GPIO.PWM(self.INT2, 500)
        self.pwm_servo = GPIO.PWM(self.servoPIN, 50)

        self.pwm1.start(0)
        self.pwm2.start(0)
        self.pwm_servo.start(7.5)

    def go(self):
        self.pwm1.ChangeDutyCycle(10)
        self.pwm2.ChangeDutyCycle(0)
        self.pwm_servo.ChangeDutyCycle(7.5)
        GPIO.output(self.INT1, GPIO.HIGH)
        GPIO.output(self.INT2, GPIO.LOW)
        # gpio.output(in3, gpio.HIGH)
        # gpio.output(in4, gpio.LOW)


# 定义向右
    def right(self):
        self.pwm1.ChangeDutyCycle(15)
        self.pwm2.ChangeDutyCycle(0)
        self.pwm_servo.ChangeDutyCycle(10.5)
        
        # gpio.output(in1, gpio.HIGH)
        # gpio.output(in2, gpio.LOW)
        # gpio.output(in3, gpio.LOW)
        # gpio.output(in4, gpio.HIGH)


    # 定义向左
    def left(self):
        self.pwm1.ChangeDutyCycle(15)
        self.pwm2.ChangeDutyCycle(0)
        self.pwm_servo.ChangeDutyCycle(4.5)
        # gpio.output(in2, gpio.HIGH)
        # gpio.output(in3, gpio.HIGH)
        # gpio.output(in4, gpio.LOW)


    # 定义向后
    def back(self):
        self.pwm1.ChangeDutyCycle(0)
        self.pwm2.ChangeDutyCycle(15)
        self.pwm_servo.ChangeDutyCycle(7.5)
        GPIO.output(self.INT1, GPIO.LOW)
        GPIO.output(self.INT2, GPIO.HIGH)
        # gpio.output(in3, gpio.LOW)
        # gpio.output(in4, gpio.HIGH)


    # 定义停止
    def stop(self):
        self.pwm1.ChangeDutyCycle(0)
        self.pwm2.ChangeDutyCycle(0)
        #self.pwm_servo.ChangeDutyCycle(7.5)
        # gpio.output(in1, gpio.LOW)
        # gpio.output(in2, gpio.LOW)
        # gpio.output(in3, gpio.LOW)
        # gpio.output(in4, gpio.LOW)
    
    
    
    def self_driving(self, prediction):

        if prediction == 0:
            self.go()
            print("Forward")
        elif prediction == 1:
            self.left()
            print("Left")
        elif prediction == 2:
            self.right()
            print("Right")
        else:
            self.stop()


class NeuralNetwork(object):

    def __init__(self):
        self.annmodel = cv2.ml.ANN_MLP_load('mlp_xml/mlp.xml')

    def predict(self, samples):
        ret, resp = self.annmodel.predict(samples)
        return resp.argmax(-1)  # find max


class CamDataHandle(object):

    def __init__(self):

        self.model = NeuralNetwork()
        print('load ANN model.')
        #self.obj_detection = ObjectDetection()
        self.car = Carctrl()

        print('----------------Caminit completed-----------------')
        self.handle()

    def handle(self):

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 320)
        self.cap.set(4, 240)

        try:
            while True:
                ret, cam = self.cap.read()
                gray = cv2.cvtColor(cam, cv2.COLOR_RGB2GRAY)
                ret, th3 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                roi = th3[120:240, :]

                image_array = roi.reshape(1, 38400).astype(np.float32)
                prediction = self.model.predict(image_array)
                cv2.imshow('roi',roi)
                #cv2.imshow('cam', cam)

                
                self.car.self_driving(prediction)
                if cv2.waitKey(1) & 0xFF == ord('l'):
                    break

        finally:
            cv2.destroyAllWindows()
            print('Shut down')


if __name__ == '__main__':
    CamDataHandle()