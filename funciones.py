import pygame
def recortar(img,l,h):
    '''Funcion que recorta cada elemento de una imagen horizontalmente'''
    #l: lenght, h: heigh, img: la imagen
    info = img.get_rect()
    mt=[]
    j=0
    while(j < info[3]):
        ls=[]
        i=0
        while(i < info[2]):
            cuadro=img.subsurface(i,j,l,h)
            ls.append(cuadro)
            i+=l
        mt.append(ls)
        j+=h
    return mt

def recortar2(img,l,h):
    '''Funcion que recorta cada elemento de una imagen verticalmente'''
    #l: lenght, h: heigh, img: la imagen
    info = img.get_rect()
    mt=[]
    j=0
    while(j < info[2]):
        ls=[]
        i=0
        while(i < info[3]):
            cuadro=img.subsurface(j,i,l,h)
            ls.append(cuadro)
            i+=h
        mt.append(ls)
        j+=l
    return mt

def recortarLista(imgList,cantList):
    mt=[]
    for j in range(len(imgList)):
        info = imgList[j].get_rect()
        l = int(info[2]/cantList[j])
        h = int(info[3])
        i=0
        ls=[]
        while(i < cantList[j]):
            cuadro=imgList[j].subsurface(i*l,0,l,h)
            ls.append(cuadro)
            i+=1
        mt.append(ls)
    return mt

def flatten(mat):
    a=[]
    for row in mat:
        for e in row:
            a.append(e)
    return a

def spriteFlip(asset):
    if(isinstance(asset[0],list)):
        return leftMat(asset)
    else:
        return left(asset)

def left(norm): ########################
    #flip sprite to left
    left = []
    for e in norm:
        left.append(pygame.transform.flip(e,True,False))
    return left
def leftMat(norm): ########################
    #flip sprite to left
    left = []
    for row in norm:
        ls=[]
        for e in row:
            ls.append(pygame.transform.flip(e,True,False))
        left.append(ls)
    return left
