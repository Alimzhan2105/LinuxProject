import tkinter as tk
from tkinter import scrolledtext, ttk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.classify import NaiveBayesClassifier
import nltk
from nltk.corpus import stopwords
from ttkthemes import ThemedStyle

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    words = word_tokenize(text.lower())
    words = [lemmatizer.lemmatize(word) for word in words if word.isalnum()]
    words = [word for word in words if word not in stop_words]
    return dict([(word, True) for word in words])

positive_reviews = [("I love this product", "positive"),
                    ("This product is amazing", "positive"),
		    ("Like", "positive"), ("Lovely", "positive"),
                    ("Great purchase, highly recommended", "positive")]

negative_reviews = [("I'm disappointed with this product", "negative"),
                    ("Poor quality, waste of money", "negative"),
                    ("Avoid this product, it's terrible", "negative"),
		    ("bad", "negative"), ("badly", "negative")]

training_data = [(preprocess_text(review), sentiment) for review, sentiment in positive_reviews + negative_reviews]

classifier = NaiveBayesClassifier.train(training_data)

def analyze_text(event=None):
    text = input_area.get("1.0", tk.END).strip()
    if text:
        if "?" in text:
            sentiment = "question"
        else:
            processed_text = preprocess_text(text)
            sentiment = classifier.classify(processed_text)
        
        result_label.config(text="Text Sentiment: {}".format(sentiment))
        
        history_text = "{} - {}".format(text.strip(), sentiment)
        output_area.insert(tk.END, history_text + "\n")
        input_area.delete("1.0", tk.END)
    else:
        result_label.config(text="Enter text to analyze")

def clear_history():
    output_area.delete("1.0", tk.END)

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
root.geometry("500x400")

style = ThemedStyle(root)
style.set_theme("equilux")

style.configure("Analyze.TButton", background="green", foreground="white")
style.map("Analyze.TButton", background=[("active", "red")])
style.configure("Clear.TButton", background="blue", foreground="white")
style.map("Clear.TButton", background=[("active", "red")])

output_area = scrolledtext.ScrolledText(root, height=10, width=60, wrap=tk.WORD, font=("Helvetica", 10))
output_area.grid(row=0, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")

input_area = scrolledtext.ScrolledText(root, height=5, width=60, wrap=tk.WORD, font=("Helvetica", 10))
input_area.grid(row=1, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")

analyze_button = ttk.Button(root, text="Analyze", command=analyze_text, style="TButton")
analyze_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
analyze_button.bind("<Enter>", on_enter_analyze)
analyze_button.bind("<Leave>", on_leave_analyze)

clear_button = ttk.Button(root, text="Clear History", command=clear_history, style="TButton")
clear_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
clear_button.bind("<Enter>", on_enter_clear)
clear_button.bind("<Leave>", on_leave_clear)

result_label = ttk.Label(root, text="", font=("Helvetica", 12))
result_label.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

input_area.bind("<Return>", analyze_text)

root.mainloop()
