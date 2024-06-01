import sqlite3
import tkinter
from tkinter import messagebox
import matplotlib.pyplot as plt

root = tkinter.Tk()
root.title("BMI CALCULATOR")
root.geometry('450x350')
root.config(bg='#66c2ff')

font1 = ('Times', 30, 'bold')
font2 = ('Times', 18, 'bold')
font3 = ('Times', 12)

conn = sqlite3.connect('bmi_calculator.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS bmi_records
             (id INTEGER PRIMARY KEY AUTOINCREMENT, height REAL, weight REAL, bmi REAL, category TEXT)''')
conn.commit()

def calculate_bmi():
    try:
        height = float(height_entry.get())
        weight = float(weight_entry.get())
        if height <= 0:
            messagebox.showerror('Error', 'Height must be greater than 0!')
            return None
        bmi = weight / (height ** 2)
        result_label.configure(text="Your BMI is {:.1f}".format(bmi))
        return bmi
    except ValueError:
        messagebox.showerror('Error', 'Enter a valid number')
        return None

def determine_category(bmi):
    if bmi < 18.5:
        stage = "Underweight"
    elif 18.5 <= bmi < 25:
        stage = "Normal weight"
    elif 25 <= bmi < 30:
        stage = "Overweight"
    else:
        stage = "Obese"
    category_label.configure(text="Category: {}".format(stage))
    return stage

def on_calculate():
    bmi = calculate_bmi()
    if bmi is not None:
        category = determine_category(bmi)
        save_to_db(height_entry.get(), weight_entry.get(), bmi, category)

def save_to_db(height, weight, bmi, category):
    conn = sqlite3.connect('bmi_calculator.db')
    c = conn.cursor()
    c.execute("INSERT INTO bmi_records (height, weight, bmi, category) VALUES (?, ?, ?, ?)",
              (height, weight, bmi, category))
    conn.commit()
    conn.close()
    messagebox.showinfo('Success', 'Record saved to database')

def fetch_data():
    conn = sqlite3.connect('bmi_calculator.db')
    c = conn.cursor()
    c.execute("SELECT height, weight, bmi, category FROM bmi_records")
    data = c.fetchall()
    conn.close()
    return data

def plot_data():
    data = fetch_data()
    if not data:
        messagebox.showinfo('No Data', 'No data available to plot')
        return

    heights, weights, bmis, categories = zip(*data)
    
    category_mapping = {'Underweight': 1, 'Normal weight': 2, 'Overweight': 3, 'Obese': 4}
    category_values = [category_mapping[cat] for cat in categories]

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(heights, weights, 'b-', label='Height vs Weight')
    plt.xlabel('Height (m)')
    plt.ylabel('Weight (kg)')
    plt.title('Height vs Weight')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(bmis, category_values, 'r-', label='BMI vs Category')
    plt.xlabel('BMI')
    plt.ylabel('Category')
    plt.yticks(ticks=[1, 2, 3, 4], labels=['Underweight', 'Normal weight', 'Overweight', 'Obese'])
    plt.title('BMI vs Category')
    plt.legend()

    plt.tight_layout()
    plt.show()

title_label = tkinter.Label(root, font=font1, text='BMI CALCULATOR', fg="black", bg="#66c2ff")
title_label.place(x=20, y=20)
height_label = tkinter.Label(root, font=font2, text='Height (m)', fg="black", bg="#66c2ff")
height_label.place(x=20, y=100)
weight_label = tkinter.Label(root, font=font2, text='Weight (kg)', fg="black", bg="#66c2ff")
weight_label.place(x=20, y=160)
result_label = tkinter.Label(root, font=font2, fg="black", bg="#66c2ff", text="")
result_label.place(x=20, y=260)
category_label = tkinter.Label(root, font=font2, fg="black", bg="#66c2ff", text="")
category_label.place(x=20, y=300)

height_entry = tkinter.Entry(root, font=font2, width=10)
height_entry.place(x=150, y=100)
weight_entry = tkinter.Entry(root, font=font2, width=10)
weight_entry.place(x=150, y=160)

result_button = tkinter.Button(root, text='Calculate', width=10, font=font3, command=on_calculate)
result_button.place(x=20, y=200)

graph_button = tkinter.Button(root, text='View Graph', width=10, font=font3, command=plot_data)
graph_button.place(x=170, y=200)

root.mainloop()
