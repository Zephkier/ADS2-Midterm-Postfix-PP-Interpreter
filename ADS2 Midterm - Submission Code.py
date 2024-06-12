# Import for Interpreter's "/cls" and "/clear" commands
import os

# ANSI escape codes
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
RESET = "\033[0m"


class SymbolTable:
    # SymbolTable works like a dict, but "the only language structure you can use is the array"
    # Thus, initialise as 2 arrays
    def __init__(self, display_steps):
        self.keys_fake_dict = []
        self.values_fake_dict = []
        self.display_steps = display_steps

    def search(self, key):
        # If incoming "key" exists in "keys" array...
        if key in self.keys_fake_dict:
            # Then get its existing index
            found_index = self.keys_fake_dict.index(key)
            # Notify user
            if self.display_steps:
                print(f"{YELLOW}SymbolTable.search() -> '{key}' exists -> {key} = {self.values_fake_dict[found_index]}{RESET}")
            # Return that value
            return self.values_fake_dict[found_index]
        # Else, if incoming key does not exist in "keys" array, then notify user, and return False
        else:
            if self.display_steps:
                print(f"{YELLOW}SymbolTable.search() -> '{key}' does not exist{RESET}")
            return False

    def insert(self, key, value):
        # Limit "key" to 1 character only, as per Task 4's "The Target Hardware"
        if len(key) == 1:
            # If incoming "key" exists in "keys" array...
            if key in self.keys_fake_dict:
                # Then get its existing index
                found_index = self.keys_fake_dict.index(key)
                # Set the same index in "values" array to be the new "value"
                self.values_fake_dict[found_index] = value
            # Else, if incoming key does not exist in "keys" array, then append new "key" and "value" into respective array
            else:
                self.keys_fake_dict.append(key)
                self.values_fake_dict.append(value)
            # After successful insertion, notify user
            if self.display_steps:
                print(f"{YELLOW}SymbolTable.insert() -> {key} = {value}{RESET}")
            print(f"Assign : {key} = {value}")
        # Else, if "key" is not 1 character, then notify user
        else:
            print(f"{RED}Error! Cannot initialise variable '{key}': {RESET}variables must be 1 character long")

    def delete(self, key):
        # If incoming "key" exists in "keys" array...
        if key in self.keys_fake_dict:
            # Then get its existing index
            found_index = self.keys_fake_dict.index(key)
            # Notify user
            if self.display_steps:
                print(f"{YELLOW}SymbolTable.delete() -> '{key}' = {self.values_fake_dict[found_index]}{RESET}")
            # "Pop" elements from both arrays at that same index
            self.keys_fake_dict.pop(found_index)
            self.values_fake_dict.pop(found_index)
        # Else, if incoming "key" does not exist in "keys" array, then notify user
        else:
            if self.display_steps:
                print(f"{YELLOW}SymbolTable.delete() -> '{key}' does not exist in the first place{RESET}")

    def display(self):
        print(f"{YELLOW}class SymbolTable's variable assignment pair(s):{RESET}")
        # Go through every element in "keys" array, and print both array's elements
        for i in range(len(self.keys_fake_dict)):
            print(f"{YELLOW}{self.keys_fake_dict[i]} = {self.values_fake_dict[i]}{RESET}")


# Although there is ".isdigit()" method, it returns False for negative integers. Thus, this custom function
def is_integer(incoming_string):
    try:
        int(incoming_string)
        return True
    except:
        return False


# There is no ".isfloat()" method. Thus, this custom function
def is_float(incoming_string):
    try:
        # At this point, integer dtype should be filtered, so left with either float or string dtype
        float(incoming_string)
        return True
    except:
        return False


# This function only takes in string dtype, and will filter according to mathematical dtype
def append_string_into_stack(incoming_string, which_stack, which_stack_again, display_steps):
    # Store copy of current stack for printing before-and-after at the end of this function
    old_stack = which_stack.copy()

    # Standardise "incoming_string" dtype, in case another dtype is passed in
    standardised_incoming = str(incoming_string)

    # Append into respective arrays depending dtype
    if is_integer(standardised_incoming):
        which_stack.append(int(standardised_incoming))
    elif is_float(standardised_incoming):
        which_stack.append(float(standardised_incoming))
    elif standardised_incoming.isalpha():
        which_stack.append(str(standardised_incoming))

    # Display steps
    if display_steps:
        print(f"{YELLOW}{which_stack_again} = {old_stack} -> {which_stack}{RESET}")


def return_arithmetic_calculation(value1, value2, symbol):
    if symbol == "+":
        return value1 + value2
    if symbol == "-":
        return value1 - value2
    if symbol == "*":
        return value1 * value2
    if symbol == "/":
        return value1 / value2


def return_arithmetic_calculation_in_stack(incoming_symbol, which_stack, display_steps):
    # PDF brief says "3 4 +" means "3 + 4"
    value1 = which_stack.pop()  # "Pop" 4 first
    value2 = which_stack.pop()  # "Pop" 3 second

    # Then do 3 + 4 (aka. second + first)
    result = return_arithmetic_calculation(value2, value1, incoming_symbol)

    # Display steps
    if display_steps:
        print(f"{YELLOW}Calculate arithmetic{RESET}")
        print(f"{YELLOW}Pop {value1}, pop {value2}, do {value2} {incoming_symbol} {value1} = {result}{RESET}")

    return result


def print_help_menu():
    # Must remove indentation for text to show properly in terminal
    print(
        f"\n\
{CYAN}Useful commands{RESET}\n\
Clear terminal  : {YELLOW}/cls{RESET} or {YELLOW}/clear{RESET}\n\
See SymbolTable : {YELLOW}/s{RESET}   or {YELLOW}/symbol{RESET}\n\
Quit Interpreter: {YELLOW}/q{RESET}   or {YELLOW}/quit{RESET}\n\
\n\
{CYAN}Usage examples (try copy-pasting!){RESET}\n\
Output should be -46.0      : {YELLOW}5 40 10 / * 64 2 + -{RESET}\n\
Output should be -65.8      : {YELLOW}5 4 100 / * 64 2 + -{RESET}\n\
Assign 1-character variables: {YELLOW}a 1 = A 2 = b a ={RESET}"
    )


def run_postfix_pp_interpreter(display_steps=False):
    # To hold numbers (both integer and float dtype)
    numbers_stack = []
    # To hold alphabets (string dtype)
    alphabets_stack = []
    # Call class
    symbol_table = SymbolTable(display_steps)
    # Run Interpreter endlessly
    while True:
        # (Re)set "peoi_flag" to true at beginning
        print_end_of_input_flag = True
        # Notify user about Interpreter (must remove indentation for text to show properly in terminal)
        print(
            f"\n\
{BLUE}Enter {YELLOW}postfix arithmetic expression {BLUE}with (case-sensitive) variables, separated by spaces\n\
Enter {YELLOW}/help {BLUE}for commands and examples{RESET}"
        )
        # Prompt for user input
        initial_postfix_string = input(f"{BLUE}" + "> " + f"{RESET}")
        # Split incoming string via its spaces
        terms = initial_postfix_string.split()
        # Go through every term in "terms" array ("i" is used when term == "=")
        for i, term in enumerate(terms):
            # Notify user the current term
            print(f"Reading: {term}")
            # Ensure to append "term" as per its mathematical dtype
            # Ensure to always append for easy reference using "[-1]"
            if is_integer(term) or is_float(term):
                append_string_into_stack(term, numbers_stack, "numbers_stack", display_steps)
            elif term.isalpha():
                append_string_into_stack(term, alphabets_stack, "alphabets_stack", display_steps)
                # Get "term"'s value
                value = symbol_table.search(term)
                # This has 2 possibilities
                # 1. If creating a new variable, then "symbol_table" will return False
                if value == False:
                    # Notify user, and no need to append as it has already been done
                    print(f"'{term}' does not exist")
                # 2. If calling an existing variable...
                else:
                    # Then notify user of the key-value pair
                    print(f"{term} = {value}")
                    # In event user wants to use variable, append value into respective array
                    append_string_into_stack(value, numbers_stack, "numbers_stack", display_steps)
            # For arithmetic symbols
            elif term == "=":
                try:
                    # If previous term is alphabet (eg. "a b =")...
                    if terms[i - 1].isalpha():
                        # Then "pop" array to get "b", in which its value will be assigned to "a"
                        get_my_value = alphabets_stack.pop()
                        the_value = symbol_table.search(get_my_value)
                        # "Pop" array (again) to get "a", in which it will receive value from "b"
                        assign_to_me = alphabets_stack.pop()
                        # If "b" has no value, then notify user and "break" out of "for" loop (better than using "continue" to stop further errors)
                        if the_value == False:
                            print(f"{RED}Error! Invalid variable: {RESET}'{get_my_value}' has no value to assign to anything")
                            break
                        # Insert variable's (new) value
                        symbol_table.insert(assign_to_me, the_value)
                    # Else, if it is a normal expression (eg. "a 2 ="), then insert as per normal
                    else:
                        # Insert variable's (new) value
                        symbol_table.insert(alphabets_stack.pop(), numbers_stack.pop())
                except IndexError:
                    print(f"{RED}Error! Invalid postfix expression: {RESET}no variable or value to assign")
            elif (term == "+") or (term == "-") or (term == "*") or (term == "/"):
                try:
                    # Do arithmetic calculation
                    result = return_arithmetic_calculation_in_stack(term, numbers_stack, display_steps)
                    # Display result
                    print(f"Result : {result}")
                    # Append result into respective array
                    append_string_into_stack(result, numbers_stack, "numbers_stack", display_steps)
                # If cannot properly do calculation, then notify user and "break" out of "for" loop (better than using "continue" to stop further errors)
                except IndexError:
                    print(f"{RED}Error! Invalid postfix expression: {RESET}no element to 'pop' for arithmetic calculation")
                    break
            # For commands (during this, set "peoi_flag" to False)
            elif term == "/help":
                print_end_of_input_flag = False
                print_help_menu()
            elif (term == "/s") or (term == "/symbol"):
                print_end_of_input_flag = False
                symbol_table.display()
            elif (term == "/cls") or (term == "/clear"):
                print_end_of_input_flag = False
                # For Windows
                if os.name == "nt":
                    os.system("cls")
                # For non-Windows
                else:
                    os.system("clear")
            elif (term == "/q") or (term == "/quit"):
                print(f"{YELLOW}Quitting Postfix++ Interpreter...{RESET}")
                return
            # When "term" does not match anything above
            else:
                print_end_of_input_flag = False
                print(f"Nothing happened, please check what you have entered")
        # Clear arrays to keep "display_steps" tidy
        if print_end_of_input_flag:
            print(f"...............................")
            print(f"(end of input, clearing stacks)")
            numbers_stack = []
            alphabets_stack = []


# Run Postfix++ Interpreter
# @param "display_steps": boolean, refers to displaying behind-the-scene steps
#                         default is False
run_postfix_pp_interpreter(display_steps=False)

"""
In Interpreter, test these postfix expressions:
Expression    Reason
*in /help*    Normal programming
2 5 + +       See error for invalid expression
ab 12 =       See error for invalid assignment
1 =           See error for invalid assignment
=             See error for invalid assignment
"""
