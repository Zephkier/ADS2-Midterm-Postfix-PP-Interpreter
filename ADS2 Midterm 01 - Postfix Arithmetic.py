def calculate_arithmetic(value1, value2, symbol):
    if symbol == "+":
        return value1 + value2

    if symbol == "-":
        return value1 - value2

    if symbol == "*":
        return value1 * value2

    if symbol == "/":
        return value1 / value2


def calculate_postfix_arithmetic(postfix_expression_string):
    # Create empty array to hold digits
    my_stack = []

    # Split incoming string (via spaces) into array of terms and symbols
    terms = postfix_expression_string.split()

    # Indicate entire expression and how it is split (aka. its terms)
    print("-----")
    print(f"Expression: {postfix_expression_string}")
    print(f"Terms:      {terms}")
    print("-----")

    # Go through every term
    for term in terms:
        # Indicate current term
        print(f"Read: {term}")

        # If term is digit, then append (as integer) into array
        if term.isdigit():
            print(f"Append into 'my_stack'")

            my_stack.append(int(term))
            print(f"{my_stack}")

        # If term is arithmetic symbol, then do arithmetic, and append (as integer) into array
        elif (term == "+") or (term == "-") or (term == "*") or (term == "/"):
            try:
                print(f"Do arithmetic")

                # PDF brief says: "3 4 +" means "3 + 4"
                value1 = my_stack.pop()  # Pop 4 first
                value2 = my_stack.pop()  # Pop 3 second
                value_output = calculate_arithmetic(
                    value2, value1, term
                )  # Thus, do 3 + 4 (aka. second + first)
                my_stack.append(int(value_output))

                print(f"Pop {value1} first")
                print(f"Pop {value2} second")
                print(f"Thus, do {value2} {term} {value1}, which is {value_output}")
                print(f"Append into 'my_stack'")
                print(f"{my_stack}")

            except IndexError:
                print(
                    "Invalid postfix expression: Not enough elements within 'my_stack' to 'pop' for arithmetic calculation"
                )
                return

        # If term is neither digit nor arithmetic symbol (eg. @ or $), then do nothing
        else:
            print(f"Do nothing")
            print(f"{my_stack}")

        # Indicate end of current term
        print("-----")

    # Read array's final result
    print(f"Final result")
    print(f"{my_stack}")


# Prompt user to enter input
# calculate_postfix_arithmetic(
#     input("Enter postfix expression, separated by spaces (eg. 5 10 +):\n")
# )

# With space
# calculate_postfix_arithmetic("3 4 5 + *")  # 27

# Without space
# calculate_postfix_arithmetic("345+*")  # []

# With weird symbols
# calculate_postfix_arithmetic("3 4 ! 50 + * @# $ ")  # 162 with "Do nothing"s
# calculate_postfix_arithmetic(" 3   4 ! 50 + * @# $ ")  # 162 with "Do nothing"s
# calculate_postfix_arithmetic("3 4 + * / -")  # IndexError: pop from empty list

# More tests
# calculate_postfix_arithmetic("45 72+ -*")  # 45
# calculate_postfix_arithmetic("3 4 + 2 * 7 /")  # 2
calculate_postfix_arithmetic("5 40 10 / * 64 2 + -")  # -46

# calculate_postfix_arithmetic("4 5 7 2 + - *")  # -16
# calculate_postfix_arithmetic("4 5 7 2+ - *")  # -8 with "Do nothing"
# calculate_postfix_arithmetic("4 5 7 -2 - *")  # -8 with "Do nothing"

# calculate_postfix_arithmetic("3 +")  # IndexError: pop from empty list
