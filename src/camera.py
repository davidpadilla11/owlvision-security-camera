import time
import picamera
import numpy as np
import os
import send_email

with picamera.PiCamera() as camera:
    camera.rotation = 90
    camera.resolution = (320, 240)
    camera.framerate = 24
    time.sleep(2)
    camera.start_preview()

    while True:
        output1 = np.empty((240, 320, 3), dtype=np.uint8)
        camera.capture(output1, 'rgb')

        time.sleep(3)
        
        output2 = np.empty((240, 320, 3), dtype=np.uint8)
        camera.capture(output2, 'rgb')
        
        diff = np.subtract(output2, output1, dtype=int) # calcular la diferencia pixel a pixel
        diff = np.abs(diff)
        diff = diff > 25 # si la diferencia de pixeles es mayor que 25 (10% of 255)
        is_image_diff = diff.sum() > 23040 # La imagen es diferente si mas del 10% de los pixeles son diferentes.
        
        print('Movement detected:', is_image_diff)
        
        if is_image_diff:
            print('\tRecording video ... ', end='')
            camera.resolution = (1280, 720)
            camera.start_recording('/home/pi/Documents/Projects/Camera/video.h264')
            time.sleep(8)
            camera.stop_recording()
            camera.resolution = (320, 240)
            print('\tDone!')
            
            print('\tConverting video ... ', end='')
            os.system('/home/pi/Documents/Projects/Camera/convert.sh')
            print('\tDone!')
            
            print('\tSending email ... ', end='')
            send_email.send()
            print('\tDone!')
