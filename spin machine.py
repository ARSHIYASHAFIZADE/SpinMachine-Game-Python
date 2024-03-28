import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# Define constants and data
MAX_LINES = 3
MIN_BET = 1
MAX_BET = 100

ROWS = 3
COLS = 3

symbol_count = {
    'A': 2,
    'B': 4,
    'C': 6,
    'D': 8
}
symbol_value = {
    'A': 5,
    'B': 4,
    'C': 3,
    'D': 2
}

# Initialize variables
balance = 0
lines = 1
bet = MIN_BET


def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]  # a copy of all symbols
        for _ in range(rows):
            value = random.choice(all_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns


def check_winning(columns, lines, bet, values):
    winnings = 0
    winning_lines = []

    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
            else:
                winnings += values[symbol] * bet
                winning_lines.append(line + 1)
    return winnings, winning_lines


def spin():
    global balance
    global lines
    global bet

    try:
        total = int(bet) * int(lines)
        if total > balance:
            messagebox.showerror("Error", "You do not have enough balance to bet that amount.")
            return

        slots = get_slot_machine_spin(ROWS, COLS, symbol_count)

        # Create a result window
        result_window = tk.Toplevel()
        result_window.title("Spin Result")

        for col_index, column in enumerate(slots):
            column_frame = tk.Frame(result_window)
            column_frame.pack(side=tk.LEFT, padx=10)

            for symbol in column:
                # Load the symbol image
                symbol = int(symbol)
                symbol_image = Image.open(f"img_{symbol}.png")  # Use the image file name with 'img_' prefix
                symbol_image = symbol_image.resize((20, 20), Image.ANTIALIAS)
                symbol_photo = ImageTk.PhotoImage(symbol_image)

                # Create a label to display the image
                symbol_label = tk.Label(column_frame, image=symbol_photo)
                symbol_label.image = symbol_photo  # Keep a reference to avoid garbage collection
                symbol_label.pack()

        winnings, winning_line = check_winning(slots, int(lines), int(bet), symbol_value)
        balance += winnings - total

        # Display the spin result
        result_label = tk.Label(result_window,
                                text=f"You won ${winnings}\nWinning lines: {', '.join(map(str, winning_line))}")
        result_label.pack()

        # Update the balance label in the main window
        update_balance_label()
    except ValueError:
        messagebox.showerror("Error", "Invalid input for lines or bet.")


def update_balance_label():
    balance_label.config(text=f"Balance: ${balance}")


def set_lines(new_lines):
    global lines
    lines = new_lines


def set_bet(new_bet):
    global bet
    bet = new_bet


def deposit():
    global balance
    deposit_amount = deposit_entry.get()
    if deposit_amount.isdigit() and int(deposit_amount) > 0:
        balance += int(deposit_amount)
        update_balance_label()
    else:
        messagebox.showerror("Invalid Input", "Please enter a valid deposit amount.")


# Create the main window
window = tk.Tk()
window.title("Slot Machine Game")

# Create and place widgets
balance_label = tk.Label(window, text=f"Balance: ${balance}")
balance_label.pack()

deposit_label = tk.Label(window, text="Deposit:")
deposit_label.pack()

deposit_entry = tk.Entry(window)
deposit_entry.pack()

deposit_button = tk.Button(window, text="Deposit", command=deposit)
deposit_button.pack()

lines_label = tk.Label(window, text="Lines (1-3):")
lines_label.pack()

lines_scale = tk.Scale(window, from_=1, to=3, orient="horizontal", length=200, label="Lines", sliderlength=20,
                       command=set_lines)
lines_scale.pack()

bet_label = tk.Label(window, text=f"Bet (${MIN_BET}-${MAX_BET}):")
bet_label.pack()

bet_scale = tk.Scale(window, from_=MIN_BET, to=MAX_BET, orient="horizontal", length=200, label="Bet", sliderlength=20,
                     command=set_bet)
bet_scale.pack()

spin_button = tk.Button(window, text="Spin", command=spin)
spin_button.pack()

update_balance_label()

# Start the main loop
window.mainloop()
