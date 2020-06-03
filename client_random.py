import socketio
import sys
import random

sio = socketio.Client()

class DotsAndBoxes:
	def __init__(self,username,tid):
		self.name=username
		self.tournamentId=tid
		self.playerId=0
		self.gameId=""
		self.board=[]
		

		print(self.name)
		print(self.tournamentId)

	def createBoard(self):
		self.horizontal=[

		]
		self.Vertical=[]

	def restart(self):
		self.playerId=0
		self.gameId=""
		self.board=[]
		


@sio.on('connect')
def onConnect():
    print('Connection Successfully')
    sio.emit('signin', {
        'user_name': Dot.name,
        'tournament_id': Dot.tournamentId,
        'user_role': 'player'
    })

@sio.on('ready')
def onReady(server):
    print('Ready')
    print(server)

    Dot.playerId = server['player_turn_id']
    Dot.gameId = server['game_id']

    Dot.board=server['board']

    #movementType = int(input("0: Horizontal\n1: Vertical\n\t"))
    #movementIndex = int(input("0 - 29: "))
    movementType=random.randint(0, 1)
    movementIndex=random.randint(0, 29)
    
    while int(Dot.board[movementType][movementIndex]) != 99:
    	movementType=random.randint(0, 1)
    	movementIndex=random.randint(0, 29)

        #movementType = int(input("0: Horizontal\n1: Vertical\n\t"))
        #movementIndex = int(input("0 - 29: "))
	
    sio.emit('play', {
        'player_turn_id': Dot.playerId,
        'tournament_id': Dot.tournamentId,
        'game_id': Dot.gameId,
        'movement': [movementType, movementIndex]
    })

@sio.on('finish')
def on_finish(server):


    if (server['player_turn_id'] == server['winner_turn_id']):
        print("Win")
    else:
        print("Loose")
    
    sio.emit('player_ready', {
        'tournament_id': Dot.tournamentId,
        'game_id': Dot.gameId,
        'player_turn_id': Dot.playerId
    })
    
    Dot.restart()

#print(sys.argv)

'''
host
tid
nombre
'''

Dot=DotsAndBoxes('random',12)
sio.connect('http://localhost:4000')

		