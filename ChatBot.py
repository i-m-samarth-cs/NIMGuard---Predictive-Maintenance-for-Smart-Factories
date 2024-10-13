import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Dict
from datetime import datetime, timedelta

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

if __name__ == "__main__":
    root = tk.Tk()
    app = PredictiveMaintenanceChatbotGUI(root)
    root.mainloop()
