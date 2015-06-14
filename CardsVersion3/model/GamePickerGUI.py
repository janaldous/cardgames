from Tkinter import *
from Game import *
from Lucky9GUI import *


def start_game(game_name):
	GameFactory.createGame(game_name)
	main_menu.destroy()
	app = Lucky9GUI()
	

def put_widgets():
	lPickGame = Label(main_menu, text="Pick a Game")

	lPickGame.pack()

	def gameGen():
		games = Game.__subclasses__()
		for game in games:
			yield game

	games = [game for game in gameGen()]

	print games

	for game in games:
		Button(main_menu, text=game.name, command=lambda: start_game(game.__name__)).pack()

		
main_menu = Tk()
main_menu.title("ME 3")
		
put_widgets()
		
main_menu.mainloop()