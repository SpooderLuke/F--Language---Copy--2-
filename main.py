import threading
import tkinter as tk

class SimpleGameInterpreter:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=700, height=1200)
        self.canvas.pack()
        self.commands = {
            'PIZZA': self.draw_rectangle,
            'BURGER': self.get_input,
            'SALAD': self.display_message,
            'SUSHI': self.condition_check,
            'PASTA': self.end_if,
            'TACOS': self.set_variable,
            'STEAK': self.check_variable,
            'RAMEN': self.add_var,
            'SANDWICH': self.create_label,
            'CURRY': self.jump_to_label,
            'KFC': self.clear_screen,
            'COOK': self.set_function,
            'EAT': self.call_function,
            'CHICKEN': self.multiply_var,
            'TURKEY': self.divide_var,
            'CHOCOLATE': self.check_variable_greater,
            'BROCCOLI': self.check_variable_less
        }
        self.variables = {}
        self.functions = {}
        self.if_block = False
        self.labels = {}
        
        self.defs = {}

    def ReadDefs(self,defs):
        lines = defs.split('\n')
        for line in lines:
            parts = line.split(':')
            num = parts[0]
            value = parts[1]
            self.defs[num] = value

    def interpret(self, code):
        self.current_line = 0
        lines = code.split('\n')
        while self.current_line < len(lines):
            line = lines[self.current_line]
            if line:
                parts = line.split(' ')
                beanno = parts[0].split('-')
                command = list(self.commands.keys())
                command = command[len(beanno) -1]
                
                args = parts[1:]

                # Check for variable references and replace them with values
                args_with_values = []
                for arg in args:
                    beanNo = len(arg.split('-'))
                    newArg = self.defs[str(beanNo)]
                    if newArg.startswith('$'):
                        arg_name = newArg[1:]
                        if arg_name in self.variables:
                            args_with_values.append(str(self.variables[arg_name]))
                        else:
                            print(f"Variable '{arg_name}' not found")
                    else:
                        args_with_values.append(newArg)
                print(str(self.current_line)+"--"+command + " " +" ".join(args_with_values))
                if command in self.commands:
                    self.commands[command](*args_with_values)
                else:
                    print(f"Invalid command: {command}")
            self.current_line += 1

    def interpret_ifs(self, code):
        self.current_line = 0
        lines = code.split(',')
        while self.current_line < len(lines):
            line = lines[self.current_line]
            if line:
                parts = line.split(' ')
                command = parts[0].strip("-")
                args = parts[1:]

                # Check for variable references and replace them with values
                args_with_values = []
                for arg in args:
                    if arg.startswith('$'):
                        arg_name = arg[1:]
                        if arg_name in self.variables:
                            args_with_values.append(str(self.variables[arg_name]))
                        else:
                            print(f"Variable '{arg_name}' not found")
                    else:
                        args_with_values.append(arg)

                if command in self.commands:
                    self.commands[command](*args_with_values)
                else:
                    print(f"Invalid command: {command}")
            self.current_line += 1

    def run_interpreter(self, code):
        self.interpret(code)

    def run(self, code):
        interpreter_thread = threading.Thread(target=self.run_interpreter, args=(code,))
        interpreter_thread.start()
        self.root.mainloop()

    def clear_screen(self):
        self.canvas.delete('all')  # Delete all items on the canvas

    def draw_rectangle(self, x, y, width, height):
        print(f"Drawing rectangle at ({x}, {y}) with width {width} and height {height}")
        self.canvas.create_rectangle(int(x), int(y), int(x) + int(width), int(y) + int(height), outline='black')

    def draw_circle(self, x, y, radius):
        print(f"Drawing circle at ({x}, {y}) with radius {radius}")

    def draw_line(self, x1, y1, x2, y2):
        print(f"Drawing line from ({x1}, {y1}) to ({x2}, {y2})")

    def move_cursor(self, x, y):
        print(f"Moving cursor to ({x}, {y})")

    def get_input(self):
        user_input = input("What to do next: ")
        self.variables['input'] = user_input
        #print(f"User input: {user_input}")

    def display_message(self, *message):
        print(" ".join(message))

    def condition_check(self, condition, *code_block):
        if 'input' in self.variables and self.variables['input'] == condition:
            self.if_block = True
            sub_code = " ".join(code_block)
            print(sub_code)
            self.interpret_ifs(sub_code)

    def check_end_if(self):
        if 'ENDIF' in self.variables and self.if_block:
            self.if_block = False
            del self.variables['ENDIF']

    def create_label(self, label_name):
        self.labels[label_name] = self.current_line

    def jump_to_label(self, label_name):
        if label_name in self.labels:
            self.current_line = self.labels[label_name]

    def end_if(self):
        self.variables['ENDIF'] = True

    def set_variable(self, var_name, value, input_type):
        if input_type == 'TEXT':
            self.variables[var_name] = value
        if input_type == 'NUM':
            self.variables[var_name] = int(value)

    def add_var(self, var_name, add):
        self.variables[var_name] += int(add)

    def multiply_var(self, var_name, add):
        self.variables[var_name] * int(add)

    def divide_var(self, var_name, add):
        self.variables[var_name] / int(add)

    def check_variable(self, var_name, var_type, condition, *code_block):
        if var_type == 'TEXT':
            if var_name in self.variables and self.variables[var_name] == condition:
                self.if_block = True
                sub_code = " ".join(code_block)
                self.interpret_ifs(sub_code)
        if var_type == 'NUM':
            if var_name in self.variables and self.variables[var_name] == int(condition):
                self.if_block = True
                sub_code = " ".join(code_block)
                self.interpret_ifs(sub_code)

    def check_variable_greater(self, var_name, condition, *code_block):
        if var_name in self.variables and self.variables[var_name] > int(condition):
            self.if_block = True
            sub_code = " ".join(code_block)
            self.interpret_ifs(sub_code)

    def check_variable_less(self, var_name, condition, *code_block):
        if var_name in self.variables and self.variables[var_name] < int(condition):
            self.if_block = True
            sub_code = " ".join(code_block)
            self.interpret_ifs(sub_code)

    def set_function(self,name,*code_block):
        sub_code = " ".join(code_block)
        self.functions[name] = sub_code

    def call_function(self,name):
        
        self.interpret_ifs(self.functions[name])


# Example usage:
interpreter = SimpleGameInterpreter()
with open('Definitions.txt', 'r') as file:
    defs = file.read()
interpreter.ReadDefs(defs)
with open('code.txt', 'r') as file:
    code = file.read()
interpreter.run(code)
