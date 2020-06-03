from math import inf
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


	def simulateMovement(self, movement, player_id, tempBoardIn):
		# Duplicar arreglo mapeado para recorrerlo
		tempBoard = list(map(list, tempBoardIn))
		initialScore = 0
		finalScore = 0
		stacker = 0
		counter = 0

		# Se basa en el algoritmo brindado por DAVID SOTO en un foro de canvas
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

		# Ciclo sencillo que itera el tablero
		for i in range(ROWS):
			for j in range(COLS):
				if int(newBoard[i][j]) == 99:
					movements.append((i, j))

		return movements


	def getBestMove(self, board):
		opt_score = -inf
		allMoves = self.getAllMoves(board)
		total_score = int(np.sum(board))
		 
		# Evaluar si tenemos un puntaje que aplique a optimización o no
		if total_score in self.canOptimize():
			return allMoves[0]
		else:
			for movement in allMoves:
				score = self.minimax(movement, self.look_ahead, -inf, inf, False, board)

				if score > opt_score:
					opt_score = score
					allMoves = []

				if score >= opt_score:
					allMoves.append(movement)

		return allMoves[len(allMoves)-1]


	def minimax(self, movement, depth, alpha, beta, opt_player, tempBoardIn):
		# Extraer arreglo del unidimensional del arreglo
		single_arr = np.asarray(tempBoardIn).reshape(-1)
		# Obtener id del jugador que se está evaluando
		if opt_player:
			curr_id = self.player_id
		else:
			curr_id = self.opponent_id

		score = self.getPointsFromHeuristic(movement, curr_id, tempBoardIn)

		if depth == 0 or 99 not in single_arr or score != 0 :
			return self.getPointsFromHeuristic(movement, curr_id, tempBoardIn)

		# Simular movimiento en tablero y extraer todos los posibles movimientos
		tempBoard = self.simulateMovement(movement, curr_id, tempBoardIn)
		allMoves = self.getAllMoves(tempBoard)

		# Si es necesario optimizar al jugador, usar max
		if opt_player:
			max_res = -inf
			# Recorrer lista de posibles movimientos, esto nos va a permitir crear un arbol por cada escenario
			# y evaluar cual es el mejor tiro
			for movement in allMoves:
				# Evaluar cada jugada con minimax
				new_res = self.minimax(movement, depth - 1, alpha, beta, False, tempBoard)
				max_res = max(max_res, new_res)
				# Comparar el nuevo alpha y almacenarlo si es necesario
				alpha = max(alpha, new_res)
				if beta <= alpha:
					break

			return max_res

		# De lo contrario, usar min
		else:
			mins_res = inf
			# Repetir instrucciones de if anterior
			for movement in allMoves:
				# Evaluar cada jugada con minimax
				new_res = self.minimax(movement, depth - 1, alpha, beta, True, tempBoard)
				mins_res = min(mins_res, new_res)
				beta = min(beta, new_res)
				if beta <= alpha:
					break

			return mins_res
	

	def getPointsFromHeuristic(self, move, turn_id, board):

		# Map the board
		tempBoard = list(map(list, board))
		initialScore = 0
		finalScore = 0
		stacker = 0
		counter = 0
		multiplier = 0

		# Algoritmo brindado por DAVID SOTO en un foro de canvas
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

		if turn_id == self.player_id:
			return -1*(finalScore - initialScore)
		else:
			return (finalScore - initialScore)
