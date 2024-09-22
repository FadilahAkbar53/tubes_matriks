import tkinter as tk
from tkinter import messagebox, Scrollbar, Frame
import numpy as np

def reset_fields():
    """Reset semua input dan hasil."""
    entry_rows_a.delete(0, tk.END)
    entry_cols_a.delete(0, tk.END)
    entry_rows_b.delete(0, tk.END)
    entry_cols_b.delete(0, tk.END)
    entry_scalar.delete(0, tk.END)
    clear_matrix_entries()
    label_result.config(text="")
    label_steps.config(text="")
    operation.set("Penjumlahan")
    option_matrix.set("Matriks A")

def create_matrix_entries():
    """Buat entri matriks berdasarkan input pengguna."""
    try:
        rows_a = int(entry_rows_a.get())
        cols_a = int(entry_cols_a.get())
        rows_b = int(entry_rows_b.get())
        cols_b = int(entry_cols_b.get())

        if (operation.get() in ["Penjumlahan", "Pengurangan"] and (rows_a != rows_b or cols_a != cols_b)) or \
           (operation.get() == "Perkalian Matriks" and cols_a != rows_b):
            messagebox.showerror("Error", "Ukuran matriks tidak sesuai untuk operasi yang dipilih.")
            return

        clear_matrix_entries()

        # Buat entri matriks A
        tk.Label(frame_a, text="Matriks A").grid(row=0, columnspan=cols_a)
        for i in range(rows_a):
            row_entries = []
            for j in range(cols_a):
                entry = tk.Entry(frame_a, width=5)
                entry.grid(row=i + 1, column=j)
                row_entries.append(entry)
            entries_a.append(row_entries)

        # Buat entri matriks B
        tk.Label(frame_b, text="Matriks B").grid(row=0, columnspan=cols_b)
        for i in range(rows_b):
            row_entries = []
            for j in range(cols_b):
                entry = tk.Entry(frame_b, width=5)
                entry.grid(row=i + 1, column=j)
                row_entries.append(entry)
            entries_b.append(row_entries)

    except ValueError:
        messagebox.showerror("Error", "Masukkan angka yang valid.")

def clear_matrix_entries():
    """Hapus entri matriks yang ada."""
    for entry in entries_a:
        for e in entry:
            e.destroy()
    for entry in entries_b:
        for e in entry:
            e.destroy()
    entries_a.clear()
    entries_b.clear()

def perform_operation():
    """Lakukan operasi berdasarkan pilihan pengguna."""
    try:
        rows_a = int(entry_rows_a.get())
        cols_a = int(entry_cols_a.get())
        rows_b = int(entry_rows_b.get())
        cols_b = int(entry_cols_b.get())

        if operation.get() == "Perkalian Skalar":
            scalar = float(entry_scalar.get())
            selected_matrix = option_matrix.get()
            if selected_matrix == "Matriks A":
                a = np.array([[float(entries_a[i][j].get()) for j in range(cols_a)] for i in range(rows_a)])
                result = scalar * a
                steps = f"Langkah-langkah Perkalian Skalar (dengan skalar {scalar}):\n"
                for i in range(rows_a):
                    for j in range(cols_a):
                        steps += f"{scalar} * {a[i][j]} = {result[i][j]}\n"
            elif selected_matrix == "Matriks B":
                b = np.array([[float(entries_b[i][j].get()) for j in range(cols_b)] for i in range(rows_b)])
                result = scalar * b
                steps = f"Langkah-langkah Perkalian Skalar (dengan skalar {scalar}):\n"
                for i in range(rows_b):
                    for j in range(cols_b):
                        steps += f"{scalar} * {b[i][j]} = {result[i][j]}\n"

        else:
            a = np.array([[float(entries_a[i][j].get()) for j in range(cols_a)] for i in range(rows_a)])
            b = np.array([[float(entries_b[i][j].get()) for j in range(cols_b)] for i in range(rows_b)])

            steps = ""

            if operation.get() == "Penjumlahan":
                result = a + b
                steps += "Langkah-langkah Penjumlahan:\n"
                for i in range(rows_a):
                    for j in range(cols_a):
                        steps += f"{a[i][j]} + {b[i][j]} = {result[i][j]}\n"

            elif operation.get() == "Pengurangan":
                result = a - b
                steps += "Langkah-langkah Pengurangan:\n"
                for i in range(rows_a):
                    for j in range(cols_a):
                        steps += f"{a[i][j]} - {b[i][j]} = {result[i][j]}\n"

            elif operation.get() == "Perkalian Matriks":
                result = np.dot(a, b)
                steps += "Langkah-langkah Perkalian Matriks:\n"
                for i in range(rows_a):
                    for j in range(cols_b):
                        step_value = sum(a[i][k] * b[k][j] for k in range(cols_a))
                        steps += f"Baris {i+1}, Kolom {j+1}: "
                        steps += " + ".join([f"({a[i][k]} * {b[k][j]})" for k in range(cols_a)]) + f" = {step_value}\n"

            elif operation.get() == "Transpose Matriks":
                selected_matrix = option_matrix.get()
                if selected_matrix == "Matriks A":
                    result = a.T
                    steps += "Langkah-langkah Transpose Matriks A:\n"
                    for i in range(rows_a):
                        for j in range(cols_a):
                            steps += f"Elemen ({i+1}, {j+1}) menjadi elemen ({j+1}, {i+1})\n"
                elif selected_matrix == "Matriks B":
                    result = b.T
                    steps += "Langkah-langkah Transpose Matriks B:\n"
                    for i in range(rows_b):
                        for j in range(cols_b):
                            steps += f"Elemen ({i+1}, {j+1}) menjadi elemen ({j+1}, {i+1})\n"

            elif operation.get() == "Invers Matriks":
                if np.linalg.det(a) == 0:
                    messagebox.showerror("Error", "Matriks tidak memiliki invers (determinant = 0).")
                    return
                result = np.linalg.inv(a)
                steps += "Langkah-langkah Invers Matriks:\n"
                steps += "Gunakan rumus untuk menghitung invers.\n"

            elif operation.get() == "Determinan Matriks":
                result = np.linalg.det(a)
                steps += "Langkah-langkah Determinan Matriks:\n"
                steps += f"Determinant = {result}\n"

        label_result.config(text=str(result))
        label_steps.config(text=steps)

    except ValueError:
        messagebox.showerror("Error", "Pastikan semua nilai adalah angka.")

# Setup Tkinter
root = tk.Tk()
root.title("Aplikasi Matriks")

# Frame untuk scroll
scroll_frame = Frame(root)
scroll_frame.pack(pady=10)

scrollbar = Scrollbar(scroll_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Canvas untuk konten scroll
canvas = tk.Canvas(scroll_frame, yscrollcommand=scrollbar.set)
canvas.pack(side=tk.LEFT)

scrollbar.config(command=canvas.yview)

# Frame konten
content_frame = Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")

def configure_scroll_region(event):
    """Mengatur area scroll."""
    canvas.configure(scrollregion=canvas.bbox("all"))

content_frame.bind("<Configure>", configure_scroll_region)

# Frame untuk ukuran matriks
frame_size = tk.Frame(content_frame)
frame_size.pack(pady=10)

tk.Label(frame_size, text="Jumlah Baris Matriks A:").grid(row=0, column=0)
entry_rows_a = tk.Entry(frame_size, width=5)
entry_rows_a.grid(row=0, column=1)

tk.Label(frame_size, text="Jumlah Kolom Matriks A:").grid(row=0, column=2)
entry_cols_a = tk.Entry(frame_size, width=5)
entry_cols_a.grid(row=0, column=3)

tk.Label(frame_size, text="Jumlah Baris Matriks B:").grid(row=1, column=0)
entry_rows_b = tk.Entry(frame_size, width=5)
entry_rows_b.grid(row=1, column=1)

tk.Label(frame_size, text="Jumlah Kolom Matriks B:").grid(row=1, column=2)
entry_cols_b = tk.Entry(frame_size, width=5)
entry_cols_b.grid(row=1, column=3)

# Tombol untuk membuat entri matriks
btn_create = tk.Button(frame_size, text="Buat Matriks", command=create_matrix_entries)
btn_create.grid(row=2, columnspan=4)

# Frame untuk matriks A
frame_a = tk.Frame(content_frame)
frame_a.pack(pady=10)

# Frame untuk matriks B
frame_b = tk.Frame(content_frame)
frame_b.pack(pady=10)

# Pilihan operasi
operation = tk.StringVar(value="Penjumlahan")
operations = [
    "Penjumlahan",
    "Pengurangan",
    "Perkalian Matriks",
    "Perkalian Skalar",
    "Transpose Matriks",
    "Invers Matriks",
    "Determinan Matriks"
]
tk.Label(content_frame, text="Pilih Operasi:").pack()
for op in operations:
    tk.Radiobutton(content_frame, text=op, variable=operation, value=op).pack(anchor=tk.W)

# Pilihan untuk mana matriks yang akan dihitung
option_matrix = tk.StringVar(value="Matriks A")
tk.Label(content_frame, text="Pilih Matriks (untuk Transpose/Perkalian Skalar):").pack()
tk.Radiobutton(content_frame, text="Matriks A", variable=option_matrix, value="Matriks A").pack(anchor=tk.W)
tk.Radiobutton(content_frame, text="Matriks B", variable=option_matrix, value="Matriks B").pack(anchor=tk.W)

# Input untuk skalar
tk.Label(content_frame, text="Nilai Skalar:").pack()
entry_scalar = tk.Entry(content_frame, width=5)
entry_scalar.pack(pady=5)

# Tombol untuk menghitung
btn_calculate = tk.Button(content_frame, text="Hitung", command=perform_operation)
btn_calculate.pack(pady=10)

# Label untuk hasil
label_result = tk.Label(content_frame, text="", font=("Arial", 12))
label_result.pack(pady=10)

# Label untuk langkah-langkah pengerjaan
label_steps = tk.Label(content_frame, text="", font=("Arial", 10), justify=tk.LEFT)
label_steps.pack(pady=10)

# Tombol reset
btn_reset = tk.Button(content_frame, text="Reset", command=reset_fields)
btn_reset.pack(pady=10)

entries_a = []
entries_b = []

root.mainloop()
