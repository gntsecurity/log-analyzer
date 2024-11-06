import tkinter as tk
from tkinter import filedialog, messagebox
import argparse
import re
import csv
from datetime import datetime

def parse_log(file_path, start_date=None, end_date=None, level=None, keyword=None):
    logs = []
    date_format = "%Y-%m-%d %H:%M:%S"  # Adjust this format to match your logs

    with open(file_path, 'r') as file:
        for line in file:
            if start_date or end_date or level or keyword:
                date_match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)
                if date_match:
                    log_date = datetime.strptime(date_match.group(), date_format)
                    if start_date and log_date < datetime.strptime(start_date, date_format):
                        continue
                    if end_date and log_date > datetime.strptime(end_date, date_format):
                        continue
                if level and level not in line:
                    continue
                if keyword and keyword.lower() not in line.lower():
                    continue
            logs.append(line.strip())
    return logs

def export_to_csv(logs, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Log Entry'])
        for log in logs:
            csv_writer.writerow([log])

def analyze_logs():
    file_path = file_path_entry.get()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    level = level_entry.get()
    keyword = keyword_entry.get()
    output_file = output_file_entry.get() or 'filtered_logs.csv'

    if not file_path:
        messagebox.showerror("Error", "Please select a log file.")
        return

    logs = parse_log(file_path, start_date, end_date, level, keyword)
    
    if logs:
        export_to_csv(logs, output_file)
        messagebox.showinfo("Success", f"{len(logs)} log entries found and exported to {output_file}")
    else:
        messagebox.showinfo("No Results", "No log entries found matching the specified criteria.")

def browse_file():
    filename = filedialog.askopenfilename(title="Select Log File", filetypes=(("Log files", "*.log"), ("All files", "*.*")))
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, filename)

# GUI setup
root = tk.Tk()
root.title("Log Analyzer")

tk.Label(root, text="Log File:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
file_path_entry = tk.Entry(root, width=50)
file_path_entry.grid(row=0, column=1, padx=10, pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Start Date (YYYY-MM-DD HH:MM:SS):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
start_date_entry = tk.Entry(root, width=50)
start_date_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="End Date (YYYY-MM-DD HH:MM:SS):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
end_date_entry = tk.Entry(root, width=50)
end_date_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Log Level (e.g., ERROR):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
level_entry = tk.Entry(root, width=50)
level_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Keyword:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
keyword_entry = tk.Entry(root, width=50)
keyword_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Output File Name (optional):").grid(row=5, column=0, padx=10, pady=5, sticky="e")
output_file_entry = tk.Entry(root, width=50)
output_file_entry.grid(row=5, column=1, padx=10, pady=5)

analyze_button = tk.Button(root, text="Analyze Logs", command=analyze_logs)
analyze_button.grid(row=6, column=1, pady=20)

root.mainloop()
