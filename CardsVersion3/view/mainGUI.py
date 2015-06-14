from Tkinter import *
from ttk import *
import random

class Game():
    def __init__(self, root):
        self.root = root
        self.frame = Frame(self.root)
        self.notebook = Notebook(self.frame)
        
        self.f1 = Frame(self.notebook, width=600, height=500)
        self.f2 = Frame(self.notebook, width=600, height=500)
        self.f3 = Frame(self.notebook, width=600, height=500)
        self.f4 = Frame(self.notebook, width=600, height=500)
        self.notebook.add(self.f1, text="Player 1")
        self.notebook.add(self.f2, text="Player 2")
        self.notebook.add(self.f3, text="Player 3")
        self.notebook.add(self.f4, text="Player 4")

        #build notebook tabs
        self.build_player1_window()
        self.build_player2_window()
        self.build_player3_window()
        self.build_player4_window()
        
        self.label = Label(self.frame, text="Lucky 9")

        self.deal_button = Button(self.frame, text = "Deal")
        self.show_button = Button(self.frame, text = "Show")
        self.play_button = Button(self.frame, text = "Play")
        self.takecard_button = Button(self.frame, text = "Take card")
        self.exit_button = Button(self.frame, text = "Exit game", command = self.root.destroy)

        # Layout
        self.frame.grid(row=0, column=0, sticky=(N, S, E, W), rowspan=5)
        self.notebook.grid(row=0, column=0, sticky=(N, S, E, W), rowspan=5)
        self.deal_button.grid(row=0, column=1)
        self.show_button.grid(row=1, column=1)
        self.play_button.grid(row=2, column=1)
        self.takecard_button.grid(row=3, column=1)
        self.exit_button.grid(row=4, column=1)
        
        # Resize rules
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=2)
        self.frame.rowconfigure(0, weight=2)

        # this data is used to keep track of an 
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}

        # create a couple movable objects
        self.deal_ctr = 0
        self.player1cards = []
        self.player2cards = []
        self.player3cards = []
        self.player4cards = []
        self.player = 1
        self.ctr = 0
        self._create_token()
        self.deck = []
        suits = ["c", "d", "h", "s"]
        for suit in suits:
            for n in range(1, 11):
                self.deck.append(suit+str(n))
        random.shuffle(self.deck)

        #bindings
        self.deal_button.bind("<ButtonPress-1>", self.deal)
        self.show_button.bind("<ButtonPress-1>", self.show)
        self.play_button.bind("<ButtonPress-1>", self.play)
        self.takecard_button.bind("<ButtonPress-1>", self.takecard)
        self.notebook.bind_all("<<NotebookTabChanged>>", self.tabChangedEvent)

    def tabChangedEvent(self, event):
        if event.widget.tab(event.widget.index("current"), "text") == "Player 1":
            self.player = 1
        elif event.widget.tab(event.widget.index("current"), "text") == "Player 2":
            self.player = 2
        elif event.widget.tab(event.widget.index("current"), "text") == "Player 3":
            self.player = 3
        elif event.widget.tab(event.widget.index("current"), "text") == "Player 4":
            self.player = 4

    def build_player1_window(self):
        self.canvas1 = Canvas(self.f1, width = 600, height = 500)
        self.canvas1.pack(fill = "both", expand = True)
        self.canvas1.create_rectangle((0,0), (1600,1400), fill = "dark green", outline = "dark green")

    def build_player2_window(self):
        self.canvas2 = Canvas(self.f2, width = 600, height = 500)
        self.canvas2.pack(fill = "both", expand = True)
        self.canvas2.create_rectangle((0,0), (1600,1400), fill = "dark green", outline = "dark green")

    def build_player3_window(self):
        self.canvas3 = Canvas(self.f3, width = 600, height = 500)
        self.canvas3.pack(fill = "both", expand = True)
        self.canvas3.create_rectangle((0,0), (1600,1400), fill = "dark green", outline = "dark green")

    def build_player4_window(self):
        self.canvas4 = Canvas(self.f4, width = 600, height = 500)
        self.canvas4.pack(fill = "both", expand = True)
        self.canvas4.create_rectangle((0,0), (1600,1400), fill = "dark green", outline = "dark green")

    def _create_token(self):
        #[1,2]
        #[3,4]
        self.back_photo = PhotoImage(file="card_pics/b1fv.gif")
        label = Label(image=self.back_photo)
        label.image = self.back_photo # keep a reference!
        self.canvas1.create_image((300, 250), image=self.back_photo)
        self.canvas2.create_image((300, 250), image=self.back_photo)
        self.canvas3.create_image((300, 250), image=self.back_photo)
        self.canvas4.create_image((300, 250), image=self.back_photo)
        label.destroy()

    def deal(self, event):
        if self.ctr < 40 and self.deal_ctr <= 1:
            self.backv = PhotoImage(file="card_pics/b1fv.gif")
            self.backh = PhotoImage(file="card_pics/b1fh.gif")

            self.photo2 = PhotoImage(file="card_pics/"+self.deck[self.ctr]+" copy.gif")
            label2 = Label(image=self.photo2)
            label2.image = self.photo2 # keep a reference!
            self.player2cards.append(self.deck[self.ctr])
            self.ctr += 1
            self.canvas1.create_image((100, 100), image=self.backh, tags="back")
            self.canvas2.create_image((100, 100), image=self.photo2, tags="token")
            self.canvas3.create_image((100, 100), image=self.backh, tags="back")
            self.canvas4.create_image((100, 100), image=self.backh, tags="back")

            self.photo4 = PhotoImage(file="card_pics/"+self.deck[self.ctr]+" copy.gif")
            label4 = Label(image=self.photo4)
            label4.image = self.photo4 # keep a reference!
            self.player4cards.append(self.deck[self.ctr])
            self.ctr += 1
            self.canvas1.create_image((500, 400), image=self.backh, tags="back")
            self.canvas2.create_image((500, 400), image=self.backh, tags="back")
            self.canvas3.create_image((500, 400), image=self.backh, tags="back")
            self.canvas4.create_image((500, 400), image=self.photo4, tags="token")

            self.photo3 = PhotoImage(file="card_pics/"+self.deck[self.ctr]+".gif")
            label3 = Label(image=self.photo3)
            label3.image = self.photo3 # keep a reference!
            self.player3cards.append(self.deck[self.ctr])
            self.ctr += 1
            self.canvas1.create_image((500, 100), image=self.backv, tags="back")
            self.canvas2.create_image((500, 100), image=self.backv, tags="back")
            self.canvas3.create_image((500, 100), image=self.photo3, tags="token")
            self.canvas4.create_image((500, 100), image=self.backv, tags="back")

            self.photo1 = PhotoImage(file="card_pics/"+self.deck[self.ctr]+".gif")
            label1 = Label(image=self.photo1)
            label1.image = self.photo1 # keep a reference!
            self.player1cards.append(self.deck[self.ctr])
            self.ctr += 1
            self.canvas1.create_image((100, 400), image=self.photo1, tags="token")
            self.canvas2.create_image((100, 400), image=self.backv, tags="back")
            self.canvas3.create_image((100, 400), image=self.backv, tags="back")
            self.canvas4.create_image((100, 400), image=self.backv, tags="back")

            self.deal_ctr += 1

    def show(self, event):
        for index, card in enumerate(self.player1cards):
            x = 100 + (20*index)
            y = 400
            self.photo1 = PhotoImage(file="card_pics/"+card+".gif")
            label1 = Label(image=self.photo1)
            label1.image = self.photo1 # keep a reference!
            self.canvas1.create_image((x, y), image=self.photo1, tags="token")
            self.canvas2.create_image((x, y), image=self.photo1, tags="back")
            self.canvas3.create_image((x, y), image=self.photo1, tags="back")
            self.canvas4.create_image((x, y), image=self.photo1, tags="back")

        for index, card in enumerate(self.player2cards):
            x = 100
            y = 100 + (20*index)
            self.photo2 = PhotoImage(file="card_pics/"+card+" copy.gif")
            label2 = Label(image=self.photo2)
            label2.image = self.photo2 # keep a reference!
            self.canvas1.create_image((x, y), image=self.photo2, tags="back")
            self.canvas2.create_image((x, y), image=self.photo2, tags="token")
            self.canvas3.create_image((x, y), image=self.photo2, tags="back")
            self.canvas4.create_image((x, y), image=self.photo2, tags="back")

        for index, card in enumerate(self.player3cards):
            x = 500 - (20*index)
            y = 100
            self.photo3 = PhotoImage(file="card_pics/"+card+".gif")
            label3 = Label(image=self.photo3)
            label3.image = self.photo3 # keep a reference!
            self.canvas1.create_image((x, y), image=self.photo3, tags="back")
            self.canvas2.create_image((x, y), image=self.photo3, tags="back")
            self.canvas3.create_image((x, y), image=self.photo3, tags="token")
            self.canvas4.create_image((x, y), image=self.photo3, tags="back")

        for index, card in enumerate(self.player4cards):
            x = 500
            y = 400 - (20*index)
            self.photo4 = PhotoImage(file="card_pics/"+card+" copy.gif")
            label4 = Label(image=self.photo4)
            label4.image = self.photo4 # keep a reference!
            self.canvas1.create_image((x, y), image=self.photo4, tags="back")
            self.canvas2.create_image((x, y), image=self.photo4, tags="back")
            self.canvas3.create_image((x, y), image=self.photo4, tags="back")
            self.canvas4.create_image((x, y), image=self.photo4, tags="token")

    def play(self, event):
        self.ctr = 0
        self.deal_ctr = 0
        self.player1cards = []
        self.player2cards = []
        self.player3cards = []
        self.player4cards = []
        self.canvas1.destroy()
        self.canvas2.destroy()
        self.canvas3.destroy()
        self.canvas4.destroy()
        self.build_player1_window()
        self.build_player2_window()
        self.build_player3_window()
        self.build_player4_window()
        self._create_token()


    def takecard(self, event):
        if self.ctr < 40:
            if self.player == 1:
                x = 100 + (20*len(self.player1cards))
                y = 400
                self.photo1 = PhotoImage(file="card_pics/"+self.deck[self.ctr]+".gif")
                label1 = Label(image=self.photo1)
                label1.image = self.photo1 # keep a reference!
                self.player1cards.append(self.deck[self.ctr])
                self.ctr += 1
                self.canvas1.create_image((x, y), image=self.photo1, tags="token")
                self.canvas2.create_image((x, y), image=self.backv, tags="back")
                self.canvas3.create_image((x, y), image=self.backv, tags="back")
                self.canvas4.create_image((x, y), image=self.backv, tags="back")
            elif self.player == 2:
                x = 100
                y = 100 + (20*len(self.player2cards))
                self.photo2 = PhotoImage(file="card_pics/"+self.deck[self.ctr]+" copy.gif")
                label2 = Label(image=self.photo2)
                label2.image = self.photo2 # keep a reference!
                self.player2cards.append(self.deck[self.ctr])
                self.ctr += 1
                self.canvas1.create_image((x, y), image=self.backh, tags="back")
                self.canvas2.create_image((x, y), image=self.photo2, tags="token")
                self.canvas3.create_image((x, y), image=self.backh, tags="back")
                self.canvas4.create_image((x, y), image=self.backh, tags="back")
            elif self.player == 3:
                x = 500 - (20*len(self.player3cards))
                y = 100
                self.photo3 = PhotoImage(file="card_pics/"+self.deck[self.ctr]+".gif")
                label3 = Label(image=self.photo3)
                label3.image = self.photo3 # keep a reference!
                self.player3cards.append(self.deck[self.ctr])
                self.ctr += 1
                self.canvas1.create_image((x, y), image=self.backv, tags="back")
                self.canvas2.create_image((x, y), image=self.backv, tags="back")
                self.canvas3.create_image((x, y), image=self.photo3, tags="token")
                self.canvas4.create_image((x, y), image=self.backv, tags="back")
            elif self.player == 4:
                x = 500
                y = 400 - (20*len(self.player4cards))
                self.photo4 = PhotoImage(file="card_pics/"+self.deck[self.ctr]+" copy.gif")
                label4 = Label(image=self.photo4)
                label4.image = self.photo4 # keep a reference!
                self.player4cards.append(self.deck[self.ctr])
                self.ctr += 1
                self.canvas1.create_image((x, y), image=self.backh, tags="back")
                self.canvas2.create_image((x, y), image=self.backh, tags="back")
                self.canvas3.create_image((x, y), image=self.backh, tags="back")
                self.canvas4.create_image((x, y), image=self.photo4, tags="token")


if __name__ == '__main__':
    root = Tk()
    app = Game(root)
    root.mainloop()