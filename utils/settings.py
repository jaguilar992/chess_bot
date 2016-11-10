import os
from themes import THEMES
from engines import ENGINES
from info import update_info
def create_settings(cid):
	path="./settings"
	name="st"+str(cid)
	full=os.path.join(path,name)
	if not os.path.isfile(full):
		file=open(full,"w")
		file.write("theme: wood\n")
		file.write("engine: stockfish")
	# print file

def get_settings(cid):
	path="./settings"
	full=os.path.join(path,'st'+str(cid))
	if os.path.isfile(full):
		file=open(full,"r")
		info={}
		lines1=file.readlines()
		for line in lines1:
			if len(line)!=1:
				line=line.split("\n")[0].split(": ")
				if line[0]!="fen":
					info[line[0]]=str(line[1]).replace(" ","")
				else:
					info[line[0]]=str(line[1])
		file.close()
		return info
	else:
		default={
				"theme": "wood",
				"engine": "stockfish",
		}
		return default

def update_settings(cid,theme="N",engine="N"):
	info=get_settings(cid)
	if theme!="N" and theme.lower() in THEMES:
		info["theme"]=theme.lower()
		update_info(cid,theme=theme.lower())
	if engine!="N" and engine.lower() in ENGINES:
		info["engine"]=engine.lower()
	
	path="./settings/"
	full=os.path.join(path,'st'+str(cid))
	if os.path.isfile(full):
		file=open(full,"w")
		for key in info.keys():
			file.write(key+": "+info[key]+"\n")
		file.close()
	return info

def settings_exist(cid):
	fullpath="./settings/"
	address=os.path.join(fullpath,'st'+str(cid))
	return os.path.isfile(address)