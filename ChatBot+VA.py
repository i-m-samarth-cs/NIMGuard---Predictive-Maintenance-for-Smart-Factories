import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Dict
from datetime import datetime, timedelta
import speech_recognition as sr
import pyttsx3
import random
import threading


class PredictiveMaintenanceChatbotGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Predictive Maintenance Chatbot")
        self.master.geometry("800x600")
        self.master.configure(bg="#2C3E50")  # Dark blue background

        self.machine_data: Dict[str, Dict[str, float]] = {}
        self.maintenance_schedule: Dict[str, str] = {}
        
        self.current_machine_name = "Machine1"  # Default machine name
        self.input_step = 0  # To track the current input step

        self.create_widgets()
        self.get_machine_data()  # Start by collecting machine data

    def create_widgets(self):
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, bg="#ECF0F1", fg="#2C3E50")
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)

        # User input field
        self.user_input = ttk.Entry(self.master, font=("Arial", 12))
        self.user_input.pack(padx=10, pady=5, fill=tk.X)

        # Send button
        self.send_button = ttk.Button(self.master, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        # Voice Assistant Button
        self.voice_assistant_button = ttk.Button(self.master, text="Open Voice Assistant", command=self.open_voice_assistant)
        self.voice_assistant_button.pack(pady=5)

    def display_bot_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "Chatbot: " + message + "\n\n", "bot")
        self.chat_display.tag_config("bot", foreground="#27AE60")  # Green color for bot messages
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def display_user_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "You: " + message + "\n\n", "user")
        self.chat_display.tag_config("user", foreground="#2980B9")  # Blue color for user messages
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def send_message(self):
        user_message = self.user_input.get()
        if user_message.strip() != "":
            self.display_user_message(user_message)
            self.user_input.delete(0, tk.END)

            # Process the user input
            self.collect_data(user_message.strip())

    def open_voice_assistant(self):
        # Create and run the Voice Assistant in a new window
        assistant_window = tk.Toplevel(self.master)
        assistant_app = PredictiveMaintenanceAssistant(assistant_window)

    def get_machine_data(self):
        self.display_bot_message("Welcome to the Predictive Maintenance Chatbot! Please provide the following details one by one:\n"
                                 "1. Age of the machine (in years)")
        self.input_step = 1  # Start collecting age

    def collect_data(self, user_input):
        if self.input_step == 1:  # Age
            self.machine_data[self.current_machine_name] = {}
            self.machine_data[self.current_machine_name]["age"] = float(user_input)
            self.display_bot_message("Thank you! Next, please provide the average operating hours per day.")
            self.input_step += 1
        
        elif self.input_step == 2:  # Operating Hours
            self.machine_data[self.current_machine_name]["operating_hours"] = float(user_input)
            self.display_bot_message("Thank you! Next, please provide the current operating temperature (in °C).")
            self.input_step += 1
        
        elif self.input_step == 3:  # Temperature
            self.machine_data[self.current_machine_name]["temperature"] = float(user_input)
            self.display_bot_message("Thank you! Next, please provide the current vibration level (in mm/s).")
            self.input_step += 1
        
        elif self.input_step == 4:  # Vibration
            self.machine_data[self.current_machine_name]["vibration"] = float(user_input)
            self.display_bot_message("Thank you! Finally, please provide the date of last maintenance (YYYY-MM-DD).")
            self.input_step += 1
        
        elif self.input_step == 5:  # Last Maintenance
            self.maintenance_schedule[self.current_machine_name] = user_input
            self.display_bot_message("Thank you for providing all the details!")
            self.display_bot_message(self.generate_maintenance_recommendation(self.current_machine_name))
            self.input_step = 0  # Reset for future use

    def analyze_machine_data(self, machine_name: str):
        data = self.machine_data[machine_name]
        issues = []

        if data["age"] > 10:
            issues.append("The machine is relatively old and may require more frequent maintenance.")

        if data["operating_hours"] > 16:
            issues.append("The machine is operating for extended periods, which may lead to increased wear and tear.")

        if data["temperature"] > 80:
            issues.append("The operating temperature is high, which could indicate overheating issues.")

        if data["vibration"] > 10:
            issues.append("The vibration level is high, which could indicate potential mechanical problems.")

        last_maintenance = datetime.strptime(self.maintenance_schedule[machine_name], "%Y-%m-%d")
        days_since_maintenance = (datetime.now() - last_maintenance).days

        if days_since_maintenance > 180:
            issues.append("It has been over 6 months since the last maintenance; consider scheduling a check-up soon.")

        return issues

    def generate_maintenance_recommendation(self, machine_name: str) -> str:
        issues = self.analyze_machine_data(machine_name)
        if not issues:
            return f"Based on the current data, {machine_name} appears to be in good condition. Continue with regular maintenance schedules."

        recommendation = f"Here are some recommendations for {machine_name}:\n"
        for issue in issues:
            recommendation += f"- {issue}\n"

        next_maintenance = datetime.strptime(self.maintenance_schedule[machine_name], "%Y-%m-%d") + timedelta(days=180)
        recommendation += f"\nRecommended next maintenance: {next_maintenance.strftime('%Y-%m-%d')}"

        return recommendation


class PredictiveMaintenanceAssistant:
    def __init__(self, window):
        # Initialize recognizer and TTS engine
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

        # Machine data
        self.machines = {
            "machine1": {"status": "operational", "last_maintenance": "2023-09-15"},
            "machine2": {"status": "needs attention", "last_maintenance": "2023-07-01"},
            "machine3": {"status": "critical", "last_maintenance": "2023-03-20"},
        }

        self.window = window
        self.window.title("Predictive Maintenance Assistant")

        # Create text area for displaying conversation history
        self.output_screen = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=60, height=20, font=("Arial", 12))
        self.output_screen.grid(column=0, row=0, padx=10, pady=10)

        # Add a label for showing status
        self.status_label = tk.Label(self.window, text="Welcome! Ready to assist.", font=("Arial", 12))
        self.status_label.grid(column=0, row=1, padx=10, pady=5)

        # Add a button to start listening
        self.listen_button = tk.Button(self.window, text="Listen for Command", command=self.start_listening, font=("Arial", 12))
        self.listen_button.grid(column=0, row=2, padx=10, pady=10)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Display the available commands on initialization
        self.display_commands()

    def display_commands(self):
        commands = (
            "Here are some commands you can use:\n"
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
        self.output_screen.insert(tk.END, f"{commands}\n")
        self.output_screen.yview(tk.END)

    def speak(self, text):
        # Use TTS to speak the provided text
        self.engine.say(text)
        self.engine.runAndWait()

    def start_listening(self):
        # Start a thread for listening to voice commands
        threading.Thread(target=self.listen_for_commands).start()

    def listen_for_commands(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.output_screen.insert(tk.END, "Listening...\n")
            self.output_screen.yview(tk.END)
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio)
            self.output_screen.insert(tk.END, f"You said: {command}\n")
            self.output_screen.yview(tk.END)
            self.process_command(command)
        except sr.UnknownValueError:
            self.output_screen.insert(tk.END, "Sorry, I did not understand that.\n")
            self.output_screen.yview(tk.END)
        except sr.RequestError:
            self.output_screen.insert(tk.END, "Could not request results from the speech recognition service.\n")
            self.output_screen.yview(tk.END)

    def process_command(self, command):
        command = command.lower()
        if "status of machine" in command:
            machine_name = command.split("machine")[-1].strip()
            status = self.machines.get(f"machine{machine_name}", {}).get("status", "unknown machine")
            self.output_screen.insert(tk.END, f"{machine_name} status: {status}\n")
            self.speak(f"The status of {machine_name} is {status}.")
        
        elif "maintenance schedule" in command:
            machine_name = command.split("machine")[-1].strip()
            last_maintenance = self.machines.get(f"machine{machine_name}", {}).get("last_maintenance", "unknown machine")
            self.output_screen.insert(tk.END, f"{machine_name} last maintenance date: {last_maintenance}\n")
            self.speak(f"The last maintenance date for {machine_name} was {last_maintenance}.")
        
        elif "failure prediction" in command:
            self.output_screen.insert(tk.END, "Failure prediction not implemented yet.\n")
            self.speak("Sorry, failure prediction is not implemented yet.")
        
        elif "efficiency" in command:
            self.output_screen.insert(tk.END, "Efficiency check not implemented yet.\n")
            self.speak("Sorry, efficiency check is not implemented yet.")
        
        elif "alerts" in command:
            self.output_screen.insert(tk.END, "No alerts or warnings at the moment.\n")
            self.speak("There are no alerts or warnings at the moment.")
        
        elif "optimization" in command:
            self.output_screen.insert(tk.END, "Optimization recommendations not implemented yet.\n")
            self.speak("Sorry, optimization recommendations are not implemented yet.")
        
        elif "energy consumption" in command:
            self.output_screen.insert(tk.END, "Energy consumption data not available.\n")
            self.speak("Energy consumption data is not available.")
        
        elif "summary report" in command:
            self.output_screen.insert(tk.END, "Summary report generation not implemented yet.\n")
            self.speak("Summary report generation is not implemented yet.")
        
        elif "exit" in command or "goodbye" in command:
            self.output_screen.insert(tk.END, "Goodbye!\n")
            self.speak("Goodbye!")
            self.window.destroy()
        
        else:
            self.output_screen.insert(tk.END, "Command not recognized.\n")
            self.speak("Sorry, I did not recognize that command.")

    def on_closing(self):
        # Close the assistant window
        self.window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PredictiveMaintenanceChatbotGUI(root)
    root.mainloop()
