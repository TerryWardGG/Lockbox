import os
import shutil


def startup():
    folder_path = str(os.getcwd())+'/userdata'
    file_path = str(os.getcwd())+'/userdata/settings.dat'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        settingsdat = open(file_path, 'w')
        settingsdat.write('allowdeletedata = False')
        settingsdat.close()
        return ['allowdeletedata = False']
    else:
        files = []
        directory ='userdata'
        files += os.listdir(directory)
        if 'settings.dat' in files:
            settingsdat = open(file_path, 'r')
            settings = settingsdat.read()
            if settings == 'allowdeletedata = False':
                return ['allowdeletedata = False']
            elif settings == 'allowdeletedata = True':
                return ['allowdeletedata = True']
        else:
            settingsdat = open(file_path, 'w')
            settingsdat.write('allowdeletedata = False')
            settingsdat.close()
            return ['allowdeletedata = False']


def deleteuserdata():
    folder_path = str(os.getcwd())+'/userdata'
    shutil.rmtree(folder_path)
    startup()

def writenewdat(namefile, data):
    folder_path = str(os.getcwd())+'/userdata'
    file_path = folder_path +'/'+ namefile
    newdata = open(file_path, 'w')
    newdata.write(data)
    newdata.close()

def finddatr(nameoffile):
    files = []
    directory ='userdata'
    files += os.listdir(directory)
    if nameoffile in files:
        file_path = str(os.getcwd())+'/userdata/'+ nameoffile
        userdata = open(file_path, 'r')
        userdata = userdata.read()
        return userdata
    else:
        return False
    

def updatesettingsstart():
    folder_path = str(os.getcwd())+'/userdata'
    file_path = str(os.getcwd())+'/userdata/settings.dat'
    settingsdata = open(file_path, 'r').readline()
    if settingsdata == 'allowdeletedata = False':
        #settingsdata.close()
        settingsdat = open(file_path, 'w')
        settingsdat.write('allowdeletedata = True')
        settingsdat.close()
    elif settingsdata == 'allowdeletedata = True':
        #settingsdata.close()
        settingsdat = open(file_path, 'w')
        settingsdat.write('allowdeletedata = False')
        settingsdat.close()


def deletethisuserdata(data):
    folder_path = str(os.getcwd())+'/userdata/'+ data
    os.remove(folder_path)

def checkifadminexist():
    files = []
    directory ='userdata'
    files += os.listdir(directory)
    if len(files) >1:
        out = False
    else:
        out = True
    return out

def updateuserdata(namefile, data):
    folder_path = str(os.getcwd())+'/userdata'
    file_path = folder_path +'/'+ namefile
    newdata = open(file_path, 'w')
    newdata.write(data)
    newdata.close()