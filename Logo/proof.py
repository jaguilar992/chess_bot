import utils.chessUtils as csu
import utils.info as info


# print csu.get_legal_moves(-146417536)
import chess

board=chess.Board("rnb1kbnr/1ppp1ppp/p7/4p3/6Pq/4PP2/PPPP3P/RNBQKBNR w KQkq - 1 4")

print str(board.legal_moves).split("(")[1].split(")")[0].replace(" ","").split(",")