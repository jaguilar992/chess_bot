import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import utils.themes as th
from utils.info import *
# Chess piece images: https://en.wikipedia.org/wiki/Chess_piece
# Attribution: By en:User:Cburnett - Own work. This vector image was created with Inkscape., CC BY-SA 3.0




class Renderer():
	'''Renderer class that will convert chess positions to images'''
	
	def __init__(self,cid=0):
		'''Pre-draw an empty board and pre-load the pieces'''
		self.info=get_info(cid)
		self.theme=self.info["theme"]
		self.isflipped=bool(int(self.info["flipped"]))
		self.size=60
		self.grid_size = (self.size,self.size)
		self.board = self.draw_empty_board()
		self.piece_locations = './pieces'
		self.pieces, self.masks = self.load_pieces()

	def grid_to_coords(self, grid):
		coords = [grid[i] * self.grid_size[i] for i in range(2)] * 2
		coords[2] += self.grid_size[0]
		coords[3] += self.grid_size[1]
		return coords
 
	def draw_empty_board(self):
		'''Draws an empty 8x8 board with axis labels
		Coordinate wise, we are going to draw a 10x10 grid, with the 8x8 board inside'''

		# Create a white 10x10 board
		# 'L' mode stands for greyscale
		board = Image.new('RGB', [10*x for x in self.grid_size], color="#ffffff")

		# Fill in the black cells with grey
		[text_color,lightcolor,darkcolor]=th.THEMES[self.theme]
		white_cells = [(r,c) if r % 2 != 0 else (r,c+1) for r in range(1,9) for c in range(1,9,2)]
		black_cells = [(r,c) if r % 2 == 0 else (r,c+1) for r in range(1,9) for c in range(1,9,2)]
		for bc in white_cells:
			ImageDraw.Draw(board).rectangle(self.grid_to_coords(bc), fill = lightcolor)
		for bc in black_cells:
			ImageDraw.Draw(board).rectangle(self.grid_to_coords(bc), fill = darkcolor)

		# Draw black outline for board
		ImageDraw.Draw(board).line([self.grid_size[0], self.grid_size[1], 9 * self.grid_size[0], self.grid_size[1]], width=int(0.06*self.size), fill=darkcolor)
		ImageDraw.Draw(board).line([self.grid_size[0], self.grid_size[1], self.grid_size[0], 9 * self.grid_size[1]], width=int(0.06*self.size), fill=darkcolor)
		ImageDraw.Draw(board).line([9 * self.grid_size[0], self.grid_size[1], 9 * self.grid_size[0], 9 * self.grid_size[1]], width=int(0.06*self.size), fill=darkcolor)
		ImageDraw.Draw(board).line([self.grid_size[0], 9 * self.grid_size[1], 9 * self.grid_size[0], 9 * self.grid_size[1]], width=int(0.06*self.size), fill=darkcolor)

		# Write down axis
		if self.isflipped:
			letters = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']
			axes = [[str(i), j * self.grid_size[0], i * self.grid_size[1]] for i in range(1,9) for j in [0,9]]
		else:
			letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
			axes = [[str(9-i), j * self.grid_size[0], i * self.grid_size[1]] for i in range(1,9) for j in [0,9]]
		
		axes += [[letters[i-1], i * self.grid_size[0], j * self.grid_size[1]] for i in range(1,9) for j in [0,9]]
		font = ImageFont.truetype("./fonts/HelvLight Regular.ttf", int(0.33*self.size))
		for [txt, x, y] in axes:
			# Add __ * self.grid_size to try to center the text
			ImageDraw.Draw(board).text((x + 0.35*self.grid_size[0], y + 0.35*self.grid_size[1]), txt, font=font,fill=text_color)

		return board

	def load_pieces(self):
		'''Loads in chess pieces'''
		white, black = 'KQBNRP', 'kqbnrp'
		piece_images = dict(zip(white,
			(Image.open('{}/w{}.png'.format(self.piece_locations, p)).resize(self.grid_size) for p in white)))
		piece_images.update(dict(zip(black,
			(Image.open('{}/b{}.png'.format(self.piece_locations, p)).resize(self.grid_size) for p in black))))
		piece_masks = dict((piece, img.split()[3]) for piece, img in piece_images.items())
		return piece_images, piece_masks

	# Modified from http://wordaligned.org/articles/drawing-chess-positions
	def expand_fen(self, fen):
		'''Expand the digits in an FEN string into spaces
		E.g. 'rk4q3' becoes 'rk    q   '
		'''
		def expand(match):
			return ' ' * int(match.group(0))
		return re.compile(r'\d').sub(expand, fen).replace('/','')

	def draw_fen(self):
		'''Draws a chess board position from a given FEN chess position'''
		# Replace numbers in fen with spaces
		# print(fen)
		fen=self.info["fen"]
		
		if self.isflipped:
			points = filter(lambda x: x[0] != ' ',
				[(p, pt) for (p, pt) in zip(self.expand_fen(fen), [(r,c) for c in range(8,0,-1) for r in range(8,0,-1)])])
		else:
			points = filter(lambda x: x[0] != ' ',
			[(p, pt) for (p, pt) in zip(self.expand_fen(fen),
										[(r,c) for c in range(1,9) for r in range(1,9)])])
		board = self.board # Get empty board
		
		ref=self.size*10
		if self.isflipped:
			white_signal=[ref*0.93,ref*0.03,ref*0.97,ref*0.07]
			black_signal=[ref*0.93,ref*0.93,ref*0.97,ref*0.97]
		else:
			white_signal=[ref*0.93,ref*0.93,ref*0.97,ref*0.97]
			black_signal=[ref*0.93,ref*0.03,ref*0.97,ref*0.07]

		player=fen.split(" ")[1]
		if player=="w":
			coords=white_signal
		else:
			coords=black_signal
		[text_color,lightcolor,darkcolor]=th.THEMES[self.theme]
		ImageDraw.Draw(board).ellipse(coords, fill=darkcolor)
		
		for (p, pt) in points:
			board.paste(self.pieces[p], self.grid_to_coords(pt), self.masks[p])
		return board

###############
# For testing #
###############
# cid=-146417536
# rend = Renderer(cid)
# rend.draw_fen().save(str(cid)+".jpg", "JPEG")
