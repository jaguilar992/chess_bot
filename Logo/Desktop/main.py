from Renderer import *

import os
import chess
import chess.uci
import utils.info as info
import utils.chessUtils as csu

engines_path="/home/antonio/Escritorio/Chess/engines/"
engines_names=["arasan","critter","fruit","greko","jazz","komodo","rocinante","stockfish","toga"]
engine_name=engines_names[3]
engine_file=os.path.join(engines_path,engine_name)
engine=chess.uci.popen_engine(engine_file)
engine.uci()

info.create_info(1)
ditc=info.get_info(1)
fen=ditc["fen"]
board=chess.Board(fen)

user_pieces_color=str(raw_input("Select color (B/W): ").upper())
if user_pieces_color=="B":
	info.update_info(1,flipped="1")

rend=Renderer(1)
rend.draw_fen().save("0.jpg","JPEG")

while (not board.is_checkmate() and not board.is_stalemate()):
	turn=csu.check_turn(board.fen())
	if turn==user_pieces_color:
		legal_moves=csu.parsed_moves(str(board.legal_moves).split("(")[1].split(")")[0].replace(" ","").split(","))
#		print legal_moves
		move=str(raw_input("user_move: "))
		while not move in legal_moves:
			print "Invalid move...\n"
			move=str(raw_input("user_move: "))
			move=move.replace("#","")
			move=move.replace("+","")
		board.push_san(move)
	else:
		engine.position(board)
		best_move=engine.go(movetime=1000)[0]
		print "uci_move: "+str(board.san(best_move))
		print
		board.push(best_move)

	info.update_info(1,fen=board.fen())
	rend=Renderer(1)
	rend.draw_fen().save("0.jpg","JPEG")
	ditc=info.get_info(1)
	fen=ditc["fen"]
	board=chess.Board(fen)
	# print 
	# print board


