import socketio
from GameManager import GameManager
from Algorithm import Algorithm

# New client with socketio
sio = socketio.Client()

@sio.on('connect')
def onConnect():
	print('Connected to tournament!')
	sio.emit('signin', {
		'user_name': manager.username,
		'tournament_id': manager.tid,
		'user_role': 'player'
	}) 


@sio.on('ready')
def onReady(data):
	print('Ready')

	# We get our player_id and game_id from the server and define
	# our game manager class
	manager.player_id = data['player_turn_id']
	manager.game_id = data['game_id']
	manager.board = data['board']

	# Print the board just for debugging purposes
	print(manager.printBoard())

	# Set the data for the algorithm to work properly
	algo.setData(manager.player_id)
	# We decide where to move next
	# This is where minimax comes in handy
	movement = algo.getBestMove(manager.board)


	# Emit the play to the server
	sio.emit('play', {
		'player_turn_id': manager.player_id,
		'tournament_id': manager.tid,
		'game_id': manager.game_id,
		'movement': movement
	})

	print('Play emitted!')


@sio.on('finish')
def on_finish(server):
	print('Torunament with id', manager.game_id, 'has finished.')

	# Check if we are either the winner or the loser
	if server['player_turn_id'] == server['winner_turn_id']:
		print('You won!')
	else:
		print('You lost')

	sio.emit('player_ready', {
		'tournament_id': manager.tid,
		'game_id': manager.game_id,
		'player_turn_id': manager.player_id
	})

	# Reset the match settings
	manager.Reset()


# username = input('Username: ')
# tid = input('Tournament ID: ')
# host = input('Host: ')

username = 'Oscar'
tid = 12
host = 'http://7233309d38e2.ngrok.io'

manager = GameManager(username, tid)
# Look ahead as parameter
algo = Algorithm(2)
sio.connect(host)
