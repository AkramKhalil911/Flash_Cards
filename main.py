import random
import tkinter
import pandas

# ----------------------- Window --------------------- #

BACKGROUND_COLOR = "#B1DDC6"

window = tkinter.Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flash Cards (French)")
current_card = {}
flip_time = 3000

# ----------------------- get data --------------------- #

get_data = pandas.read_csv("data/french_words.csv")
get_new_word = get_data.to_dict(orient="records")

try:
    get_learn_data = pandas.read_csv("data/need_to_learn.csv")
except (FileNotFoundError, pandas.errors.EmptyDataError, AttributeError):
    get_learn_data = get_data.to_csv("data/need_to_learn.csv", index=False)
else:
    get_learn_words = get_learn_data.to_dict(orient="records")

# ----------------------- Next/show card --------------------- #

def next_card():
    global current_card, flip_time
    window.after_cancel(flip_time)
    try:
        current_card = random.choice(get_learn_words)
    except NameError:
        current_card = random.choice(get_new_word)
    canvas.itemconfig(create_img, image=front_img)
    canvas.itemconfig(card_title, text='French', fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    flip_time = window.after(3000, showcard)

def showcard():
    canvas.itemconfig(create_img, image=back_img)
    canvas.itemconfig(card_title, text='English', fill="White")
    canvas.itemconfig(card_word, text=current_card["English"], fill="White")

# ----------------------- Right/Wrong function --------------------- #

def right_answer():
    try:
        get_learn_words.remove(current_card)
        learn_words = pandas.DataFrame(get_learn_words)
    except NameError:
        get_new_word.remove(current_card)
        learn_words = pandas.DataFrame(get_new_word)
    learn_words.to_csv("data/need_to_learn.csv", index=False)
    next_card()

def wrong_answer():
    next_card()

# ----------------------- front/back canvas --------------------- #

canvas = tkinter.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_img = tkinter.PhotoImage(file="images/card_front.png")
back_img = tkinter.PhotoImage(file="images/card_back.png")
create_img = canvas.create_image(400,263, image=front_img)
canvas.grid(row=0, column=0, columnspan=2)
card_title = canvas.create_text(400, 150, text="Language", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))

# ----------------------- Wrong button --------------------- #

wrong_image = tkinter.PhotoImage(file="images/wrong.png")
wrong_button = tkinter.Button(image=wrong_image, highlightthickness=0,command=wrong_answer)
wrong_button.grid(row=1, column=0)

# ----------------------- Right button --------------------- #

right_image = tkinter.PhotoImage(file="images/right.png")
right_button = tkinter.Button(image=right_image, highlightthickness=0,command=right_answer)
right_button.grid(row=1, column=1)
next_card()

window.mainloop()