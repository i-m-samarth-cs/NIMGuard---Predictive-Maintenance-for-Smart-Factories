import tkinter as tk
from tkinter import scrolledtext, ttk
from openai import OpenAI
import speech_recognition as sr
import pyttsx3
import random
import threading
from datetime import datetime, timedelta

class IntegratedAssistant:
    def _init_(self):
        self.window = tk.Tk()
        self.window.title("Integrated AI Assistant")
        self.window.geometry("800x600")
        self.window.configure(bg='#f0f0f0')

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.setup_chatbot_gui()
        self.setup_voice_assistant()

        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key="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"
        )

    def setup_chatbot_gui(self):
        self.chat_frame = ttk.Frame(self.window, padding="10")
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, width=70, height=20, font=("Arial", 12))
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        input_frame = ttk.Frame(self.chat_frame)
        input_frame.pack(fill=tk.X, pady=5)

        self.question_entry = ttk.Entry(input_frame, width=60, font=("Arial", 12))
        self.question_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.question_entry.bind("<Return>", self.on_enter)

        ask_button = ttk.Button(input_frame, text="Ask", command=self.get_chatbot_response)
        ask_button.pack(side=tk.LEFT, padx=(10, 0))

        va_button = ttk.Button(self.chat_frame, text="Open Voice Assistant", command=self.open_voice_assistant)
        va_button.pack(pady=10)

    def setup_voice_assistant(self):
        self.va_window = None
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.listening = False

        self.machines = {
            "machine1": {"status": "operational", "last_maintenance": "2023-09-15"},
            "machine2": {"status": "needs attention", "last_maintenance": "2023-07-01"},
            "machine3": {"status": "critical", "last_maintenance": "2023-03-20"},
        }

    def open_voice_assistant(self):
        if self.va_window is None or not self.va_window.winfo_exists():
            self.va_window = tk.Toplevel(self.window)
            self.va_window.title("Voice Assistant")
            self.va_window.geometry("600x500")

            va_frame = ttk.Frame(self.va_window, padding="20")
            va_frame.pack(fill=tk.BOTH, expand=True)

            self.va_output = scrolledtext.ScrolledText(va_frame, wrap=tk.WORD, width=60, height=20, font=("Arial", 12))
            self.va_output.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

            self.va_status = ttk.Label(va_frame, text="Voice Assistant Ready", font=("Arial", 12))
            self.va_status.pack(pady=5)

            self.listen_button = ttk.Button(va_frame, text="Start Listening", command=self.toggle_listening)
            self.listen_button.pack(pady=10)

            self.va_window.protocol("WM_DELETE_WINDOW", self.close_voice_assistant)
            self.display_va_commands()

    def close_voice_assistant(self):
        self.listening = False
        self.va_window.destroy()
        self.va_window = None

    def on_enter(self, event):
        self.get_chatbot_response()

    def get_chatbot_response(self):
        question = self.question_entry.get()
        if not question:
            self.output_text.insert(tk.END, "Please enter a question.\n")
            return

        self.output_text.insert(tk.END, f"You: {question}\n", "user")
        self.output_text.tag_configure("user", foreground="green")

        completion = self.client.chat.completions.create(
            model="meta/llama-3.2-3b-instruct",
            messages=[{"role": "user", "content": question}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=True
        )

        self.output_text.insert(tk.END, "Assistant: ", "assistant_tag")
        self.output_text.tag_configure("assistant_tag", foreground="blue")

        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                self.output_text.insert(tk.END, chunk.choices[0].delta.content, "assistant")
                self.output_text.see(tk.END)
                self.output_text.update_idletasks()

        self.output_text.insert(tk.END, "\n\n")
        self.output_text.tag_configure("assistant", foreground="blue")
        self.question_entry.delete(0, tk.END)

    def display_va_commands(self):
        commands = (
            "Voice Assistant Commands:\n"
            "1. Ask for the status of machine1, machine2, or machine3\n"
            "2. Inquire about maintenance schedules for a specific machine\n"
            "3. Request failure predictions for a specific machine\n"
            "4. Check machine efficiency for machine1, machine2, or machine3\n"
            "5. Ask for alerts or warnings\n"
            "6. Request optimization recommendations\n"
            "7. Inquire about energy consumption\n"
            "8. Generate a summary report\n"
            "9. Say 'exit' or 'goodbye' to close the assistant"
        )
        self.va_output.insert(tk.END, f"{commands}\n\n")
        self.va_output.yview(tk.END)

    def toggle_listening(self):
        if not self.listening:
            self.listening = True
            self.listen_button.config(text="Stop Listening")
            threading.Thread(target=self.voice_assistant_loop, daemon=True).start()
        else:
            self.listening = False
            self.listen_button.config(text="Start Listening")
            self.va_status.config(text="Listening stopped. Click 'Start Listening' to begin.")

    def voice_assistant_loop(self):
        while self.listening:
            command = self.listen()
            if command:
                if "exit" in command or "goodbye" in command:
                    self.speak("Thank you for using the Voice Assistant. Goodbye!")
                    self.close_voice_assistant()
                    break
                self.process_command(command)
        self.listening = False
        self.listen_button.config(text="Start Listening")

    def listen(self):
        with sr.Microphone() as source:
            self.va_status.config(text="Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                self.va_output.insert(tk.END, f"You: {text}\n", "user")
                self.va_output.tag_configure("user", foreground="green")
                self.va_output.yview(tk.END)
                return text.lower()
            except sr.WaitTimeoutError:
                self.va_status.config(text="Listening timed out. Click 'Start Listening' to try again.")
                return ""
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that. Could you please repeat?")
                return ""
            except sr.RequestError:
                self.speak("Sorry, there's an issue with the speech recognition service.")
                return ""

    def speak(self, text):
        self.va_output.insert(tk.END, f"Assistant: {text}\n", "assistant")
        self.va_output.tag_configure("assistant", foreground="blue")
        self.va_output.yview(tk.END)
        self.engine.say(text)
        self.engine.runAndWait()

    def get_machine_from_command(self, command):
        for machine in self.machines:
            if machine in command:
                return machine
        return None

    def process_command(self, command):
        if "status" in command:
            machine = self.get_machine_from_command(command)
            if machine:
                self.speak(f"The status of {machine} is {self.machines[machine]['status']}.")
            else:
                self.speak("For which machine would you like to know the status? Please specify machine1, machine2, or machine3.")

        elif "maintenance" in command:
            machine = self.get_machine_from_command(command)
            if machine:
                last_maintenance = datetime.strptime(self.machines[machine]['last_maintenance'], "%Y-%m-%d")
                next_maintenance = last_maintenance + timedelta(days=random.randint(30, 90))
                self.speak(f"The last maintenance for {machine} was on {last_maintenance.strftime('%Y-%m-%d')}. The next maintenance is scheduled for {next_maintenance.strftime('%Y-%m-%d')}.")
            else:
                self.speak("For which machine would you like to know the maintenance schedule?")

        elif "predict" in command or "forecast" in command:
            machine = self.get_machine_from_command(command)
            if machine:
                failure_probability = random.randint(1, 100)
                self.speak(f"Based on current data, the probability of failure for {machine} in the next month is {failure_probability}%.")
            else:
                self.speak("For which machine would you like a failure prediction?")

        elif "efficiency" in command or "performance" in command:
            machine = self.get_machine_from_command(command)
            if machine:
                efficiency = random.randint(70, 100)
                self.speak(f"The current efficiency of {machine} is {efficiency}%.")
            else:
                self.speak("For which machine would you like to know the efficiency?")

        elif "alert" in command or "warning" in command:
            critical_machines = [m for m, data in self.machines.items() if data['status'] == 'critical']
            if critical_machines:
                self.speak(f"Warning! The following machines are in critical condition: {', '.join(critical_machines)}")
            else:
                self.speak("There are no critical alerts at the moment.")

        elif "optimize" in command:
            self.speak("Based on current data, I recommend the following optimizations:")
            self.speak("1. Increase preventive maintenance frequency for Machine 2")
            self.speak("2. Adjust operating parameters for Machine 3 to reduce stress")
            self.speak("3. Schedule a comprehensive check-up for Machine 1 within the next two weeks")

        elif "energy" in command:
            total_energy = random.randint(1000, 5000)
            self.speak(f"The total energy consumption of the factory today is {total_energy} kWh.")
            self.speak("Machine 2 is consuming 15% more energy than usual. I recommend checking its efficiency.")

        elif "report" in command:
            self.speak("Generating a summary report for all machines:")
            for machine, data in self.machines.items():
                efficiency = random.randint(70, 100)
                self.speak(f"{machine}: Status - {data['status']}, Efficiency - {efficiency}%, Last maintenance - {data['last_maintenance']}")

        elif "help" in command:
            self.display_va_commands()

        else:
            self.speak("I'm sorry, I didn't understand that command. Could you please try again or ask for help?")

    def run(self):
        self.window.mainloop()

if __name__ == "_main_":
    assistant = IntegratedAssistant()
    assistant.run()