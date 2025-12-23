import os, sysconfig, json


class FileCheck:
    filename = "store.json"
    filelist = dict()

    def ListFileLocal(self, path):
        # get file list in path
        for path, subdirs, files in os.walk(path):
            for name in files:
                # full path
                fp = os.path.join(path, name)
                # info file
                info = os.stat(name)

                self.filelist[str(fp)] = [name, info.st_mtime]

        print(self.filelist)
        f = open(self.filename, 'w')
        f.write(json.dumps(self.filelist))
        return True

    def FileCheck(self, path):
        # Carica storico file salvati
        # Crea file per salvataggio
        # Scorri elenco file cartella
        # Controlla nello storico se presente il file
        #     se non predente aggiungi nel file di salvataggio
        #     altrimenti copia i dati di quello salvato
        fr = open(self.filename, 'r')
        stojson = fr.reads()
        sto = json.load(stojson)
        print(sto)

        f = open(self.filename, 'w+')

        for path, subdirs, files in os.walk(path):
            for name in files:
                # full path
                fp = os.path.join(path, name)
                # info file
                info = os.stat(name)

                self.filelist[str(fp)] = [name, info.st_mtime]
                if self.filelist[str(fp)] in dic(sto):
                    print('dosome')


fc = FileCheck()
# fc.ListFileLocal(path='/Users/riccardotesta_1/progetti-sviluppo-codice/Biennale/backup-script')
fc.FileCheck(path='/Users/riccardotesta_1/progetti-sviluppo-codice/Biennale/backup-script')
