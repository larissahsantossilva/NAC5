import cv2
import os, sys, os.path
import numpy as np

#azul
image_lower_hsv1 = np.array([70, 50, 100])
image_upper_hsv1 = np.array([100, 255, 255])

#vermelho
image_lower_hsv2 = np.array([0, 130, 190])
image_upper_hsv2 = np.array([15, 255, 255])


def filtro_de_cor(img_bgr, low_hsv, high_hsv):
    img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img, low_hsv, high_hsv)
    return mask

#retorna 2 masks
def mascara_or(mask1, mask2):
    """ retorna a mascara or"""
    mask = cv2.bitwise_or(mask1, mask2)
    return mask



def desenha_cruz(img, cX, cY, size, color):
    """ faz a cruz no ponto cx cy"""
    cv2.line(img, (cX - size, cY), (cX + size, cY), color, 5)
    cv2.line(img, (cX, cY - size), (cX, cY + size), color, 5)


def escreve_texto(img, text, origem, color):
    """ faz a cruz no ponto cx cy"""
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, str(text), origem, font, 1, color, 2, cv2.LINE_AA)

def image_da_webcam(img):
    mask_hsv1 = filtro_de_cor(img, image_lower_hsv1, image_upper_hsv1)
    mask_hsv2 = filtro_de_cor(img, image_lower_hsv2, image_upper_hsv2)

    mask_hsv = mascara_or(mask_hsv1, mask_hsv2)

    contornos, _ = cv2.findContours(mask_hsv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    mask_rgb = cv2.cvtColor(mask_hsv, cv2.COLOR_GRAY2RGB)
    contornos_img = mask_rgb.copy()

    maior1 = None
    maior2 = None
    maior3 = None
    maior4 = None

    lista = []


    for c in contornos:
        area = int(cv2.contourArea(c))
        lista.append(area)
    lista.sort(reverse=True)

    print(lista)

    for d in contornos:
        area = int(cv2.contourArea(d))
        if lista[0] == area:
            maior1 = d
        elif lista[1] == area:
            maior2 = d
        elif lista[2] == area:
            maior3 = d
        elif lista[3] == area:
            maior4 = d
            

    M1 = cv2.moments(maior1)
    M2 = cv2.moments(maior2)
    M3 = cv2.moments(maior3)
    M4 = cv2.moments(maior4)

    # Verifica se existe alguma para calcular, se sim calcula e exibe no display
    if M1["m00"] != 0 and M2["m00"] != 0 and M3["m00"] and M4["m00"]:
        cX1 = int(M1["m10"] / M1["m00"])
        cY1 = int(M1["m01"] / M1["m00"])
        cX2 = int(M2["m10"] / M2["m00"])
        cY2 = int(M2["m01"] / M2["m00"])

        cv2.drawContours(contornos_img, [maior1], -1, [11, 11, 117], thickness=cv2.FILLED)
        cv2.drawContours(contornos_img, [maior2], -1, [208, 226, 79], thickness=cv2.FILLED)
        cv2.drawContours(contornos_img, [maior3], -1, [0, 0, 0], thickness=cv2.FILLED)
        cv2.drawContours(contornos_img, [maior4], -1, [0, 0, 0], thickness=cv2.FILLED)
    
        #faz a cruz no centro de massa
        desenha_cruz(contornos_img, cX1, cY1, 20, (11, 11, 177))
        desenha_cruz(contornos_img, cX2, cY2, 20, (208, 226, 79))

        # Para escrever vamos definir uma fonte
        texto1 = cY1, cX1
        origem1 = (cY1+80, cX1-150)

        texto2 = cY2, cX2
        origem2 = (cY2+80, cX2-150)

        escreve_texto(contornos_img, texto1, origem1, (11, 11, 177))
        escreve_texto(contornos_img, texto2, origem2, (208, 226, 79))

        coord1 = (cX1, cY1)
        coord2 = (cX2, cY2)
        cv2.line(contornos_img, coord1, coord2, (0, 255, 0), 4)

    else:
    # nao tem o que exibir
        cX1, cY2 = 0, 0
        texto = 'Nao exibe'
        origem = (0, 50)
        escreve_texto(contornos_img, texto, origem, (0, 0, 255))

    return contornos_img


cv2.namedWindow("preview")
# define a entrada de video para webcam
vc = cv2.VideoCapture(0)


#configura o tamanho da janela 
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if vc.isOpened():  
    rval, frame = vc.read()
else:
    rval = False

while rval:

    
    img = image_da_webcam(frame) 

    cv2.imshow("preview", img)
    cv2.imshow("original", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: 
        break

cv2.destroyWindow("preview")
vc.release()
