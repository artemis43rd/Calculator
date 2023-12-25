import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def on_button_click(button_text):
    current_text = expression_var.get()

    # Запрет на ввод первым символом символы операций
    if not current_text and button_text in '+.*/^':
        return

    # Запрет на введение двух и более символов операций
    if button_text in '+-*/^.' and current_text and current_text[-1] in '+-*/^.':
        on_delete()
        current_text = current_text[:-1]
    elif button_text == '±':
        on_unary_minus()
        return

    # Ограничение на количество цифр в текущем операнде
    if button_text.isdigit() and '.' not in current_text:
        operand = current_text.split('+')[-1].split('-')[-1].split('*')[-1].split('/')[0]
        if len(operand.replace('-', '')) >= 15:
            return

    current_text += button_text

    expression_var.set(current_text)


def on_key_press(event):
    key = event.char
    if key.isdigit() or key in ['+', '-', '*', '/', '.', '^', '(', ')']:
        on_button_click(key)
    elif event.keysym == 'BackSpace':
        on_delete()
    elif event.keysym == 'Return':
        on_calculate()
    root.update()


def on_clear():
    expression_var.set("")


def on_delete():
    current_text = expression_var.get()
    expression_var.set(current_text[:-1])


def on_calculate():
    infix_expression = expression_var.get()
    try:
        result = eval(infix_expression.replace('^', '**'))
        expression_var.set(str(result))
    except Exception as e:
        messagebox.showerror("Error", "Invalid expression")
        expression_var.set("")


def on_unary_minus():
    current_text =expression_var.get()

    # Добавляем унарный минус только если текущее выражение не пусто
    if current_text and not current_text.startswith('-'):
        expression_var.set('-' + current_text)
    elif current_text and current_text.startswith('-'):
        expression_var.set(current_text[1:])


# Создаем основное окно
root = tk.Tk()
root.title("Калькулятор")
root.resizable(width=False, height=False)

# Прямоугольник под полем для ввода символов
canvas = tk.Canvas(root, width=400, height=40)
canvas.grid(row=0, column=0, columnspan=4, pady=5)
canvas.create_rectangle(0, 0, 400, 40, outline='gray', fill='gray')

# Виджет для отображения текста (метка)
expression_var = tk.StringVar()
label = ttk.Label(root, textvariable=expression_var, font=('Arial', 14))
label.grid(row=0, column=0, columnspan=4, sticky='w', padx=10)

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
ttk.Button(root, text='=', command=on_calculate).grid(row=5, column=3, padx=5, pady=5)
ttk.Button(root, text='±', command=on_unary_minus).grid(row=5, column=2, padx=5, pady=5)

# Привязываем событие нажатия клавиши к функции on_key_press
root.bind('<KeyPress>', on_key_press)

# Запускаем цикл событий
root.mainloop()