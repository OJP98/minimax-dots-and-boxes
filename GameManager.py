from Algorithm import Algorithm
import numpy as np
import time

class GameManager:
	def __init__(self, _username, _tid):
		self.username = _username
		self.tid = _tid
		self.game_id = ''
		self.board = [[99 for i in range(30)] for j in range(2)]
		# El jugador que actualmente está haciendo la jugada
		self.player_id = 0
		# El id del oponente
		self.opponent_id = 0


	def Reset(self):	
		self.player_id = 0
		self.opponent_id = 0
		self.game_id = ''
		self.board = [[99 for i in range(30)] for j in range(2)]


	def printBoard(self):
		res = ''
		stacker = 0

		for i in range(int(len(self.board[0])/5)):
			if self.board[0][i] == 99:
				res = res + '*   '
			else:
				res = res + '* - '
			if self.board[0][i+6] == 99:
				res = res + '*   '
			else:
				res = res + '* - '
			if self.board[0][i+12] == 99:
				res = res + '*   '
			else:
				res = res + '* - '
			if self.board[0][i+18] == 99:
				res = res + '*   '
			else:
				res = res + '* - '
			if self.board[0][i+24] == 99:
				res = res + '*   *\n'
			else:
				res = res + '* - *\n'

			if i != 5:
				for j in range(int(len(self.board[1])/5)):
					if self.board[1][j + stacker] == 99:
						res = res + '    '
					else:
						res = res + '|   '
				stacker = stacker + 6
				res = res + '\n'

		return res