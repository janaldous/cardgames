from Tkinter import *
#from ttk import Notebook
#from MyFrame import MyFrame

class Lucky9GUI:

	def __init__(self):
		lucky9_window = Tk()
		lucky9_window.title("Lucky 9")

		self.currentplayer = StringVar()
		self.currentplayer.set("current player: none")
		lCurrentPlayer = Label(lucky9_window, textvariable=self.currentplayer)

		button = Button(lucky9_window, text="Click me to next player!", command=lambda:self.change_curplayer("jats"))

		self.canvas = Canvas(lucky9_window, width=600, height=500, background='dark green')
		self.setup_canvas()
		
		bHit = Button(lucky9_window, text="Hit", command=lambda:self.hit())
		bStand = Button(lucky9_window, text="Stand", command=lambda:self.stand())
		bBuyChips = Button(lucky9_window, text="Buy chips", command=lambda:self.buy_chips())
		
		lCurrentPlayer.pack()
		button.pack()
		self.canvas.pack()
		bHit.pack()
		bStand.pack()
		bBuyChips.pack()
		lucky9_window.mainloop()
	
	def change_curplayer(self, curplayer):
		self.currentplayer.set("current player: " + curplayer)
		
	def setup_canvas(self):
		back_pic = PhotoImage(file="card_pics/b1fv.gif")
		self.canvas.create_text((550, 20), text="deck of cards")
		self.canvas.create_image((300, 250), image=back_pic)
		
		self.canvas.create_rectangle((300, 200, 20, 20))
		
		#put deck of cards on top right side
		#put rectangles for dealer's cards
		#put bet circles () and text, max 6 players
		
		
	def hit(self):
		print "hit"
		
	def stand(self):
		print "Stand"
		
	def buy_chips(self):
		print "buy chips"
		

if __name__ == '__main__':
	app = Lucky9GUI()
	
