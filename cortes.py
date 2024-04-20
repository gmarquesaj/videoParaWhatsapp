import os
import math 
from datetime import timedelta
import platform
import sys
file = open("teste.bat", "w")
sys.stdout = file
sistema=platform.system()
#caminho do ffmpeg
ffc=''
if(sistema=='Windows'):
    ffc='C:\\Users\\gmarq\\Downloads\\ffmpeg-2024-04-15-git-5e380bcdb1-full_build\\ffmpeg-2024-04-15-git-5e380bcdb1-full_build\\bin\\'
    print("@echo off")
#caminho dos arquivos de entrada
arqs=os.listdir("./teste/")
if(sistema=='Windows'):
    print("rmdir /s /q conv")
    print("mkdir .\\conv\\")
else:
    print("rm -f -R ./conv/")
    print("mkdir ./conv/")
segs=25
for f in arqs:
    nome=f[:len(f)-4]
    f= "./teste/"+f
    if(os.path.isfile(f)==False):
        print("arquivo invalido \"",f,"\"")
    else:
        result = os.popen(ffc+'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \"'+f+"\"").read()
        duracao = (float(result[:len(result)-1]))
        pedacos = max(1,math.floor(duracao/segs))
        soma = pedacos*segs
        dif = duracao - soma
        if(sistema=='Windows'):
            print("\n:: \"",nome,"\" | duracao : ",duracao," | pedacos : ",pedacos," soma ",soma," dif ",dif)
            print("mkdir \".\\conv\\"+nome+"\"")
        else:
            print("\n# \"",nome,"\" | duracao : ",duracao," | pedacos : ",pedacos," soma ",soma," dif ",dif)
            print("mkdir ./conv/"+nome)
        if(dif>1):
            pedacos+=1
        for i in range(0,pedacos):
            ini= timedelta(seconds=i*segs)
            fim= timedelta(seconds=i*segs+segs)
            codigo = ffc+"ffmpeg -ss "+str(ini)+" -to "+str(fim)+" -i \""+f+"\"  -c:a mp3 -c:v h264_amf -vf \"scale=-2:720\" -b:v 6000k \"./conv/"+nome+"/"+nome+"_"+str(i+1)+".mp4\" -y"
         #   codigo = "ffmpeg -ss "+str(ini)+" -to "+str(fim)+" -i \""+f+"\"  -c:a mp3 -c:v hevc_amf \"./conv/"+nome+"/"+nome+"_"+str(i+1)+".mp4\" -y"
            print(codigo)
#if(sistema=='Windows'):
#    print("pause")
    

