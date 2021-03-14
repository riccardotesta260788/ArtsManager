import os
import shutil
from PIL import Image
import PIL.TiffImagePlugin as tiff

class ImageRename:
    def menu(self):
        print("\n---MENU----")
        print("1 - Remove fixed text from filename")
        print("2 - Compress image in folder")
    def __init__(self):

        self.menu()

    def remove_text_name(self):
        print('*-'*3+'REMOVE TEXT FROM FILE NAME')
        print('Source Folder path')
        s_folder=input()
        d_folder = '/'.join([s_folder, 'processed'])

        #Check if folder exists else create it
        if not os.path.isdir(d_folder):
            print("Folder is not present...")
            os.mkdir(d_folder)
            print("...Folder created - OK ")


        for root,dirs, files in os.walk(s_folder):
            for file in files:
                #Remove "Copia di " from file name

                new_name=file[9:]
                print('/'.join([root,file]))
                shutil.copy('/'.join([root,file]),'/'.join([d_folder,new_name]))
        return True

    def compress_images(self):
        print('*-'*3+'COMPRESS IMAGE FILE TYPE')
        print('Source Folder path')
        s_folder = input()
        d_folder = '/'.join([s_folder, 'compressed'])

        # Check if folder exists else create it
        if not os.path.isdir(d_folder):
            print("Folder is not present...")
            os.mkdir(d_folder)
            print("...Folder created - OK ")

        cicle=0
        for root,dirs, files in os.walk(s_folder):
            for file in files:
                print('-- Opening file: '+file)
                if not file.startswith('.'):

                    #Remove "Copia di " from file name
                    im_path='/'.join([root,file])
                    im_dest='/'.join([d_folder,file])
                    print(im_path)

                    im=Image.open(im_path)
                    im.save(im_dest, dpi=(400,400),compression='jpeg', Q=100)

                    cicle=cicle+1
        print('Terminato!')
        return True



if __name__=="__main__":
    print('\n'.join(['*'*10,'''Welcome in image utility written by Riccardo Testa - 2020''','*'*10]))
    im = ImageRename()
    command=input()

    while command!="quit":
        if command == 'help' or command=='menu':
            im.menu()
        if command =="1":
            im.remove_text_name()
        if command == "2":
            im.compress_images()

        command = input()