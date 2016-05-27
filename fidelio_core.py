"""
This file has written by Burak Topal and Melih Tolga Şahin.
Theese codes are mainframe of "fidelio project".
In theese codes, we used some third party tools like ffmpeg.
This is an open source project and source can be find at github.

"""
import hashlib
import shutil
import subprocess
import os
import threading

import numpy as np
import scipy.io.wavfile

from PIL import Image


class Fidelio(threading.Thread):
    """
    Core of fidelio project.
    Inherited from threading.Thread and this means this class calling as a thread.
    """
    def __init__(self, file_name, uploaded_file_path):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.file_name = file_name
        self.finished = False
        self.samplerate = 0

        self.file_md5_name = self.create_md5('assets/' + file_name)
        # os.mkdir(self.file_md5_name)
        os.makedirs('assets/' + self.file_md5_name)
        self.path = os.path.join(os.path.dirname(__file__), 'assets', self.file_md5_name)

        self.samplerate, self.data = self.convert_to_wav(file_name, uploaded_file_path)

        self.candy_list = []
        self.candy_rainbow_list = []
        self.candy_triple_sort_list = []
        self.candy_reverse_list = []
        self.candy_reverse_dark_list = []
        self.candy_non_sort_list = []
        self.candy_tan_list = []

        self.candy_path = ''
        self.candy_rainbow_path = ''
        self.candy_triple_sort_path = ''
        self.candy_non_sort_path = ''
        self.candy_reverse_path = ''
        self.candy_reverse_dark_path = ''
        self.candy_tan_path = ''
        self.gif_path = ''

    def search(self):
        print('SEARCH BAŞLADI')
        counter = 0

        for row in range(0, 1080):

            y = []
            w = []
            z = []
            q = []

            for col in range(0, 1920):
                y.append([self.data[counter][0], np.sin(self.data[counter][0]), np.cos(self.data[counter][0])])
                z.append(
                    [0 - self.data[counter][0], 0 - np.sin(self.data[counter][0]), 0 - np.cos(self.data[counter][0])])
                w.append([255 - self.data[counter][0], 255 - np.sin(self.data[counter][0]),
                          255 - np.cos(self.data[counter][0])])
                q.append([np.tan(self.data[counter][0]), np.sin(self.data[counter][0]), np.cos(self.data[counter][0])])
                counter += 1

            self.candy_list.append(y)
            self.candy_rainbow_list.append(y)
            self.candy_triple_sort_list.append(y)
            self.candy_non_sort_list.append(y)
            self.candy_reverse_list.append(z)
            self.candy_reverse_dark_list.append(w)
            self.candy_tan_list.append(q)
        print('SEARCH BİTTİ')

    # 1
    def candy(self):

        liste = np.array(self.candy_list)
        liste.sort(axis=0)

        img = Image.fromarray(liste, 'RGB')
        self.candy_path = '/assets/' + self.file_md5_name + '/001.png'
        img.save(self.path + '/001.png')

    # 1
    def candy_rainbow(self):

        liste = np.array(self.candy_rainbow_list)
        liste.sort(axis=0)

        for x in liste:
            x.sort(axis=0)

        img = Image.fromarray(liste, 'RGB')
        self.candy_rainbow_path = '/assets/' + self.file_md5_name + '/002.png'
        img.save(self.path + '/002.png')

    # 1
    def candy_triple_sort(self):

        liste = np.array(self.candy_triple_sort_list)
        liste.sort(axis=0)
        liste = np.sort(liste)

        for z in liste:
            z.argsort(axis=0)

        img = Image.fromarray(liste, 'RGB')
        self.candy_triple_sort_path = '/assets/' + self.file_md5_name + '/003.png'
        img.save(self.path + '/003.png')

    # 1
    def candy_non_sort(self):

        liste = np.array(self.candy_non_sort_list)
        img = Image.fromarray(liste, 'RGB')
        self.candy_non_sort_path = '/assets/' + self.file_md5_name + '/004.png'
        img.save(self.path + '/004.png')

    # 2
    def candy_reverse(self):

        liste = np.array(self.candy_reverse_list)
        liste.sort(axis=0)

        img = Image.fromarray(liste, 'RGB')
        self.candy_reverse_path = '/assets/' + self.file_md5_name + '/005.png'
        img.save(self.path + '/005.png')

    # 3
    def candy_reverse_dark(self):

        liste = np.array(self.candy_reverse_dark_list)
        liste.sort(axis=0)

        img = Image.fromarray(liste, 'RGB')
        self.candy_reverse_dark_path = '/assets/' + self.file_md5_name + '/006.png'
        img.save(self.path + '/006.png')

    # 4
    def candy_tan(self):

        liste = np.array(self.candy_tan_list)
        liste.sort(axis=0)

        img = Image.fromarray(liste, 'RGB')
        self.candy_tan_path = '/assets/' + self.file_md5_name + '/007.png'
        img.save(self.path + '/007.png')

    def make_gif(self):
        a = os.path.join(os.path.dirname('__file__'), 'assets', self.file_md5_name)
        subprocess.call(['ffmpeg', '-framerate', '1/0.5', '-i', '%03d.png', 'output.gif'], cwd=a)
        self.gif_path = a + '/output.gif'

    def create_md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def convert_to_wav(self, file_name, uploaded_file_path):
        path = os.path.join(os.path.dirname(__file__), uploaded_file_path)

        subprocess.call(['ffmpeg', '-i', path + '/' + file_name, '-acodec', 'pcm_u8', '-ar', '44100',
                         self.file_md5_name + '.wav'], cwd=self.path)

        new_path = os.path.join(os.path.dirname(__file__), 'assets', self.file_md5_name, self.file_md5_name + '.wav')

        samplerate, data = scipy.io.wavfile.read(new_path)
        self.samplerate = samplerate
        os.remove(new_path)

        return samplerate, data

    def get_images(self):
        images = [self.candy_path,
                  self.candy_rainbow_path,
                  self.candy_triple_sort_path,
                  self.candy_non_sort_path,
                  self.candy_reverse_path,
                  self.candy_reverse_dark_path,
                  self.candy_tan_path]
        return images

    def run(self):
        print('FİDELİO RUN')
        self.search()
        self.candy()
        self.candy_tan()
        self.candy_rainbow()
        self.candy_triple_sort()
        self.candy_reverse()
        self.candy_reverse_dark()
        self.candy_non_sort()
        self.make_gif()
        self.finished = True
