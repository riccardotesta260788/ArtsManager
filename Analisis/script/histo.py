'''
Script per la generazione dell'elenco dei colori predominanti
https://www.youtube.com/watch?v=guWxEIqYy_I
'''

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os
import webcolors
from datetime import datetime
import os.path
import json
from json import JSONEncoder
from PIL import ImageColor, Image

PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))
DEF_PATH = PROJECT_ROOT
COLOR_DENSITY = 64


class ColorExtract:
    number_of_colors = 128
    height = 200
    width = 200
    hex_colors = []
    rgb_colors = []
    normalize = []
    c_density = []
    l_color = []

    def __init__(self):
        print("ColorExtract initialized")

    def RGB_id(self, p):
        r = sum([k * (255 ** id) for id, k in enumerate(p)])
        return r

    def closest_color_rgb(self, rgb):
        ti = datetime.now()
        differences = {}
        for color_hex, color_name in webcolors.CSS3_HEX_TO_NAMES.items():
            r, g, b = webcolors.hex_to_rgb(color_hex)
            fr, fg, fb, = rgb
            # sq=sum([
            #         (r-fr)**2,
            #         (g-fg)**2,
            #         (b-fb)**2,
            #         (r-fr)**2*(r-fg)*(r-fb),
            #         (g-fr)**2*(g-fg)*(g-fb),
            #         (b-fr)**2*(b-fg)*(b-fb),
            #         (r-fr)*(r-fg)**2*(r-fb),
            #         (g-fr)*(g-fg)**2*(g-fb),
            #         (b-fr)*(b-fg)**2*(b-fb),
            #         (r-fr)*(r-fg)*(r-fb)**2,
            #         (g-fr)*(g-fg)*(g-fb)**2,
            #         (b-fr)*(b-fg)*(b-fb)**2,
            #         ]
            #        )
            sq = (self.RGB_id([r, g, b]) - self.RGB_id([r, g, b])) ** 2
            differences[sq] = color_name

        # print ("Execution {}".format(datetime.now() - ti))
        # print ("Sosrted {}".format(differences[min(differences.keys())]))

        return differences[min(differences.keys())]

    def RGB2HEX(self, color):
        r, g, b = int(color[0]), int(color[1]), int(color[2])
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def get_image(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def get_col_density(self, image):
        density = {}
        sd = 1
        for p in image:
            # quantizzazione livelli più significativi
            # p[0], p[1], p[2]=int(p[0]/sd)*sd,int(p[1]/sd)*sd,int(p[2]/sd)*sd
            n = self.RGB2HEX(p)
            if (n in density.keys()):
                density[n] = density[n] + 1
            else:
                density[n] = 1

        print(list(sorted(density.items(), key=lambda item: item[1]))[:-10])
        print(len(density))
        return sorted(density.items(), key=lambda item: item[1])

    def extract_old(self, path):

        # Lettura immagine
        image = cv2.imread(path)
        print("\n\n-----\n Immagine:{}\n\n-------\n".format(path))
        # print("The type of this input is {}".format(type(image)))
        # print("Shape: {}".format(image.shape))

        # Ridimesionamento della superficie
        w, h = self.width, self.height
        #
        modified_image = cv2.resize(image, (w, h), interpolation=cv2.INTER_AREA)
        modified_image = modified_image.reshape(modified_image.shape[0] * modified_image.shape[1], 3)

        # Creazione modello cluster dei colori
        clf = KMeans(n_clusters=self.number_of_colors, n_init=2, random_state=10, max_iter=10)

        # Addestramento con immagine estrazione elenco etichette
        labels = clf.fit_predict(modified_image)
        counts = Counter(labels)
        center_colors = clf.cluster_centers_

        # print ("Cluster:\n {} \n------\n".format(center_colors))
        # Ordine precedenza colori
        ordered_colors = [center_colors[i] for i in counts.keys()]
        # Codifica in esadecimale
        self.hex_colors = hex_colors = [self.RGB2HEX(ordered_colors[i]) for i in counts.keys()]
        self.rgb_colors = rgb_colors = [ordered_colors[i] for i in counts.keys()]

        # print ("HEX color:\n {}\n----\n".format(hex_colors))
        # print ("RGB color:\n {}\n----\n".format(rgb_colors))
        somma_counts = self.height * self.width

        # Domalizzato valori in percentuale 100%
        self.normalize = normalize = {hex_colors[key]: round(counts[key] / somma_counts * 100, 2) for key in counts}

        # print (normalize)

        # plt.figure(figsize = (8, 6))
        # plt.pie(counts.values(), labels = hex_colors, colors = hex_colors)
        #
        # plt.show()

    def extract(self, path):

        # Lettura immagine
        image = cv2.imread(path)
        print("\n\n-----\n Immagine:{}\n\n-------\n".format(path))
        # print("The type of this input is {}".format(type(image)))
        # print("Shape: {}".format(image.shape))

        # Ridimesionamento della superfi
        w, h = self.width, self.height
        #
        modified_image = cv2.resize(image, (w, h), interpolation=cv2.INTER_AREA)
        modified_image = modified_image.reshape(modified_image.shape[0] * modified_image.shape[1], 3)

        # Colori maggiormente presenti
        self.c_density = self.get_col_density(modified_image)
        ordered_colors = self.c_density

        # Codifica in esadecimale
        self.hex_colors = [i[0] for i in ordered_colors]
        self.rgb_colors = [ImageColor.getrgb(i[0]) for i in ordered_colors]

        somma_counts = self.height * self.width

        # Domalizzato valori in percentuale 100%
        self.normalize = {i[0]: round(i[1] / somma_counts * 100, 2) for i in ordered_colors}

        # print (normalize)

    def get_colorspace(self, mainpath):
        # print ("\n\n-----\n ColorSpaceImage:{}\n\n-------\n".format(mainpath))
        self.extract_old(DEF_PATH + mainpath)
        self.l_color = l_color = {}

        # ti=datetime.now()
        for rgb in self.rgb_colors:
            try:
                cname = webcolors.rgb_to_name(rgb)
            except ValueError:
                cname = self.closest_color_rgb(rgb)
            # print ("Color {} -> {}".format(rgb,cname))

            if (cname not in l_color.keys()):
                l_color[cname] = 1
            else:
                l_color[cname] += 1
        # print ("\n Esecuzione totale: {}s".format(datetime.now() - ti))
        # print ("Colori associati {}".format(l_color))

        self.l_color = l_color
        return l_color

    def get_colorspace_base(self, mainpath):
        self.extract(DEF_PATH + mainpath)
        self.l_color = {key: self.rgb_colors[idx] for idx, key in enumerate(self.hex_colors)}
        print(self.l_color)
        return self.l_color
