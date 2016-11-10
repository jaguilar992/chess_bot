import chess.uci
import os
import chess

lista=os.listdir(".")
#print lista

for eng in lista:
	if not (len(eng.split("."))==2):
		print eng ,"\n"
		play=chess.uci.popen_engine("./"+eng)
		play.uci()
		board=chess.Board()
		play.position(board)
		print play.go(movetime=1000)
		play.quit()

