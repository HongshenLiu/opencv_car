import numpy as np
import cv2
import pygame
from pygame.locals import *
import time
import os
import RPi.GPIO as GPIO

class CollectData(object):

    def __init__(self):
        # set IO and GPIO mod
        # pygame init
        pygame.init()
        
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
        
        self.save_img = True
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,320)
        self.cap.set(4,240)
        
        # create labels
        self.k = np.zeros((3, 3), 'float')
        for i in range(3):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 3), 'float')
 
        screen=pygame.display.set_mode((320,240))
 
        self.collect_image()
        
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
    
    def collect_image(self):
        frame = 1
        saved_frame = 0
        total_frame = 0
        label_0 =0
        label_1 =1
        label_2 =2
        # collect images for training
        print('Start collecting images...')

        e1 = cv2.getTickCount()
        image_array = np.zeros((1, 38400))
        label_array = np.zeros((1, 3), 'float')
        # collect cam frames
        try:
 
            while self.save_img:
                ret, cam = self.cap.read()    
                roi = cam[120:240,:]
                #print(roi.shape)
                #image = cv2.imdecode(np.frombuffer(cam,dtype=np.uint8),cv2.IMREAD_GRAYSCALE)                
                gauss = cv2.GaussianBlur(roi,(5,5),0)
                gray = cv2.cvtColor(gauss,cv2.COLOR_RGB2GRAY)
                dst = cv2.Canny(gray,50,50)
                ret,thresh1 = cv2.threshold(gray,90,255,cv2.THRESH_BINARY)  
                ret,th3 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)                
                
                #print(th3.shape)
                #cv2.imwrite('./training_images/frame{:>05}.jpg'.format(frame),dst)
                #cv2.imshow('cam',cam)
                #cv2.imshow('dst',dst)
                #cv2.imshow('gray',gray)
                #cv2.imshow('roi',roi)
                #cv2.imshow('thresh1',thresh1)
                #cv2.imshow('th3',th3)
                
                temp_array = th3.reshape(1,38400).astype(np.float32)
                frame += 1          
                total_frame += 1
 
                if cv2.waitKey(1) & 0xFF == ord('l'): 
                    print("exit")  
 
                    break
                
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_w]:                          
                            image_array = np.vstack((image_array, temp_array))
                            label_array = np.vstack((label_array, self.k[0]))
                            saved_frame += 1
                            self.go()
                            cv2.imwrite('./training_images/{:1}_frame{:>05}.jpg'.format(label_0,saved_frame),th3)                          
                            print("forward")
                            print(saved_frame)

                        elif keys[pygame.K_a]:
                            image_array = np.vstack((image_array, temp_array))
                            label_array = np.vstack((label_array, self.k[1]))
                            saved_frame += 1
                            self.left()
                            cv2.imwrite('./training_images/{:1}_frame{:>05}.jpg'.format(label_1,saved_frame),th3)
                            print("left")
                            print(saved_frame)

                        elif keys[pygame.K_d]:
                            image_array = np.vstack((image_array, temp_array))
                            label_array = np.vstack((label_array, self.k[2]))
                            saved_frame += 1
                            self.right()
                            cv2.imwrite('./training_images/{:1}_frame{:>05}.jpg'.format(label_2,saved_frame),th3)
                            print("right")
                            print(saved_frame)

                        elif keys[pygame.K_s]:
                            self.back()                           
                            print("back")
     
                        elif keys[pygame.K_p]:
                            print('exit')
                            self.save_img = False                               
                            break

                    elif event.type == KEYUP:
                        self.stop()               
                        print("stop")
  
            # save training images and labels
            train = image_array[1:, :]
            train_labels = label_array[1:, :]
            print(train.shape)
            # save training data as a numpy file

            file_name = str(int(time.time()))
            directory = "training_data"
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                np.savez(directory + '/' + file_name + '.npz', train=train, train_labels=train_labels)
            except IOError as e:
                print(e)
            e2 = cv2.getTickCount()
 
            time0 = (e2 - e1) / cv2.getTickFrequency()
            print('Video duration:', time0)
            print('Streaming duration:', time0)

            print((train.shape))
            print((train_labels.shape))
            print('Total frame:', total_frame)
            print('Saved frame:', saved_frame)
            print('Dropped frame', total_frame - saved_frame)

            
        finally:                     
            self.cap.release()
            cv2.destroyAllWindows()    
 
if __name__ == '__main__':
    CollectData()