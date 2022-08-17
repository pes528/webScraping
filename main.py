import requests
import lxml.html as html
import os
import datetime
import time
import pytz

#ESTE SCRIPT EXTRAE DE MANERA AUTOMATICA LAS NOTICIAS DEL SECTOR ECONOMICO DEL PERIODICO EL DEBER.COM [TAREA PARA LA FACULTAD DE ECONOMIA FCEFA 1ER AÑO ]    

#AUTHOR: MIGUEL
#TELEGRAM: @pes528

#PARA ENVIAR LOS ARCHIVOS AL CANAL DE TELEGRAM, EL BOT DEBE SER ADMINISTRADOR DEL CANAL

#la diferencia entre el sector economia y el sector economia/dinero es que el sector economia se actualiza constantemente en cambio el sector
#economia/dinero lo hace de manera diferente y mas tardia y los xpath de ambos sectores son distintos






#---------------------LINKS----------------------------------------
#$x("//div[@class='layout']/div[not(@class='area area-temp-40 area--title__image area--txt__light area--tematica area--tematica__txt-light')]//a[@class='jsx-2404121536 nota-link']/@href"
#link=https://eldeber.com.bo/economia
sectorEconomia="//a[@class='jsx-742874305 nota-link']/@href"
#link="https://eldeber.com.bo/economia/dinero"
sectorEconomiaDinero= "//div[@class='layout']/div[not(@class='area area-temp-40 area--title__image area--txt__light area--tematica area--tematica__txt-light')]//a[@class='jsx-2404121536 nota-link']/@href" #links filtrados
#"//a[@class='jsx-2404121536 nota-link']/@href" >>>>#links completos de noticias el deber
TITLE="//div[@class='text']/h1/text()" #titulo
h2="//article/h2/text()" #h2
texto = "//div[@class='text-editor']/div[not(@class)]/p//text()"
#"//div[@class='text-editor']/div[not(@class)]/p[not(@class)]/text()" #texrto?
#--------------------------------------------------------------------


#-----------------------FUNCIONES UTILITARIAS-------------------------
def enviaMensaje(mensaje):
    user="NOMBRE DEL CANAL" #<<<<NOMBRE DEL CANAL DE TELEGRAM
    token="TOKEN" #<<<<<<<<<<<<<<TOKEN DEL BOT
    pay={"chat_id":user,"text":mensaje}
    res=requests.get(f"https://api.telegram.org/bot{token}/sendMessage", data=pay)

def linkoficial(noticed):
    noticiasLinks = []
    for i in noticed:
        noticiasLinks.append("https://eldeber.com.bo"+i)

    return noticiasLinks
#------------------------------------------------------------------------

#-------------------------------------------------------ECONOMIA------------------------------------------------

def parceNoticed(link, today):
    try:
        response = requests.get(link)
        if response.status_code==200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            title = parsed.xpath(TITLE)[0]
            title = title.replace("\"", "")
            sumary = parsed.xpath(h2)[0]
            cuerpo = parsed.xpath(texto)
            e = open(today, "a", encoding="utf-8")
            e.write(f"TITULO: {title}\n\n")
            e.write(f"RESUMEN: {sumary}\n\n")
            e.write("CUERPO: \n")
            for i in cuerpo:

                e.write(f"{str(i)}")
            e.write("\n")    
            e.write(f"{'-'*100}\n\n")    
            e.close()
            


        else:
             enviaMensaje("ocurrio un error al escribir los datos en el archivo")
            

    except:
        enviaMensaje("ocurrio un error en la funcion ParsedNoticed")



def parseMode():
    try:
        response = requests.get("https://eldeber.com.bo/economia")#si se usa el link economiaDinero no olvidar adjuntar /dinero en este link, en cambio si es solo economia omitir el /dinero
        if response.status_code==200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            noticed = parsed.xpath(sectorEconomia)
            links = linkoficial(noticed=noticed)
            print("hecho")
            today =f"noticiasEconomia-{datetime.date.today().strftime('%d-%m-%Y')}.txt"
            print(links)
            for linkNoticias in links:
                parceNoticed(linkNoticias, today)

        elif response.status_code==401:
            enviaMensaje(response.status_code)
        else:
            enviaMensaje("ocurrio un error en la funcion principal")

    except:
        enviaMensaje("ocurrio un error en la peticion principal")
#---------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------ECONOMIA/DINERO-----------------------------------------------------------------------
def parcedEcoDin(link, today):
    try:
        response = requests.get(link)
        if response.status_code==200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            title = parsed.xpath(TITLE)[0]
            title = title.replace("\"", "")
            sumary = parsed.xpath(h2)[0]
            cuerpo = parsed.xpath(texto)
            e = open(today, "a", encoding="utf-8")
            e.write(f"TITULO: {title}\n\n")
            e.write(f"RESUMEN: {sumary}\n\n")
            e.write("CUERPO: \n")
            for i in cuerpo:

                e.write(f"{str(i)}")
            e.write("\n")    
            e.write(f"{'-'*100}\n\n")    
            e.close()
            


        else:
             enviaMensaje("ocurrio un error al escribir los datos en el archivo EcoDin")
            

    except:
        enviaMensaje("ocurrio un error en la funcion ParsedNoticed EcoDin")



def EconomiaDinero():
    try:
        response = requests.get("https://eldeber.com.bo/economia/dinero")#si se usa el link economiaDinero no olvidar adjuntar /dinero en este link, en cambio si es solo economia omitir el /dinero
        if response.status_code==200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            noticed = parsed.xpath(sectorEconomiaDinero)
            links = linkoficial(noticed=noticed)
            print("hecho")
            today =f"noticiasEconomiaDinero-{datetime.date.today().strftime('%d-%m-%Y')}.txt"
            print(links)
            for linkNoticias in links:
                parcedEcoDin(linkNoticias, today)


        else:
            enviaMensaje("ocurrio un error en la funcion principal EconomiaDinero")

    except:
        enviaMensaje("ocurrio un error en la peticion principal EcoDin")
#----------------------------------------------------------------------------------------------------------------

#--------------------------------CLASE PARA ENVIAR LOS ARCHIVOS A TELEGRAM----------------------------------------

#REQUISITOS: CANAL DE TELEGRAM Y BOT

class sendFile:

    def __init__(self):
        self.telegram="https://api.telegram.org/bot"
        self.TOKEN="TOKEN" #-------------TOKEN DEL BOT------ 
        self.channel="CANAL DE TELEGRAM" #------------NOMBRE DEL CANAL DE TELEGRAM-------
        self.verificado=False
        self.nameFileEconomia=f"noticiasEconomia-{datetime.date.today().strftime('%d-%m-%Y')}.txt"
        self.nameFileEcoDinero=f"noticiasEconomiaDinero-{datetime.date.today().strftime('%d-%m-%Y')}.txt"
        self.enviado = False
    
    
    def verifica(self):
        if os.path.isfile(self.nameFileEconomia) and os.path.isfile(self.nameFileEcoDinero):
            self.verificado=True
        else:
            enviaMensaje("1 o ambos Archivos no encontrados, verificar links o funciones ")
            print("archivos no encontrados")  

   


    def envia(self):
        hora = datetime.datetime.now(pytz.timezone("America/La_Paz"))
        if self.verificado:
            enviaMensaje(f"Enviando noticias al la fecha de hoy: {datetime.date.today().strftime('%d-%m-%Y')}:{hora.strftime('%H:%M:%S')}")
            nombreArchivos=[self.nameFileEcoDinero, self.nameFileEconomia]
            cont = 0
            for i in nombreArchivos:

        
                data={"chat_id":self.channel}
                file={"document": open(f"{nombreArchivos[cont]}", "rb")}
                requests.get(f"{self.telegram}{self.TOKEN}/sendDocument", data=data , files=file)
                print("hecho")
                cont +=1
            self.enviado = True
        else:
            enviaMensaje("no pude enviar los archivos class sendFile > envia")
            print("class > envia < algo salio mal")

    
    def removeFile(self):
        if self.enviado:
            cont=0
            names = [self.nameFileEcoDinero, self.nameFileEconomia]
            for i in names:
                os.remove(names[cont])
                cont += 1
            enviaMensaje("""Aclarar que el sector ECONOMIA/DINERO no se actualiza constantemente como si lo hace el sector /ECONOMIA
            \nEntonces podrian existir noticias repetidas en el archivo noticias/economia/dinero
            \nEsto es responsalibilidad del sitio web de noticias :/
            \nContacto: @pes528""")    
            print("archivos eliminados")   


#------------------------------------------------------------------------------------------------------------------------
enviar=sendFile()

#---FUNCION PRINCIPAL-------------
def run():
    enviaMensaje("iniciando...")
    parseMode()
    EconomiaDinero()
    time.sleep(5)
    enviar.verifica()
    
    enviar.envia()
    time.sleep(2)
    enviar.removeFile()
    


if __name__ == "__main__":
#PARA EJECUTAR EL SCRIPT CADA DIA INCLUIR UN WHILE TRUE CON UN TIME.SLEEP DE 86400 O UN CRONTAB EN LA MAQUINA
      
    run()
          
