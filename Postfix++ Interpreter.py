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
    # Midterm requirements: "3 4 +" means "3 + 4"
    first = output_stack.pop()  # Pop 4 first
    second = output_stack.pop()  # Pop 3 second

    # "3 + 4" = "second + first"
    result = return_arithmetic_calculation(second, first, input_symbol)

    if show_steps:
        print(f"{SPACE}{YELLOW}Calculate arithmetic{RESET}")
        print(f"{SPACE}{YELLOW}Pop {first}, pop {second}{RESET}")
        print(f"{SPACE}{YELLOW}Do {second} {input_symbol} {first}, get {result}{RESET}")

    return result


def print_help_menu():
    print()
    print(f"{CYAN}Examples (try copy-paste!){RESET}")
    print(f"Output is -65.8: {YELLOW}5 4 100 / * 64 2 + -{RESET}")
    print(f"Assign vars (1): {YELLOW}A 1 = B 2 ={RESET}")
    print(f"Assign vars (2): {YELLOW}A 3 = C A ={RESET}")
    print(f"Use vars       : {YELLOW}A B C + +{RESET}")
    print(f"Test sorting   : {YELLOW}D 41 = A 50.1 = F -36 = C 0.01 = B 50 = G -36.1 = E 1 ={RESET}")
    print()
    print(f"{CYAN}SymbolTable commands{RESET}")
    print(f"See SymbolTable (sort by 'keys') (1): {YELLOW}/s     {RESET}or {YELLOW}/symbol{RESET}")
    print(f"                                 (2): {YELLOW}/s-key {RESET}or {YELLOW}/symbol-key{RESET}")
    print(f"                                 (3): {YELLOW}/s-var {RESET}or {YELLOW}/symbol-var{RESET}")
    print(f"See SymbolTable (sort by 'values')  : {YELLOW}/s-val {RESET}or {YELLOW}/symbol-val{RESET}")
    print()
    print(f"{CYAN}General commands{RESET}")
    print(f"Clear terminal  : {YELLOW}/cls {RESET}or {YELLOW}/clear{RESET}")
    print(f"Quit Interpreter: {YELLOW}/q   {RESET}or {YELLOW}/quit{RESET}")


# ----- Implementation code
class SymbolTable:
    # Works like a dictionary but Midterm requirements: "only language structure you can use is the array"
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
            if self.show_steps:
                print(f"{SPACE}{YELLOW}SymbolTable.insert('{key}', {value}) -> overwrite var{RESET}")

    # Does not return anything (default = sort by keys)
    # https://www.youtube.com/watch?v=cVZMah9kEjI
    def merge_sort(self, keys, values, sort_by_keys=True):
        if len(keys) > 1:
            # Get midpoint to split array into half
            mid = len(keys) // 2
            keys_L = keys[:mid]
            keys_R = keys[mid:]
            values_L = values[:mid]
            values_R = values[mid:]

            # Recursive call to split array till it has 1 element to do merge sort
            self.merge_sort(keys_L, values_L, sort_by_keys)
            self.merge_sort(keys_R, values_R, sort_by_keys)

            i = 0  # Index of array L
            j = 0  # Index of array R
            k = 0  # Index of array_merged

            # Merge sorted halves back into array_merged
            while i < len(keys_L) and j < len(keys_R):
                # Check if sorting by keys or values
                # Compare L's and R's elements
                # Put smaller element into array_merged

                # When (L < R)
                if (sort_by_keys and keys_L[i] < keys_R[j]) or (not sort_by_keys and values_L[i] < values_R[j]):
                    keys[k] = keys_L[i]
                    values[k] = values_L[i]
                    i += 1
                # When (R < L) or (R == L)
                else:
                    keys[k] = keys_R[j]
                    values[k] = values_R[j]
                    j += 1
                k += 1

            # Add L's remaining elements into array_merged
            while i < len(keys_L):
                keys[k] = keys_L[i]
                values[k] = values_L[i]
                i += 1
                k += 1

            # Add R's remaining elements into array_merged
            while j < len(keys_R):
                keys[k] = keys_R[j]
                values[k] = values_R[j]
                j += 1
                k += 1

    # Does not return anything
    def display_and_sort(self, sort_by="keys"):
        # Default = sort by keys
        if sort_by == "keys":
            sort_by_keys = True
        else:
            sort_by_keys = False
        self.merge_sort(self.keys, self.values, sort_by_keys)
        print(f"\n{CYAN}class SymbolTable's key-value (variable assignment) pairs, sorted by '{sort_by}':{RESET}")
        for i in range(len(self.keys)):
            print(f"{SPACE}{self.keys[i]} = {self.values[i]}")


def run_postfix_pp_interpreter(show_steps=False):
    """
    Run the Postfix++ Interpreter

    Args:
        show_steps (bool, optional): Show workings and steps. Defaults to False.
    """

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
        print(f"{BLUE}Enter {YELLOW}/help {BLUE}for examples and commands{RESET}")

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
                # Midterm requirements: "variable namespace 'A'-'Z'"
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
                        if show_steps:
                            print(f"{SPACE}{YELLOW}Do assignment (var-to-value){RESET}")
                        value = numbers_stack.pop()
                        var = alphabets_stack.pop()
                        symbol_table.insert(var, value)
                        # Notify assignment
                        print(f"Assign : {var} = {value}")
                    # Do var-to-var assignment (eg. "A B =", A is assignee, B is assigner)
                    else:
                        if show_steps:
                            print(f"{SPACE}{YELLOW}Do assignment (var-to-var){RESET}")
                        # Get assigner and assignee
                        assigner = alphabets_stack.pop()
                        assignee = alphabets_stack.pop()
                        # Assigner should already exist (returns a value or False)
                        assigner_value = symbol_table.search(assigner)
                        if assigner_value != False:
                            symbol_table.insert(assignee, assigner_value)
                            # Notify assignment
                            print(f"Assign : {assignee} = {assigner_value}")
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

            elif term in ["/s-key", "/symbol-key", "/s", "/symbol", "/s-var", "/symbol-var"]:
                end_of_input_flag = False
                symbol_table.display_and_sort(sort_by="keys")

            elif term in ["/s-val", "/symbol-val"]:
                end_of_input_flag = False
                symbol_table.display_and_sort(sort_by="values")

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
            print(f"-------------------------------")
            print(f"(end of input, clearing stacks)")
            numbers_stack = []
            alphabets_stack = []


run_postfix_pp_interpreter(show_steps=False)
