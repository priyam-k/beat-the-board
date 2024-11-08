from tkinter import *
import random
import math

root = Tk()
root.title("Beat the Board")
root.geometry("800x600")
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
root.bind("<F11>", lambda e: root.attributes("-fullscreen", not root.attributes("-fullscreen")))

snapped = {}
score = IntVar()
score.set(0)

START_TIME = IntVar()
START_TIME.set(60)
START_CARDS = IntVar()
START_CARDS.set(10)

pause = False
def pause_game(event):
    global pause
    pause = not pause
root.bind("<space>", pause_game)

root.bind("-", lambda e: START_TIME.set(max(START_TIME.get()-1, 1)))
root.bind("=", lambda e: START_TIME.set(START_TIME.get()+1))
root.bind("_", lambda e: START_CARDS.set(max(START_CARDS.get()-1, 1)))
root.bind("+", lambda e: START_CARDS.set(START_CARDS.get()+1))

time = IntVar()
time.set(START_TIME.get())

def drag_start(event):
    widget = event.widget
    widget["bg"] = "white" 
    if widget in snapped:
        del snapped[widget]
    widget.lift()
    widget.startX = event.x
    widget.startY = event.y

def drag_motion(event):
    widget = event.widget
    x = min(max(0, event.x - widget.startX + widget.winfo_x()), root.winfo_width() - widget.winfo_width())
    y = min(max(0, event.y - widget.startY + widget.winfo_y()), root.winfo_height() - widget.winfo_height())
    widget.place(x=x, y=y)

def card_snap(event):
    widget = event.widget
    for pocket in pockets:
        if abs(widget.winfo_x() - pocket.winfo_x()) < 35 and abs(widget.winfo_y() - pocket.winfo_y()) < 35:
            widget.place(x=pocket.winfo_x()+7, y=pocket.winfo_y()-30)
            widget.lower()
            snapped[widget] = pocket
            break

# INCLUDES SCUFFED ANSWER THINGY
def create_cards(num):
    num = min(len(card_labels), num)
    batch = 10
    new_cards = random.sample(card_labels, k=num)

    x = 0
    for i in range(math.ceil(num/10)):
        if i == num//10:
            batch = num%10
        for j in range(batch):
            card = new_cards[x]
            # card answer is at the end of card text lmao (after "@")
            cards.append(Label(root, bg="white", text=card[0]+"\n"*10+"@"+card[1]+"@"+card[2], wraplength=50, anchor="n", width=8, height=4, relief="solid"))
            cards[-1].place(x=1460-5*i, y=775-75*j-5*i)
            cards[-1].bind("<Button-1>", drag_start)
            cards[-1].bind("<B1-Motion>", drag_motion)
            cards[-1].bind("<ButtonRelease-1>", card_snap)
            #cards[-1]["tag"] = card[1]
            x += 1

def reset(event):
    for i in range(len(cards)):
        cards[i].destroy()
    cards.clear()
    snapped.clear()
    time.set(START_TIME.get())
    score.set(0)
    create_cards(START_CARDS.get())

def check(event):
    score.set(0)
    print("--------------------")
    for card in snapped.keys():
        if card["text"].split("@")[1] == snapped[card]["text"].lower() and card["text"].split("@")[2] == snapped[card]["bg"]:
            card["bg"] = "green"
            score.set(score.get()+1)
        else:
            card["bg"] = "red"
            print(card["text"].split("@")[1], "---", card["text"].split("@")[2], "---", snapped[card]["text"].lower())

def update_timer():
    if not pause:
        time.set(max(time.get()-1, 0))
    if time.get() == 0:
        check(None)
    root.update()
    root.after(1000, update_timer)

# colors
green = "#9ed9a5"
blue = "#619eed"
purple = "#c781e6"
pink = "#f777a8"
orange = "#f5a351"
yellow = "#fafa78"
lightblue = "#b3c1c9"
lightpink = "#b3a9ba"
black = "#000000"
white = "#ffffff"

# (name, color, font)
pocket_labels = [
    [
        ("Function", green),
        ("INSTITUTION", green),
        ("Represented By", blue),
        ("House Majority #", blue),
        ("Represented By", purple),
        ("Senate Majority #", purple),
        ("Function", pink),
        ("INSTITUTION", pink),
        ("Function", orange),
        ("INSTITUTION", orange),
        ("ARTICLE II", yellow),
        ("ARTICLE I", yellow),
        ("Amend", black),
        ("", ""),
        ("", ""),
        ("", ""),
    ],
    [
        ("power", green),
        ("power", green),
        ("Term", blue),
        ("House Majority", blue),
        ("Term", purple),
        ("Senate Majority", purple),
        ("Term", pink),
        ("Age", pink),
        ("Lower Court", orange),
        ("UPPER COURT", orange),
        ("ARTICLE III", yellow),
        ("Impeach", black),
        ("State Power", lightblue),
        ("State Power", lightblue),
        ("National Power", lightblue),
        ("National Power", lightblue),
    ],
    [
        ("power", green),
        ("power", green),
        ("Age", blue),
        ("House Majority", blue),
        ("Age", purple),
        ("Senate Majority", purple),
        ("Residency", pink),
        ("Citizenship", pink),
        ("Term", orange),
        ("Age", orange),
        ("ARTICLE IV", yellow),
        ("GOAL OF POWER", lightblue),
        ("Repeal", black),
        ("Principle", lightpink),
        ("Appeal", black),
        ("Principle", lightpink),
    ],
    [
        ("power", green),
        ("power", green),
        ("Residency", blue),
        ("House Majority", blue),
        ("Residency", purple),
        ("Senate Majority", purple),
        ("power", pink),
        ("power", pink),
        ("Residency", orange),
        ("Citizenship", orange),
        ("ARTICLE V", yellow),
        ("First Amendment", white),
        ("Second Amendment", white),
        ("Third Amendment", white),
        ("Fourth Amendment", white),
        ("Fifth Amendment", white),
    ],
    [
        ("power", green),
        ("power", green),
        ("Citizenship", blue),
        ("House 2/3 #", blue),
        ("Citizenship", purple),
        ("Senate 2/3 #", purple),
        ("power", pink),
        ("power", pink),
        ("power", orange),
        ("power", orange),
        ("ARTICLE VI", yellow),
        ("Sixth Amendment", white),
        ("Seventh Amendment", white),
        ("Eight Amendment", white),
        ("Ninth Amendment", white),
        ("Tenth Amendment", white),
    ],
    [
        ("*Legislative Checks Executive", green),
        ("*Legislative Checks Executive", green),
        ("Leader", blue),
        ("House 2/3", blue),
        ("Leader", purple),
        ("Senate 2/3", purple),
        ("power", pink),
        ("power", pink),
        ("power", orange),
        ("power", orange),
        ("ARTICLE VII", yellow),
        ("11th Amendment", white),
        ("12th Amendment", white),
        ("13th Amendment", white),
        ("14th Amendment", white),
        ("15th Amendment", white),
    ],
    [
        ("*Legislative Checks Executive", green),
        ("*Legislative Checks Executive", green),
        ("Total House #", blue),
        ("House 2/3", blue),
        ("Total Senate #", purple),
        ("Senate 2/3", purple),
        ("power", pink),
        ("power", pink),
        ("*Judicial Checks Legislative", orange),
        ("*Judicial Checks Executive", orange),
        ("Principle", lightpink),
        ("Veto", black),
        ("16th Amendment", white),
        ("17th Amendment", white),
        ("18th Amendment", white),
        ("19th Amendment", white),
    ],
    [
        ("*Legislative Checks Executive", green),
        ("*Legislative Checks Executive", green),
        ("*Legislative Checks Judicial", green),
        ("House 2/3", blue),
        ("Senate 2/3", purple),
        ("Senate 2/3", purple),
        ("*Executive Checks Legislative", pink),
        ("*Executive Checks Legislative", pink),
        ("*Executive Checks Judicial", pink),
        ("*Judicial Checks Executive", orange),
        ("Ratify", black),
        ("GOAL OF POWER", lightblue),
        ("20th Amendment", white),
        ("21th Amendment", white),
        ("22th Amendment", white),
        ("23th Amendment", white),
    ],
    [
        ("LIMIT", green),
        ("*Legislative Checks Judicial", green),
        ("LIMIT", green),
        ("*Legislative Checks Judicial", green),
        ("LIMIT", green),
        ("Senate 2/3", purple),
        ("*Executive Checks Legislative", pink),
        ("*Executive Checks Legislative", pink),
        ("*Executive Checks Judicial", pink),
        ("*Judicial Checks Executive", orange),
        ("Principle", lightpink),
        ("Principle", lightpink),
        ("24th Amendment", white),
        ("25th Amendment", white),
        ("27th Amendment", white),
        ("27th Amendment", white),
    ],
]

pockets = []

# create pockets
for i in range(9):
    for k in range(16):
        if pocket_labels[i][k][0] != "":
            pockets.append(Label(root, bg=pocket_labels[i][k][1], text=pocket_labels[i][k][0], wraplength=75, width=10, height=3, relief="solid", fg=(white if pocket_labels[i][k][1] == black else black)))
            pockets[-1].place(x=20+90*k, y=75+90*i)


# (name, pocket)
card_labels = [
    ("To make Law", "function", green),
    ("THE CONGRESS", "institution", green),
    ("pay debt", "power", green),
    ("regulate commerce", "power", green),
    ("establish infrastructure", "power", green),
    ("print and coin money", "power", green),
    ("collect taxes & tariffs", "power", green),
    ("borrow money", "power", green),
    ("fix standards of weights & measures", "power", green),
    ("declare war", "power", green),
    ("*approve or reject treaties", "*legislative checks executive", green),
    ("*control spending", "*legislative checks executive", green),
    ("*select president if vote is tied", "*legislative checks executive", green),
    ("*override a veto", "*legislative checks executive", green),
    ("*approve or reject appointments", "*legislative checks executive", green),
    ("*impeach & remove president", "*legislative checks executive", green),
    ("*propose constitutional amendments", "*legislative checks judicial", green),
    ("*impeach & remove judges", "*legislative checks judicial", green),
    ("cannot pass ex post facto laws", "limit", green),
    ("cannot suspend habeas corpus", "limit", green),
    ("cannot pass bills of attainder", "limit", green),

    ("Population", "represented by", blue),
    ("218", "house majority #", blue),
    ("2 years", "term", blue),
    #("Change # of justices", "house majority", blue),
    ("25", "age", blue),
    ("Pass a bill", "house majority", blue),
    ("In District", "residency", blue),
    ("decide pres if no electoral majority", "house majority", blue),
    ("7 years", "citizenship", blue),
    ("290", "house 2/3 #", blue),
    ("Speaker", "leader", blue),
    ("Propose constitutional amendments", "house 2/3", blue),
    ("overturn a veto", "house 2/3", blue),
    ("Change # of justices", "house 2/3", blue),
    ("435", "total house #", blue),
    ("Impeach President", "house majority", blue),
    #("decide VP if no electoral majority", "house 2/3", blue),
    #("Confirm Nominations", "house 2/3", blue),

    ("Equality", "represented by", purple),
    ("51", "senate majority #", purple),
    ("6 years", "term", purple),
    ("decide VP if no electoral majority", "senate majority", purple),
    #("Ratify treaties", "senate majority", purple), wrong
    ("30", "age", purple),
    #("overturn a veto", "senate majority", purple),
    ("Confirm Nominations", "senate majority", purple),
    ("In State", "residency", purple),
    ("Pass a bill", "senate majority", purple),
    ("9 years", "citizenship", purple),
    ("67", "senate 2/3 #", purple),
    ("Vice-President", "leader", purple),
    ("Change # of justices", "senate 2/3", purple),
    ("100", "total senate #", purple),
    ("Ratify treaties", "senate 2/3", purple),
    ("Overturn a veto", "senate 2/3", purple),
    ("Propose constitutional amendments", "senate 2/3", purple),
    #("Impeach President", "senate 2/3", purple),
    ("Remove President", "senate 2/3", purple),

    ("To Execute Law", "function", pink),
    ("THE PRESIDENT", "institution", pink),
    ("4 years", "term", pink),
    ("35", "age", pink),
    ("14 years in US", "residency", pink),
    ("Born in US", "citizenship", pink),
    ("give state of the union", "power", pink),
    ("grant pardons", "power", pink),
    ("make appointments", "power", pink),
    ("make treaties", "power", pink),
    ("call special session of Congress", "power", pink),
    ("conduct foreign policy", "power", pink),
    ("Commander in Chief", "power", pink),
    ("veto", "power", pink),
    ("*VP is president of Senate", "*executive checks legislative", pink),
    ("*the bully pulpit", "*executive checks legislative", pink),
    ("*grant pardons", "*executive checks judicial", pink),
    ("*appoint federal judges", "*executive checks judicial", pink),
    ("*veto", "*executive checks legislative", pink),
    ("*call a special session of Congress", "*executive checks legislative", pink),

    ("To Judge Law", "function", orange),
    ("THE SUPREME COURT", "institution", orange),
    ("Federal District", "lower court", orange),
    ("FEDERAL APPELATE", "upper court", orange),
    ("Lifetime", "term", orange),
    ("none", "age", orange),
    ("none", "residency", orange),
    ("none", "citizenship", orange),
    ("oversee trial of federal officers", "power", orange),
    ("decide conflicts between states", "power", orange),
    ("decide constutionality of laws", "power", orange),
    ("decide conflicts involving govt", "power", orange),
    ("*judicial review", "*judicial checks legislative", orange),
    ("*can rule executive actions unconstitutional", "*judicial checks executive", orange),
    ("*cannot be fired by president", "*judicial checks executive", orange),
    ("*Chief Justice sits as judge in federal trials", "*judicial checks executive", orange),

    ("THE LEGISLATIVE BRANCH", "article i", yellow),
    ("THE EXECUTIVE BRANCH", "article ii", yellow),
    ("THE JUDICIAL BRANCH", "article iii", yellow),
    ("RELATIONSHIP BETWEEN STATES & NATL GOV", "article iv", yellow),
    ("AMENDMENT PROCESS", "article v", yellow),
    ("SUPREME LAW OF THE LAND", "article vi", yellow),
    ("RATIFICATION", "article vii", yellow),

    ("change", "amend", black),
    ("approve", "ratify", black),
    ("reject", "veto", black),
    ("accuse", "impeach", black),
    ("take back", "repeal", black),
    ("challenge", "appeal", black),

    ("Separation of Powers", "principle", lightpink),
    ("Federalism", "principle", lightpink),
    ("Checks & Balances", "principle", lightpink),
    ("Limited Government", "principle", lightpink),
    ("Republicanism", "principle", lightpink),

    ("LIMITED", "goal of power", lightblue),
    ("BALANCED", "goal of power", lightblue),
    ("Shared", "state power", lightblue),
    ("Reserved", "state power", lightblue),
    ("Expressed", "national power", lightblue),
    ("Implied", "national power", lightblue),
]

cards = []

# buttons
resetbutton = Button(root, text="Reset")
resetbutton.bind("<Button-1>", reset)
resetbutton.place(x=1460, y=20)

checkbutton = Button(root, text="Check")
checkbutton.bind("<Button-1>", check)
checkbutton.place(x=1460, y=60)

# create cards to start
create_cards(START_CARDS.get())

#timer = Label(root, textvariable="{}:{}".format(int(time.get())//60, int(time.get())%60), font=("Helvetica", 20))
timer = Label(root, textvariable=time, font=("Helvetica", 20))
timer.place(x=1300, y=40)
update_timer()

scorelabel = Label(root, textvariable=score, font=("Helvetica", 20))
scorelabel.place(x=1300, y=80)

Label(root, textvariable=START_TIME).place(x=1420, y=20)
Label(root, textvariable=START_CARDS).place(x=1420, y=60)

'''whitehouse = PhotoImage(file="whitehouse.png")
congress = whitehouse
supremecourt = whitehouse
#congress = PhotoImage(file="congress.jpg")
#supremecourt = PhotoImage(file="supremecourt.jpg")'''

Label(root, text="congress", width=10, height=3, bg=green).place(x=65, y=10)
Label(root, text="HOR", width=10, height=3, wraplength=75, bg=blue).place(x=245, y=10)
Label(root, text="The Senate", width=10, height=3, bg=purple).place(x=425, y=10)
Label(root, text="whitehouse", width=10, height=3, bg=pink).place(x=605, y=10)
Label(root, text="supremecourt", width=10, height=3, bg=orange).place(x=785, y=10)

Label(root, text="Made by Priyam K").place(x=1300, y=10)

root.mainloop()