import flet as ft
import encryption as encryption
import datacontroller as datacontrol
import json
import copy

import secrets
import string
from random import randrange

#parttimesettings
firstlogin = False
lastsearch = None
opentextnamen = '@LockBox@-New-Text'


#userdatakey
authorized = False
nameofdatafileopen = None
keyofdatafileopen = None
dataofuseropen = None
isuseradmin = False
servicesofpasswords = []
namesoftexts = []

#settings
allowdeletedata = False


#load up
def loadupsettings():
    global allowdeletedata
    settings = datacontrol.startup()
    if 'allowdeletedata = False' in settings:
        allowdeletedata = False
    else:
        allowdeletedata = True

loadupsettings()

#main
def main(page: ft.Page):
    page.title = 'LockBox'
    #page.window.icon = "/logo.ico"
    #page.bgcolor = ft.colors.WHITE
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 350
    page.window.height = 400
    page.window.resizable = False
    page.window.full_screen = False
    page.window.maximizable =False
    page.window.center()
    page.theme_mode = ft.ThemeMode.DARK


    #functions
    def validater(e):
        if all([username_fieldr.value, password_fieldr.value]):
            btn_reg.disabled = False
        else:
            btn_reg.disabled = True
        page.update()
    
    def validatel(e):
        if all([username_fieldl.value, password_fieldl.value]):
            btn_log.disabled = False
        else:
            btn_log.disabled = True
        page.update()


    def reguserdat(e):
        global keyofdatafileopen
        global nameofdatafileopen
        global dataofuseropen
        global authorized
        global isuseradmin
        global firstlogin
        key = str(password_fieldr.value)+str(username_fieldr.value)
        key = encryption.genencryptionkey(key)
        accountname = str(username_fieldr.value)
        nameoffile = str(key)
        nameoffile = (str(encryption.genencryptionkey(nameoffile)) + '.dat').replace('/', '0')
        nameofdatafileopen = nameoffile
        keyofdatafileopen = key
        isadminuser = datacontrol.checkifadminexist()
        isuseradmin = isadminuser
        encryptiondata = {
        "name": accountname,
        "nameoffile": nameoffile,
        "texts":{},
        "passwords":{},
        "isadmin":isadminuser
        }
        dataofuseropen = encryptiondata
        authorized = True
        encryptiondata = json.dumps(encryptiondata)
        encrypteddata = encryption.encryptwithkey(key, encryptiondata)
        datacontrol.writenewdat(nameoffile, encrypteddata)
        firstlogin = True
        mainconsole(page)


    def loaduserdat(e):
        global keyofdatafileopen
        global nameofdatafileopen
        global dataofuseropen
        global authorized
        global isuseradmin
        global servicesofpasswords
        global namesoftexts
        key = str(password_fieldl.value)+str(username_fieldl.value)
        key = encryption.genencryptionkey(key)
        nameoffile = str(key)
        nameoffile = (str(encryption.genencryptionkey(nameoffile)) + '.dat').replace('/', '0')
        dataoffile = datacontrol.finddatr(nameoffile)
        if dataoffile == False:
            page.open(ft.SnackBar(ft.Text('Password or login is incorrect')))
        else:
            decrypteddata = encryption.decryptwithkey(key, dataoffile)
            decrypteddata = json.loads(decrypteddata)
            keyofdatafileopen = key
            nameofdatafileopen = nameoffile
            dataofuseropen = decrypteddata
            isuseradmin = dataofuseropen['isadmin']
            authorized = True
            if dataofuseropen['passwords'] == {}:
                pass
            else:
                servicesofpasswords = dataofuseropen['passwords'].keys()
                servicesofpasswords = list(servicesofpasswords)
            if dataofuseropen['texts'] == {}:
                pass
            else:
                namesoftexts = dataofuseropen['texts'].keys()
                namesoftexts = list(namesoftexts)
            mainconsole(page)

        

    def deleteuserdat(e):
        global allowdeletedata
        if allowdeletedata == False:
            page.close(infoonlogin)
            page.open(cannotdeleteuserdat)
        else:
            datacontrol.deleteuserdata()
            allowdeletedata = False
            page.open(userdatadeletets)

    def switchpagetl(e):
        page.clean()
        page.add(loginpage)

    def switchpagetr(e):
        page.clean()
        page.add(registerpage)


    def closeinfoonreg(e):
        page.close(infoonreg)

    def closeinfooflogin(e):
        page.close(infoonlogin)

    def closecannotdeletedata(e):
        page.close(cannotdeleteuserdat)

    def closeuserdatadel(e):
        page.close(userdatadeletets)

    #buttons and fields
    backgroundph = ft.Image(src_base64="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",width= 300)

    username_fieldl = ft.TextField(label="Username", width=300,on_change=validatel)
    password_fieldl = ft.TextField(label="Password", password=True, width=300,on_change=validatel)
    btn_log = ft.OutlinedButton(text='Log in',width=300, on_click=loaduserdat, disabled=True)


    username_fieldr = ft.TextField(label="Username", width=300,on_change=validater)
    password_fieldr = ft.TextField(label="Password", password=True, width=300,on_change=validater, can_reveal_password=True)
    btn_reg = ft.OutlinedButton(text='Create',width=300, on_click=reguserdat, disabled=True)


    swichlogin = ft.TextButton(text="Log in?", icon="LOGIN_ROUNDED", on_click=switchpagetl)
    swichreg = ft.TextButton(text="Create?", icon="KEY_ROUNDED",on_click=switchpagetr)

    infoonreg_btn = ft.TextButton("About account",icon="INFO_OUTLINE_ROUNDED", on_click=lambda e: page.open(infoonreg))
    infoonlogin_btn = ft.TextButton("Delete data",icon="KEY_OFF", on_click=lambda e: page.open(infoonlogin))

    

    infoonreg = ft.AlertDialog(
        modal=True,
        title=ft.Text("About registration"),
        content=ft.Text("We don't store, read, shere, collect any of your data. Your data store locally on your device under full encryption. This account creates only locally. If you lose your password or login we cannot restore it."),
        actions=[
            ft.TextButton("Ok", on_click=closeinfoonreg),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        )

    infoonlogin = ft.AlertDialog(
        modal=True,
        title=ft.Text("Do you want to delete all data?"),
        content=ft.Text("If you lost password or login we cannot restore it. You only can delete all your data from all accounts and create a new account. Do you want to delete all data?"),
        actions=[
            ft.TextButton("Yes",style=ft.ButtonStyle(color=ft.Colors.RED), on_click=deleteuserdat),
            ft.TextButton("No", on_click=closeinfooflogin),
        ],actions_alignment=ft.MainAxisAlignment.END)

    cannotdeleteuserdat = ft.AlertDialog(
        modal=True,
        title=ft.Text("We cannot delete user data"),
        content=ft.Text("We cannot delete user data because there no user data or user disallow us to delete data"),
        actions=[
            ft.TextButton("Ok", on_click=closecannotdeletedata),
        ],actions_alignment=ft.MainAxisAlignment.CENTER)

    userdatadeletets = ft.AlertDialog(
        modal=True,
        title=ft.Text("All data successfully deleted"),
        content=ft.Text("Now you can create a new account and setup new settings."),
        actions=[
            ft.TextButton("Ok", on_click=closeuserdatadel),
        ],actions_alignment=ft.MainAxisAlignment.CENTER)



    #page
    loginpage = ft.Row(
            [   
                ft.Column([backgroundph,username_fieldl,password_fieldl,btn_log,ft.Row([swichreg,infoonlogin_btn])]),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    
    registerpage = ft.Row(
            [   
                ft.Column([backgroundph,username_fieldr,password_fieldr,btn_reg,ft.Row([swichlogin,infoonreg_btn])]),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )   


    page.add(loginpage)



def mainconsole(page: ft.Page):
    page.title = 'LockBox'
    #page.bgcolor = ft.colors.WHITE
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 1000
    page.window.height = 600
    page.window.resizable = False
    page.window.maximizable =False
    page.theme_mode = ft.ThemeMode.DARK
    #page.window.min_width= 600
    #page.window.min_height = 500
    page.window.center()
    page.clean()
    #globalsettings
    

    #functions
    def logoutapp():
        page.window.close()


    def railnavig(e):
        if e == 0:
            page.clean()
            page.floating_action_button = None
            page.add(homepageconsole)
        elif e == 1:
            page.clean()
            page.add(textconsole)
            page.floating_action_button = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=openandedittext, bgcolor=ft.Colors.BLUE_800, height= 60, width=60)
            textpageopenlist()
        elif e == 2:
            page.clean()
            page.floating_action_button = None
            page.add(passwordconsole)
            passwordpageopenlist()
        elif e == 3:
            page.clean()
            page.floating_action_button = None
            page.add(settingsconsole)
        elif e == 4:
            logoutapp()


    def openandedittext(e):
        global opentextnamen
        if type(e) == ft.ControlEvent:
            opentextnamen = '@LockBox@-New-Text'
        else:
            opentextnamen = e.value
        def closedialtext(e):
            page.close(textopen)
        def dletedialtext(e):
            del dataofuseropen['texts'][nametext.value]
            userdataupdated = copy.deepcopy(dataofuseropen)
            userdataupdated = json.dumps(userdataupdated)
            userdataupdated = encryption.encryptwithkey(keyofdatafileopen, userdataupdated)
            datacontrol.updateuserdata(nameofdatafileopen,userdataupdated)
            namesoftexts.remove(nametext.value)
            page.close(textopen)
            textpageopenlist()
            if lastsearch != None:
                textboxsearch_changed(lastsearch)
                page.update()
        def editpressdial(e):
            nametext.read_only = False
            textfielddial.read_only = False
            closedialbtn.disabled = True
            editdialbtn.icon = ft.Icons.SAVE
            editdialbtn.on_click = saveedittext
            deletedialbtn.icon = ft.Icons.CANCEL
            deletedialbtn.on_click = closedialtext
            page.update()
        def exitfromeditmodetext():
            nametext.read_only = True
            textfielddial.read_only = True
            closedialbtn.disabled = False
            editdialbtn.icon = ft.Icons.MODE_EDIT
            editdialbtn.on_click = editpressdial
            deletedialbtn.icon = ft.Icons.DELETE
            deletedialbtn.on_click = dletedialtext
            page.update()
        def saveedittext(e):
            global dataofuseropen
            global namesoftexts
            global opentextnamen
            userdataupdated = dataofuseropen
            if opentextnamen == '@LockBox@-New-Text' and nametext.value in namesoftexts or nametext.value in servicesofpasswords:
                page.open(ft.SnackBar(ft.Text("This name of text allready exist")))
            elif nametext.value == '':
                page.open(ft.SnackBar(ft.Text("Type name of text")))
            elif textfielddial.value == '':
                page.open(ft.SnackBar(ft.Text("Type something in text field")))
            elif textfielddial.value != '' and nametext.value != '' and opentextnamen == '@LockBox@-New-Text' and not nametext.value in namesoftexts and not nametext.value in servicesofpasswords:
                userdataupdated['texts'][nametext.value] = textfielddial.value
                dataofuseropen = userdataupdated
                opentextnamen = nametext.value
                userdataupdated = json.dumps(userdataupdated)
                userdataupdated = encryption.encryptwithkey(keyofdatafileopen, userdataupdated)
                datacontrol.updateuserdata(nameofdatafileopen,userdataupdated)
                namesoftexts.append(nametext.value)
                exitfromeditmodetext()
                textpageopenlist()
            elif textfielddial.value != '' and nametext.value != '' and opentextnamen != '@LockBox@-New-Text':
                if nametext.value == opentextnamen:
                    userdataupdated['texts'][nametext.value] = textfielddial.value
                    dataofuseropen = userdataupdated
                    userdataupdated = json.dumps(userdataupdated)
                    userdataupdated = encryption.encryptwithkey(keyofdatafileopen, userdataupdated)
                    datacontrol.updateuserdata(nameofdatafileopen,userdataupdated)
                    exitfromeditmodetext()
                    textpageopenlist()
                elif nametext.value != opentextnamen and not nametext.value in namesoftexts:
                    namesoftexts.remove(opentextnamen)
                    del userdataupdated['texts'][opentextnamen]
                    opentextnamen = nametext.value
                    userdataupdated['texts'][nametext.value] = textfielddial.value
                    dataofuseropen = userdataupdated
                    userdataupdated = json.dumps(userdataupdated)
                    userdataupdated = encryption.encryptwithkey(keyofdatafileopen, userdataupdated)
                    datacontrol.updateuserdata(nameofdatafileopen,userdataupdated)
                    namesoftexts.append(nametext.value)
                    exitfromeditmodetext()
                    textpageopenlist()
                elif nametext.value != opentextnamen and nametext.value in namesoftexts or nametext.value in servicesofpasswords:
                    page.open(ft.SnackBar(ft.Text("This name of text allready exist")))
        nameoftextvalue = ''
        textfielddialvalue = ''
        if opentextnamen != '@LockBox@-New-Text':
            nameoftextvalue = e.value
            textfielddialvalue = dataofuseropen['texts'][e.value]
        nametext = ft.TextField(label='Name',read_only=True,value=nameoftextvalue)
        textfielddial = ft.TextField(label='',read_only=True,multiline=True,min_lines=13,max_lines=13,value=textfielddialvalue)
        closedialbtn = ft.TextButton("Ok", on_click=closedialtext)
        editdialbtn = ft.IconButton(icon=ft.Icons.MODE_EDIT,on_click=editpressdial)
        deletedialbtn = ft.IconButton(icon=ft.Icons.DELETE,on_click=dletedialtext)
        btnsrowdiala = ft.Row(controls=[closedialbtn, editdialbtn,deletedialbtn],spacing=10,alignment=ft.MainAxisAlignment.CENTER)
        textopen = ft.AlertDialog(
            modal=True,
            title=nametext,
            content=ft.Column(
            controls=[
                textfielddial,
                btnsrowdiala
            ],height=400, width=700))
        
        page.open(textopen)
        if type(e) == ft.ControlEvent:
            editpressdial(0)

    def swithdelchanged(e):
        datacontrol.updatesettingsstart()

    def deleteuserdatsetings(e):
        datacontrol.deletethisuserdata(nameofdatafileopen)
        logoutapp()

    def deletealluserdatsetings(e):
        global isuseradmin
        if isuseradmin == True:
            datacontrol.deleteuserdata()
            logoutapp()
        else:
            page
        

    def closedeleteuserdat(e):
        page.close(deleteuserdatadial)

    def closedeleteuserdatall(e):
        page.close(deletealluserdatadial)

    def closefitslogindialog(e):
        page.close(fitslogindialog)


    def generatepassword(e):
        alphabet = string.ascii_letters + string.digits + '-_!'
        password = ''.join(secrets.choice(alphabet) for i in range(randrange(18, 24)))
        passwordfield.value = password
        page.update()

    def addpassword(e):
        global servicesofpasswords
        global dataofuseropen
        dataofuserupdated = dataofuseropen
        outputdata = []
        if len(passwordfield.value) >=1 and len(servicefield.value) >=1:
            if loginfield.value == '':
                outputdata.append('@LockBox@-None')
            else:
                outputdata.append(loginfield.value)
            outputdata.append(passwordfield.value)
            if emailfield.value == '':
                outputdata.append('@LockBox@-None')
            else:
                outputdata.append(emailfield.value)
            if extrafield.value == '':
                outputdata.append('@LockBox@-None')
            else:
                outputdata.append(extrafield.value)
            if servicesofpasswords == [] and not servicefield.value in namesoftexts:
                servicesofpasswords.append(servicefield.value)
                dataofuserupdated['passwords'][servicefield.value] = outputdata
                passwordfield.value = ''
                servicefield.value = ''
                loginfield.value = ''
                emailfield.value = ''
                extrafield.value = ''
                dataofuseropen = dataofuserupdated
                if lastsearch != None:
                    textboxsearch_changed(lastsearch)
                page.update()
                dataofuserupdated = json.dumps(dataofuserupdated)
                dataofuserupdated = encryption.encryptwithkey(keyofdatafileopen, dataofuserupdated)
                datacontrol.updateuserdata(nameofdatafileopen,dataofuserupdated) 
                passwordpageopenlist()
            else:
                if servicefield.value in servicesofpasswords or servicefield.value in namesoftexts:
                    page.open(ft.SnackBar(ft.Text('This Service name already exist')))
                else:
                    servicesofpasswords.append(servicefield.value)
                    dataofuserupdated['passwords'][servicefield.value] = outputdata
                    passwordfield.value = ''
                    servicefield.value = ''
                    loginfield.value = ''
                    emailfield.value = ''
                    extrafield.value = ''
                    dataofuseropen = dataofuserupdated
                    if lastsearch != None:
                        textboxsearch_changed(lastsearch)
                    page.update()
                    dataofuserupdated = json.dumps(dataofuserupdated)
                    dataofuserupdated = encryption.encryptwithkey(keyofdatafileopen, dataofuserupdated)
                    datacontrol.updateuserdata(nameofdatafileopen,dataofuserupdated) 
                    passwordpageopenlist()
        else:
            pass


    def textboxsearch_changed(string):
        global lastsearch
        passwordsandtexts = servicesofpasswords + namesoftexts
        lastsearch = string
        def iconseter(name):
            if name in namesoftexts:
                return ft.Icons.PASTE
            else:
                return ft.Icons.KEY
        listofpaswordsmain = {
        name: ft.ListTile(
            title=ft.Text(name),
            leading=ft.Icon(iconseter(name)),
            on_click=lambda e: paswordpressed(e.control.title)
        )
        for name in passwordsandtexts
        }
        str_lower = string.control.value.lower()
        listofiteamssearch.controls = [
            listofpaswordsmain.get(n) for n in passwordsandtexts if str_lower in n.lower()
        ] if str_lower else [] 
        page.update()

    def passwordpageopenlist():
        listofpaswordspassword.controls.clear()
        for item in servicesofpasswords[::-1]:
            listofpaswordspassword.controls.append(ft.ListTile(title=ft.Text(item),
            leading=ft.Icon(ft.Icons.KEY),
            on_click=lambda e: paswordpressed(e.control.title)
        ))
        page.update()

    def textpageopenlist():
        listoftexts.controls.clear()
        for item in namesoftexts[::-1]:
            listoftexts.controls.append(ft.ListTile(title=ft.Text(item),
            leading=ft.Icon(ft.Icons.PASTE),
            on_click=lambda e: textpressed(e.control.title)
        ))
        page.update()

    def textpressed(e):
        if e.value in servicesofpasswords:
            pass
        else:
            #servicetextsdialog = e.value
            openandedittext(e)
    
    def paswordpressed(e):
        if e.value in namesoftexts:
            textpressed(e)
        else:
            servicepasworddialog = e.value
            def closepasswordopen(e):
                page.close(passwordopen)
            def editmodestart(e):
                closedialbtn.disabled = True
                editdialbtn.icon = ft.Icons.SAVE
                editdialbtn.on_click = editmodesave
                deletedialbtn.icon = ft.Icons.CANCEL
                deletedialbtn.on_click = closepasswordopen
                passwordfielda.read_only = False
                loginfielda.read_only = False
                emailfielda.read_only = False
                extrafielda.read_only = False
                page.update()
            def editmodesave(e):
                global dataofuseropen
                userdataupdated = copy.deepcopy(dataofuseropen)
                if loginofuser != loginfielda.value:
                    userdataupdated['passwords'][servicepasworddialog][0] = loginfielda.value
                elif loginfielda.value == '':
                    userdataupdated['passwords'][servicepasworddialog][0] = '@LockBox@-None'
                if passwordofuser != passwordfielda.value:
                    userdataupdated['passwords'][servicepasworddialog][1] = passwordfielda.value
                elif loginfielda.value == '':
                    userdataupdated['passwords'][servicepasworddialog][1] = '@LockBox@-None'
                if emailofuser != emailfielda.value:
                    userdataupdated['passwords'][servicepasworddialog][2] = emailfielda.value
                elif loginfielda.value == '':
                    userdataupdated['passwords'][servicepasworddialog][2] = '@LockBox@-None'
                if extraofuser != extrafielda.value:
                    userdataupdated['passwords'][servicepasworddialog][3] = extrafielda.value
                elif loginfielda.value == '':
                    userdataupdated['passwords'][servicepasworddialog][3] = '@LockBox@-None'
                passwordfielda.read_only = True
                loginfielda.read_only = True
                emailfielda.read_only = True
                extrafielda.read_only = True
                closedialbtn.disabled = False
                editdialbtn.icon = ft.Icons.MODE_EDIT
                editdialbtn.on_click = editmodestart
                deletedialbtn.icon = ft.Icons.DELETE
                deletedialbtn.on_click = deletepassword
                if userdataupdated['passwords'][servicepasworddialog] != dataofuseropen['passwords'][servicepasworddialog]:
                    dataofuseropen = userdataupdated
                    userdataupdated = json.dumps(userdataupdated)
                    userdataupdated = encryption.encryptwithkey(keyofdatafileopen, userdataupdated)
                    datacontrol.updateuserdata(nameofdatafileopen,userdataupdated)
                page.update() 

            def deletepassword(e):
                def canceldeletepassword(e):
                    page.close(infoodletepass)
                def approvedeletepassword(e):
                    del dataofuseropen['passwords'][servicepasworddialog]
                    userdataupdated = copy.deepcopy(dataofuseropen)
                    userdataupdated = json.dumps(userdataupdated)
                    userdataupdated = encryption.encryptwithkey(keyofdatafileopen, userdataupdated)
                    datacontrol.updateuserdata(nameofdatafileopen,userdataupdated)
                    page.close(infoodletepass)
                    servicesofpasswords.remove(servicepasworddialog)
                    passwordpageopenlist()
                    if lastsearch != None:
                        textboxsearch_changed(lastsearch)
                    page.update()
                infoodletepass = ft.AlertDialog(
                modal=True,title=ft.Text("Do you want to delete password?"),actions=[ft.TextButton("Yes",style=ft.ButtonStyle(color=ft.Colors.RED), on_click=approvedeletepassword),ft.TextButton("No", on_click=canceldeletepassword),],actions_alignment=ft.MainAxisAlignment.END)
                page.open(infoodletepass)
            loginofuser = dataofuseropen['passwords'][e.value][0]
            passwordofuser = dataofuseropen['passwords'][e.value][1]
            emailofuser = dataofuseropen['passwords'][e.value][2]
            extraofuser = dataofuseropen['passwords'][e.value][3]
            if loginofuser == '@LockBox@-None':
                loginofuser = ''
            if emailofuser == '@LockBox@-None':
                emailofuser = ''
            if extraofuser == '@LockBox@-None':
                extraofuser = ''
            loginfielda = ft.TextField(label='Login',read_only=True, value=loginofuser)
            passwordfielda = ft.TextField(label='Password',read_only=True, value=passwordofuser)
            emailfielda = ft.TextField(label='Email',read_only=True, value=emailofuser)
            extrafielda = ft.TextField(label='Extra info',read_only=True,multiline=True,min_lines=1,max_lines=2, value=extraofuser)
            closedialbtn = ft.TextButton("Ok", on_click=closepasswordopen)
            editdialbtn = ft.IconButton(icon=ft.Icons.MODE_EDIT,on_click=editmodestart)
            deletedialbtn = ft.IconButton(icon=ft.Icons.DELETE,on_click=deletepassword)
            btnsrowdiala = ft.Row(
            controls=[closedialbtn, editdialbtn,deletedialbtn],spacing=10,alignment=ft.MainAxisAlignment.CENTER)
            passwordopen = ft.AlertDialog(
            modal=True,
            title=ft.Text(e.value),
            content=ft.Column(
            controls=[
                loginfielda,
                passwordfielda,
                emailfielda,
                extrafielda,
                btnsrowdiala
            ],height=280, width=350))
            page.open(passwordopen)

#buttons and etc


    listofpaswordspassword = ft.ListView(expand=True, padding=10)

    searchbarmain = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.Colors.BLUE_700,
        bar_hint_text="Search among passwords & texts",
        view_hint_text="Choose what you need",
        on_change=textboxsearch_changed,
    )
    '''
    moneyonacount = ft.Stack(
                   [ft.Container(
                    content=ammountmoneytext,
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.BLACK12,
                    width=500,
                    height=120,
                    border_radius=10,),
                    ft.Container(
                    top=25,
                    left=30,
                    content=ft.Text(spans =[ft.TextSpan("Available Balance:",ft.TextStyle(weight=ft.FontWeight.BOLD),)]),
                    width=200,
                    height=100,
        ),])
    '''
    logooflockbox = ft.Image(src_base64="iVBORw0KGgoAAAANSUhEUgAAAyYAAAB9CAYAAABXlnebAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAuIwAALiMBeKU/dgAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAACAASURBVHic7Z13nCRVtce/p3pmA2nJOSxRARGQqCKCCRARQcEsZtRnTqCC7jPz9GEOKAYQlbdkFESfCiICEgyooDyCgsAiIOwCG5jp+r0/blV3dU93T3dVdfeE8/18Zru66t5zb/fOdN9T95zzM2YqixdXtl599c2BreIKGzASz1Ok1U2sFUeaR6R5FvGwKvEjwlaqomUWxY+qEt214rHlt/9731csG/ZL6JaN9YENhD0RtE1MvNCItzLGNwGtB1of4tUgHoF4TYgBrTTiFRA/BvEDoAcg/pfQHTD+d9BtMH7jvZxzO4aG/frasY3WWcDY3B0qkbaXVbczaWukDYx4Q8TGWLxGmL4WQBwZWgVajmIM3Q+6D6veZ7J7oji+DeMWg1viOfztL8Zjw359juM4juM4swkb9gQKs2hRtN0T9t1xzLSvme1JpG0UaRsitsQ0h0goAiKFHwOlxxFgSp4nbazW/n4quk2m2zC7iSi+euXI+NX/3n64DstG+szqxvK9Y9gP9GSo7gbxJonDQXiMseQxe47MOWtxLvs8ub4M9CeIfwu6ooqu/JddeO+gXzMAItp2bMvdraL9kfaU4j3NtD3IwnwVXoMyx7Q5btHGpPS/nyhmLBI3RDHXVeCaOOaya9fmtqG8bsdxHMdxnFnC9HNMFi2Kttr2yftaxLMtYl8iezKRFihxOlIHRInTUcAxSfo22I0VcSOmqxXp15U54xfdtfkxD/T7Ja+nk3asoEMhPgTi/UBzJjobfXFMWvX/I/ATGP/JPSz4DXZWtV+vezttt0G1Wn2BRTqYmAMgXjeP05HDMQn/3Y2Pf7cqv4iMH4+v4KdXbcGKfr1ux3Ecx3Gc2ci0cEx2Xrx4zvKH1ziganZkFPF8ItuEimGR1RyKATkmDXaJqMp0uaL4/EqF8+/e9FV3lPWaN9DJ2wEvgfjFED9hotPQ2uHI75jk6a8lEJ8N1TPv5tIrywj7Wqjd1iZe8dLIdJQU7w9xxRCog6MxGMcEqz9/NIKLrcoPl97Nj6/fk7Gir9txHMdxHGe2My0cky1OuXhbi+K1GR2tnxyF0eQRYCxzidGxhnYTj8danx8N18Z67QfYaCxY/te7Nz12+eSvqA1aPGcD7j3CqL5R6ECIrZVjMHUck4ZzfzPib4rotLvtsvt7fekLx55wgEXjrxe8EOJ5ExyKqeWYZB//VYk5nYhTL9mMv/X6uh3HcRzHcZzAtHBMnBmKiLbkiYdSjU8wi/fu6FBMXceEKE422mJ+EcV88cfb8KOBv5eO4ziO4zjTHHdMnKGxhXbfNFQPA5qioUabo6PGmqOlxtoct+jb8flY0qf+tNXxaKZbx2OgsoKbL3w8D+M4juM4juM4juM4juM4juNMH3zHxBkIW2jPJxi2MYxnzo5nHsYZqZ2vTmzTcBweR3poC1Dp1LZKbfyR5NJIcqmSPNauVxvbNVxv0a4yDqpw01mP4y4cx3Ecx3GclrhjMiA2WnL66ivnPTIHgAXd9lqa+/qCrvoXG6Ob6zHV1YjHP2zGGyZojvSSPzL1c0wm6/dIFHPi+I186ayj6VuJZcdxHMdxnOmKOyb9RouiDR/e4j0YH1XEvJZliy2tfJUulNvri9QX2EPTMenYv2HBr0kchNnlmKTtrrMxjvn+k7ixyK+V4ziO4zjOTGNk8iblsOn7znxSXKlsSyUJfakkB+kP9eeVSnKdzPWkfYXG5/U21foxUK0AVDP2m9pkzlUbzlVLsysUaVn0Vizej+ISH84MwGDPqMJ1r/4Dx313V75chvaL4ziO4zjOTKD/jsmiRdEmD+/4QWGLTFQQKLJkl8DCgwyLwnMAyUAKAoqQtBPIgsAhBghTIrCIQh8j3FmPFCyZJdcIt6wJbZTegY+yYyd9zTLtO9sNryXMqz6Put3wqD7sS/ladpozX/DF1/yBg6MreeW3nsK/hz0hx3Ecx3GcYRP10/im7/nB+hs/uONFgo9R30twCuMReDOE52ouf3jdtew97Ik4juM4juMMm77umGilVreKnQCcQAxUBDGoIohHoZKkDhiMJjsSCIhGk8fEUKSwyxGNhr2CGKjAaKzg7gjG0t0VGUSJsETWRmxQCW0sHqv1Q2CVRGA9MmCMseZ+o4RJpv0yczBZGLMCKF5N0snAtul7UHchkpgdK77bYS2O2rcsOl43YxDRQ0q/08AWZlx27LW86pS9OHvYk3Ecx3EcxxkWfuvdKcR2OmTuclaeBnqxJ7/32K/xmiLx0a/vw6IB/dc5juM4juNMKdwxcQqxqQ5YX9hW4VlxBfa2faeR8vtoxnyr405jjfybP3/puazCcRzHcRzHcRzHcRzHcRzHGSy+Y+L0zOY6aF1hzwyq66lWYLvHcFzp1KbaRZtu7HTbptq6TUMl6LQCdLWpinSO663aTXZ9ZJyxtZ/GhYuCYIzjOI7jOM6MZ2A6JjONze9cPD+Kx+ZNuNCUAr60xdF0Vn6PsdWqVM834j3DGSNUAgiPVku4t0yOSVKiuVUbVCsI0LGNumiTlnCerI1NbBPKUSeVoOOkhkLyshSHugjpY6vr1uG6NdnJXpfVK1lLyXVBHMFDv+FLwNu7+E90HMdxHMeZ9viOSQ42+78zNo8rdiURW6iWMU2oHhYlx6bkOTV199pxYeX39orsrvw+bZPfW9qsxJxw8tP5RN7fVcdxHMdxnOlCoR2TdV962pMrI7Z5TYkdGpXbGxTUM8ruND6fbsrvscWLQFv0+n6VRxllgJ3pgOBj7/0VSz77dL417Lk4juM4juP0k9yOyfovPf3pRPwvMJrGoViUKqunyuiGRYCl4TjGjFB+d5zBYRJff98vuPMzz+Rnw56M4ziO4zhOv8il/L7gqNO3RjqLTLVTZ5D0Y7fEd2AGTvdv+QjGD9/7U7bu42wcx3Ecx3GGSq4dE/HY0koU7YvmhoJGqXsSp8eCqiARcCeeh7Jt5qSGxNwqMBISj6nOrduqZmZXFRpNkp9jYHTeRFvJsFRX1vuJzPystmNjowCr6srvDTYsGTvsjaxKaiJFlbHDzPhIj2/VDFB+Zx4wv6gRpzDrVkY4820Xs7/rnDiO4ziOMxPxyCSnLQv16nmrWHY1xLt68vtwkt9bnP/ap57NW/r9f+84juM4jjNovFyw05ZxHrUYOzJk/qcS5pb8ZJ+n1QJWMrfWO0rc3uzN/ca2kOznWDivCW0NiJiXtG09fvYcsKrxfD0raDyzd5SNYMzOOdkwqySbbCuTTTdLNtDGMptwyUtJN+nmJtOQQTWj6C4DtbA3Wp9W2GhMXoKiYK8WIxkl18fr9lCt9rHjOM5QkLQQ2Al4AnChmf11uDNyHGcm4DsmjuM4juO0RNI6wM4EJyR93A1YP9PsIDPz4hyO4xTGd0ycCWygo9aooEPCs6w6ev240uJc68fm9i0eXfm95+smVnz8IH6M4zhOCUhaG9iW4HzsQXBAdgE2Gua8HMeZXbhj0g4tirb80y4La8FF81Y2Xp/b1L6mAb+qizbZ6012m23Qqk2v13uzYVTfZcRvzSq6p1fSc2pxzpXfe1R+F22V35VU1G53HcGin3DookO4uMV/tuM4TkskrQVsz8RdkG2GOS/HcRxwx6Qtm/9xp9dXo+oplUSlnWqlruRuSdWxCGrK7+Mk1yt15fe4Sfm9SqPye1UQVVoov0c0JpVXMs9jrOl5/bpqzycqtzfabBwjbhrDmQ7E8MVFl/LLRQe29G4dx3GQtAD4EGH3Yydgy+HOyHEcpz2TOiZrP/ebh0cjlY2IICKqZ+VWCIvqCmHNW4moRGSehwV6VAGiKHM+2y8K4Sk1m5P3qSRjkR2L7HEMFahGUIt7qbWNM23riu5xzUZcsyfiT0xdbY+pOi9nwGzLCt4NfHLYE3EcZ8qyDvC+YU/CcRynGzo6Jus859QnAOcgVYLqeqI3ElkIkbEmhfUklz4bPhMicBKV9lRHJFFxR8mOgixReU/DbFLbGeX31B4kYT2W2CTsVJDOLRmvYV5Jn1pITBojk55X3cFJ5zSlKUWfxJkJiA8uuohvLzqUJcOeiuM4juM4ThE675hEnES9vqvjOFOP1U28H3j3sCdSBpJOBt417Hm0YFczu2HYk3Acp/9IOgc4ctjzaMFKYAWwDHgQeAi4D7gTuCP5uRG4xcyq7Yw4zlSmo2MSVx57RTgA4gXh5IJMg1TUodp4fkGq/F5lYp80jWF8QVe2gKD8XhWs1rRPkE2JaO7TbBODBemOTuZ6InKX2tCqVe+V6SVpk2a5iLb7FLULifWuFN7z7np0o/jeyzgCbD1av4vOFMfgTYsu4LOLDufuYc/FcZwpx8PANwghXRVgK2AHYM1hTsrJxbzkZx3C/2M7Vki6EbgGuBy43Mz8+8GZFnR0TJZe9JYH8xhdmm8uU4UPJT+zB2Eb86o/EpIjnenH/IpxPPD2YU/EcZyphZk9ABzbfF7SE4GPA4cNfFJOv5lPKPm8B/BmAEl/As4BzjWzPw1xbo7TEa/K5QBHRWL8BeE4VWFPpMZrau2u/D5VlN+rBvOi2ltIDIzEDW+I4zhOR8zsBkkvABYDLxz2fJy+s0vys0jSdcBXgTPNbMVwp+U4jbjyu+M4UwZJewH7AZsCmwFPBB7H4G6iLANuAv4ELCHEcD8EnG1m03wz2HEmImlT4HZgTgEzM0r5XdIzgL0Jn0E7EXYeZmKo873AJ4BTzOyxYU/GccAdk1nPpnrNFiI+JNx3T5OC0uM0+aZK6+sTjysN56ldi5qeN/SLC/RtHreav2+tmnQ1qTAdZ6pKNx9n2hG3Pq5Vn65mqlVnjlMl9zLGStloY75z7J4za/dE0nzgCOAtwFP7MQTwPeArwHVmtawzx5kVSDoPeEEBEzPKMWlGkgFPJxTmeP6Qp9MPbgfeNJP/D53pg4dyJWz12wu3VjRWd9SS+J6ZrvxeJT7e0BvCuVTFXRmPNZs4X1eBt0zberu0ZHQ4Z6qrqytjq15QIKPG3tyXpr7qsq+16Ns8rib2tdR+5uXUqkrHtW5BhT29nkwrVXBX6ohY43UjU5W6/hbWrrUaK6mY3XIsWoyVtr3vbu4FLmAGkYQa/EDSD4HPAO8p0fxK4IVmdnGJNh1nuvFzijkmMxozE3AZcJmk44FPlWT6TuDXwCMd2swjFCpYk5D0vi4h8b1MYYOtgUskfQt4h5ktL9G24/SEOybApleevXuV8d8BQaE9AuKwCpyayu9RrW1x5XdnaPRBikbwKmaYY5JiZpL0fuBA4EklmX2HOyWOw03DnsB0wcw+Lekw4CkFTd0D7GxmD/faUdKawG7A7sCzgOcw8VZorxjwemA3Sc83s3sK2nOcXDQ4Jms+9auPi+ZUnt5WxX2mKr+j5xZ+JweKCyzOCPrx32g8b9GPWH/RYdxfsuUpgZnFko4D/rcEczcDp5Zgx3GmO/8Y9gSmGR8FLilo43d5nBKApN+vk58vSlqPEOr6XmCtgvPaE7hK0n5m9s+CthynZxocExuJjjd4NRJqodQ+Y5Xfp7zSu+N0zZyKcRTwtWFPpI9cRqhKXjQZ9UeeT+I4QAgpSrfWncm5jCB0OL+AjdJyAZOS0B+T9E3g28AhBU1uBfxU0tPM7N+FJ+g4PVD/ENp58RyTHT7EuTiOUwbxjEzOrGFm44Q7hUX5ZQk2HGfak1Rk8qpzXWJmq4Brhz2PZsxsCfA8ytkJ3qkkO47TE/Udk7/cOM5+G26rNDF3glr7zFR+F+OvBr283indp0nSprN1y8zqHRvOZw8aY3Ms80/Q7FCbfq2OW5HuHnXXlpZtDWADYMtJDDjTEePARYtZY9HRHRMqpzu3lmDjxhJsOM5MYUZV8xsAdwx7Aq1Iwl2PJXy/P6eguSMkvcLMzihhao7TFZlQrkXx0ivIpfTezDS77fK55GdWsbFe/2XgP+pnPGdl4PTvLZ87Mo+DCCq/M5W7S7CxpAQbjjNTcB2L3rhv2BNoR+KcvAb4G7BGQXOfkLTYdU6cQeFVuWYpVeYcPx+dONGNTNXZU4X2VteDInvr6ylRiw2diW0bld87t209/sS2Cya0hfrr6WQbtDSzyZbaygxZ24Rb2jwWdeX3KNO/aahU+b2a2Kv1X5q5nh0/W9whM78Jr7XpvV61BjNdzfdfBfs/aGatanU7zmzFd0x644FhT6ATZna3pC8BHyhoaktCtUcP63IGgjsms5T77KszOczHmfkUdSr8999xGnHHpDemww7C14D303hnLg+vxB0TZ0C4YzIL2VDH7hoRH9yo8J5N2IkTxfT215lwPduPCW3Djf9qCxvpQ3PfulJ7Z5tNKvRxnHwCT+zTqALfdD6j0h4lx1FcV16P4nq16ShRZk/V29NrabXqhv5N9sjaI7Gf2sv2z17Pjl9tfF5Tl29BdYRvLjqYmVpRpZWK6CD7O85Mwx2T3pjyjomZ3SnpGuDJBU3tJ2njJLnecfrKrHZMNr/y/F2iqubUdFRGAcbCp/NopmHteKzN+Xrf5nO1T/rRsaa2Tf1qTHbcXdvRDterxG8FvXqiqntdzV01ZXRr+olrrRv7pRrrzcrvJOfrtmzCsajPRYmVpsT9CcrvNFzP2qyPFWcKGaiuAi8a7CvtrxBVZonqeq1wQVwfLdXTTNtlxORrauxG0iYtT231atWRgcX1Nun5tE1Eo+1U8b2hf/ZtSfplayqkVMb4EzBTxQOLOhZTflHhOAPG/yZ6Y7q8X7+guGMSAfsC5xefjuN0ZvY6JpdeOmLx0msUMU/pijAWWESUUX5XpKS6uyCKEgmVRL1dGeV3Ea7H6eoyKL9HqfJ7HNVV4JXotdSOUxX2IMRSV21PV77pcZxcb6Xm3tg2rl2f2LZxce/MWMTuzFzHpKj+yHRZVDjOoPAdk96YLhpIvyvJzq64Y+IMgBEOWDSy4LEN30OUqKlHQBQF9fWR7LlKWGSnquxpu4jg3lTqbStRtg0wmrSLGu1RIemfBKNEEYxklN9rbZPnozTZSR/jegRlEgMT1+JiMjYqmee2bF3BvL69s33FHQtncmTsPuw5TGH8j8hxGnHHZGZye0l2FpZkx3E6MrLm8vW3YcQ+HZ5aCCFJY1iSCJuskntANeX3ettE3Z1UuR0wq4ekpCrtUO+bUXK3TIyKZPUxyNqpz6muNxKOpWzsTUb53RS0SNJYFyXK761iXxxnZrHLsCfgOM60wR2TmUkpMhC0VotznNKJINpp2JNwHKd8DLZatKhtbrzjOE4WD2+cmTxUkp3VSrLjOB0Zefiat5zP5BLiM44tLj/vRLDDJ77y6aD83ryD1b5tC+X3DYEtJunozAzmjuzGZsCdw56I4zhTHg8jmJkso55oWoTlJczFcSZl1ia/37n/ER8DPjbseQyajfWmRUIfGfY8nMEQj7AQd0wcx3FmK2lmbVHuKcGG40zKrHVMZisjzD8pYuUXOiu7u/L7QJTfgQVNb3NZyu8p627sQoKO4zizmLVKsnNzSXYcpyPumMwy/mmfWwGsGPY8HMdxHMfpOwtLsnNFSXYcpyPumMwyNtSbXh6hzScqt7vy+0xTfgcw46oTDuXyDk0cp2ckbQLsA2wPbANsCawHzCXcoa0SYtsfBe4HbgVuA24CrjWzGRuvLqkC7EzQfdiGsDDcFFiHIKm7FqEC1iOExORHkp+/ATcCfwFuMbPxQc/dmZE8oQQb/wR+X4KdvpH83e0C7E74u9sG2ITw97Ya4bPpUWAloVLZXYTPpFuB683Md4SmCLPTMVm8uLLlJqO71Z7PIuX3mPiDQjvVFddTXPl94MrvcX+V3wl9PwPumDjFkDQPOBh4AbA/sHUBc2OSfgdcBpxtZtcVn+FwkbQd8ELgIGAvYI2CJh+TdDXwI+DCmbRokrQX8LUhDH2+mX18COMOmwNKsHG6mU05QUlJCwl/d4cQbpTk/ruT9C/gSuAi4Dwze6CMOXYY74eEGzvD5FQz+3q7i5J+SXmhgO14jZn9KXtiVjomm607srZk16UK7dNP+b3etnfld2c2oXCXyHFyIWlf4D+Aw4E1SzI7SlhE7AMcJ+l24PvA183srpLG6DuS1gKOAV5H2B0pkzkEB3B/4DOSbga+S1hI3FfyWINmLWCPIYxblgL6tEHSXMLfbhEeBb5QwnRKQdLqwCuA1wN7lmh6Q8KNlxcAX0sW5d8kOLT92L3cCXhiH+z2wsWTXN8VWLfPc1i9+cTImvt85VNRpWI1JfcRkoV1XXk9qinAWxK7AlGi0p5VYI8sPVd/tPQWcqrSPpLpa9ZijKRtJWmXKMPXFN/TvOfaORKl97h+rRY7E47j9Fxym18jWt0rIzpDZ2J16dKJxLz+juDMNBQUbo8C3ke5X/zt2Bo4geCknAt82sz+MIBxcyFpY+ADwGsoz1mbjB2ATwInSPoy4T0qSzjPmbm8hBBiWYSPmdm/yphMESStD7wfeAOwdp+HGwGek/zcKekrwFfMzIvJDIARw44LASFhlaQkrsRq8Sr1MJwGpXWSdsqcs8zVpviVmj2A9Lql4TKporsl/ev/huaqq8EnivJhVhl79cb1f2txMontND6nGwkQx5kBKGooR+Y4HZH0DOAkBuOQNDMKvBg4KglzONHMbh/CPFoiaTXgPYTFUdFQrbyslox/jKS3m9niIc3DmeIkv68fLWjmSuDkEqaTm+R1vIvwe9/vsKJWbAF8GniXpI8C3zSzsUn6OAWYlaFcjjNrECuHPQVn6iNpXUK4xiuGPRfCXvfLgRdK+k/gs8NOBJf0FOB0YNthziPDRsD/SDoQePs0WyjdBXyD4IimDt58QqLyJoSQmjLWJquAWwgJzsuAX5dgczrxRUJRirzcARw9zN8tSU8Hvk1IZB82GwFfAd4s6bVmdm1Be+cTEu83AJ5EuOkwCJYCfyAUJZksv++HwGaEOe5FCDEtSgz8nfDa7wPubW4wsuy3bylDeGdascGli9eYx5zzgHoitGpPGhXaG3ZXNGGnxaAuDy81RuZY/XzNbgsbzfE8anO+Ycy2Wz7W9KimR/ZhcOEHTicGEU1oPDaAUZxpjKSDgO8QFoV5WQpcTagq9SBh0bk+sBshnyDPF9o84FPAkZJeaWZ/KzC/XEiKgP8khG7l3X28Hfgt8A/Ce7MWwcF5NsXjt98EbCbpKDNbVdDWQDCzvwLHtrsuaU3CztmX6T1H7m5CvtKFhOpv0+I9KRtJJxByn/JyJ3DQsHK+JM0BPgO8jWLxLX8jLL7vJDinaxOq5O1F/gIeTwCulPQZ4MN5b5qYWU3oOskFeiZhZ2aXnPOajLuAtwMXdft3YWZvTY+Tv8vXEnbQevUbYuAc4AfAL8zs4U6NZ+WOyX0HHv0I4Uth1rGRjr0SePKw5+EwkBwTxa5Z47RH0nsJX4Z5F93XJv3bftlJWoew0DyOfJoKewHXSHqFmf0o5zx7RtJ84HuEqj+9EgOLCbs917exPw/4MHA8xRZfhxF2II4pYGPKkCxaTpX0JrpPkr+L4EB+d5rtHpWKpFHCwvGtk7XtwFXAkWa2pJxZ9YakDQmL2P1ymniMkLT+VTO7scM4uxEc+9fSWCu1G0YINyv2kfRiM7s/51wBSD47L5Z0KfA/hL/psnmJmeXWokn+Lr8gaW/gZT10/RXwZjO7Ke/YjuM4Ux5JB6sYs65CTxZJFUnfKvD+LZP0GkldL6glzZG0SNJYzjGrko7r5/uSmesCSVfmnOedCiFW3Y712uS1FeXlBV/zJQXGfk6RsVvMZQd193sSS/q6QoW0gSLp2ALvlySdV/J8niLpDwXndKrC3fuhIOlxkv5RYP5XSeqpBK+k7SX9psCYt0l6fInvwXxJlxeYTyvG1MNn9STz+0gPY76zrHEdx3GmNHLHJDcKTskZBd67OyTtWGD8AyQ9WGD8ogm9k81vNUm/zjm3v0nqOa5f0gkF3o+UuxRCYPK+7inhmCg4sFd1MeZDkl5Q1rg55jl0x0TSqKTnSrqo4Fz+oh6c6X4g6fGS7i7wGr4lKVcUkMJn4tcLjL1E0s4lvhdrJ/8nZbJDSXM7s4uxliqECOdiVoZyzWY20LEHR8QH1LVQmhXdxzPnlDkfZ66TUYZX0/V6+yjOPq/byiq5Ry37KqPqnqrDxxP61vuozfnxJD6isS1xPMF+RBykasgor6cVqMfrquwjMQ3tLKsIP55UyU77p+lEGXsjGXupEryR2EztZ65lx4iAEU1UkM/OoZlKhW9/8FBmjDibUwyFu1ffISSX5+Ee4Glm9o+8czCzyxSqf/2KfPluJ0rCzD6cdw7tUFjYnEu+MJL7gUPM7I4cfT8BPJUgYpmXTQkhIOcUsDEVOBnYd5I2twDPNbP/G8B8phQKju8uBH2SIylWDvg+Qi7H54ec5L4tcCmwcU4T3wSONWsnNdwZM6sCb5K0ipCH0SsbAb+UdEAZIUtm9pCkI4BrgAVF7SW8LfnJjaTNCTovnVgOPM/MchebmLWOyRaXnvsEG4k2ZgTGqTa+E2m09ch44/n0uDJee15N2zVcTzskdifYGIdKssSvXRuvPY6kfZvONz52e735Wnwk2BsmJjikdZVTRXbLnFPT9Vb9Ag3K7BlpdJvQNqPGrmZF+FR5PmMzrSOQVZbPzLFWWEDKjJWtDW31uRlMmHNa6yCjsp5qaaZmLJlqrU2mjkFaDbtZyT1VgLfUTLaSdlZlPlPJeoLtTLvUfu0lpO3abJZqnB+0vuLMUo4HXpmz7yrgsCJOSYqZ/V7Si4Ef03siJQTn5FYzO63oXJr4T4J6ex5eZ2a35eloZpL0euDPFNNoeAbT2DGR9BaCoGcnriUsfIaurVGQhZLe2ObaHILw3DqEymWrE7RsdqachepNwOeA75nZUCs3KiRVX0B+p+RS4C15nZIm3kWoAPa8HH03BH4kaZ8yVOPN7GZJxwDnUY7AxbGSTjGzP+fprFAI5FQ6F6R4DHhhEacEq8gBZAAAIABJREFUZrFjQiV6rYx3BXV2q6u7W7LIjcLyT7Hqt7SloN4uqym/W6LqnirHK1J9RRslS+E4sRsRVpaR1fumq1cgXXLGDXf/bcJjfQHffF2kCu9WO5/d9XBmGyOhIpDjIOlQ4OMFTHy4XSJ3HszsJ5I+D7w7p4lTJP2fmV1ZxnyS0IPjc3Y/28wuLDK+md0l6R1AEWdrqyJzGCaSXg18aZJmvwQOnyFCd7sBpwxwvIcI1cp+APyspIV8IZId3O8RHK48LAWOKaucuJnFkl4L3EA+R2lb4CxJB5WxA2VmF0j6BEGAtiijwPcl7Z2zWt176XzTpgq83MwuyTW7DCNr7/WV3TRaeclsUn6PQ9zL7kXfvOEx9M8TZ3pw33GH07EsnzM7kLQe8C3y7U5AuJP/3+XNqMYJwIvIp7cwl/BF+8TJyk9OhqTVCeEged6fMeCDRcZPMbPTJR1JCNPJw7Qs/5/snp1K5/lfQKgs5NpMvfF94Ezgf6dg+eTXk/93HeAjZnZnWZMBMLP7FKoVnpHTxIGEGxwfK2lKHyEI3hYJ80x5IolYZC+dJO1L55taAt5gZmcXmFuNkapV5kfouNmk/G6ZECPHmcHMuvhrpy2fJ8RB5+W4JA67VMxshaQPEe6a5mEh8F/AmwtO5QSCwnMezis51+FYQkn3DXP0vafEeQyEJJb+e3QuWf094LXDFtqcpmwDvAN4naQHCcKJdwB/Av5oZkPRupK0BfDZAiZuAb5a0nSa+QHhPdsrZ/8TJF1gZjcUnUiyi/Nygh5LXu2VLO+Q9BMz+1k3jSWtTRBa7FRS+QNm9p0S5gbASDQn/iuxPdhwdkI0W3fhbS1btTs56AJircdbZ8CzcJxB8vthT8AZPpIOoJii+w3AT8qZTUt+SMjtyKvufKykM8zsN3k6S1pI/nAygK8X6DsBM7tX0quAi+l9ByTXezAsJB1NuDPdadHzZeAdZubxyPnopFs2Jul6wu/aj81skN8ZJxPERnP371fCfpLz9UlCfkce5gDflLRvGSFzZvbvZCf1NxRXiDfgu8lOc0f9lSTU7rt01p/6hpmdVHBODYwsveItD1JcfXZassUV552DWGv6Kb938uomU343hB5vsHkHI85MQO6YOECxvBKAr/QzHt3MqpK+TFio5DJBCE94Ws7+7yafMj0EJffLc/Zti5n9VNJngff30O0hoJRQikGQOF/fpvNOycfN7MQBTWk2MkqogLYv8FFJNxJCGk8za7phXSKS9iCfcGnKoxTLxeqGCwk5mnl3KfYmhKmeVcZkzOwPCqKjp5dgbhNC6ORkFbaOo3Oo3SVMXqyiZ2Zv8jtw535HFPnDmLZspGPfRrhD2QWTbW31svXVa9tu10KZiltFsZaHLdt19c50aGTNT7p5CT28LVGF0hKVnemJpIMJZWjz8hglfbFOwlmEsI68ORL7STqsV2V4SesDr8s5JoQk4tJD3BI+SLiB1K3K8rvMbFmf5lIqkt5A2Glq9/8t4H1m1o+8Jqc9OxGqdf1nUpjic2b2UB/G+RjF4mYuMbPlZU2mFUkI1Vn0dnOgmY9LOq/E5PzvSdqLgmV/Ew6XdKyZtSzAkJR073RT6wbgxR5e6TiOAy6w2CUqJponSRcPcK5F1JclqeedC0nvKTjmMf14LzLziyQtkrSqwxxWKZTZLTrWQAQWJb1NQbG9HeOSijiLA0HFBRYvlbRHm5+nS3qWpCMkHSXpdcl4H5b0FUkXSPqjpJUF5zAZSxTC7cp83x6nzv//3VAkNLWXue5V+B2UXlTynEaVXwC2mUfVQrVe0uaS7u3Q758KmiaO4zgOuGPSDZIWSqoWfJ96qt5ScL7vLDhXqUf1ZUnXFxxvIF/OCv+XH5H0S0m3SrpdYXHyCeVQmm8zRt8dE0nvn8TOKklHlfF6+o2mhvJ7JGlbSS+T9EVJNxWcUzvOVKhcV8b79pmCc3lM0kDygyWZwt9aEX7eh3ltIunugvNKuV7SnIztOZKu7ND+YUl9rWo7q0O5ZjMb6fUvNeJdJ6q2u/L7TFB+Nzj/hOdzNc5s5jUULx/7qzIm0iUXEsJIivAG4J3dNFS4U/ikAmMtM7N/FujfNWb2d7oOv52aSPo48KEOTZYDR5rZTwc0pWlPUhDg1uTnBwAKzvnLgDcC65c01IuBxyuES+YuzytpBHhVwbn8tp/5L1mSJPgLyacGn/IMSduXWbnPzO5RcOAvpXPhiG54EiFkKw1Z+2/aF0yoEkp29zV/ddY7Jltddc6TxmXbUiFJwavWU/EqQKVaPwaq2Ta1dpk2Teeq7eymbbIq8bXHao5zjdcrk/aJDyd82CRkhRpd+b32ajNmDKaN8nsc8X2c2U4e9eIsVeDGMibSDWZ2m6R7KVbW+Pl06ZgAhxQYB+Dmgv1nBQqVfT5P58XdI8DBeSurOXXM7C/AhxSE+Y4l6GCUoRa/K3CZpAPN7I6cNvYiXxnsLH8q2L9XrqaYY2KEz6VS86XM7DcKO9pfLsHceyRdQhCVfGuHdm83s4tKGK8js94xiePKrhbF3waS1aAFLZcoWfAmeitBsV113ZVkMRuU3hOhSISU3E5P1OGtjd1QpSuzeg0TANIFd9xwjsw5a3GucREeZ9wBtWw36GrNzkD5x4cPHfiHtzOFUEjq3q2gmVuHIGZ3LcUcqq17uDuZt4pXijsmkyCpAnwDeO0kTedR/5JySiBJDv+cpDMJ4qpFHXEIJb1/KWkfM3sgR/9nlTCHP5dgoxeuKcHGQfRBoNbMviJpb4rvQkWEst2dyjf/t5n1SzemgZpjsvmTT57/8Ojqn4sqWE35fSQorVuq0j5CWNeORDWV98iAkWTxnii2W/JIlCzYUxX3Vn1GwliWjEVmrChVn68kKu8Vqyu6V6IwjgEjMUpLnI8QFvppO2tSfo8gTmNsRgAGE6voOINCQSHZmd0cSPEwrr+UMZEe+SvFd3qexSTiosld/P0KjuMCph1I4tbPALrJGRkBzpC0m5k93N+ZzS6SsJ/nAScB7y3B5LbAYkkH5ajIdGAJ4w/6c+nvwCpgbgEbT5M018xWlTOlBt4E7AIUzfvYpMO1cylWnawnao7JP69694oF+5+ym2AfsESCIxMnYmDpzkAa46JE7V2AZdU16uIf2X/TnQGl+h6WKMdH1HYVULohka3HWld5b7BXi6+BVKW+QTMkGw+D1ca3dC61WB3HmUGIc4c9BWfoPKEEG4O+MwnlLPZ36aLNpsAGBce5r2D/GYuk+YQS0If20G0b4IuE3CinRJJclPdJiigmJpryDEI564/22K+Mz6WBOiaJztKthFLKeZkH7EAfwtDMbIWkFxKU4fuhSfhb4BWDFDhtCOWS6fuG7TCLlN9TRoA1BzMRx+krt594GJd/eNizcIbNhBKQOVhSgo1eubcEG9289m1LGOfREmzMOCStSShkcECO7q+WdJGZTRuhyGnGe4GdCaFFRfmgpLPNrKs8NEnrUvxmwNhkauV94l6KOSYAO9Kn/Bgzu13Sy4CLKb5TnuV24PlmtqJEm5PS4Jgs+9WbvgR8aZATmApsd/XFa61i5TdJPCZBZielcXemIceEJG+7diGbXB12aOr+UJPdWsZyqx2bVl6UdTxqzCfp6dw+QCnlJp0e6c9m3elWmtqkM43ZoQQbwwipKUMgsJvX7o5JH0gWnz8hqF7n5RRJV5nZXSVNy0lIqky9GrgJWLugubnAf9F96OX2BceDUCRhGJTxufS4Emy0xcx+KulE4BMlmXwQONTM/lWSva6Z9cnvALfs+9xlNFSomj1sote8QmH7vA2TbW31svXVa9sZrvyefYndvtxJ2lWN07uw4sx8ysidG4ZjsrQEG92EM3SKp+4Wd0wySNoI+BnwxIKm1gW+m+QweEJ8yZjZEkmfpbOqd7ccmiTC/7aLtmWEGZXhIAxr3H6EWTXzKULlsxeUYGslwTkZOO6YzHLuse+cQUhQdBxn5lBGaOp03TGZL2lkksTcMsTi3DGpswUh2qKMnToIBQzeCZxckj2nkS8CxwNrlGDrHQTdlMkoY6xhFUYo43Op7+kCyY7YMYRKYkV3aDYhFDl4ppmNFZ9d95QZi+Y4juNMDabrIqCsO6KTLQLKcEz8xl6dr1KeU5LySUlFd1+cFiSVz84pydwRSQjfZEzXzySYJo4JgJktA46knPfqaYRqbgPFP1gd0AEjG7PFyUJzg7K7aK3sLurK7+lx83Vqzy1On6c3LkPbaIJie4u+NPVVgb7N48YT+1qiBh+JutJ6WlV6vJ5CNJIqrauuuj6Spg2NZ6pVp6rtTccjSbvJxsrabx7LkpeWHcti/nri8wurZjszhzFgTkEblcmblE5Z30mT3eGbV8IYZSy0ZgpFf9daMRf4vqS9hqCnMxs4FzimBDvzCNXXvjdJuzLuug/jM6mscQe262BmN0p6LbCY4qWm3inpajNbXMLUusIdkyY2veasp9gomwEzXPl9wrl9DO3dOYmhLoOuCSrwqXBjpq/V+zTmgNQ0zjPK72qRJ9JF3+ZxlbNvXTOzoS6BpQrt6TGNf+Wp2ntW+d2a34LkIFVut+a3uMVY9DqWdaUV4MweHqH4rsAwFt5l3FWMmTzMqowqM+6YdOZBiuc6PQH4NCGsyymXXxP+VsqInHkWkzsmZSSuD6t6aifhwW4Z6G6PmZ0t6TMU1x8x4FuS/mRmN5UwtUlxx6SJSiXaIpbOnPnK7636OtMRgz9Xr3ftEqeBR4CNCtoYxiKgjAXAI2aTClQtL2EcLzHfnr8AzyYsVp9Z0NbbJV1sZj8rPi0nxcwelHQbsF0J5p7aRZsyHJNh3QyYdo5JwgcJTuOTCtpZAzgnKXTQ99fR0TFZ9+BTPyazDWe28nsaIxNem0SEMT7Ze+M4UwZx4qJFNS/TcQDuoXhJ3OnqmNzTRZvpvEia6vwOOMjM7pf0euAGiv0uGaFK1xOHpGExk7mVchyThZLmTRJyV4Yu0nTeMenmc6lsDqQ7wdlu2JGwc/LiLm78FKLj4lvSEiJOSGujzkzl92Q+6WvynQNnOmFcdcLzuODEYc/D6TuSNgS+3HT6JDO7vkXzm4H9Cg45jIV3GQuAv3XR5p8ljLNeCTZmGlcDh5jZQwBm9ndJ7we+VtDuJsA3CEm9TnncWZKdCrA1QR+lHbdQPHRsOu+Y/LUEG10jaUfgLGC0RLNHEf7G+1otr6Nj8uD98TfW2ajyUmCTNOYdSPyUXvJpGqPlG3wtm3DQ8mlbew05BZP1azWAJvoi4dLaDKbutOPkJY5i3uaCirOGZ8CEXKJmRyWlm8X5ZGxago1eKUNfpJvXfnsJ42xTgo2ZxK+Aw1qEepwCvIjiIV1HSHqdmX2roB2nTpmChR3zicxspaQ7gIUFxhiRtOEQRP/K+FwamGOS3MS6iOIimq04SdJ1ZnZ5H2wDk4UrXX/s2IPF77pNSza/fvF2inhf85pP6e5MmmOSelkNWdO03H2p7fbUdnWaM5wzOzq1I01ynKdt9kyrBHaeQ7EPD2cwfPPDz6PV3XJnZnJAi3P/btP2DyWMt1MJNnqlDHXo33fR5tYSxilDPX6m8FPgSDObkLuTaCuUEdIF8HlJvzKzWwracQJlFIFI6WY3448UX1vsDAzMMZE0QvE5PwD8o/hsJkfSPOB8wg5WPxgB/kfSHmZ2d78GcFrwzz2OvgU4dtjzGAYb6+gDgVM7tZm4Y9bupn2rLaxObSdW5mq5wdYuYb+bHbNahF+HjYY2lbVaFQ6bMGSbdl3R/d7H8rFRPtR1a2cmcGCLc+0ckyuAVYSSq3nZuUDfvDy+YH8Bv5iskZndI+kuSCow5mNnSaODFh+bopzcyilJKTGkaw3gDEn7TSKg6XRHmaFR1cmb8Evg8ILj7ARcWtBGL2xH8XCoX5pZ3/NAJRnwXeDJbZqsAi4Aji441MYE5+QZ/fj8c8fEmcASW3wpfjfQmdkMqx5+LiRtRmsBu5aOiZktl3QVrXdZumWbLhJaSyP5Ut2roJkbegjzuJKJoXG9MI9QzrabHRqnvJCufYATgY8UnpGzfom2HuqizaQ3Dbpg0Du5RT+TAP63BBvd8DHgxR2uHwt8n3BDpptKap3YD/gMfSjl7crvjuPMRqZbRaVntDi3fBKn4UcFx6wQKrEMiu0onlB+fg9tryg4FsD+JdiYFSSVfF5POWVTPyjpKSXYme2UWcCh3e5tlhuB2wqOU1aVqW7Zt2D/MYp/Fk+KpGOgYxTFZ83stGSn8eV050hOxjskvaQEOw34jonTloV6wdqPEX1SxBVXfg9Nh638Hom7P/0sPtpCjdLpjTKqrAySVnf2J1sInAF8imKq3PszuB2B5xTsHwPf7qH9BcDn6aFkSgsOBr5QoP+sosSQrhHge5J2G4SuQp+YN+wJUE5SN4Qk+klzKJJ8o+8CHy0w1j6SFpjZ0gI2euHZBfv/2MzKKJXcFklPJ1Sta8fFwPHpEzP7h6Q3EpThi/LNRHzxLyXYAtwx6ZpN/vrDPYnsSWGPKVFsT/ebKnHtOK5UM+eTNpWwIK5GBLX3huvpQjsNz4yT47jFuXBc6aFta7sQddFvVVi47wHsHc6nmfqu/F6zmNHI7Fn5vak+QRfK72MWc6A7JaUwbcTxJK0LHNTiUkfHxMz+JenHFCux+mwGt/B+bsH+PzOzO7ptnHw5X0vt8y0XB0pax8weLGBjJtCLc1dWSNc2wBeB1xS0Myw6VrHqN5LmU96O6O97yKE4DVhE/oidOcAhwJk5+3eNpO0pXpDjm2XMpR2SdgDOpf0NqBuBl5pZQw6QmZ0l6VTCLmYRUvHFvc1sWUFbgDsmXVOpVm6LrXqWxMLaClQkyu+EnyizlLTswjs8D+v0TFUuqXYtEPq0r8oV1202rGwntrXabkC9X51sQnn2ev24yC1Ep0+I933qOfxm2NOYIhQNQ50rab6ZlVmVpl+8htZfOt2ETnyBYo7JMwdxd1LS+gSF4iJ8Jkef71PMMZkLvITiOwBTgSLrga6Tg0uu0vVqSReZ2dkF7eSh6NfksOUInkZ5a8DLum1oZndIOg94YYHxXsAAHBPC33YRbiBUrOsLktYjlAVu97v0APD8Dg7DOwm5IkWLjjwO+Lako8oQX8z1S7neS07fx0zvoWLh7m8lKLRHFQu7AFZXfrdKuB5ZeE7yPLQzLFV2T56HfomCfCURTcwqv2fsW2rPhCKSGJgYKskd8Kzye+ac0viYNP21kqrChzZxusuRsRuHnY1BbR06TgMGi096loeMZChSbSplO+BPJdjpG0mpyv9oc3lSx8TMLpf0S1rnqHTDPIJj852c/bvlJRQLOfuFmf0yR7/vEO7eFrl7/R+SThlE1Z0+U+T976lqUYkhXQCnSLrKzO4qwVYvFA3F2mzIVd2OKNHWD3psvygZP+8NpkP6XZgjKcbxyoJmTujX54KkucB5hO+xVowDR5tZ29LoZvaopJcSRBOLfqe+EHgv+W4QNZDLMXngzFf9doOXnLZc4phsuI6Sm/jBYcoIIEp1tXfAlMaspGeEMs+tJsmemskov9d2GDL2a3OomUuigzK1XNN+2fiY5JwaYmYyIUHNdh1nGBjXr2a8btjTmGLML8HGE5nijgnwOtrXo+9mxwRC9aK8jgnAW+ijYyIpAt5exASdkz7bYmYPSzqFTPx1DnYm3ME9t4CNqUCRhUmecqqnECoIHVBgXAh3i0+T9JwBO4dFP4NWI1R8urKEufSEpAWEBOgyuNrMehIPNLM/S1pM/h2JtYCX0VtOWa8cSrEwrivNrC9J74nTdCph16sd7+vmZo2Z/UHScYR8u6J8UtK1ZnZZESO5t/EWLF167IPrrL2GYQvTc437mtZ4suHRJlxu9YwW1yzbzJqv1p/Vw51aNKgF+bcaMlXoSCxM6AeguYQykUOijYbHlLPpdKS7t/yW8TEOXfSsUhV6ZwJlJI4eSAjlmZIkuSX/2aFJV46JmV0h6QzgFTmnsqekA4p+2XTgRRRbAJxiZr8t0P+/gTdSLLTmJEkXD6q0cp8o8je1eq8dkpCuNxFE94rerX0m8C7C/+WgKOMz6ACG4JgQ7myXlWd3Ys5+7yPkleUtRPJuSac1506UyAcK9B0D3lzWRFpwIp0/z79nZr04Gl8k5BMeWmhWwac4MxFfzL2D6akEOdn4th+8z0zbxSPJDRojlGdKQ8iSMkqKkuem5DyE8kpJeFgaQpapEtVYMSp73KoKVutjq7Wli37Z6lXjk8yhOh/0ciOO6ufr7ayW+xKHnbFW55uPVVIbBMrXxqQQyad6lazmR2tzvqH6Vi/9Jre5JIKnfu5phcsrzjgkfQD4ZEEzDwCbT9XFpKSz6RyHfbyZndSlrfWBm8ivW3ANsG8Z8cNZJM0hJGfm1U36J7Bz0aRLSW8FvlTEBnCSmRXZeekJSWsTKvFcZGanlWBvCbBRzu7vN7NcIRySPkII7SnKKmAfM/tjCbYmRdLXgDcVNHMT4fd3YHcFJe0MXEc5jtUlZnZIgbm8BfhKgfFfZ2al75pIOhI4p4CJj5nZh8uaTxZJLyNUXGy3fr8O2L/X/ElJGxE+i8vIfboSOCBvmKI7Jk7PbKJD3hCh4+tVvrLOSbNjAlBtcgTS3fZmp4OarXr75GZIrVxwfQxr5xBNdhyndupznuCYZJyHJN1o4rW4ntJEk8ORbWdxi2vtHJNqza8dU5WXfunpLt7WCklfpZw7Um8xsymXuCzpRCYvqflGM+u64oukFxHKQ+b93H+TmZ2Ss29LJH2U/Hdcx4GDzaywaFuSy3MVsGcRM8Dh/QrfaBhIeibwLWArYBmwq5n9vYC9EcLCPm/M/3+Z2XE5x54L/IHiCbgAfwb2GsTNBkkXUbySHMArzGwgO7dJsvQVlPNe3wfsXuTOeBLGeQn5S/LeC+xiZvflnUOLOa1N2MXbMqeJawiOwaqy5pQi6akEkcp2O4yPEP5Pbslp/zWUFx73JTMrEqLrOI4zfZB0icrhAUl5v4D6gqTju5x7z1VtJP1XgffqEUllLGjSuTxd0niB+by7rLkk89lO0tIC85GkRyUdUOa8mua4iaQzWoz7K4VFXl672xR83YUqJEnaX1JccA4pAykSIummkuZ7v6R2eWRlzncjSdeVNOcxSa1KmOeZ13qSbi8wl/MllXKTXZJJ+p8Cc7lH0mZlzKXF3LaVdN8k4xcq/Zu8/p8XeP3NvKys1+84jjNlkTRPYZFcFn+WtOkUeF0LJJ3Ww7wPzDHGiKSfFnivbpW0YQmvdUcFpzAvfUl6lfRiFV8gPyqprMTidF7rSzopsd2O9xew/+qCr/nmEl7jqQXnkBIrh9Pe41y3VHmOlBQW5mVpirSa7zMl3VnSXMdV/u/37pIeLjCnT5c0j08UmMOjkp5SxjxazGsdTe4I/6qksbaVtKrA+5DlEUm79joHD+VyCrGFnr1pzPinBfNCyBbUcmWUzVHJhnVl2tBlm7hLO8o3VhTHtTQgS8KpKtUkBSjR00x1NVtdz7br+noyjTRUrCL+MXI/J3zpuZS+BTyTkPQ8oOxwmbuBN5vZhSXbnRSFMJqXAJ8GernbtlueeHpJqwM/oXNFl07cBDzHzP6Zp7OkvQn/f3kdnB8Ar+pX0qukUkpeEgorvN/M7i4wlz0IIYsvY/IqUO8zs8/mHOeHFNNsiIGNi4TUKIQZ3QosKDCPlGWEcJq+5JtIehshYbhMlgOfAL5gZo+WYVDS7sAHCQUmyuAx4A1mdnpJ9mooqJdfTKhWloeTgA/kyddR2HH5L0JRgDysAA4rI6y0GUnzCJ/XB0zS9GAzK0UzRdLpFC+VnPJ3Qu7Xv7rt4I5JiSy8/TvzVqwevQxTqHY2zZXf07aTjRFR3U/olZ78Xij5/doReP5X92YJTlskVQgx0vv2aYjfEJIxf2xmD/dpDIBUsfdogoDiNjlMbGlmd+Yce01CbHfeO3z3Aq82s0t6GDMC3kEoWpA38faHBKdkfNKWBZD0CcKCrigrCA7KacBVkzlTklYj/G4/i+6rlQl4r5mdnGeCCsnQf6Su7JWX9+SdQ2YuHwI+XnAeKUsICbh/K8keUPvb+TP5cxAm41HgQuAs4Ndmdn8Pc6sAuxLKgx9NKEdcFkuAF5lZ30R+JT0LuID8zsmPCAnxXTvICrvl3wGek3PMR4EjzexnOfu3RaGs8/8A3YTNbZH3ZlGLcV9K79o0nfgT8Mxu/1/cMSmZjZac/gwiLSbSekSJQGOy4q0dJ0KOqh1n7+KnyeGtqmJlE8PjFj/KtGnfv5443n6cvP3dMcnlmCyO4DXf2JPl+X/zZj7JwvYrFK+E0w2PEUSnriPsENwF3AncZWYPdmtEIbF3S0KScvq4I/BkYPOCc1zTzHKXkZY0n5DoWORO+QXApzqV603eg8MJSe55y6yLUDr5o4OqYCTp7cDJFF+wpzwE/B64GXgweb4WsAbhd2M7goJyL5ogK4H/yFuZSKEk9U+AvfP0b+IOQuJtt/o6reazBsHpzbswbeYBwmL6sjKMJfM7Czi4DHtdch/BEbqTsAheBjxMSIBeAKydPG5J+Gwpo9pWMxcQdpTv6YPtBpJdwgvobfc4y0OEHc9TO92lV8gtfDPwNnKUu064g1Dw4g85+7dF0sGE77tub1o9x8z+t6SxDyHsXpXJLcARZvbnyRr21THZ+F0/2NlkH9JIZWS6K7+3sksEcSX5jqyQlAcWRLYQi/dyx8Qdk0kck3ETx317dz5Xk95xJpBsZR8GvAfYZ8jTgbAYXEGoVf8I4Q9gKWGRWSEsEqLMYz9YZWaFFyBJCMMJBBHGIgvwWwk7WX8jLAZHCaFauwH7ExZPeXmIcBd04AKGkg4Dvks5JTTL5u+ERff1vXZMnPxDCeErpRU0AC4jVJkqUqnpasr9O4+BrxPKOd+Rc07rEHYgjqO94OlM5E7g3WZ29iAHVUi1qYoNAAAI9UlEQVQgP4divwdjhLK11xBuLK0gaLcsJDjie1Ls8/ky4CVmdm8BGw0o5O89F3gDve9m/xl4bt5d9MwcjFCOuB+J66uAzxHCFdtGh/R9x2TDt//wKdFodKZFtkXqmASHwiBKHRML55quh3OZ65WkffP1SGGRnzoXqUNgmeNWDkHSRulxCweik12ixJapcR6txi7VMWnvMLhjMk0cE7jD4BXf3ZVf9/L3NJORtBNhF2Fdgt7G4wh3APeknLjzmcQSM9ukLGOSnkwINyoidNgPfkZwSkoJUchDskg6jSDiNxWICaWCj+tm9y5Z7OxCcBQ3A55EWPRs1af5PQKcC/yacEf5LjP7S9OcImB36g78moQ7/ofQXdhKHqqEheplwF8JoUn/zt7tlrQv4fNnHcL79XhgJ0JIVFERyOnEP4FPAd/qR9nbbkhy7z5A2GntZRex36wAPkRYXMd5DEjanrATsl7yk/5N7lDC3H5MKH3+T8LO7B1m1rY4haTdCN+3CwhhgIcm8+knY4TPh18TbmYtAf6Vfk4MJJRrsw+cu161OvZls2h7RsAsCvqQZvWdkMjqOyUNzkp6HK41tE93VDKL/dRhiGu7GolDUElWnQaqpNdCe2Uci9qOSLKKrO2IJDsssqRvpdm5IHFU4gbHJHFeFmJab2o7JuU4Nu6YdNGvyvfnj/Mf39iTpd39Bc0OJF1JCHFyJudGM9u5TINJfsOHCXkg/QgH6YW7CV/+pw1SfK4dyV3EVxKSk4uG4BXhd4TQrau77SDpnYS7lMPiejNr0IdJCjDkDkMskWVmVrvpIalK/3Y5pzoiaGR8A7jAzB4b8nwA0gT+L5C/WEeZXETIpSqUtyTpAuD55UxpUn5uZm11YiTdT3COhs1fzWxHCO5B37nrU0c+ALx0EGNNRTZddsr644y8FbN5wQkxEGHhLkscE6C2WM5+D1vmJ1yrR/1Yi+s09W31nd48BoTP4rh2TZOMUfdoG88r20bC0NoyXs3sutvUjrsFb/vebgw8JMWZceSO42+HmS0HjlcQr/w4YSu/rPyKbnmIsIj+77IqE5VB4hydLuls4O3JT2k7Vl1wBaFq28VTwVFzZgxVwu/W+cD5RUQ6+4WZ/R7YX9IRhMIZZYYedsu1wPFm9sshjD3rGIhjMtu5e61j7wcWDXsew2Iz7X2yic+AdUhms6Y0iyanyjpt7mX6qkXfjhuDTeNmmlo7vy5pZ9njFu0sY09w9fhKPnSW75I45VC6Y5KSxOG/StKHgbcCr6f/oXS3E+6Kfrvf1dCKkDhvn5Z0MqFowGsJd3L7cZf9XkKi9Rmdigs4Tg88AtxAqD54OfCbXop5DBMzOy/ZaXgu8E76H1oZE6p8fc7MStEIcbrDHROn79xl19xMqMrjOE459M0xSUnunr43cVAOJST/HsrkehrdsoSQi7CYUBY1V7z2MEjCXE4n7KJsDBxBWCg9Gcgr1rmCcGf2cuBS4Ff90mpxZiwPE3Yd7yMkrv+DkOdzM/AX4PbpvOOWfEb8GPhxkqdxFOFzqWcRvzaIkJ+xGDhnmLltsxkvF+w4zpRA0uPJX7ZxtnFf3gpDRUhKDO8F7EfQ29iBUKVoziRdlxIqd91IuFt7BSFPZto4I92SlCHdkVD9Z2tCIvUCQjjrCMEBeTB5vIPwvtwK3NyPuP4k+X2Lsu32wHIzuyl7IpP8PmyqTcnvewxzMj3yEPU9/WXAQ/3W95mqJAUq9gOeSkjc3hbYeJJuMSFB/FZCWfgrCDtID/RxqgBI2pZilQp7YZmZ/V+HuezK1NikWDnQ5HfHacVWesKOiu0dZto2m98CMVEt6T7JqYkzx0AIja0fB1V3ksT2dK0TJ/EVaYJ+cqxUEV7UlN8R1pzEXq1Vga4pvzcnt1cEliq7h+e/Hh/naz/ZntwKyI4znUgWmZsSEijnESosxQRn5FGCE9X3L3vHcZyUpMDCpoQy7qsTbp6sAJYTbgzcPVUS/J1G3DGZSuiU0fUYe15EvEP4Xk8V15sW1rWf9tcrtevNfZrttLYRdTFG43UQenCU6ll32BXdx6yKaKvqzkcYegemp03TqlyrTJwHnHzJllzb9Wt3HMdxHMdxarhjMtWQbH0+//QIXi/iw0FrTCwX3KqEbznlfnP0r0L8K6HvzIWz/26Xrcz70rfW4x6nmNeCXmVo46numFjMnyP41nw440ebcn/e1+04juM4juNME8dky69fvJNVeIEqtr9FVFINk8hIYm0IeiOpfkiq5J7omtT0Q5LCl6qtOAFUs0ElnI/TY6NR4ySKgwYK1PtHQuguG7ELjEd/evemxy4v63VvqlNWG+ORQyE+GqrPhnhB3Wlo7TDkd0y6729oTMS/MarnjjF+1n12WVsFz1yIysLx7Z5mkR0J1SMMbT6FHJM/RjHnRjHnXLoJf2k5f8dxHMdxHKdnpoVjkrLZaT9fbzQeO4zIjtCIPSOKbI0hKb8L002M6EJFdt6SzV92Lf2udKFFI+sz56lG9SCDp0G8J8TzBrRjEoNuNOJfi/jnq4h//m/7ybK+vt7a68a2ZutdLNYzUfxMg/0hXnNQjomJuysxl0bw85GYX1y+HncO5HU7juM4juPMMqaVY9LA4sWVhWNr7xJV9BSN2L6xxU82Y7s+OSaPEOlaWXxlHEVXj1RXXXXXjscMNZlzO31x7jLuexKwK8S7QrwzaDuINynimIj4ISO+zajeKHSDwQ2jrLzmDrtoatQ6F9FCNt0hqmqPSOyBaUeItze0FWikgGOyMhL/Z/B/VuUvEVw3z7j+qtW4a4iv1nEcx3EcZ9YwfR2TFiw879K1NbJqm4h4mziyrUW8jVXirWS2Aab5VDQfYx1Fmkek+UQ8iGmFIq0g4iGM5aroLuA2G4lvF7qtOqd625LHV+7Ejp4W9eQXatG8VSzfWoxtGKP1QBtExGsnDshqIh41WJo8f1TED4ix+yG6dx7jd95hP5gaDkiP7CFGH2ajLeLxsY0qFm9ArA1Aa2KaCxqF6hoGDxlIih814mUWxfcprt5bHefem+dzd5PCo+M4juM4jjNA/h//fEhawl+YXwAAAABJRU5ErkJggg==",width= 350)

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        min_width=100,
        min_extended_width=400,
        leading=ft.Image(src_base64="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",height=40),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.HOUSE_OUTLINED, selected_icon=ft.Icons.HOUSE, label="Home"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.PASTE_OUTLINED),
                selected_icon=ft.Icon(ft.Icons.PASTE),
                label="Texts",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.KEY_OUTLINED),
                selected_icon=ft.Icon(ft.Icons.KEY),
                label="Passwords",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icon(ft.Icons.SETTINGS),
                label_content=ft.Text("Settings"),
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.EXIT_TO_APP_OUTLINED,
                selected_icon=ft.Icon(ft.Icons.EXIT_TO_APP),
                label_content=ft.Text("Log out"),
            )
        ],
        on_change=lambda e: railnavig(e.control.selected_index),
    )
    allowdeletedataswitch = ft.Switch(label="Allow delete data without login",value=allowdeletedata, on_change=swithdelchanged)

    deleteuserdatadial = ft.AlertDialog(
        modal=True,
        title=ft.Text("Do you want to delete all data from this account?"),
        content=ft.Text("If you delete this account and all it data you cannot restore it. After delete app close."),
        actions=[
            ft.TextButton("Yes",style=ft.ButtonStyle(color=ft.Colors.RED), on_click=deleteuserdatsetings),
            ft.TextButton("No", on_click=closedeleteuserdat),
        ],actions_alignment=ft.MainAxisAlignment.END)

    deletealluserdatadial = ft.AlertDialog(
        modal=True,
        title=ft.Text("Do you want to delete ALL data and All accounts?"),
        content=ft.Text("If you delete all data and accounts you cannot restore it. After delete app close."),
        actions=[
            ft.TextButton("Yes",style=ft.ButtonStyle(color=ft.Colors.RED), on_click=deletealluserdatsetings),
            ft.TextButton("No", on_click=closedeleteuserdatall),
        ],actions_alignment=ft.MainAxisAlignment.END)
    
    fitslogindialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("First created local account is admin!"),
        content=ft.Text("Only from this account you can manage global settings"),
        actions=[
            ft.TextButton("Ok", on_click=closefitslogindialog),
        ],actions_alignment=ft.MainAxisAlignment.CENTER)
    
    delalluserdat_btn = ft.TextButton("Delete THIS account?",style=ft.ButtonStyle(color=ft.Colors.RED), on_click=lambda e: page.open(deleteuserdatadial))
    deletalleuserdat_btn = ft.TextButton("Delete ALL accounts and All data?",style=ft.ButtonStyle(color=ft.Colors.RED), on_click=lambda e: page.open(deletealluserdatadial))

    passwordadd_btn = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=addpassword)
    servicefield = ft.TextField(label="Service", password=False, width=120,)
    loginfield = ft.TextField(label="Login*", password=False, width=160,on_change=None)
    passwordfield = ft.TextField(label="Password", password=False, width=210,)
    emailfield = ft.TextField(label="Email*", password=False, width=170,on_change=None)
    extrafield = ft.TextField(label="Extra info*", password=False, width=140,on_change=None, multiline=True,min_lines=1,max_lines=2,)

    generatepasswordbtn = ft.FilledButton(text="Generate password", on_click=generatepassword)

    listofiteamssearch = ft.ListView(expand=True, padding=10)

    listoftexts = ft.ListView(expand=True, padding=10)

    

    #page
    homepageconsole = ft.Row(
            [   
                rail,
                ft.VerticalDivider(width=1),
                ft.Column([ft.Row([logooflockbox], alignment=ft.MainAxisAlignment.CENTER),ft.Row([searchbarmain],alignment=ft.MainAxisAlignment.CENTER),listofiteamssearch], alignment=ft.MainAxisAlignment.START, expand=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER, expand=True,
        )
    textconsole = ft.Row(
            [   
                rail,
                ft.VerticalDivider(width=1),
                ft.Column([ listoftexts], alignment=ft.MainAxisAlignment.START, expand=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER, expand=True,
        )
    passwordconsole = ft.Row(
            [   
                rail,
                ft.VerticalDivider(width=1),
                ft.Column([ft.Row([servicefield , loginfield , passwordfield, emailfield,extrafield,]),ft.Row([passwordadd_btn,generatepasswordbtn]), listofpaswordspassword], alignment=ft.MainAxisAlignment.START, expand=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER, expand=True,
        )
    if isuseradmin == True:
        settingsconsole = ft.Row(
            [   
                rail,
                ft.VerticalDivider(width=1),
                ft.Column([ft.Text("Settings", size=70, weight=ft.FontWeight.W_800, selectable=True),allowdeletedataswitch,delalluserdat_btn,deletalleuserdat_btn], alignment=ft.MainAxisAlignment.START, expand=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER, expand=True,
        )
    else:
        settingsconsole = ft.Row(
            [   
                rail,
                ft.VerticalDivider(width=1),
                ft.Column([ft.Text("Settings", size=70, weight=ft.FontWeight.W_800, selectable=True),ft.Text("You don't have acces here. Only admin user can controle settings.", size=50), delalluserdat_btn], alignment=ft.MainAxisAlignment.START, expand=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER, expand=True,
        )

    page.add(homepageconsole)

    if firstlogin == True and isuseradmin == True:
        page.open(fitslogindialog)
    else:
        pass



ft.app(target=main,  assets_dir="assets")
