import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re

def infix_to_postfix(infix_expression):
    stack = []
    postfix = []
    operators = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '(': 0, 'unary_minus': 4}

    for token in re.findall(r"[+-/*^]|\d+\.\d+|\d+|\(|\)", infix_expression):
        if token.isnumeric() or '.' in token:
            postfix.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()  # Remove '(' from stack
        elif token in operators or token == 'unary_minus':
            while stack and operators.get(stack[-1], 0) >= operators.get(token, 0):
                postfix.append(stack.pop())
            stack.append(token)

    while stack:
        postfix.append(stack.pop())
    return postfix

def evaluate_postfix(postfix_expression):
    stack = []
    for token in postfix_expression:
        if token.isnumeric() or '.' in token:
            stack.append(float(token))
        elif token == 'unary_minus':
            operand = stack.pop()
            stack.append(-operand)
        else:
            operand2 = stack.pop()
            operand1 = stack.pop()
            if token == '+':
                stack.append(operand1 + operand2)
            elif token == '-':
                stack.append(operand1 - operand2)
            elif token == '*':
                stack.append(operand1 * operand2)
            elif token == '/':
                stack.append(operand1 / operand2)
            elif token == '^':
                stack.append(operand1 ** operand2)
    return stack.pop()

def on_button_click(button_text):
    current_text = entry.get()

    # Запрет на ввод символов, не являющихся цифрами или разрешенными операторами
    if not re.match(r'^[0-9./*^+\-()]$', button_text):
        return

    # Запрет на введение двух и более символов операций
    if button_text in '+-*/^' and current_text and current_text[-1] in '+-*/^':
        on_delete()
        current_text = current_text[:-1]
    current_text += button_text

    entry.insert(tk.END, current_text)

def on_key_press(event):
    current_text = entry.get()

    # Запрет на ввод символов, не являющихся цифрами или разрешенными операторами
    if re.match(r'^[0-9./*^+\-()]$', event.char):
        return

    # Запрет на введение двух и более символов операций
    if (event.char in '+-*/^') and current_text and current_text[-1] in '+-*/^':
        on_delete()
        current_text = current_text[:-1]

    current_text += event.char

    entry.insert(tk.END, current_text)

def on_clear():
    entry.delete(0, tk.END)

def on_delete():
    current_text = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current_text[:-1])

def on_calculate():
    infix_expression = entry.get()
    try:
        postfix_expression = infix_to_postfix(infix_expression)
        result = evaluate_postfix(postfix_expression)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception as e:
        messagebox.showerror("Error", "Invalid expression")
        entry.delete(0, tk.END)

def on_unary_minus():
    current_text = entry.get()

    # Добавляем унарный минус только если текущее выражение не пусто
    if current_text and not current_text.startswith('-'):
        entry.delete(0, tk.END)
        entry.insert(tk.END, '-' + current_text)
    elif current_text and current_text.startswith('-'):
        entry.delete(0, tk.END)
        entry.insert(tk.END, current_text[1:])

# Создаем основное окно
root = tk.Tk()
root.title("Калькулятор")

# Виджет для ввода текста
entry = ttk.Entry(root, width=30, font=('Arial', 14), validate='key')
entry['validatecommand'] = (entry.register(lambda s: True), '%S')

entry.grid(row=0, column=0, columnspan=4)

# Кнопки для цифр и операций
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '^', '+'
]

row_val = 1
col_val = 0

for button in buttons:
    ttk.Button(root, text=button, command=lambda b=button: on_button_click(b)).grid(row=row_val, column=col_val, padx=5,
                                                                                    pady=5)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# Кнопки для дополнительных операций
ttk.Button(root, text='(', command=lambda: on_button_click('(')).grid(row=5, column=0, padx=5, pady=5)
ttk.Button(root, text=')', command=lambda: on_button_click(')')).grid(row=5, column=1, padx=5, pady=5)
ttk.Button(root, text='C', command=on_clear).grid(row=6, column=2, padx=5, pady=5)  
ttk.Button(root, text='DEL', command=on_delete).grid(row=6, column=1, padx=5, pady=5)
ttk.Button(root, text='±', command=on_unary_minus).grid(row=5, column=2, padx=5, pady=5)
ttk.Button(root, text='=', command=on_calculate).grid(row=5, column=3, padx=5, pady=5)

# Запускаем цикл событий
root.bind("<Key>", on_key_press)
root.mainloop()