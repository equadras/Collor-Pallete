import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import cv2
import extcolors
from colormap import rgb2hex
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
import shutil
import seaborn as sns



def exact_color(input_image, resize, tolerance, zoom):
    #adiciona o background
    bg = 'bg.png'
    fig, ax = plt.subplots(figsize=(192,108),dpi=10)
    fig.set_facecolor('white')
    plt.savefig(bg)
    plt.close(fig)
    
    #diminuindo imagem
    output_width = resize
    img = Image.open(input_image)
    if img.size[0] >= resize:
        wpercent = (output_width/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((output_width,hsize), Image.ANTIALIAS)
        resize_name = 'resize_'+ input_image
        img.save(resize_name)
    else:
        resize_name = input_image
    
    #cria dataframe
    img_url = resize_name
    colors_x = extcolors.extract_from_path(img_url, tolerance = tolerance, limit = 13)
    df_color = df_cores(colors_x)
    
    #cria o texto
    lista_de_cores = list(df_color['c_code'])
    list_precent = [int(i) for i in list(df_color['occurence'])]
    nome_cores = [c + ' ' + str(round(p*100/sum(list_precent),1)) +'%' for c, p in zip(lista_de_cores, list_precent)]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(160,120), dpi = 10)      

        # adicionar imagem de ref
    img = mpimg.imread(resize_name)
    imagebox = OffsetImage(img, zoom=zoom)
    ab = AnnotationBbox(imagebox, (1, 1))
    ax1.add_artist(ab)
  
        #paleta
    x_posi, y_posi, y_posi2 =  160, -170, -180
    for c in lista_de_cores:
        if lista_de_cores.index(c) <= 5:
            y_posi += 180
            rect = patches.Rectangle((x_posi, y_posi), 360, 160, facecolor = c)
            ax2.add_patch(rect)
            ax2.text(x = x_posi+400, y = y_posi+100, s = c, fontdict={'fontsize': 130})
        else:
            y_posi2 += 180
            rect = patches.Rectangle((x_posi + 1000, y_posi2), 360, 160, facecolor = c)
            ax2.add_artist(rect)
            ax2.text(x = x_posi+1400, y = y_posi2+100, s = c, fontdict={'fontsize': 130})

        #grafico de pizza
    pizza = ax1.pie(list_precent, labels= nome_cores, labeldistance= 0.80, colors = lista_de_cores,textprops={'fontsize': 100, 'color':'black'})
    plt.setp(pizza, width=0.3)

    fig.set_facecolor('white')
    ax2.axis('off')
    bg = plt.imread('bg.png')
    plt.imshow(bg)       
    plt.tight_layout()
    return plt.show()

def df_cores(input):
    cor_list_temp = str(input).replace('([(','').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in cor_list_temp]
    df_percent = [i.split('), ')[1].replace(')','') for i in cor_list_temp]
    
    #converte RGB to HEX code
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(","")),
                          int(i.split(", ")[1]),
                          int(i.split(", ")[2].replace(")",""))) for i in df_rgb]
    
    df = pd.DataFrame(zip(df_color_up, df_percent), columns = ['c_code','occurence'])
    return df



#abrindo o arquivo
janela_padrao = Tk().withdraw()
caminho_do_arquivo = askopenfilename(filetypes = (("Arquivos de jpg", "*.jpg"), ("Arquivos jpeg", "*.jpeg"), ("Arquivos png", "*.png")))
nome_do_arquivo = os.path.basename(caminho_do_arquivo)
#print("\n\n\nO CAMINHO DO ARQUIVO E", caminho_do_arquivo)

#verificando se ja existe na pasta
arquivo = "C:/Users/emanu/Documents/Projetos/Collor-Pallete/" + nome_do_arquivo 
if os.path.isfile(arquivo):
    print('O caminho {} existe'.format(arquivo))
else:
    shutil.move(caminho_do_arquivo, "C:/Users/emanu/Documents/Projetos/Collor-Pallete/" )
    print("\n\n\nO CAMINHO DO ARQUIVO E", caminho_do_arquivo)

colors_x = extcolors.extract_from_path(nome_do_arquivo, tolerance = 20, limit = 18)
colors_x

exact_color(nome_do_arquivo, 720, 10, 1)
