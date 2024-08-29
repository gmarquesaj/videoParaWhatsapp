import os
import math 
from datetime import timedelta
import platform
import sys

sistema=platform.system()
conversoes=[]
videos=[]
# Definir como o script de conversão sera criado
arqSaida="converter."
if(sistema=='Windows'):
    arqSaida+="bat"
else:
    arqSaida+="sh"

# Criar ou nao uma pasta para cada video
criarPastas=0
# Duracao maxima dos pedaços
segs=59
# inverter ou nao a sequencia de arquivos
inverter=0

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
manterNomeOri=1
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
    videos.append(nome)
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
        print("# NOME::",nome," DUR::",duracao," PED::",pedacos," SOMA::",soma," DIF::",dif,"\n")
        if(dif>1):
            pedacos+=1
        for i in range(0,pedacos):
            ini= timedelta(seconds=i*segs)
            fimi=i*segs+segs
            fim= timedelta(seconds=fimi)
            usargpu=1
            if(math.floor(duracao)<=fimi):
                fim= timedelta(seconds=(duracao))
                usargpu=0
            if(inverter==1):
                va=pedacos-i
            else:
                va=i
            pNum=str(va).zfill(5)

            saida="\"./convertido/"+(nome if manterNomeOri==1 else "")+( "/" if criarPastas==1 else str(vNum).zfill(5)+"_" if manterNomeOri==0 else "_")+pNum+".mp4\"" 
            conversoes.append({"usargpu":usargpu,"duracao":str(duracao),"pedacos":str(pedacos),"nome":nome,"pedaco":va,"soma":str(soma),"dif":str(dif),"inicio":str(ini),"fim":str(fim),"entrada":"\""+f+"\"","saida":saida})

if(criarPastas==1):
    for v in videos:
        if(sistema=='Windows'):
            print("mkdir .\\convertido\\"+v)
        else:
            print("mkdir \"./convertido/"+v+"\"")
reso="720"
#prox="" 

for v in conversoes:
    inicio=v["inicio"]
    fim=v["fim"]
    arqIn=v["entrada"]
    arqOut=v["saida"]
    usargpu=v["usargpu"]
    usargpu=0

    encoder="h264_amf" if sistema=='Windows'else "h264_vaapi" if usargpu==1 else "h264"
   # encoder="copy"
    device="" if sistema=='Windows' else " -vaapi_device /dev/dri/renderD128 "  if usargpu==1 else " "
    qualidade="-b:v 6000k" if sistema=='Windows' else "-qp 20" 
    filtro="" if encoder=="copy" else " -vf scale=-2:"+reso if sistema=='Windows' else " -vf format=nv12,hwupload,scale_vaapi=-2:"+reso if usargpu==1 else " -vf format=nv12,scale=-2:"+reso

    codigo = ffc+"ffmpeg -ss "+inicio+" -to "+fim+" "+device+" -i "+arqIn+"  -c:a mp3 -c:v "+encoder+" "+ filtro+" "+qualidade+" "+arqOut+" -y"
    print(codigo)

 
    

