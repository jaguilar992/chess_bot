import info
import chess
import os
import renderer as drw
import settings
import math

def clean_str(string):
	return string.replace("[","").replace("]","").replace("'","").replace(",","")


######################################################## GAME UTILS
def game_exist(cid):
	fullpath="./games/"
	address=os.path.join(fullpath,'game'+str(cid))
	return os.path.isfile(address)

def delete_game(cid):
	fullpath="./games/"
	address=os.path.join(fullpath,'game'+str(cid))
	if os.path.isfile(address):
		os.remove(address)

def finished(m):
	# print m.is_game_over()
	return (m.is_game_over())

######################################################## MOVE UTILS
def parsed_moves(legal_moves):
	for i in range(0,len(legal_moves)):
		if "#" in legal_moves[i]:
			legal_moves[i]=legal_moves[i].replace("#","")
		if "+" in legal_moves[i]:
			legal_moves[i]=legal_moves[i].replace("+","")
	return legal_moves

def get_legal_moves(cid):
	fen=info.get_info(cid)["fen"]
	board=chess.Board(fen)
	return parsed_moves(str(board.legal_moves).split("(")[1].split(")")[0].replace(" ","").split(","))

def get_step(cid): #OBSOLOTE
    return str(int(info.get_info(cid)["fen"].split(" ")[-1])-1)

######################################################## BOARD UTILS
def send_board_image(bot,cid,str_caption="",silent=False):
    drw.Renderer(cid).draw_fen().save("./photos/"+str(cid)+".png","PNG")
    pic=open("./photos/"+str(cid)+".png")
    bot.send_photo( cid, pic,caption=str_caption,disable_notification=silent)
    # return pic


def check_turn(fen):
	turn=fen.split(" ")[1]
	return turn.upper()
######################################################## USER MOVE MAKERS

def make_user_move(cid,move): #UPDATE FOR ID
	old_fen=info.get_info(cid)["fen"]
	board=chess.Board(old_fen)
	if not finished(board):
		board.push_san(move)
		new_fen=board.fen()
		info.update_info(cid,fen=new_fen)
		if board.is_checkmate():
			move+="#"
		if board.is_check():
			move+="+"
		update_pgn_buffer(cid,move)
		return move
	else:
		return "FINISHED"

def make_allowed_user_move(cid,user,move):
	user=str(user)
	fen=info.get_info(cid)['fen']
	turn=check_turn(fen)
	if turn=="W":
		if info.white(cid)==user:
			move=make_user_move(cid,move)
		else:
			move="INCORRECT_TURN"
	elif turn=="B":
		if info.black(cid)==user:
			move=make_user_move(cid,move)
		else:
			move="INCORRECT_TURN"
	return move

def make_engine_move(cid):
	path="./engines"
	name=settings.get_settings(cid)['engine']
	# print name
	fen=info.get_info(cid)["fen"]
	board=chess.Board(fen)
	if not finished(board):
		engine_name=os.path.join(path,name)
		engine=chess.uci.popen_engine(engine_name)
		engine.uci()
		engine.position(board)
		engine_move=engine.go(movetime=750)[0]
		engine_san=str(board.san(engine_move))
		board.push(engine_move)
		info.update_info(cid,fen=board.fen())
		update_pgn_buffer(cid,engine_san)
		return engine_san
	else:
		return "FINISHED"


def create_pgn_buffer(cid):
	path="./pgn"
	name=str(cid)
	full=os.path.join(path,name)
	file=open(full,"w")
	file.close()
	return True

def update_pgn_buffer(cid,move):
	path="./pgn"
	name=str(cid)
	full=os.path.join(path,name)
	if os.path.isfile(full):
		file=open(full,"a")
		file.write(str(move)+"\n")
		file.close()	
		return True

def get_last_from_pgn(cid):
	# turn 			#game_type
	# W : White 		0: vs Engine
	# B : Black 		1: vs Human
	path="./pgn"
	name=str(cid)
	full=os.path.join(path,name)
	turn=check_turn(info.get_info(cid)["fen"])
	game_type=info.get_info(cid)["game_type"]

	if os.path.isfile(full):
		file=open(full,"r")
		moves=file.readlines()
		file.close()
		new=[]
		for i in range(0,len(moves)):
			if not moves[i]=="\n":
				new+=[moves[i].split("\n")[0]]
		length=len(new)
		par=not bool(length%2)
		pairs=[]
		numb=int(math.ceil(length/float(2)))
		if par:
			for i in range(0,length,2):
				pairs+=[[new[i],new[i+1]]]
		else:
			for i in range(0,length-1,2):
				pairs+=[[new[i],new[i+1]]]
			pairs+=[[new[-1]]]

		if length!=0:
			if (turn=="W"):
				# A imprimir al final de cada turno negro
				return str(numb)+". " +clean_str(str(pairs[-1]))
			if (turn=="B"):
				previous=""
				if numb!=1:
					previous=clean_str(str(pairs[-2]))
					previous=str(numb-1)+". "+previous
				actual=str(numb)+". " +clean_str(str(pairs[-1]))+" ..."
				return previous+"\n"+actual

			# if (turn and game_type):
			# if (turn and game_type):
		print pairs,numb
# print delete_game(-146417536)
# print check_turn("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
# legal_moves=['Na6', 'Nc6', 'Qh4#', 'Qg5', 'Qf6', 'Qe7', 'Ke7', 'Ba3', 'Bb4', 'Bc5', 'Bd6', 'Be7', 'Nf6', 'Nh6', 'Ne7', 'e4', 'a6', 'b6', 'c6', 'd6', 'f6', 'g6', 'h6', 'a5', 'b5', 'c5', 'd5', 'f5', 'g5', 'h5']
# print parsed_moves(legal_moves)

