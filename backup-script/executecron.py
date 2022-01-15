'''
Script per il caricamento automatico di una copia della cartella immagine
salvataggio eventi in log.txt e elementi salvati record.txt (contiente il nome dei file per il controllo)
'''

import datetime
import os
import re
from ftplib import FTP, FTP_TLS
import unicodedata
import numpy as np
import config

# from django.conf import settings as st
# st.configure() #env configurazione

# percorso assoluto per la memorizzazione dei log
# abspath = 'repo/'
abspath = '/home/acqui/log/cron/'
# percorso salvataggio dati su FTP
backup_folder = 'www.titansolution.it/backup-biennale/Archivio'
# processed = "repo/processed"
processed = "processed"
#percorso base locale server di partenza
base_path='/home/acqui/'

#cartelle remote salvataggio
remotefold_images="immagini/"
remotefold_database="DB/"

#credenziali per l'accesso FTP
rl = config.rl


def lg(log, c='', m=''):
    """
    Funzione per la stampa dei log con time stamp
    :param log: file handler
    :param c: line header
    :param m: text message
    :return:
    """
    log.write('\n%s\t [%s] - %s' % (str(c), str(datetime.datetime.now()), str(m)))


def linkFtp(folder=''):
    """
    Handlser FTP per il caricamento dei dati su server remoto
    :param folder: sotto cartella di salvataggio remota
    :return: handler per la gestione
    """
    # ftp = FTP_TLS()
    ftp = FTP_TLS(host=rl['host'])
    ftp.set_debuglevel(2)
    status = ftp.login(user=rl['username'], passwd=rl['password'])

    # comando per il cambio della directory di upload
    ftp.cwd(backup_folder+'/'+folder)
    # print the content of directory
    print(ftp.dir())
    return ftp, status


def get_db_to_upload(locpath=""):
    """
    Estrazione file contenenti dati del database
    :param locpath: percorso dove trovare i file
    :return: elenco dei file presenti
    """
    # se non viene scelto un percorso specifico viene dato quello del server locale
    if locpath=="":
        locpath = base_path+"local_db"

    # Formati accettati json e sqlite3
    rx = re.compile(r'\.(json|sqlite3)')
    r = []

    # Effettua la ricerca nelle sotto cartelle
    for path, dnames, fnames in os.walk(locpath):
        r.extend([os.path.join(path, x) for x in fnames if rx.search(x)])

    print(r)
    return r


def get_file_to_upload(locpath="",locpathnp=""):
    # se non viene scelto un percorso specifico viene dato quello del server locale
    if locpath=="":
        locpath = base_path+"media"

    if locpathnp=="":
        locpathnp = base_path+"log/cron/"

    # file elenco storico file caricati
    npfile=locpathnp+processed+'.npy'

    print('\n -- Caricamento file storico')
    # try:
    #     pr = np.load(npfile)
    # except:
    #     pr = np.array([])

    # elenco file ammessi
    rx = re.compile(r'\.(jpg|png|psd|tiff|svg|jpeg)')
    r = []

    # Effettua la ricerca nelle sotto cartelle
    for path, dnames, fnames in os.walk(locpath):
        r.extend([os.path.join(path, x) for x in fnames if rx.search(x)])


    # r = np.array(r)
    print(r)
    # ex_data = np.setdiff1d(r, pr)

    print('---------\n\n\n---------\n')
    # print(ex_data)
    # np.extact(pr, ex_data)  # aggiunge i nuovi file
    # np.save(npfile, pr)  # salva il file con i nomi dei files

    # return ex_data
    print('\n -- File da mandare in backup  %d'%(len(r)))
    return r

def to_FTP(f, ftp, log,folder_name=""):
    # legge il file da caricare
    fp = open(f, 'rb')
    # carica il file via ftp
    ftp, status = linkFtp(folder=folder_name)

    #clean file name

    f=re.sub(r'[\\/*?:"<>|];',"",f)
    print('\n\n\ENCODE\n....----\n'+str(f))
    f=unicodedata.normalize("NFKD",f)
    f=f.encode('latin-1', errors="ignore")

    print('\n\n\ENCODE\n....----\n'+str(f))

    res = ftp.storbinary('STOR %s' % os.path.basename(f), fp, 25600)
    ftp.close()

    # mette il log del file caricato
    lg(log, 'cpf', '%s,%s' % (str(f), str(res)))


def addprocessed(r):
    fp = open(abspath+processed + '.txt', 'a+')
    fp.write('%s, %s\n' % (str(r), str(datetime.datetime.now())))

# Change directories - create if it doesn't exist
def chdir(dir):
    ftp, status = linkFtp()
    if directory_exists(dir) is False: # (or negate, whatever you prefer for readability)
        ftp.mkd(dir)
    ftp.cwd(dir)
    return ftp,dir

# Check if directory exists (in current location)
def directory_exists(dir):
    ftp, status = linkFtp()
    filelist = []
    ftp.retrlines('LIST',filelist.append)
    for f in filelist:
        if f.split()[-1] == dir and f.upper().startswith('D'):
            return True
    return False

def storeRemoteFtp(path=abspath):

    print("Cronjob executed still uploading")
    log = open(path + 'log.txt', 'a+')
    lg(log, 'sss', 'Start cronjob')
    ftp, status = linkFtp()
    lg(log, '--', status)

    #Create folder backup con l'oraraio di creazione
    data=datetime.date
    folder_name=str(data.today())+"-"+str(datetime.time())


    """ CARICAMENTO DATABASE """
    print('*'*5+'\nCARICAMENTO DATABASE')
    # Creazione cartella salvataggio e ritorno handler per operazioni  e nome cartella salvataggio
    ftp, rfolder=chdir(remotefold_database+folder_name)
    lg(log, 'FFF', 'Caricamento DATABASE')

    # legge i databse da caricare nella cartella media
    db = get_db_to_upload()

    #ciclo invio dati via FTP
    for f in db:
        to_FTP(f, ftp, log,rfolder)

    #Chiusura handlser FTP
    ftp.close()

    """ CARICAMENTO IMMAGINI """
    print('*'*5+'\nCARICAMENTO IMMAGINI')
    # Creazione cartella salvataggio e ritorno handler per operazioni  e nome cartella salvataggio
    ftp, rfolder=chdir(remotefold_images+folder_name)

    lg(log, 'FFF', 'Caricamento FILES')

    # legge i file da caricare nella cartella media
    files = get_file_to_upload()

    for f in files:
        to_FTP(f, ftp, log,rfolder)
        addprocessed(f)  # salva il file nel record dei caricati, solo per le immagini

    lg(log, 'xxx', 'End cronjob')
    ftp.close()
    pass


storeRemoteFtp('')


