import speech_recognition as sr
import pyttsx3
import random
import tkinter as tk
from tkinter import scrolledtext
import threading

class PredictiveMaintenanceAssistant:
    def __init__(self):
        # Initialize recognizer and TTS engine
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

        # Machine data
        self.machines = {
            "machine1": {"status": "operational", "last_maintenance": "2023-09-15"},
            "machine2": {"status": "needs attention", "last_maintenance": "2023-07-01"},
            "machine3": {"status": "critical", "last_maintenance": "2023-03-20"},
        }

        # Setup GUI
        self.window = tk.Tk()
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
        # Update GUI and speak text
        self.output_screen.insert(tk.END, f"Assistant: {text}\n")
        self.output_screen.yview(tk.END)  # Scroll to the end of the text area
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        # Listen for voice input and convert it to text
        with sr.Microphone() as source:
            self.status_label.config(text="Listening...")
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)
                self.output_screen.insert(tk.END, f"You: {text}\n")
                self.output_screen.yview(tk.END)
                return text.lower()
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that. Could you please repeat?")
                return ""
            except sr.RequestError:
                self.speak("Sorry, there's an issue with the Google API.")
                return ""

    def get_machine_from_command(self, command):
        """Extract the machine name from the command if specified."""
        for machine in self.machines:
            if machine in command:
                return machine
        return None

    def process_command(self, command):
        # Process voice command
        if "status" in command:
            machine = self.get_machine_from_command(command)
            if machine:
                self.speak(f"The status of {machine} is {self.machines[machine]['status']}.")
            else:
                self.speak("For which machine would you like to know the status? Please specify machine1, machine2, or machine3.")

        elif "maintenance" in command:
            if "schedule" in command or "next" in command:
                machine = self.get_machine_from_command(command)
                if machine:
                    days = random.randint(1, 30)
                    self.speak(f"The next maintenance for {machine} is scheduled in {days} days.")
                else:
                    self.speak("For which machine would you like to know the maintenance schedule?")

            elif "last" in command or "previous" in command:
                machine = self.get_machine_from_command(command)
                if machine:
                    self.speak(f"The last maintenance for {machine} was on {self.machines[machine]['last_maintenance']}.")
                else:
                    self.speak("For which machine would you like to know the last maintenance date?")

            else:
                self.speak("Would you like to know about the next scheduled maintenance or the last maintenance performed?")

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
            self.display_commands()  # Show the commands when help is requested

        else:
            self.speak("I'm sorry, I didn't understand that command. Could you please try again or ask for help?")

    def start_listening(self):
        # Start listening for commands in a new thread
        threading.Thread(target=self.voice_assistant_loop, daemon=True).start()

    def voice_assistant_loop(self):
        while True:
            command = self.listen()
            if command:
                if "exit" in command or "goodbye" in command:
                    self.speak("Thank you for using the Predictive Maintenance Assistant. Goodbye!")
                    self.window.quit()  # Close the GUI window
                    break
                self.process_command(command)

    def on_closing(self):
        self.speak("Thank you for using the Predictive Maintenance Assistant. Goodbye!")
        self.window.quit()  # Close the GUI window

    def run(self):
        # Start the GUI event loop
        self.window.mainloop()

if __name__ == "__main__":
    assistant = PredictiveMaintenanceAssistant()
    assistant.run()
