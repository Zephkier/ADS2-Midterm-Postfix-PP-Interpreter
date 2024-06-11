# ANSI escape codes
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
RESET = "\033[0m"


class SymbolTable:
    # Initialise as a dict
    def __init__(self, display_steps):
        self.s_table = {}
        self.display_steps = display_steps

    def insert(self, key, value):
        # Limit "key" to 1 character only, as per Task 4 "The Target Hardware"
        if len(key) == 1:
            self.s_table.update({key: value})
            if self.display_steps:
                print(f"{YELLOW}SymbolTable.insert() -> {key} = {value}{RESET}")
            print(f"Assign {key} = {value}")
        else:
            print(
                f"{RED}Error! Cannot initialise variable '{key}': {RESET}variables must be 1 character long"
            )

    def search(self, key):
        if key in self.s_table:
            if self.display_steps:
                print(
                    f"{YELLOW}SymbolTable.search() -> '{key}' exists, it is assigned {self.s_table.get(key)}{RESET}"
                )
            return self.s_table.get(key)
        else:
            if self.display_steps:
                print(f"{YELLOW}SymbolTable.search() -> '{key}' does not exist{RESET}")
            return False

    def delete(self, key):
        if key in self.s_table:
            if self.display_steps:
                print(
                    f"{YELLOW}SymbolTable.delete() -> '{key}' = {self.s_table.get(key)}{RESET}"
                )
            self.s_table.pop(key)
        else:
            if self.display_steps:
                print(
                    f"{YELLOW}SymbolTable.delete() -> '{key}' does not exist in the first place{RESET}"
                )

    def display(self):
        print(f"{YELLOW}class SymbolTable's {{key: value}} pair(s):{RESET}")
        for key, value in self.s_table.items():
            print(f"{YELLOW}'{key}': {value}{RESET}")


def is_float(incoming_string):
    try:
        float(incoming_string)
        return True
    except:
        return False


def append_string_into_stack(
    incoming_string, which_stack, which_stack_again, display_steps
):
    # Store as "old_stack" for printing before-and-after at the end of this function
    old_stack = which_stack.copy()

    # Set "incoming_string" to string dtype, in case another dtype is passed in
    converted_to_string = str(incoming_string)

    # Append into respective stack depending on "incoming_string"'s dtype
    if converted_to_string.isdigit():
        which_stack.append(int(converted_to_string))

    elif is_float(converted_to_string):
        which_stack.append(float(converted_to_string))

    elif converted_to_string.isalpha():
        which_stack.append(str(converted_to_string))

    # Display steps
    if display_steps:
        print(f"{YELLOW}{which_stack_again} = {old_stack} -> {which_stack}{RESET}")


def assign_into_dict(incoming_alphabet, incoming_digit, assign_dict, display_steps):
    assign_dict.update({incoming_alphabet: incoming_digit})
    print(f"Assign {incoming_alphabet} = {incoming_digit}")

    # Display steps
    if display_steps:
        print(f"{YELLOW}{assign_dict}{RESET}")


def calculate_arithmetic(value1, value2, symbol):
    if symbol == "+":
        return value1 + value2

    if symbol == "-":
        return value1 - value2

    if symbol == "*":
        return value1 * value2

    if symbol == "/":
        return value1 / value2


def calculate_arithmetic_in_stack(incoming_symbol, which_stack, display_steps):
    # PDF brief says "3 4 +" means "3 + 4"
    value1 = which_stack.pop()  # Pop 4 first
    value2 = which_stack.pop()  # Pop 3 second

    # Then do 3 + 4 (aka. second + first)
    value_output = calculate_arithmetic(value2, value1, incoming_symbol)

    # Display steps
    if display_steps:
        print(f"{YELLOW}Do arithmetic{RESET}")
        print(
            f"{YELLOW}Pop {value1}, pop {value2}, do {value2} {incoming_symbol} {value1} = {value_output}{RESET}"
        )

    return value_output


def print_help_menu():
    # Must remove indentation for text to show properly
    print(
        f"\n\
{CYAN}Useful commands{RESET}\n\
See SymbolTable: {YELLOW}/s{RESET} or {YELLOW}/symbol{RESET}\n\
Quit program   : {YELLOW}/q{RESET} or {YELLOW}/quit{RESET}\n\
\n\
{CYAN}Usage examples (try copy-pasting!){RESET}\n\
Output should be -46.0             : {YELLOW}5 40 10 / * 64 2 + -{RESET}\n\
Output should be -65.8             : {YELLOW}5 4 100 / * 64 2 + -{RESET}\n\
Make 'a' and 'A' separate variables: {YELLOW}a 3 = A 4 ={RESET}"
    )


def calculate_postfix_arithmetic_with_vars(display_steps=False):
    # Create empty array to hold numbers (both integer and float dtype)
    numbers_stack = []
    # Create empty array to hold alphabets (string dtype)
    alphabets_stack = []
    # Create empty symbol table
    symbol_table = SymbolTable(display_steps)
    # Run program endlessly
    while True:
        # Prompt for user input
        postfix_expression_string = input(
            "\n\033[34mEnter \033[33mpostfix arithmetic expression \033[34mwith (case-sensitive) variables, separated by spaces\nEnter \033[33m/help\033[34m for commands and examples\n> \033[0m",
        )
        # Split incoming string via input's spaces
        terms = postfix_expression_string.split()
        # Go through every term
        for term in terms:
            # Indicate what is being read
            print(f"Read: {term}")
            # If term is number (both integer and float dtype), then append into its array for easy "array[-1]" reference
            if term.isdigit() or is_float(term):
                append_string_into_stack(
                    term, numbers_stack, "numbers_stack", display_steps
                )
            # If term is alphabet...
            elif term.isalpha():
                # Then append into its array for easy "array[-1]" reference
                append_string_into_stack(
                    term, alphabets_stack, "alphabets_stack", display_steps
                )
                # And if term is an existing variable...
                value = symbol_table.search(term)
                if value != False:
                    # Then display the key-value pair
                    print(f"{term} = {value}")
                    # Then append the value into its array for easy "array[-1]" reference
                    append_string_into_stack(
                        value,
                        numbers_stack,
                        "numbers_stack",
                        display_steps,
                    )
            # If term is "=", then call "symbol_table"'s .insert() method
            elif term == "=":
                try:
                    symbol_table.insert(alphabets_stack[-1], numbers_stack[-1])
                except IndexError:
                    print(
                        f"{RED}Error! Invalid postfix expression: {RESET}no variable or value to assign"
                    )
            # If term is arithmetic symbol...
            elif (term == "+") or (term == "-") or (term == "*") or (term == "/"):
                try:
                    # Then do arithmetic calculation
                    output = calculate_arithmetic_in_stack(
                        term, numbers_stack, display_steps
                    )
                    # Display final output
                    print(f"Result: {output}")
                    # Output is either integer or float dtype, but following function takes in string dtype only
                    append_string_into_stack(
                        output, numbers_stack, "numbers_stack", display_steps
                    )
                except IndexError:
                    print(
                        f"{RED}Error! Invalid postfix expression: {RESET}no element to 'pop' for arithmetic calculation"
                    )
            # When term is a command
            elif term == "/help":
                print_help_menu()
            elif (term == "/s") or (term == "/symbol"):
                symbol_table.display()
            elif (term == "/q") or (term == "/quit"):
                print(f"{YELLOW}Quitting program...{RESET}")
                return
            # When term does not match anything above
            else:
                print(f"Nothing happened, please check what you have entered")
        # Clear stacks to keep it tidy
        print(f"...............................")
        print(f"(end of input, clearing stacks)")
        numbers_stack = []
        alphabets_stack = []


# Start program (param "display_steps" = False by default)
calculate_postfix_arithmetic_with_vars(display_steps=True)
