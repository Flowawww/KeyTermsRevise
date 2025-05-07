import tkinter as tk
from tkinter import messagebox, filedialog
import random

# Load dictionary from selected file
def load_dictionary_from_file():
    file_path = filedialog.askopenfilename(title="Choose a glossary text file", filetypes=[("Text Files", "*.txt")])
    if not file_path:
        messagebox.showerror("Error", "No file selected.")
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    entries = content.split("\n\n")
    glossary = {}
    for entry in entries:
        if ':' in entry:
            term, definition = entry.split(":", 1)
            glossary[term.strip()] = definition.strip().replace("\\n", "\n")
    return glossary

# Save wrong answers in the same format
def save_wrong_answers(filename, wrong_dict):
    with open(filename, "w", encoding="utf-8") as f:
        for key, value in wrong_dict.items():
            value = value.replace("\n", "\\n")
            f.write(f"{key}:{value}\n\n")

# Ask next question
def next_question():
    global current_key
    if not glossary:
        label_question.config(text="🎉 All terms completed!")
        return
    current_key = random.choice(list(glossary.keys()))
    label_question.config(text=glossary[current_key])
    entry_answer.delete(0, tk.END)

# Show how many terms remain
def show_remaining_words():
    count = len(glossary)
    messagebox.showinfo("Words Remaining", f"There are {count} term(s) left.")
# Check answer
def check_answer():
    user_input = entry_answer.get().strip()
    if user_input.lower() == current_key.lower():
        messagebox.showinfo("Correct", "Well done!")
        glossary.pop(current_key)
    else:
        messagebox.showerror("Incorrect", f"The correct term was: {current_key}")
        wrong_answers[current_key] = glossary[current_key]
    next_question()

# Load glossary and start quiz
def start_quiz():
    global glossary
    loaded = load_dictionary_from_file()
    if loaded:
        glossary.update(loaded)
        next_question()

# Quit and save wrong answers
def quit_and_save():
    if wrong_answers:
        save_wrong_answers("wrong_answers.txt", wrong_answers)
    root.destroy()

# UI setup
root = tk.Tk()
root.title("Key Terms Revision")
root.geometry("800x600")

glossary = {}
wrong_answers = {}
current_key = ""

label_question = tk.Label(root, text="Click 'Start Quiz' to begin", wraplength=550, font=("Arial", 20), justify="left")
label_question.pack(pady=20)

entry_answer = tk.Entry(root, font=("Arial", 20))
entry_answer.pack(pady=15)
entry_answer.bind("<Return>", lambda event: check_answer())

button_start = tk.Button(root, text="Start Quiz", command=start_quiz)
button_start.pack(pady=5)

button_submit = tk.Button(root, text="Submit", command=check_answer)
button_submit.pack(pady=5)

button_quit = tk.Button(root, text="Quit and Save", command=quit_and_save)
button_quit.pack(pady=10)

button_remaining = tk.Button(root, text = "Words Remaining", command = show_remaining_words)
button_remaining.pack(pady = 5)

root.mainloop()