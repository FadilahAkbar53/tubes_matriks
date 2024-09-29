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
    text_steps.delete("1.0", tk.END)
    text_result.delete("1.0", tk.END)
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
        tk.Label(frame_a, text="Matriks A").grid(row=0, columnspan=cols_a, pady=5)
        for i in range(rows_a):
            row_entries = []
            for j in range(cols_a):
                entry = tk.Entry(frame_a, width=5, font=("Arial", 14))
                entry.grid(row=i + 1, column=j, padx=5, pady=5)
                row_entries.append(entry)
            entries_a.append(row_entries)

        # Buat entri matriks B
        tk.Label(frame_b, text="Matriks B").grid(row=0, columnspan=cols_b, pady=5)
        for i in range(rows_b):
            row_entries = []
            for j in range(cols_b):
                entry = tk.Entry(frame_b, width=5, font=("Arial", 14))
                entry.grid(row=i + 1, column=j, padx=5, pady=5)
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

def format_matrix(matrix):
    """Format output sebagai string matriks."""
    return "\n".join(["\t".join([f"{val:.2f}" for val in row]) for row in matrix])

def perform_operation():
    """Lakukan operasi berdasarkan pilihan pengguna."""
    try:
        rows_a = int(entry_rows_a.get())
        cols_a = int(entry_cols_a.get())
        rows_b = int(entry_rows_b.get())
        cols_b = int(entry_cols_b.get())

        text_steps.delete("1.0", tk.END)  # Clear previous steps
        text_result.delete("1.0", tk.END)  # Clear previous result

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

            elif operation.get() == "Determinant":
                if rows_a != cols_a:
                    messagebox.showerror("Error", "Determinant hanya dapat dihitung untuk matriks kuadrat.")
                    return
                result = np.linalg.det(a)
                steps += f"Determinant Matriks A: {result}\n"

            elif operation.get() == "Transpose":
                result = np.transpose(a)
                steps += "Langkah-langkah Transpose:\n"
                for i in range(cols_a):
                    for j in range(rows_a):
                        steps += f"({a[j][i]}) => ({i},{j})\n"

            elif operation.get() == "Invers":
                if rows_a != cols_a:
                    messagebox.showerror("Error", "Invers hanya dapat dihitung untuk matriks kuadrat.")
                    return
                result = np.linalg.inv(a)
                steps += "Langkah-langkah Invers:\n"
                steps += format_matrix(result) + "\n"

            elif operation.get() == "SPL":
                try:
                    augmented_matrix = np.hstack([a, b])
                    rows, cols = augmented_matrix.shape
                    
                    # Eliminasi Gauss
                    for i in range(min(rows, cols - 1)):
                        if augmented_matrix[i, i] == 0:
                            for j in range(i + 1, rows):
                                if augmented_matrix[j, i] != 0:
                                    augmented_matrix[[i, j]] = augmented_matrix[[j, i]]
                                    break
                        if augmented_matrix[i, i] != 0:
                            augmented_matrix[i] = augmented_matrix[i] / augmented_matrix[i, i]
                        for j in range(i + 1, rows):
                            augmented_matrix[j] = augmented_matrix[j] - augmented_matrix[i] * augmented_matrix[j, i]

                    steps += "Langkah-langkah Penyelesaian SPL menggunakan eliminasi Gauss:\n"
                    steps += "Matriks setelah eliminasi Gauss:\n"
                    steps += format_matrix(augmented_matrix) + "\n"

                    no_solution = False
                    infinite_solutions = False

                    for i in range(rows):
                        if np.all(augmented_matrix[i, :-1] == 0) and augmented_matrix[i, -1] != 0:
                            no_solution = True
                            break
                        elif np.all(augmented_matrix[i] == 0):
                            infinite_solutions = True
                    
                    if no_solution:
                        text_result.insert(tk.END, "SPL tidak memiliki solusi.\n")
                        steps += "Sistem tidak memiliki solusi.\n"
                    elif infinite_solutions:
                        text_result.insert(tk.END, "SPL memiliki solusi tak hingga.\n")
                        steps += "Sistem memiliki solusi tak hingga.\n"
                    else:
                        result = np.linalg.solve(a, b)
                        text_result.insert(tk.END, "Solusi SPL:\n" + format_matrix(result) + "\n")
                        steps += "Sistem memiliki solusi unik:\n"
                        steps += format_matrix(result) + "\n"

                except Exception as e:
                    messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
                    return

        text_steps.insert(tk.END, steps)
        text_result.insert(tk.END, format_matrix(result))

    except ValueError:
        messagebox.showerror("Error", "Masukkan angka yang valid.")

# Inisialisasi Tkinter
root = tk.Tk()
root.title("Kalkulator Matriks")
root.geometry("800x600")

# Frame untuk input
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

# Input untuk jumlah baris dan kolom matriks A
tk.Label(frame_input, text="Matriks A (Baris):").grid(row=0, column=0)
entry_rows_a = tk.Entry(frame_input, width=5)
entry_rows_a.grid(row=0, column=1)

tk.Label(frame_input, text="Matriks A (Kolom):").grid(row=0, column=2)
entry_cols_a = tk.Entry(frame_input, width=5)
entry_cols_a.grid(row=0, column=3)

# Input untuk jumlah baris dan kolom matriks B
tk.Label(frame_input, text="Matriks B (Baris):").grid(row=1, column=0)
entry_rows_b = tk.Entry(frame_input, width=5)
entry_rows_b.grid(row=1, column=1)

tk.Label(frame_input, text="Matriks B (Kolom):").grid(row=1, column=2)
entry_cols_b = tk.Entry(frame_input, width=5)
entry_cols_b.grid(row=1, column=3)

# Dropdown untuk operasi
operation = tk.StringVar(value="Penjumlahan")
operation_menu = tk.OptionMenu(frame_input, operation, "Penjumlahan", "Pengurangan", "Perkalian Matriks", "Perkalian Skalar", "Determinant", "Transpose", "Invers", "SPL")
operation_menu.grid(row=2, column=0, columnspan=4)

# Input untuk skalar
tk.Label(frame_input, text="Skalar:").grid(row=3, column=0)
entry_scalar = tk.Entry(frame_input, width=5)
entry_scalar.grid(row=3, column=1)

# Pilihan matriks untuk perhitungan skalar
option_matrix = tk.StringVar(value="Matriks A")
option_menu = tk.OptionMenu(frame_input, option_matrix, "Matriks A", "Matriks B")
option_menu.grid(row=3, column=2)

# Tombol untuk membuat entri matriks dan menghitung hasil
tk.Button(frame_input, text="Buat Entri Matriks", command=create_matrix_entries).grid(row=4, column=0)
tk.Button(frame_input, text="Hitung", command=perform_operation).grid(row=4, column=1)
tk.Button(frame_input, text="Reset", command=reset_fields).grid(row=4, column=2)

# Frame untuk matriks A dan B
frame_a = tk.Frame(root)
frame_a.pack(side=tk.LEFT, padx=10)

frame_b = tk.Frame(root)
frame_b.pack(side=tk.LEFT, padx=10)

# Scrollbar untuk hasil
scrollbar = Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Frame untuk langkah-langkah
text_steps = tk.Text(root, width=40, height=20, yscrollcommand=scrollbar.set)
text_steps.pack(padx=10, pady=10)

# Frame untuk hasil
text_result = tk.Text(root, width=40, height=20, yscrollcommand=scrollbar.set)
text_result.pack(padx=10, pady=10)

scrollbar.config(command=lambda *args: [text_steps.yview(*args), text_result.yview(*args)])

# Daftar untuk menyimpan entri matriks
entries_a = []
entries_b = []

# Menjalankan aplikasi
root.mainloop()
