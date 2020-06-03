from math import inf
import random
import numpy as np

# Constants
EMPTY = 99
FILL = 0
FILLEDP11 = 1
FILLEDP12 = 2
FILLEDP21 = -1
FILLEDP22 = -2
N = 6

ROWS = 30
COLS = 2


class Algorithm():
	def __init__(self, look_ahead):
		super(Algorithm, self).__init__()
		# Tomar en cuenta el look ahead como parte de la clase.
		self.look_ahead = look_ahead


	def setData(self, player_id):
		# Setear data del match, más específicamente el id del 
		# player y el oponente
		self.player_id = player_id
		if player_id == 1: self.opponent_id = 2
		else: self.opponent_id = 1


	def doMovement(self, movement, player_id, tempBoardIn):
		tempBoard = list(map(list, tempBoardIn))
		initialScore = 0
		finalScore = 0
		stacker = 0
		counter = 0

		for i in range(len(tempBoard[0])):
			if ((i + 1) % N) != 0:
				if tempBoard[0][i] != EMPTY and tempBoard[0][i + 1] != EMPTY and tempBoard[1][counter + stacker] != EMPTY and tempBoard[1][counter + stacker + 1] != EMPTY:
					initialScore = initialScore + 1
				stacker = stacker + N
			else:
				counter = counter + 1
				stacker = 0

		tempBoard[movement[0]][movement[1]] = FILL

		stacker = 0
		counter = 0

		for i in range(len(tempBoard[0])):
			if ((i + 1) % N) != 0:
				if tempBoard[0][i] != EMPTY and tempBoard[0][i + 1] != EMPTY and tempBoard[1][counter + stacker] != EMPTY and tempBoard[1][counter + stacker + 1] != EMPTY:
					finalScore = finalScore + 1
				stacker = stacker + N
			else:
				counter = counter + 1
				stacker = 0
		
		if initialScore < finalScore:
			if player_id == 1:
				if (finalScore - initialScore) == 2:
					tempBoard[movement[0]][movement[1]] = FILLEDP12
				elif (finalScore - initialScore) == 1:
					tempBoard[movement[0]][movement[1]] = FILLEDP11
			elif player_id == 2:
				if (finalScore - initialScore) == 2:
					tempBoard[movement[0]][movement[1]] = FILLEDP22
				elif (finalScore - initialScore) == 1:
					tempBoard[movement[0]][movement[1]] = FILLEDP21
		
		return tempBoard


	def canOptimize(self):
		whole_score = 2 * (99 * ROWS)
		temp_score = (99 * ROWS) + (99 * (ROWS - 1))
		return [whole_score, temp_score]


	def getAllMoves(self, newBoard):
		movements = []

		for i in range(len(newBoard)):
			for j in range(len(newBoard[0])):
				if int(newBoard[i][j]) == 99:
					movements.append((i, j))

		return movements


	def getBestMove(self, board):
		opt_score = -inf

		allMoves = self.getAllMoves(board)
		total_score = int(np.sum(board))
		 
		if total_score in self.canOptimize():
			return allMoves[0]
		else:
			for movement in allMoves:
				score = self.minimax_full(movement, self.look_ahead, -inf, inf, False, board)

				if score > opt_score:
					opt_score = score
					allMoves = []

				if score >= opt_score:
					allMoves.append(movement)

		return allMoves[len(allMoves)-1]


	def minimax_full(self, movement, depth, alpha, beta, opt_player, tempBoardIn):
		curr_id = self.player_id if opt_player else self.opponent_id
		score = self.addPoints(movement, curr_id, tempBoardIn)

		if depth == 0 or score != 0 or 99 not in np.asarray(tempBoardIn).reshape(-1):
			return self.addPoints(movement, curr_id, tempBoardIn)

		tempBoard = self.doMovement(movement, curr_id, tempBoardIn)
		allMoves = self.getAllMoves(tempBoard)

		# Si es necesario optimizar al jugador, usar max
		if opt_player:
			max_res = -inf
			# Recorrer lista de posibles movimientos
			for movement in allMoves:
				# Evaluar cada jugada con minimax
				eval = self.minimax_full(movement, depth - 1, alpha, beta, False, tempBoard)
				# Nodo max resultante
				max_res = max(max_res, eval)
				# Guardar alpha
				alpha = max(alpha, eval)
				if beta <= alpha:
					break

			# Deshacer movimiento
			tempBoard[movement[0]][movement[1]] = 99
			return max_res

		# De lo contrario, usar min
		else:
			mins_res = inf
			# Recorrer lista de posibles movimientos
			for movement in allMoves:
				# Evaluar cada jugada con minimax
				eval = self.minimax_full(movement, depth - 1, alpha, beta, True, tempBoard)
				# Nodo min resultante
				mins_res = min(mins_res, eval)
				# Guardar beta
				beta = min(beta, eval)
				if beta <= alpha:
					break

			# Deshacer movimiento
			tempBoard[movement[0]][movement[1]] = 99
			return mins_res
	

	def addPoints(self, move, turn_id, board):

		# Map the board
		tempBoard = list(map(list, board))
		initialScore = 0
		finalScore = 0
		stacker = 0
		counter = 0
		multiplier = 0

		if (self.player_id == turn_id):
			multiplier = -1
		else:
			multiplier = 1

		for i in range(len(tempBoard[0])):
			if ((i + 1) % N) != 0:
				if tempBoard[0][i] != EMPTY and tempBoard[0][i + 1] != EMPTY and tempBoard[1][counter + stacker] != EMPTY and tempBoard[1][counter + stacker + 1] != EMPTY:
					initialScore = initialScore + 1

				stacker = stacker + N

			else:
				counter = counter + 1
				stacker = 0

		tempBoard[move[0]][move[1]] = FILL

		stacker = 0
		counter = 0

		for i in range(len(tempBoard[0])):
			if ((i + 1) % N) != 0:
				if tempBoard[0][i] != EMPTY and tempBoard[0][i + 1] != EMPTY and tempBoard[1][counter + stacker] != EMPTY and tempBoard[1][counter + stacker + 1] != EMPTY:
					finalScore = finalScore + 1
				stacker = stacker + N
			else:
				counter = counter + 1
				stacker = 0
		
		if initialScore < finalScore:
			if turn_id == 1:
				if (finalScore - initialScore) == 2:
					tempBoard[move[0]][move[1]] = FILLEDP12
				elif (finalScore - initialScore) == 1:
					tempBoard[move[0]][move[1]] = FILLEDP11
			elif turn_id == 2:
				if (finalScore - initialScore) == 2:
					tempBoard[move[0]][move[1]] = FILLEDP22
				elif (finalScore - initialScore) == 1:
					tempBoard[move[0]][move[1]] = FILLEDP21

		return (finalScore - initialScore)*multiplier
