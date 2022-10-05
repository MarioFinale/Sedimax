from datetime import datetime
from distutils.log import error
from re import S
from tkinter import W
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUI as sg
import os
import shutil
from datetime import datetime
import csv


from sympy import rad

data_1 = [[0,0,0]]
data_2 = [[0,0,0]]
data_3 = [[0,0,0]]
data_4 = [[0,0,0]]
data_5 = [[0,0,0]]

def main():
    global data_1
    global data_2
    global data_3
    global data_4
    global data_5

    sg.theme('Dark Blue 3')


    tab1_layout =  [[sg.Table(data_1[0:][:], ['  Tiempo  ','   Altura en cm   ','   Volumen en cm3  '], num_rows=20, key='tabla_1', size=(200, 400))]]#[sg.Graph(canvas_size=(550, 300), graph_bottom_left=(-300,-300), graph_top_right=(4200,4400), background_color='white', key='graph_1', tooltip='Contenedor 1')]]
    tab2_layout =  [[sg.Table(data_2[0:][:], ['  Tiempo  ','   Altura en cm   ','   Volumen en cm3  '], num_rows=20, key='tabla_2', size=(200, 400))]]
    tab3_layout =  [[sg.Table(data_3[0:][:], ['  Tiempo  ','   Altura en cm   ','   Volumen en cm3  '], num_rows=20, key='tabla_3', size=(200, 400))]]
    tab4_layout =  [[sg.Table(data_4[0:][:], ['  Tiempo  ','   Altura en cm   ','   Volumen en cm3  '], num_rows=20, key='tabla_4', size=(200, 400))]]
    tab5_layout =  [[sg.Table(data_5[0:][:], ['  Tiempo  ','   Altura en cm   ','   Volumen en cm3  '], num_rows=20, key='tabla_5', size=(200, 400))]]


    layout = [[sg.Text('Chipisoft', size=(8, 1), justification='l', font='Helvetica 8'), sg.Text('SEDIMENTACIÓN', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image', size=(400, 250)), sg.TabGroup([[sg.Tab('Recipiente 1', tab1_layout, tooltip='tip'), sg.Tab('Recipiente 2', tab2_layout), sg.Tab('Recipiente 3', tab3_layout), sg.Tab('Recipiente 4', tab4_layout), sg.Tab('Recipiente 5', tab5_layout)]], tooltip='TIP2')],
              [sg.Image(filename='', key='processed', size=(200, 125))],
              [sg.Text("", key="Status")],
              [sg.Button('Calibrar', size=(10, 1), font='Helvetica 14'),
               sg.Button("Grabar", key="Grabar", size=(10, 1), font='Any 14'),
               sg.Button('Detectar', size=(10, 1), font='Any 14')],
               [sg.Slider(key='base', range=(10,100), orientation='h', size=(15,20)), sg.Slider(key='techo', range=(10,100), orientation='h', size=(15,20))],               
               [sg.Text('Separación inferior', size=(15, 1), justification='c', font='Helvetica 10'), sg.Text('Separación superior', size=(15, 1), justification='c', font='Helvetica 10')],
               [sg.Slider(key='brillo', range=(1,100),default_value=75, orientation='h', size=(15,20)), sg.Slider(key='contraste', range=(1,300), default_value=198, orientation='h', size=(15,20))],
               [sg.Text('Brillo', size=(15, 1), justification='c', font='Helvetica 10'), sg.Text('Contraste', size=(15, 1), justification='c', font='Helvetica 10')],
               [sg.Spin([i for i in range(1,2000)],readonly=True ,key='altura_contenedor', initial_value=382, size=(15,2))],
               [sg.Text('Altura en mm', size=(15, 1), justification='c', font='Helvetica 10')],
               [sg.Spin([i for i in range(1,20000)],readonly=True ,key='radio', initial_value=4083, size=(15,2))],
               [sg.Text('Radio en 0,01 mm', size=(15, 1), justification='c', font='Helvetica 10')]]

                    #definicion de la pantalla del programa


    window = sg.Window('Chipisoft SEDIMAX Pro beta version 1.0.1', layout)

    cap = cv.VideoCapture(0)
    grabando = False
    calibrando = False
    detectando = False
    result_number = 0
    frames_count = 0

    try:
        shutil.rmtree('./VIDEO_FRAMES/')
        shutil.rmtree('./RESULT/')
    except OSError:
        print("Error removing dirs")
    try:
        path = os.getcwd()
        os.mkdir(path + '/VIDEO_FRAMES/')
        os.mkdir(path + '/RESULT/')
    except OSError:
        print("Error creating directories")

    event, values = window.read(timeout=30)
    #graph_1 = window['graph_1']
    #graph_1.DrawLine((0,0), (4100,0))    
    #graph_1.DrawLine((0,0), (0,4200)) 
    #graph_1.DrawText( "Minutos", (4000,-100), color='green', font='Helvetica 8')
    #graph_1.DrawText( "Altura", (-100,4300), color='red', font='Helvetica 8')

    #for x in range(0, 3601, 240):    
    #    graph_1.DrawLine((x,-8), (x,8))
    #    if x != 0:    
    #        graph_1.DrawText( str(int(x/60)), (x,-100), color='green', font='Helvetica 8')

    #for y in range(0, 4001, 400):    
    #    graph_1.DrawLine((-8,y), (8,y))
    #    if y != 0:    
    #        graph_1.DrawText( str(int(y/100)), (-100, y), color='red', font='Helvetica 8')

    last_time = datetime.now()
    while True:
        event, values = window.read(timeout=30)
        base = int(values['base'])
        techo = int(values['techo'])
        brillo = int(values['brillo'])
        contraste = int(values['contraste'])
        tabla_1 = window['tabla_1']
        tabla_2 = window['tabla_2']
        tabla_3 = window['tabla_3']
        tabla_4 = window['tabla_4']
        tabla_5 = window['tabla_5']
        altura = int(values['altura_contenedor'])
        radio = int(values['radio']) / 100
        boton_grabar = window['Grabar']
        status_label = window['Status']


        ret, frame = cap.read()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            return

        elif event == 'Calibrar':
            if calibrando: calibrando = False
            else: calibrando = True            

        elif event == 'Grabar':
            if grabando: 
                grabando = False
                boton_grabar.update(text="Grabar")
                time_text_for_file = datetime.now().strftime("%H_%M_%S")
                filename1 = 'RESULT/' + time_text_for_file + "_1" + '.csv'
                filename2 = 'RESULT/' + time_text_for_file + "_2" + '.csv'
                filename3 = 'RESULT/' + time_text_for_file + "_3" + '.csv'
                filename4 = 'RESULT/' + time_text_for_file + "_4" + '.csv'
                filename5 = 'RESULT/' + time_text_for_file + "_5" + '.csv'

                with open(filename1, 'w', newline='') as result_1:
                    wr = csv.writer(result_1, dialect='excel')
                    wr.writerows([['Tiempo','Altura en cm','Volumen en cm3']])
                    wr.writerows(data_1)
                with open(filename2, 'w', newline='') as result_2:
                    wr = csv.writer(result_2, dialect='excel')
                    wr.writerows([['Tiempo','Altura en cm','Volumen en cm3']])
                    wr.writerows(data_2)
                with open(filename3, 'w', newline='') as result_3:
                    wr = csv.writer(result_3, dialect='excel')
                    wr.writerows([['Tiempo','Altura en cm','Volumen en cm3']])
                    wr.writerows(data_3)
                with open(filename4, 'w', newline='') as result_4:
                    wr = csv.writer(result_4, dialect='excel')
                    wr.writerows([['Tiempo','Altura en cm','Volumen en cm3']])
                    wr.writerows(data_4)
                with open(filename5, 'w', newline='') as result_5:
                    wr = csv.writer(result_5, dialect='excel')
                    wr.writerows([['Tiempo','Altura en cm','Volumen en cm3']])
                    wr.writerows(data_5)
                status_label.update(value="Resultados guardados como " + time_text_for_file + "_N.csv")

            else: 
                grabando = True 
                boton_grabar.update(text="Detener") 
                data_1 = [[0,0,0]]
                data_2 = [[0,0,0]]
                data_3 = [[0,0,0]]
                data_4 = [[0,0,0]]
                data_5 = [[0,0,0]]
                tabla_1.update(values=data_5)
                tabla_2.update(values=data_5)
                tabla_3.update(values=data_5)
                tabla_4.update(values=data_5)
                tabla_5.update(values=data_5)              
            
        elif event == 'Detectar':
            if detectando: detectando = False
            else: detectando = True 
            grabando = False
            

        if grabando:  
                try:
                    if not result_number == 0:                        
                        initial_time = datetime.strptime(last_time.strftime("%H:%M:%S"), "%H:%M:%S")
                        now = datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
                        delta = now-initial_time
                        print(delta)
                        if delta.seconds >= 60:
                            last_time = datetime.now()
                            analyze(window, frame, 0, 0, False, base, techo, brillo, contraste, radio, altura, tabla_1, tabla_2, tabla_3, tabla_4, tabla_5, last_time)
                            result_number += 1
                            
                    else:
                        last_time = datetime.now()
                        analyze(window, frame, 0, 0, False, base, techo, brillo, contraste, radio, altura, tabla_1, tabla_2, tabla_3, tabla_4, tabla_5, last_time)
                        result_number += 1
                        

                except TypeError as e:
                    print(e)                
        else:
            if detectando:
                    try:
                        last_time = datetime.now()
                        analyze(window, frame, 0, 0, False, base, techo, brillo, contraste, radio, altura, tabla_1, tabla_2, tabla_3, tabla_4, tabla_5, last_time)
                    except TypeError as e:
                        print(e)               
                    detectando = False
            else:
                dim = (400, 250)
                frame = cv.resize(frame, dim, interpolation=cv.INTER_AREA)
                if calibrando:
                        cv.rectangle(frame,(90, techo),(125, 250 - base), (0,255,0), 2)
                        cv.rectangle(frame,(145, techo),(175, 250 - base), (0,255,0), 2)
                        cv.rectangle(frame,(195, techo),(225, 250 - base), (0,255,0), 2)
                        cv.rectangle(frame,(245, techo),(275, 250 - base), (0,255,0), 2)
                        cv.rectangle(frame,(295, techo),(325, 250 - base), (0,255,0), 2)
                        cv.rectangle(frame,(60, techo - 5),(350, 255 - base), (0,255,0), 2)

                imgbytes = cv.imencode('.png', frame)[1].tobytes() 
                window['image'].update(data=imgbytes)


def analyze(programWindow, frame, resultCount, framesCount, debug, base, techo, brillo, contraste, radio, altura, tabla1, tabla2, tabla3, tabla4, tabla5, frame_timestamp):
    global data_1
    global data_2
    global data_3
    global data_4
    global data_5

    cv.imwrite( "VIDEO_FRAMES/%d.jpg" % framesCount, frame) 
    framesCount += 1
        
    dim = (400, 250)
    image = cv.resize(frame, dim, interpolation=cv.INTER_AREA)
    image2 = cv.resize(image, dim, interpolation=cv.INTER_AREA)

    cv.rectangle(image,(125, 0),(145, 250), (255,255,255), -1)
    cv.rectangle(image,(175, 0),(195, 250), (255,255,255), -1)
    cv.rectangle(image,(225, 0),(245, 250), (255,255,255), -1)
    cv.rectangle(image,(275, 0),(295, 250), (255,255,255), -1)
    cv.rectangle(image,(325, 0),(400, 250), (255,255,255), -1)
    
    cv.rectangle(image,(0, 0),(90, 250), (255,255,255), -1)
    cv.rectangle(image,(0, 0),(400, techo), (255,255,255), -1)
    cv.rectangle(image,(0, 250 - base),(400, 250), (255,255,255), -1)

    alpha = contraste / 100 # contrast  max 3
    beta = brillo   # brightness max 100
    print("brillo: " + str(brillo))
    print("alpha: " + str(alpha))

    new_image = np.zeros(image.shape, image.dtype)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            for c in range(image.shape[2]):
                new_image[y,x,c] = np.clip(alpha*image[y,x,c] + beta, 0, 255)

    gray = cv.cvtColor(new_image, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 3)
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen = cv.filter2D(blur, -1, sharpen_kernel)
    cv.floodFill(sharpen, None, (0,0), 0)
    cv.floodFill(sharpen, None, (0,0), 255)
    thresh = cv.threshold(sharpen,160,255, cv.THRESH_BINARY_INV)[1]

    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
    close = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel, iterations=3)

    cnts = cv.findContours(close, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    min_area = 250
    max_area = 15000
    min_ratio = 0.03
    max_ratio = 20

    image_number = 0
    rects = []

    

    for c in cnts:
        area = cv.contourArea(c)
        if area > min_area and area < max_area:
            x,y,w,h = cv.boundingRect(c)
            print(" X" + str(x) + " Y" + str(y)+ " W" + str(w)+ " H" + str(h))
            ratio = (x + 1)/ (y + 1)
            if ratio < max_ratio and ratio > min_ratio:
                if (y > 50) or (y < 50 and h > 50):
                    ROI = image[y:y+h, x:x+w]
                    cv.rectangle(image2, (x, y), (x + w, y + h), (36,255,12), 2)
                    
                    altura_max = 250 - techo - base
                    h_mm = ((h * altura) / altura_max)
                    volumen = np.pi * radio * radio * h_mm

                    row = [x, round((h_mm /10), 2) , round((volumen /1000), 2) ]
                    print("Altura maxima en pixeles: " + str(altura_max))
                    print("Altura en pixeles: " + str(h))
                    print("Altura maxima en mm: " + str(altura))
                    print("Altura en mm: " + str(h_mm))

                    if len(rects) == 0:
                        rects = row
                    else:
                        rects = np.vstack([rects, row])
                    image_number += 1
    print(rects)
    rects = rects[rects[:, 0].argsort()]
    print(rects)
    data = [[str(element) for element in index]for index in rects]
    print(rects)
    for i in range(len(data)):
        if i > 5: break
        data[i][0] = frame_timestamp.strftime("%H:%M:%S")
        if i == 0:
            print("data_1: " + str(data_1[0][0]))
            print(data_1)
            if data_1[0][0] == 0:
                data_1 = [data[i]]
            else:
                data_1 = np.concatenate((data_1, [data[i]]))

            data_1 = [[str(element) for element in index]for index in data_1]
            print(data_1)
            tabla1.update(values=data_1)
        if i == 1:
            print("data_2: " + str(data_2[0][0]))
            print(data_2)
            if data_2[0][0] == 0:
                data_2 = [data[i]]
            else:
                data_2 = np.concatenate((data_2, [data[i]]))
            data_2 = [[str(element) for element in index]for index in data_2]
            print(data_2)
            tabla2.update(values=data_2)    
        if i == 2:
            print("data_3: " + str(data_3[0][0]))
            print(data_3)
            if data_3[0][0] == 0:
                data_3 = [data[i]]
            else:
                data_3 = np.concatenate((data_3, [data[i]]))
            data_3 = [[str(element) for element in index]for index in data_3]
            print(data_3)
            tabla3.update(values=data_3)
        if i == 3:
            print("data_4: " + str(data_4[0][0]))
            print(data_4)
            if data_4[0][0] == 0:
                data_4 = [data[i]]
            else:
                data_4 = np.concatenate((data_4, [data[i]]))
            data_4 = [[str(element) for element in index]for index in data_4]
            print(data_4)
            tabla4.update(values=data_4)
        if i == 4:
            print("data_5: " + str(data_5[0][0]))
            print(data_5)
            if data_5[0][0] == 0:
                data_5 = [data[i]]
            else:
                data_5 = np.concatenate((data_5, [data[i]]))
            data_5 = [[str(element) for element in index]for index in data_5]
            print(data_5)
            tabla5.update(values=data_5)

        print(str(data[i][0]))


    print(data)
    
    cv.imwrite('RESULT/RES_{}.png'.format(resultCount), image2)
    imgbytes = cv.imencode('.png', image2)[1].tobytes() 
    programWindow['image'].update(data=imgbytes)    
    imgbytes2 = cv.imencode('.png', close)[1].tobytes()   
    programWindow['processed'].update(data=imgbytes2)
    if debug:
        cv.imshow("frame",image2)
        cv.imshow("image",image)
        cv.imshow("gray", gray)
        cv.imshow("sharpen", sharpen)
        cv.imshow("close", close)


main()
