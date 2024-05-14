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
    encoder="h264_amf"
else:
    arqSaida+="sh"
    encoder="h264_vaapi"

file = open(arqSaida, "w")
sys.stdout = file

# Caminho do ffmpeg
ffc=''
if(sistema=='Windows'):
    ffc='C:\\Users\\gmarq\\Downloads\\ffmpeg-2024-04-15-git-5e380bcdb1-full_build\\ffmpeg-2024-04-15-git-5e380bcdb1-full_build\\bin\\'
    print("@echo off")

# Caminho dos arquivos de entrada
arqs=os.listdir("./converter/")

# Excluir arquivos que ja foram processados antes e recriar a pasta
if(sistema=='Windows'):
    print("rmdir /s /q convertido")
    print("mkdir .\\convertido\\")
else:
    print("rm -f -R ./convertido/")
    print("mkdir ./convertido/")

# Duracao maxima dos pedaços
segs=25

# Para cada arquivo encontrado, cria uma pasta com o nome do arquivo, usa ffprobe para saber a duraçao do arquivo
# e ffmpeg para criar copias de no maximo "segs" segundos, de todo o arquivo, convertendo se necessario para uso no whatsapp

for f in arqs:
    nome=f[:len(f)-4]
    videos.append(nome)
    f= "./converter/"+f
    if(os.path.isfile(f)==False):
        print("arquivo invalido \"",f,"\"")
    else:
        result = os.popen(ffc+'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \"'+f+"\"").read()
        duracao = (float(result[:len(result)-1]))
        pedacos = max(1,math.floor(duracao/segs))
        soma = pedacos*segs
        dif = duracao - soma

        if(dif>1):
            pedacos+=1
        for i in range(0,pedacos):
            ini= timedelta(seconds=i*segs)
            fim= timedelta(seconds=i*segs+segs)
            conversoes.append({"duracao":str(duracao),"pedacos":str(pedacos),"nome":nome,"pedaco":i+1,"soma":str(soma),"dif":str(dif),"inicio":str(ini),"fim":str(fim),"entrada":"\""+f+"\"","saida":"\"./convertido/"+nome+"/"+str(i+1).zfill(5) +".mp4\""})


for v in videos:
    if(sistema=='Windows'):
       print("mkdir .\\convertido\\"+v)
    else:
       print("mkdir \"./convertido/"+v+"\"")
for v in conversoes:
    codigo=""
    if(sistema=='Windows'):
        codigo = ffc+"ffmpeg -ss "+v["inicio"]+" -to "+v["fim"]+" -i "+v["entrada"]+"  -c:a mp3 -c:v "+encoder+" -vf \"scale=-2:720\" -b:v 6000k "+v["saida"]+" -y"
    else:
        codigo = ffc+"ffmpeg -ss "+v["inicio"]+" -to "+v["fim"]+" -vaapi_device /dev/dri/renderD128 -i "+v["entrada"]+"  -c:a mp3 -c:v "+encoder+" -vf \"format=nv12,hwupload,scale_vaapi=-2:720\"  -f mp4  -qp 20 "+v["saida"]+" -y"
    print(codigo)

    

