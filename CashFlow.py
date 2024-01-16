import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RecordData:
    def __init__(self):
        self.columns = ["Index", "Monthly Salary", "Monthly Expense", "Investment"]
        self.records = []

    def add_record(self, values):
        index = len(self.records) + 1
        record = {"Index": index}
        record.update(dict(zip(self.columns[1:], values)))
        self.records.append(record)
        return index, record

    def calculate_cash_flow(self):
        net_cash_flow = []
        cumulative_cash_flow = 0

        for record in self.records:
            cash_flow = record["Monthly Salary"] - record["Monthly Expense"] - record["Investment"]
            cumulative_cash_flow += cash_flow
            net_cash_flow.append(cash_flow)

        return net_cash_flow, cumulative_cash_flow

class LoginPage(tk.Tk):
    def __init__(self, record_data):
        super().__init__()

        self.title("Cash Flow Login")
        self.geometry("300x150")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Label(self, text="Username:").pack()
        tk.Entry(self, textvariable=self.username_var).pack()

        tk.Label(self, text="Password:").pack()
        tk.Entry(self, textvariable=self.password_var, show="*").pack()

        tk.Button(self, text="Login", command=lambda: self.check_login(record_data)).pack()

    def check_login(self, record_data):
        username = self.username_var.get()
        password = self.password_var.get()

        if username == "admin" and password == "password":
            self.destroy()
            CashFlowApp(record_data)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

class CashFlowApp(tk.Tk):
    def __init__(self, record_data):
        super().__init__()
        self.title("Cash Flow")

        self.input_entries = []
        self.input_labels = ["Monthly Salary", "Monthly Expense", "Investment"]
        self.record_data = record_data

        self.net_cash_flow_var = tk.DoubleVar()
        self.cumulative_cash_flow_var = tk.DoubleVar()

        for i, label in enumerate(self.input_labels):
            tk.Label(self, text=f"{label}:").grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(self)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            self.input_entries.append(entry)

        tk.Button(self, text="Add Record", command=self.add_record).grid(row=len(self.input_labels), column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self, columns=["Index"] + self.input_labels, show="headings")
        for col in ["Index"] + self.input_labels:
            self.tree.heading(col, text=col)
        self.tree.grid(row=0, column=2, rowspan=len(self.input_labels) + 1, padx=10, pady=10, sticky="nsew")

        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=3, rowspan=len(self.input_labels) + 1, padx=10, pady=10, sticky="nsew")

        for i in range(len(self.input_labels) + 1):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def add_record(self):
        input_values = [float(entry.get()) if entry.get() else 0.0 for entry in self.input_entries]
        index, record = self.record_data.add_record(input_values)

        self.tree.insert("", "end", values=[index] + input_values)

        net_cash_flow, cumulative_cash_flow = self.record_data.calculate_cash_flow()

        self.ax.clear()
        for i in range(1, len(self.input_labels) + 1):
            self.ax.plot([r["Index"] for r in self.record_data.records], [r[self.input_labels[i - 1]] for r in self.record_data.records], label=self.input_labels[i - 1])
        self.ax.set_title('Input Records Over Time')
        self.ax.set_xlabel('Index')
        self.ax.set_ylabel('Amount')
        self.ax.legend()

        # Plot Net Cash Flow
        self.ax.plot([r["Index"] for r in self.record_data.records], net_cash_flow, label="Net Cash Flow", linestyle='--')

        # Plot Cumulative Cash Flow
        self.ax.plot([r["Index"] for r in self.record_data.records], [cumulative_cash_flow] * len(self.record_data.records), label="Cumulative Cash Flow", linestyle=':')

        self.canvas.draw()

if __name__ == "__main__":
    record_data = RecordData()
    login_page = LoginPage(record_data)
    login_page.mainloop()
