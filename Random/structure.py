def query_parameter_1():
    # Code for the first query

def query_parameter_2():
    # Code for the second query

# Add more query functions as needed
    def plot_parameter_1():

    # Code for plotting the first parameter

    def plot_parameter_2():
# Code for plotting the second parameter

# Add more plot functions as needed

class MongoDBUI:
    def __init__(self, master):
        # ... (existing code)

        # New buttons for additional queries and plots
        self.query_button_1 = tk.Button(master, text="Query 1", command=self.query_parameter_1)
        self.query_button_1.grid(row=1, column=0, padx=10, pady=10)

        self.plot_button_1 = tk.Button(master, text="Plot 1", command=self.plot_parameter_1)
        self.plot_button_1.grid(row=1, column=1, padx=10, pady=10)

        # Add more buttons as needed

    # ... (existing methods)

    def query_parameter_1(self):
        print("Running Query 1...")
        # Call the function for query_parameter_1

    def plot_parameter_1(self):
        print("Plotting Parameter 1...")
        # Call the function for plot_parameter_1

    # Add more methods for additional queries and plots as needed
