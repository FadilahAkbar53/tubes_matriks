import tkinter as tk
from tkinter import messagebox, Scrollbar, Frame
import numpy as np
import random


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
    entry_scalar.grid_remove()  # Pastikan skalar juga disembunyikan saat reset
    entry_scalar_label.grid_remove()


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
                        steps += f"Baris {i + 1}, Kolom {j + 1}: "
                        steps += " + ".join([f"({a[i][k]} * {b[k][j]})" for k in range(cols_a)]) + f" = {step_value}\n"

            elif operation.get() == "Determinant":
                selected_matrix = option_matrix.get()
                if selected_matrix == "Matriks A":
                    if rows_a != cols_a:
                        messagebox.showerror("Error", "Determinant hanya dapat dihitung untuk matriks kuadrat.")
                        return
                    steps += "Langkah-langkah perhitungan Determinant Matriks A:\n"
                    result = np.linalg.det(a)
                    steps += f"Determinant Matriks A: {result}\n"
                elif selected_matrix == "Matriks B":
                    if rows_b != cols_b:
                        messagebox.showerror("Error", "Determinant hanya dapat dihitung untuk matriks kuadrat.")
                        return
                    steps += "Langkah-langkah perhitungan Determinant Matriks B:\n"
                    result = np.linalg.det(b)
                    steps += f"Determinant Matriks B: {result}\n"

            elif operation.get() == "Transpose":
                selected_matrix = option_matrix.get()
                if selected_matrix == "Matriks A":
                    result = np.transpose(a)
                    steps += "Langkah-langkah Transpose Matriks A:\n"
                    for i in range(cols_a):
                        for j in range(rows_a):
                            steps += f"({a[j][i]}) => ({i},{j})\n"
                elif selected_matrix == "Matriks B":
                    result = np.transpose(b)
                    steps += "Langkah-langkah Transpose Matriks B:\n"
                    for i in range(cols_b):
                        for j in range(rows_b):
                            steps += f"({b[j][i]}) => ({i},{j})\n"

            elif operation.get() == "Invers":
                selected_matrix = option_matrix.get()
                if selected_matrix == "Matriks A":
                    if rows_a != cols_a:
                        messagebox.showerror("Error", "Invers hanya dapat dihitung untuk matriks kuadrat.")
                        return
                    result = np.linalg.inv(a)
                    steps += "Langkah-langkah Invers Matriks A:\n"
                    steps += format_matrix(result) + "\n"
                elif selected_matrix == "Matriks B":
                    if rows_b != cols_b:
                        messagebox.showerror("Error", "Invers hanya dapat dihitung untuk matriks kuadrat.")
                        return
                    result = np.linalg.inv(b)
                    steps += "Langkah-langkah Invers Matriks B:\n"
                    steps += format_matrix(result) + "\n"

            elif operation.get() == "Gauss-Jordan":
                try:
                    m, n = a.shape
                    o, q = b.shape
                    selected_matrix = option_matrix.get()
                    if selected_matrix == "Matriks A":    
                        # Implementasi eliminasi Gauss-Jordan

                        steps += "Langkah-langkah eliminasi Gauss-Jordan:\n"

                        # Proses eliminasi
                        for i in range(min(m, n)):
                            # Mencari baris dengan nilai maksimum di kolom i
                            max_row = np.argmax(np.abs(a[i:, i])) + i
                            if max_row != i:
                                steps += f"Tukar baris {i + 1} dengan baris {max_row + 1}\n"
                            a[[i, max_row]] = a[[max_row, i]]

                            # Buat pivot menjadi 1
                            pivot = a[i, i]
                            if pivot != 0:
                                a[i] = a[i] / pivot
                                steps += f"Skalakan baris {i + 1} agar elemen pivot menjadi 1\n"

                            # Eliminasi elemen di atas dan di bawah pivot
                            for j in range(m):
                                if j != i:
                                    factor = a[j, i]
                                    if factor != 0:
                                        a[j] = a[j] - factor * a[i]
                                        steps += f"Kurangi {factor} * baris {i + 1} dari baris {j + 1}\n"

                        # Output hasil akhir
                        result = a
                        steps += "Matriks setelah eliminasi Gauss-Jordan:\n"
                        steps += format_matrix(result) + "\n"
                    
                    elif selected_matrix == "Matriks B":    
                        # Implementasi eliminasi Gauss-Jordan

                        steps += "Langkah-langkah eliminasi Gauss-Jordan:\n"

                        # Proses eliminasi
                        for i in range(min(o, q)):
                            # Mencari baris dengan nilai maksimum di kolom i
                            max_row = np.argmax(np.abs(b[i:, i])) + i
                            if max_row != i:
                                steps += f"Tukar baris {i + 1} dengan baris {max_row + 1}\n"
                            b[[i, max_row]] = b[[max_row, i]]

                            # Buat pivot menjadi 1
                            pivot = b[i, i]
                            if pivot != 0:
                                b[i] = b[i] / pivot
                                steps += f"Skalakan baris {i + 1} agar elemen pivot menjadi 1\n"

                            # Eliminasi elemen di atas dan di bawah pivot
                            for j in range(o):
                                if j != i:
                                    factor = b[j, i]
                                    if factor != 0:
                                        b[j] = b[j] - factor * b[i]
                                        steps += f"Kurangi {factor} * baris {i + 1} dari baris {j + 1}\n"

                        # Output hasil akhir
                        result = b
                        steps += "Matriks setelah eliminasi Gauss-Jordan:\n"
                        steps += format_matrix(result) + "\n"

                except Exception as e:
                    messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
                    return

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
                # Tambahkan operasi lain sesuai kebutuhan
            elif operation.get() == "Jordan Normal Form":
                try:
                    import sympy as sp

                    # Mengonversi input ke matriks SymPy
                    A = sp.Matrix(a)

                    # Menghitung Jordan Normal Form dan matriks basis
                    J, P = A.jordan_form()

                    steps += "Langkah-langkah mencari Jordan Normal Form:\n"
                    steps += "Matriks A:\n" + format_matrix(A) + "\n"
                    steps += "Jordan Normal Form:\n" + format_matrix(J) + "\n"
                    steps += "Matriks Basis:\n" + format_matrix(P) + "\n"

                except Exception as e:
                    messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
                    return

        text_steps.insert(tk.END, steps)
        text_result.insert(tk.END, format_matrix(result))

    except ValueError:
        messagebox.showerror("Error", "Masukkan angka yang valid.")


def update_scalar_input(*args):
    """Menampilkan atau menyembunyikan input skalar berdasarkan pilihan operasi"""
    if operation.get() == "Perkalian Skalar":
        entry_scalar.grid(row=5, column=1, padx=5, pady=5)
        entry_scalar_label.grid(row=5, column=0, padx=5, pady=5, sticky='e')
    else:
        entry_scalar.grid_remove()
        entry_scalar_label.grid_remove()

def randomize_matrices():
    """Mengisi matriks A dan B dengan nilai acak antara 0 hingga 5."""
    try:
        rows_a = int(entry_rows_a.get())
        cols_a = int(entry_cols_a.get())
        rows_b = int(entry_rows_b.get())
        cols_b = int(entry_cols_b.get())

        # Isi matriks A dengan angka acak
        for i in range(rows_a):
            for j in range(cols_a):
                entries_a[i][j].delete(0, tk.END)  # Kosongkan entri
                random_value = random.randint(0, 5)  # Menghasilkan nilai acak antara 0 dan 5
                entries_a[i][j].insert(0, str(random_value))  # Masukkan nilai acak ke entri

        # Isi matriks B dengan angka acak
        for i in range(rows_b):
            for j in range(cols_b):
                entries_b[i][j].delete(0, tk.END)  # Kosongkan entri
                random_value = random.randint(0, 5)  # Menghasilkan nilai acak antara 0 dan 5
                entries_b[i][j].insert(0, str(random_value))  # Masukkan nilai acak ke entri

    except ValueError:
        messagebox.showerror("Error", "Masukkan angka yang valid.")

# Inisialisasi Tkinter
root = tk.Tk()
root.title("Kalkulator Matriks")
root.geometry("700x800")

# Frame untuk input
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

# Dropdown untuk operasi (Urutan 1)
operation = tk.StringVar(value="Penjumlahan")
operation.trace("w", update_scalar_input)  # Memanggil fungsi saat pilihan berubah
tk.Label(frame_input, text="Pilih Operasi:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
operation_menu = tk.OptionMenu(frame_input, operation, "Penjumlahan", "Pengurangan", "Perkalian Matriks",
                               "Perkalian Skalar", "Determinant", "Transpose", "Invers", "Gauss-Jordan", "SPL", "Jordan Normal Form")
operation_menu.grid(row=0, column=1, columnspan=3, padx=5, pady=5)

# Input untuk jumlah baris dan kolom matriks A (Urutan 2)
tk.Label(frame_input, text="Matriks A (Baris):").grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_rows_a = tk.Entry(frame_input, width=5)
entry_rows_a.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Matriks A (Kolom):").grid(row=1, column=2, padx=5, pady=5, sticky='e')
entry_cols_a = tk.Entry(frame_input, width=5)
entry_cols_a.grid(row=1, column=3, padx=5, pady=5)

# Input untuk jumlah baris dan kolom matriks B (Urutan 3)
tk.Label(frame_input, text="Matriks B (Baris):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
entry_rows_b = tk.Entry(frame_input, width=5)
entry_rows_b.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Matriks B (Kolom):").grid(row=2, column=2, padx=5, pady=5, sticky='e')
entry_cols_b = tk.Entry(frame_input, width=5)
entry_cols_b.grid(row=2, column=3, padx=5, pady=5)

# Tombol untuk membuat input matriks
button_create_matrix = tk.Button(frame_input, text="Buat Matriks", command=create_matrix_entries)
button_create_matrix.grid(row=3, column=0, columnspan=4,  pady=10)

# Input untuk skalar (Urutan 4, disembunyikan default)
entry_scalar_label = tk.Label(frame_input, text="Nilai Skalar:")
entry_scalar = tk.Entry(frame_input, width=10)
entry_scalar.grid_remove()
entry_scalar_label.grid_remove()

# Dropdown untuk memilih matriks (Urutan 5)
tk.Label(frame_input, text="Pilih Matriks untuk Skalar:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
option_matrix = tk.StringVar(value="Matriks A")
matrix_menu = tk.OptionMenu(frame_input, option_matrix, "Matriks A", "Matriks B")
matrix_menu.grid(row=4, column=1, padx=5, pady=5)

# Frame untuk matriks A dan B
frame_matrices = tk.Frame(root)
frame_matrices.pack(pady=10)

frame_a = tk.Frame(frame_matrices)
frame_a.grid(row=0, column=0, padx=10)

frame_b = tk.Frame(frame_matrices)
frame_b.grid(row=0, column=1, padx=10)

entries_a = []
entries_b = []

# Tombol untuk melakukan randomize matriks
button_calculate = tk.Button(root, text="Randomize Matriks", command=randomize_matrices)
button_calculate.pack(pady=10)# Tombol untuk melakukan operasi

# Frame untuk tombol operasi dan reset
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

# Tombol untuk melakukan operasi
button_calculate = tk.Button(frame_buttons, text="Hitung", command=perform_operation)
button_calculate.grid(row=0, column=0, padx=10)

# Tombol untuk reset
button_reset = tk.Button(frame_buttons, text="Reset", command=reset_fields)
button_reset.grid(row=0, column=1, padx=10)

# Area teks untuk langkah-langkah dan hasil
frame_results = tk.Frame(root)
frame_results.pack(pady=10)

tk.Label(frame_results, text="Langkah-langkah:").grid(row=0, column=0, padx=5, pady=5)

# Tambahkan scrollbar untuk langkah-langkah
scroll_steps = tk.Scrollbar(frame_results)
scroll_steps.grid(row=1, column=0, sticky='ns', pady=5)

text_steps = tk.Text(frame_results, width=40, height=10, yscrollcommand=scroll_steps.set)
text_steps.grid(row=1, column=0, padx=5, pady=5)

scroll_steps.config(command=text_steps.yview)  # Menghubungkan scrollbar dengan area teks

tk.Label(frame_results, text="Hasil:").grid(row=0, column=1, padx=5, pady=5)

# Tambahkan scrollbar untuk hasil
scroll_result = tk.Scrollbar(frame_results)
scroll_result.grid(row=1, column=1, sticky='ns', pady=5)

text_result = tk.Text(frame_results, width=40, height=10, yscrollcommand=scroll_result.set)
text_result.grid(row=1, column=1, padx=5, pady=5)

scroll_result.config(command=text_result.yview)  # Menghubungkan scrollbar dengan area teks


# Menjalankan aplikasi Tkinter
root.mainloop()
