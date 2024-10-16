import tkinter as tk
from tkinter import scrolledtext, ttk
from openai import OpenAI

def get_response():
    question = question_entry.get()
    if not question:
        output_text.insert(tk.END, "Please enter a question.\n")
        return

    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key="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"
    )

    completion = client.chat.completions.create(
        model="meta/llama-3.2-3b-instruct",
        messages=[{"role": "user", "content": question}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )

    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, "Response:\n", "bold")
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            output_text.insert(tk.END, chunk.choices[0].delta.content)
            output_text.see(tk.END)
            output_text.update_idletasks()
    output_text.insert(tk.END, "\n\n")
    output_text.config(state=tk.DISABLED)
    question_entry.delete(0, tk.END)

def on_enter(event):
    get_response()

# Create the main window
window = tk.Tk()
window.title("AI Chatbot")
window.geometry('800x600')
window.configure(bg='#f0f0f0')

# Custom style
style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=('Arial', 12), borderwidth=1)
style.configure('TEntry', font=('Arial', 12))
style.configure('TLabel', font=('Arial', 14, 'bold'), background='#f0f0f0')

# Frame for input
input_frame = ttk.Frame(window, padding="10")
input_frame.pack(fill=tk.X, padx=20, pady=20)

# Input label and entry
question_label = ttk.Label(input_frame, text="Ask me anything:")
question_label.pack(side=tk.LEFT, padx=(0, 10))
question_entry = ttk.Entry(input_frame, width=50)
question_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
question_entry.bind("<Return>", on_enter)

# Button to send the question
ask_button = ttk.Button(input_frame, text="Ask", command=get_response)
ask_button.pack(side=tk.LEFT, padx=(10, 0))

# Frame for output
output_frame = ttk.Frame(window, padding="10")
output_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=(0, 20))

# ScrolledText widget for displaying the output
output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=('Arial', 12))
output_text.pack(expand=True, fill=tk.BOTH)
output_text.tag_configure("bold", font=('Arial', 12, 'bold'))
output_text.config(state=tk.DISABLED)

# Run the Tkinter event loop
window.mainloop()