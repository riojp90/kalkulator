import tkinter as tk
from tkinter import ttk
import math

LARGE_FONT_STYLE = ("Arial", 20, "bold")
DEFAULT_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
LABEL_COLOR = "#25265E"
WHITE = "#FFFFFF"
LIGHT_GRAY = "#F5F5F5"
LIGHT_BLUE = "#CCEDFF"

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("400x667")
        self.window.resizable(0, 0)
        self.window.title("Scientific & Programmer Calculator")

        self.total_expression = ""
        self.current_expression = ""
        self.current_base = 10

        self.is_programmer_mode = False

        self.create_display_frame()
        self.create_buttons_frame()
        self.create_display_labels()
        self.create_mode_buttons()

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_clear_button()
        self.create_equals_button()
        self.create_special_buttons()
        self.create_scientific_buttons()
        self.create_programmer_buttons()
        
        self.bind_keys()

    def create_display_frame(self):
        self.display_frame = tk.Frame(self.window, height=100, bg=LIGHT_GRAY)
        self.display_frame.pack(expand=True, fill="both")

    def create_display_labels(self):
        self.total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=DEFAULT_FONT_STYLE)
        self.total_label.pack(expand=True, fill='both')

        self.label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        self.label.pack(expand=True, fill='both')

    def create_buttons_frame(self):
        self.buttons_frame = tk.Frame(self.window)
        self.buttons_frame.pack(expand=True, fill="both")
        for x in range(4):
            self.buttons_frame.columnconfigure(x, weight=1)
        for y in range(7):
            self.buttons_frame.rowconfigure(y, weight=1)

    def create_digit_buttons(self):
        digits = {
            1: (4, 0), 2: (4, 1), 3: (4, 2),
            4: (5, 0), 5: (5, 1), 6: (5, 2),
            7: (6, 0), 8: (6, 1), 9: (6, 2),
            0: (7, 1)
        }
        for digit, grid_value in digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE, borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

        decimal_button = tk.Button(self.buttons_frame, text=".", bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE, borderwidth=0, command=lambda: self.add_to_expression('.'))
        decimal_button.grid(row=7, column=0, sticky=tk.NSEW)

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="CE", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.clear)
        button.grid(row=1, column=3, sticky=tk.NSEW)

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_delete_button(self):
        button = tk.Button(self.buttons_frame, text="Del", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.delete)
        button.grid(row=1, column=3, sticky=tk.NSEW)

    def delete(self):
        self.current_expression = self.current_expression[:-1]
        self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.evaluate)
        button.grid(row=7, column=2, sticky=tk.NSEW)

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_special_buttons(self):
        self.create_sqrt_button()
        self.create_percent_button()

    def create_percent_button(self):
        button = tk.Button(self.buttons_frame, text="%", bg=WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.percent)
        button.grid(row=1, column=0, sticky=tk.NSEW)

    def percent(self):
        try:
            self.current_expression = str(eval(f"{self.current_expression}/100"))
            self.update_label()
        except Exception as e:
            self.current_expression = "Error"
            self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="√x", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.sqrt)
        button.grid(row=3, column=3, sticky=tk.NSEW)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_operator_buttons(self):
        operators = {
            "/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"
        }
        positions = {
            "/": (4, 3), "*": (5, 3), "-": (7, 3), "+": (6, 3)
        }
        for operator, symbol in operators.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=positions[operator][0], column=positions[operator][1], sticky=tk.NSEW)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_mode_buttons(self):
        self.mode_var = tk.StringVar(value="Scientific")

        scientific_button = tk.Radiobutton(self.window, text="Scientific", variable=self.mode_var, value="Scientific", command=self.switch_mode)
        scientific_button.pack(side=tk.LEFT)

        programmer_button = tk.Radiobutton(self.window, text="Programmer", variable=self.mode_var, value="Programmer", command=self.switch_mode)
        programmer_button.pack(side=tk.RIGHT)

    def switch_mode(self):
        mode = self.mode_var.get()
        if mode == "Scientific":
            self.show_scientific_buttons()
            self.hide_programmer_buttons()
        else:
            self.show_programmer_buttons()
            self.hide_scientific_buttons()

    def create_scientific_buttons(self):
        self.scientific_buttons = []
        self.create_trig_buttons()
        self.create_log_buttons()
        self.create_constant_buttons()
        self.create_factorial_button()
        self.create_special_buttons()

    def create_trig_buttons(self):
        trig_functions = {
            "sin": (2, 0), "cos": (2, 1), "tan": (2, 2)
        }
        for func, grid_value in trig_functions.items():
            button = tk.Button(self.buttons_frame, text=func, bg=WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda x=func: self.add_trig_function(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)
            self.scientific_buttons.append(button)

    def add_trig_function(self, func):
        try:
            if self.current_expression == "90" and func == "tan":
                self.current_expression = "Undefined"
            elif self.current_expression == "270" and func == "tan":
                self.current_expression = "Undefined"
            elif self.current_expression == "0" and func == "tan":
                self.current_expression = "0"
            elif self.current_expression == "180" and func == "tan":
                self.current_expression = "0"
            elif self.current_expression == "360" and func == "tan":
                self.current_expression = "0"
            elif self.current_expression == "0" and func == "sin":
                self.current_expression = "0"
            elif self.current_expression == "180" and func == "sin":
                self.current_expression = "0"
            elif self.current_expression == "360" and func == "sin":
                self.current_expression = "0"
            elif self.current_expression == "90" and func == "cos":
                self.current_expression = "0"
            elif self.current_expression == "270" and func == "cos":
                self.current_expression = "0"
            else:
                value = eval(f"math.{func}(math.radians(float({self.current_expression})))")
                self.current_expression = str(value)
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_log_buttons(self):
        log_functions = {
            "log": (3, 0), "ln": (3, 1)
        }
        for func, grid_value in log_functions.items():
            button = tk.Button(self.buttons_frame, text=func, bg=WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda x=func: self.add_log_function(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)
            self.scientific_buttons.append(button)

    def add_log_function(self, func):
        try:
            if func == "log":
                value = math.log10(float(self.current_expression))
            elif func == "ln":
                value = math.log(float(self.current_expression))
            self.current_expression = str(value)
            self.update_label()
        except Exception as e:
            self.current_expression = "Error"
            self.update_label()

    def create_constant_buttons(self):
        constants = {
            "π": (1, 1), "e": (1, 2), "⌫": (2, 3)
        }
        for const, grid_value in constants.items():
            button = tk.Button(self.buttons_frame, text=const, bg=WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda x=const: self.add_constant(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)
            self.scientific_buttons.append(button)

    def add_constant(self, const):
        if const == "π":
            self.current_expression += str(math.pi)
        elif const == "e":
            self.current_expression += str(math.e)
        elif const == "⌫":
            backspace_button = tk.Button(self.buttons_frame, text="⌫", bg=WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.delete)
            backspace_button.grid(row=2, column=3, sticky=tk.NSEW)
            self.scientific_buttons.append(backspace_button)

    def create_factorial_button(self):
        button = tk.Button(self.buttons_frame, text="x!", bg=WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.factorial)
        button.grid(row=3, column=2, sticky=tk.NSEW)
        self.scientific_buttons.append(button)

    def factorial(self):
        try:
            value = math.factorial(int(self.current_expression))
            self.current_expression = str(value)
            self.update_label()
        except Exception as e:
            self.current_expression = "Error"
            self.update_label()

    def show_scientific_buttons(self):
        for button in self.scientific_buttons:
            button.grid()

    def hide_scientific_buttons(self):
        for button in self.scientific_buttons:
            button.grid_remove()

    def create_programmer_buttons(self):
        self.programmer_buttons = []

        bases = ["DEC", "BIN", "OCT", "HEX"]
        self.from_base = tk.StringVar(value="DEC")
        self.to_base = tk.StringVar(value="BIN")

        from_label = tk.Label(self.buttons_frame, text="From:", bg=LIGHT_GRAY, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE)
        from_label.grid(row=0, column=0, sticky=tk.W)
        self.programmer_buttons.append(from_label)

        from_menu = ttk.Combobox(self.buttons_frame, textvariable=self.from_base, values=bases, font=DEFAULT_FONT_STYLE, state="readonly")
        from_menu.grid(row=0, column=0, sticky=tk.E)
        self.programmer_buttons.append(from_menu)

        to_label = tk.Label(self.buttons_frame, text="To:", bg=LIGHT_GRAY, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE)
        to_label.grid(row=0, column=1, sticky=tk.W)
        self.programmer_buttons.append(to_label)

        to_menu = ttk.Combobox(self.buttons_frame, textvariable=self.to_base, values=bases, font=DEFAULT_FONT_STYLE, state="readonly")
        to_menu.grid(row=0, column=1, sticky=tk.E)
        self.programmer_buttons.append(to_menu)

        self.create_base_buttons()
        self.create_conversion_button()

    def create_base_buttons(self):
        hex_digits = {
            'A': (5, 0), 'B': (5, 1), 'C': (5, 2),
            'D': (5, 3), 'E': (6, 0), 'F': (6, 1)
        }
        for digit, grid_value in hex_digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE, borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)
            self.programmer_buttons.append(button)

    def create_conversion_button(self):
        button = tk.Button(self.buttons_frame, text="Convert", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.convert_base)
        button.grid(row=6, column=2, columnspan=2, sticky=tk.NSEW)
        self.programmer_buttons.append(button)

    def convert_base(self):
        try:
            value = int(self.current_expression, self.get_base(self.from_base.get()))
            if self.to_base.get() == "DEC":
                self.current_expression = str(value)
            elif self.to_base.get() == "BIN":
                self.current_expression = bin(value)[2:]
            elif self.to_base.get() == "OCT":
                self.current_expression = oct(value)[2:]
            elif self.to_base.get() == "HEX":
                self.current_expression = hex(value)[2:].upper()
            self.update_label()
        except ValueError:
            self.current_expression = "Error"
            self.update_label()

    def get_base(self, base):
        if base == "DEC":
            return 10
        elif base == "BIN":
            return 2
        elif base == "OCT":
            return 8
        elif base == "HEX":
            return 16

    def show_programmer_buttons(self):
        for button in self.programmer_buttons:
            button.grid()

    def hide_programmer_buttons(self):
        for button in self.programmer_buttons:
            button.grid_remove()

    def update_total_label(self):
        self.total_label.config(text=self.total_expression[:11])

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        self.window.bind("<BackSpace>", lambda event: self.delete())
        self.window.bind("<Escape>", lambda event: self.clear())

        for key in range(10):
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        self.window.bind(".", lambda event: self.add_to_expression('.'))

        operators = {
            "/": "/", "*": "*", "-": "-", "+": "+"
        }
        for key, operator in operators.items():
            self.window.bind(key, lambda event, operator=operator: self.append_operator(operator))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()
