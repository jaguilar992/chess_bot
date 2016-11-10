import os
# import string
def get_info(cid):
	fullpath="./games/"
	address=os.path.join(fullpath,'game'+str(cid))
	if os.path.isfile(address):
		file=open(address,"r")
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
				"id": "0",
				"game_type": "0",
				"theme": "wood",
				"white": "0",
				"black": "0",
				"fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
				"flipped":"0",
				"uci_white":"0",
		}
		return default

def create_info(cid):
	fullpath="./games/"
	address=os.path.join(fullpath,'game'+str(cid))
	file=open(address,"w")
	file.write("id: "+str(cid)+"\n")
	file.write("theme: "+"wood"+"\n")
	file.write("flipped: "+"0"+"\n")
	file.write("game_type: "+"0"+"\n")
	file.write("uci_white: "+"0"+"\n")
	file.write("white: "+"0"+"\n")
	file.write("black: "+"0"+"\n")
	import chess
	fen=chess.Board().fen()
	file.write("fen: "+fen+"\n")
	file.close()

def update_info(cid,theme="N",flipped="N",game_type="N",uci_white="N",white="N",black="N",fen="N"):
	info=get_info(cid)
	if theme!="N":
		info["theme"]=theme
	if flipped!="N":
		info["flipped"]=flipped
	if game_type!="N":
		info["game_type"]=game_type
	if uci_white!="N":
		info["uci_white"]=uci_white
	if white!="N":
		info["white"]=white
	if black!="N":
		info["black"]=black
	if fen!="N":
		info["fen"]=fen
	fullpath="./games/"
	address=os.path.join(fullpath,'game'+str(cid))
	if os.path.isfile(address):
		file=open(address,"w")
		for key in info.keys():
			file.write(key+": "+info[key]+"\n")
		file.close()
	return info


def is_ready_info(cid):
	info=get_info(cid)
	black=info['white']!="0"
	white=info['black']!="0"
	return white and black

def white(cid):
	info=get_info(cid)
	return info['white']


def black(cid):
	info=get_info(cid)
	return info['black']
# print update_info(-146417536, game_type="0",white="47917685",theme="blue")