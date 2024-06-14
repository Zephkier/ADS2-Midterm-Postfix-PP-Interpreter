# Import for Interpreter's "/cls" and "/clear" commands
import os

# ----- Helper code
# ANSI escape codes
BLUE = "\033[34m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"
RESET = "\033[0m"
SPACE = "  "


# Although there is ".isdigit()" method, it returns False for negative integer strings
# This ensures both positive and negative integer strings are correctly filtered
# At this point, all 3 integer/float/string dtypes can come through
def is_integer(input_string):
    try:
        int(input_string)
        return True
    except:
        return False


# There is no ".isfloat()" method, thus, this custom function
# At this point, either float/string dtypes should come through
def is_float(input_string):
    try:
        float(input_string)
        return True
    except:
        return False


def append_into_stack(input_string, output_stack, output_stack_name, show_steps):
    # Store pre-append copy to compare before and after at the end
    old_stack = output_stack.copy()

    # Standardise input's dtype, in case another dtype is passed in
    standardised_incoming = str(input_string)

    # Set input according to its dtype and append
    if is_integer(standardised_incoming):
        output_stack.append(int(standardised_incoming))
    elif is_float(standardised_incoming):
        output_stack.append(float(standardised_incoming))
    elif standardised_incoming.isalpha():
        output_stack.append(str(standardised_incoming))

    # Notify before and after
    if show_steps:
        print(f"{SPACE}{YELLOW}{output_stack_name} = {old_stack} -> {output_stack}{RESET}")


def return_arithmetic_calculation(value1, value2, symbol):
    if symbol == "+":
        return value1 + value2
    elif symbol == "-":
        return value1 - value2
    elif symbol == "*":
        return value1 * value2
    elif symbol == "/":
        return value1 / value2


def return_calculation_in_stack(input_symbol, output_stack, show_steps):
    # Midterm requirements said "3 4 +" means "3 + 4"
    first = output_stack.pop()  # Pop 4 first
    second = output_stack.pop()  # Pop 3 second

    # "3 + 4" = "second + first"
    result = return_arithmetic_calculation(second, first, input_symbol)

    # Notify steps
    if show_steps:
        print(f"{SPACE}{YELLOW}Calculate arithmetic{RESET}")
        print(f"{SPACE}{YELLOW}Pop {first}, pop {second}{RESET}")
        print(f"{SPACE}{YELLOW}Do {second} {input_symbol} {first}, get {result}{RESET}")

    return result


def print_help_menu():
    print()
    print(f"{CYAN}Useful commands{RESET}")
    print(f"Clear terminal  : {YELLOW}/cls {RESET}or {YELLOW}/clear{RESET}")
    print(f"See SymbolTable : {YELLOW}/s   {RESET}or {YELLOW}/symbol{RESET}")
    print(f"Quit Interpreter: {YELLOW}/q   {RESET}or {YELLOW}/quit{RESET}")
    print()
    print(f"{CYAN}Examples (try copy-paste!){RESET}")
    print(f"Output is -65.8: {YELLOW}5 4 100 / * 64 2 + -{RESET}")
    print(f"Assign vars 1  : {YELLOW}A 1 = B 2 ={RESET}")
    print(f"Assign vars 2  : {YELLOW}A 3 = C A ={RESET}")
    print(f"Use vars       : {YELLOW}A B C + +{RESET}")


# ----- Implementation code
class SymbolTable:
    # This class works like a dict, but Midterm requirements said, "the only language structure you can use is the array"
    # Thus, create 2 arrays
    def __init__(self, show_steps):
        self.keys = []
        self.values = []
        self.show_steps = show_steps

    # Returns a value or False
    def search(self, key):
        # If "key" does not exist
        if key not in self.keys:
            if self.show_steps:
                print(f"{SPACE}{YELLOW}SymbolTable.search('{key}') -> does not exist{RESET}")
            return False
        # If "key" exists
        else:
            # Get corresponding index
            index = self.keys.index(key)
            if self.show_steps:
                print(f"{SPACE}{YELLOW}SymbolTable.search('{key}') -> exists -> get value{RESET}")
            # Return corresponding value
            return self.values[index]

    # Does not return anything
    def insert(self, key, value):
        # Create new variable
        if key not in self.keys:
            self.keys.append(key)
            self.values.append(value)
            if self.show_steps:
                print(f"{SPACE}{YELLOW}SymbolTable.insert('{key}', {value}) -> create new var{RESET}")
        # Overwrite existing variable
        else:
            # Get corresponding index
            index = self.keys.index(key)
            # Overwrite at that index
            self.values[index] = value
            # Notify accordingly
            if self.show_steps:
                print(f"{SPACE}{YELLOW}SymbolTable.insert('{key}', {value}) -> overwrite var{RESET}")
        # Notify always
        print(f"Assign : {key} = {value}")

    # Does not return anything
    def delete(self, key):
        # Delete existing variable
        if key in self.keys:
            # Get corresponding index
            index = self.keys.index(key)
            # Notify user
            if self.show_steps:
                print(f"{YELLOW}SymbolTable.delete() -> '{key}' = {self.values[index]}{RESET}")
            # Pop both arrays at same index
            self.keys.pop(index)
            self.values.pop(index)
        # If incoming “key” does not exist in its array, then notify user
        else:
            if self.show_steps:
                print(f"{YELLOW}SymbolTable.delete() -> '{key}' does not exist in the first place{RESET}")

    # Does not return anything # TODO add sorting algo.
    def display(self):
        print(f"\n{CYAN}class SymbolTable's key-value (variable assignment) pairs:{RESET}")
        for i in range(0, len(self.keys)):
            print(f"{SPACE}{self.keys[i]} = {self.values[i]}")


def run_postfix_pp_interpreter(show_steps=False):
    # Holds integer and float dtypes
    numbers_stack = []

    # Holds string dtype
    alphabets_stack = []

    # Call class
    symbol_table = SymbolTable(show_steps)

    # Notify intro
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~ Starting Postfix++ Interpreter ~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # Aesthetic reasons (lb_flag is True initially, False upon "/cls" or "/clear")
    line_break_flag = True

    # Run Interpreter endlessly
    while True:
        # (Re)Set eoi_flag to True
        end_of_input_flag = True

        # Aesthetic reasons for "Notify rules" below
        if line_break_flag:
            # Upon anything other than "/cls" or "/clear", do line break
            print()
        else:
            # Upon "/cls" or "/clear", no line break, just reset lb_flag to True
            line_break_flag = True

        # Notify rules
        print(f"{BLUE}Enter {YELLOW}postfix arithmetic expression {BLUE}with uppercase variables (all terms separated by spaces){RESET}")
        print(f"{BLUE}Enter {YELLOW}/help {BLUE}for commands and examples{RESET}")

        # Prompt for user input
        user_input_string = input(f"{BLUE}> {RESET}")
        print()

        # Split string by its spaces
        terms = user_input_string.split()

        # Go through every term (and its index) within "terms"
        for i, term in enumerate(terms):
            print(f"Reading: {term}")

            if is_integer(term) or is_float(term):
                append_into_stack(term, numbers_stack, "numbers_stack", show_steps)

            elif term.isalpha():
                # Ensure criteria is met as per Midterm requirements
                if (len(term) != 1) or (term.islower()):
                    print(f"{RED}Error! Variable name {RESET}'{term}' {RED}must be 1 uppercase character!{RESET}")
                    break
                append_into_stack(term, alphabets_stack, "alphabets_stack", show_steps)
                # Check term's existence (returns a value or False)
                value = symbol_table.search(term)
                if value == False:
                    # Notify (lack of) existence
                    print(f"'{term}' does not exist")
                else:
                    # Notify existence
                    print(f"{term} = {value}")
                    # Append term's value for potential usage
                    append_into_stack(value, numbers_stack, "numbers_stack", show_steps)

            elif term in ["+", "-", "*", "/"]:
                try:
                    result = return_calculation_in_stack(term, numbers_stack, show_steps)
                    # Notify result
                    print(f"Result : {result}")
                    append_into_stack(result, numbers_stack, "numbers_stack", show_steps)
                except IndexError:
                    print(f"{RED}Error! No element to 'pop' for arithmetic calculation!{RESET}")
                    break
                except ZeroDivisionError:
                    print(f"{RED}Error! Cannot divide by zero!{RESET}")
                    break

            elif term == "=":
                try:
                    # Do var-to-value assignment (eg. "B 1 =")
                    if not terms[i - 1].isalpha():
                        print(f"{SPACE}{YELLOW}Do assignment (var-to-value){RESET}")
                        value = numbers_stack.pop()
                        var = alphabets_stack.pop()
                        symbol_table.insert(var, value)
                    # Do var-to-var assignment (eg. "A B =", A is assignee, B is assigner)
                    else:
                        print(f"{SPACE}{YELLOW}Do assignment (var-to-var){RESET}")
                        # Get assigner and assignee
                        assigner = alphabets_stack.pop()
                        assignee = alphabets_stack.pop()
                        # Assigner should already exist (returns a value or False)
                        assigner_value = symbol_table.search(assigner)
                        if assigner_value != False:
                            symbol_table.insert(assignee, assigner_value)
                        else:
                            print(f"{RED}Error! Assigner variable has no value to assign!{RESET}")
                            break
                except:
                    print(f"{RED}Error! No variable or value to assign!{RESET}")
                    break

            # During commands, set eoi_flag to False
            elif term == "/help":
                end_of_input_flag = False
                print_help_menu()
            elif term in ["/s", "/symbol"]:
                end_of_input_flag = False
                symbol_table.display()
            elif term in ["/cls", "/clear"]:  # Set lb_flag to False too
                end_of_input_flag = False
                line_break_flag = False
                if os.name == "nt":
                    os.system("cls")  # Windows
                else:
                    os.system("clear")  # Non-Windows
            elif term in ["/q", "/quit"]:
                print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("~~~~~ Exiting Postfix++ Interpreter ~~~~~")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                return

            # When "term" does not match anything
            else:
                end_of_input_flag = False
                print(f"{RED}Invalid term, check what you have entered!{RESET}")
                break

        # Clear arrays once done reading user input
        if end_of_input_flag:
            print(f"...............................")
            print(f"(end of input, clearing stacks)")
            numbers_stack = []
            alphabets_stack = []


# Run Postfix++ Interpreter
# @param show_steps: boolean, default False, refers to displaying workings and steps
run_postfix_pp_interpreter()
