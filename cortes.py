import os
import math 
from datetime import timedelta
import platform
import sys
from dataclasses import dataclass
@dataclass
class conversao:
    inicio : str
    fim : str
    arqIn :str
    arqOut :str
    usarGpu : bool
    duracao:str
    pedacos:str
    pedaco:int
    nome:str
    soma:str
    dif:str
niveisDeLog=[ "quiet"  ,"panic"  ,"fatal"  ,"error"  ,"warning","info"   ,"verbose","debug"]
#  -------------------------------------------
#---------------CONFIGURAÇÕES----------------------
#--------------------------------------------------
# resolucao
reso:str="480"
# Criar ou nao uma pasta para cada video
criarPastas:bool=1
# Duracao maxima dos pedaços
segs:int=29
# inverter ou nao a sequencia de arquivos
inverter:bool=1
#usar copy como encoder
copiar:bool=0
#manter o nome original do video,se nao nomear o video com um numero ordenado
manterNomeOri:bool=0
nivelLog:int=4
fps:int=24
#--------------------------------------------------

sistema:str=platform.system()

def gerarCodigo(v:conversao):
    encoder:str="copy" if copiar== 1 else "h264_amf" if sistema=='Windows'else "h264_vaapi" if v.usarGpu==1 else "h264"
    device:str="" if sistema=='Windows' else " -vaapi_device /dev/dri/renderD128 "  if v.usarGpu==1 else " "
    qualidade:str="-b:v 6000k" if sistema=='Windows' else "-qp 20" 
    filtro:str="" if copiar== 1 else " -vf scale=-2:"+reso if sistema=='Windows' else " -vf format=nv12,hwupload,scale_vaapi=-2:"+reso if v.usarGpu==1 else " -vf format=nv12,scale=-2:"+reso
    filtro+= ""if (copiar== 1 or fps==0 ) else ",fps="+str(fps)
    log:str= "" if nivelLog==-1 else "-loglevel "+niveisDeLog[nivelLog]
    codigo:str = ffc+"ffmpeg "+log+" -ss "+v.inicio+" -to "+v.fim+" "+device+" -i "+v.arqIn+"  -c:a mp3 -c:v "+encoder+" "+ filtro+" "+qualidade+" "+v.arqOut+" -y"
    return codigo
def criarDiretorio(nome):
     return "mkdir .\\convertido\\"+nome if(sistema=='Windows') else  "mkdir \"./convertido/"+nome+"\""
 


# Definir como o script de conversão sera criado
arqSaida="converter."
if(sistema=='Windows'):
    arqSaida+="bat"
else:
    arqSaida+="sh"


file = open(arqSaida, "w")
sys.stdout = file

# Caminho do ffmpeg
ffc=''
if(sistema=='Windows'):
    ffc='C:\\Users\\gmarq\\Downloads\\ffmpeg-2024-04-15-git-5e380bcdb1-full_build\\ffmpeg-2024-04-15-git-5e380bcdb1-full_build\\bin\\'
    print("@echo off")
else:
    print("#!/bin/sh -x")
# Caminho dos arquivos de entrada
arqs=os.listdir("./converter/")
# Excluir arquivos que ja foram processados antes e recriar a pasta
if(sistema=='Windows'):
    print("rmdir /s /q convertido")
    print("mkdir .\\convertido\\")
else:
    print("rm -f -R ./convertido/")
    print("mkdir ./convertido/")
   # print("q=25")

# Para cada arquivo encontrado, cria uma pasta com o nome do arquivo, usa ffprobe para saber a duraçao do arquivo
# e ffmpeg para criar copias de no maximo "segs" segundos, de todo o arquivo, convertendo se necessario para uso no whatsapp
print("clear")
vNum=0
for f in arqs:
    nome=f[:len(f)-4]
  
    f= "./converter/"+f
    if(os.path.isfile(f)==False):
        print("arquivo invalido \"",f,"\"")
    else:
        result = os.popen(ffc+'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \"'+f+"\"").read()
        vNum=vNum+1
        duracao = (float(result[:len(result)-1]))
        pedacos = max(1,math.floor(duracao/segs))
        soma = pedacos*segs
        dif = duracao - soma
        print("\n# NOME::",nome," DUR::",duracao," PED::",pedacos," SOMA::",soma," DIF::",dif)
        if(criarPastas==1):
         print(criarDiretorio(nome))
        if(dif>1):
            pedacos+=1
        for i in range(0,pedacos):
            ini= timedelta(seconds=i*segs)
            fimi=i*segs+segs
            fim= timedelta(seconds=fimi)
            usarGpu=1
            if(math.floor(duracao)<=fimi):
                fim= timedelta(seconds=(duracao))
                usarGpu=0
            if(inverter==1):
                va=pedacos-i
            else:
                va=i
            pNum=str(va).zfill(5)

            saida="\"./convertido/" +(nome+"/"if(criarPastas==1) else "" )+(nome if(manterNomeOri==1) else str(vNum).zfill(5))+"_"+pNum+".mp4\""

            conv =conversao(usarGpu=usarGpu, duracao=str(duracao), pedacos=str(pedacos),nome=nome, pedaco=va, soma=str(soma),dif=str(dif), inicio=str(ini), fim=str(fim), arqIn="\""+f+"\"", arqOut=saida)
           # conversoes.append(conv)
            print(gerarCodigo(conv))





