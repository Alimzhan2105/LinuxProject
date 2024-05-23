import tkinter as tk
from tkinter import scrolledtext, ttk, filedialog
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from ttkthemes import ThemedStyle
import threading

nltk.download('vader_lexicon')

analyzer = SentimentIntensityAnalyzer()


def analyze_text(event=None):
    text = input_area.get("1.0", tk.END).strip()
    if text:
        threading.Thread(target=process_text, args=(text,)).start()
    else:
        result_label.config(text="Enter text to analyze")
        detailed_result_label.config(text="")


def process_text(text):
    if text.endswith('?'):
        sentiment = "question"
        detailed_result_label.config(text="This is a question.")
    else:
        sentiment_scores = analyzer.polarity_scores(text)
        compound_score = sentiment_scores['compound']
        pos_score = sentiment_scores['pos']
        neu_score = sentiment_scores['neu']
        neg_score = sentiment_scores['neg']

        sentiment = "neutral"
        if compound_score >= 0.05:
            sentiment = "positive"
        elif compound_score <= -0.05:
            sentiment = "negative"

        detailed_result_label.config(text=(
            f"Detailed Scores:\n"
            f"Compound: {compound_score:.2f}\n"
            f"Positive: {pos_score * 100:.2f}%\n"
            f"Neutral: {neu_score * 100:.2f}%\n"
            f"Negative: {neg_score * 100:.2f}%"
        ))

    result_label.config(text=f"Text Sentiment: {sentiment}")

    history_text = f"{text.strip()} - {sentiment}"
    output_area.insert(tk.END, history_text + "\n")
    input_area.delete("1.0", tk.END)


def clear_history():
    output_area.delete("1.0", tk.END)


def analyze_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        threading.Thread(target=process_file, args=(file_path,)).start()


def process_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            text = line.strip()
            if text:
                if text.endswith('?'):
                    sentiment = "question"
                    detailed_history_text = f"{text}\nThis is a question.\n"
                else:
                    sentiment_scores = analyzer.polarity_scores(text)
                    compound_score = sentiment_scores['compound']
                    pos_score = sentiment_scores['pos']
                    neu_score = sentiment_scores['neu']
                    neg_score = sentiment_scores['neg']

                    sentiment = "neutral"
                    if compound_score >= 0.05:
                        sentiment = "positive"
                    elif compound_score <= -0.05:
                        sentiment = "negative"

                    detailed_history_text = (
                        f"{text}\n"
                        f"Compound: {compound_score:.2f}, Positive: {pos_score * 100:.2f}%, "
                        f"Neutral: {neu_score * 100:.2f}%, Negative: {neg_score * 100:.2f}%\n"
                    )
                output_area.insert(tk.END, detailed_history_text + "\n")


def on_enter_analyze(event):
    analyze_button.config(style="Analyze.TButton")


def on_leave_analyze(event):
    analyze_button.config(style="TButton")


def on_enter_clear(event):
    clear_button.config(style="Clear.TButton")


def on_leave_clear(event):
    clear_button.config(style="TButton")


root = tk.Tk()
root.title("Text Sentiment Analyzer")
root.geometry("600x500")

style = ThemedStyle(root)
style.set_theme("equilux")

style.configure("Analyze.TButton", background="green", foreground="white")
style.map("Analyze.TButton", background=[("active", "red")])
style.configure("Clear.TButton", background="blue", foreground="white")
style.map("Clear.TButton", background=[("active", "red")])

output_area = scrolledtext.ScrolledText(root, height=10, width=80, wrap=tk.WORD, font=("Helvetica", 10))
output_area.grid(row=0, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")

input_area = scrolledtext.ScrolledText(root, height=5, width=80, wrap=tk.WORD, font=("Helvetica", 10))
input_area.grid(row=1, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")

analyze_button = ttk.Button(root, text="Analyze", command=analyze_text, style="TButton")
analyze_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
analyze_button.bind("<Enter>", on_enter_analyze)
analyze_button.bind("<Leave>", on_leave_analyze)

clear_button = ttk.Button(root, text="Clear History", command=clear_history, style="TButton")
clear_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
clear_button.bind("<Enter>", on_enter_clear)
clear_button.bind("<Leave>", on_leave_clear)

upload_button = ttk.Button(root, text="Analyze File", command=analyze_file, style="TButton")
upload_button.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

result_label = ttk.Label(root, text="", font=("Helvetica", 12))
result_label.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

detailed_result_label = ttk.Label(root, text="", font=("Helvetica", 10))
detailed_result_label.grid(row=4, column=0, padx=10, pady=10, columnspan=3)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

input_area.bind("<Return>", analyze_text)

root.mainloop()
