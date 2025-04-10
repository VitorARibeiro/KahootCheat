import requests as req
import tkinter as tk
from tkinter import ttk

def RequestQuestion(game_id):
    r = req.get(f"https://play.kahoot.it/rest/kahoots/{game_id}")
    return r.json().get("questions")

def Parser(input):
    FinalDictionary = dict()
    for QuestionNumber in input:
        Questions = QuestionNumber.get("question")
        if Questions is not None:
            Choices = QuestionNumber.get("choices") 
            Answers = [
                (Option.get("answer"), Option.get("correct"))  # True para correto
                for Option in Choices
            ]
            FinalDictionary[Questions] = Answers
    return FinalDictionary

def DisplayQuestionsAndAnswersTkinter():
    def fetch_questions():
        game_id = game_id_entry.get()
        if not game_id:
            result_label.config(text="Please enter a Game-ID.", foreground="red")
            return

        try:
            questions = RequestQuestion(game_id)
            parsed_questions = Parser(questions)
            display_results(parsed_questions)
        except Exception as e:
            result_label.config(text=f"Error: {str(e)}", foreground="red")

    def display_results(questions_dict):
        for widget in scrollable_frame.winfo_children():
            widget.destroy()  # Clear previous results

        for question, answers in questions_dict.items():
            question_frame = ttk.Frame(scrollable_frame, padding=20, style="ModernCard.TFrame")
            question_frame.pack(fill="x", pady=15, padx=50)  # Added padx to center the cards

            question_label = ttk.Label(
                question_frame, 
                text=f"Question: {question}", 
                style="ModernQuestion.TLabel",
                wraplength=600  # Limit the width of the question text
            )
            question_label.pack(anchor="w", pady=10)

            answers_frame = ttk.Frame(question_frame, style="ModernGrid.TFrame")
            answers_frame.pack()

            for i, (answer, is_correct) in enumerate(answers):
                row, col = divmod(i, 2)
                answer_label = ttk.Label(
                    answers_frame,
                    text=answer,
                    style="ModernCorrect.TLabel" if is_correct else "ModernAnswer.TLabel"
                )
                answer_label.grid(row=row, column=col, padx=10, pady=10)

    # Main Tkinter window
    root = tk.Tk()
    root.title("Kahoot Cheat")
    root.configure(bg="#1e1e1e")

    # Define modern styles
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", background="#1e1e1e", foreground="#e0e0e0", font=("Arial", 12))
    style.configure("TFrame", background="#1e1e1e")
    style.configure("TButton", background="#bb86fc", foreground="#121212", font=("Arial", 10, "bold"), borderwidth=0)
    style.map("TButton", background=[("active", "#9a67ea")])
    style.configure("ModernCard.TFrame", background="#2c2c2c", relief="solid", borderwidth=1, padding=15, 
                     borderradius=10)  # Added borderradius for rounded corners
    style.configure("ModernQuestion.TLabel", foreground="#bb86fc", font=("Arial", 14, "bold"))
    style.configure("ModernGrid.TFrame", background="#2c2c2c")
    style.configure("ModernAnswer.TLabel", background="#3a3a3a", foreground="#e0e0e0", padding=10, anchor="center", relief="solid", width=30, borderwidth=1)
    style.configure("ModernCorrect.TLabel", background="#4caf50", foreground="#ffffff", padding=10, anchor="center", relief="solid", width=30, borderwidth=1)

    # Input section
    input_frame = ttk.Frame(root, padding=20)
    input_frame.pack(fill="x")

    game_id_label = ttk.Label(input_frame, text="Enter the Game-ID:", font=("Arial", 12))
    game_id_label.pack(anchor="w", pady=5)

    # Use tk.Entry instead of ttk.Entry for custom styling
    game_id_entry = tk.Entry(input_frame, font=("Arial", 12), fg="#e0e0e0", bg="#2c2c2c", insertbackground="#e0e0e0", relief="solid", borderwidth=1)
    game_id_entry.pack(fill="x", pady=5)

    fetch_button = ttk.Button(input_frame, text="Fetch Questions", command=fetch_questions)
    fetch_button.pack(pady=10)

    result_label = ttk.Label(input_frame, text="", font=("Arial", 12))
    result_label.pack()

    # Scrollable results section
    results_frame = ttk.Frame(root, padding=20)
    results_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(results_frame, bg="#1e1e1e", highlightthickness=0)
    scrollable_frame = ttk.Frame(canvas)

    # Ensure scrollable_frame is properly initialized
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Bind mouse wheel scrolling
    def on_mouse_wheel(event):
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    canvas.pack(side="left", fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    DisplayQuestionsAndAnswersTkinter()
