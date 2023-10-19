import random

def pop(words):
    # Remove and return the first word from the list of words
    if words:
        return words.pop(0)
    else:
        return None

def can_place(word, crossword, x, y, direction):
    # Check if the word can be placed in the crossword at the specified position and direction
    if direction == 'HORIZONTAL':
        for i, letter in enumerate(word):
            if x + i >= len(crossword[y]) or (crossword[y][x + i] != ' ' and crossword[y][x + i] != letter):
                return False
        return True
    elif direction == 'VERTICAL':
        for i, letter in enumerate(word):
            if y + i >= len(crossword) or (crossword[y + i][x] != ' ' and crossword[y + i][x] != letter):
                return False
        return True
    else:
        return False

def place(word, crossword, x, y, direction):
    # Place the word in the crossword at the specified position and direction
    if direction == 'HORIZONTAL':
        for i, letter in enumerate(word):
            crossword[y][x + i] = letter
    elif direction == 'VERTICAL':
        for i, letter in enumerate(word):
            crossword[y + i][x] = letter
    return crossword

def print_crossword(crossword):
    column_indices = '  '.join(['{:2}'.format(i + 1) for i in range(len(crossword[0]))])
    print(f"  {column_indices}")
    for y in range(len(crossword)):
        row = crossword[y]
        row_str = '   '.join(row)
        print('{:02} {}'.format(y + 1, row_str))

def calculate_crossword_score(crossword):
    # Calculate the number of filled squares and the ratio of width vs. height
    total_squares = len(crossword) * len(crossword[0])
    filled_squares = sum(row.count(' ') for row in crossword)
    filled_ratio = (total_squares - filled_squares) / total_squares
    if (len(crossword[0]) > len(crossword)):
        size_ratio = len(crossword) / len(crossword[0])
    else:
        size_ratio = len(crossword[0]) / len(crossword)
    
    # Calculate the overall score using the given formula
    score = size_ratio * 10 + filled_ratio * 20
    return score

def resize_crossword(crossword):
    resized_crossword = []

    for y in range(0, len(crossword)):
        row = crossword[y][0:len(crossword[0])]
        # Check if the row is not completely blank
        if any(cell != ' ' for cell in row):
            resized_crossword.append(row)

    # Transpose the resized crossword to handle blank columns
    resized_crossword_transposed = list(map(list, zip(*resized_crossword)))

    # Remove blank rows from the transposed crossword
    final_resized_crossword = []

    for y in range(len(resized_crossword_transposed)):
        row = resized_crossword_transposed[y]
        # Check if the row is not completely blank
        if any(cell != ' ' for cell in row):
            final_resized_crossword.append(row)

    # Transpose back to the original orientation
    final_resized_crossword = list(map(list, zip(*final_resized_crossword)))

    return final_resized_crossword

def generate_crossword(words, max_words, crossword=None):
    random.shuffle(words)
    if crossword is None:
        # If crossword is not provided, create a new one with the first word
        first_word = pop(words)
        crossword_size = max(len(first_word), 15)  # Set crossword size based on the first word or a minimum size of 15x15
        crossword = [[' ' for _ in range(crossword_size)] for _ in range(crossword_size)]
        # place the first word randomly
        crossword = place(first_word, crossword, 0, 0, 'HORIZONTAL')

    count = 1

    while count < max_words and words:
        word = pop(words)
        placed = False
        for letter in word:
            for y in range(len(crossword)):
                for x in range(len(crossword[y])):
                    if crossword[y][x] == letter:
                        for direction in ['HORIZONTAL', 'VERTICAL']:
                            if not placed and can_place(word, crossword, x, y, direction):
                                crossword = place(word, crossword, x, y, direction)
                                placed = True
                                count += 1
                                break

        if not placed:
            # If the word couldn't be placed anywhere, place it randomly
            empty_spots = [(x, y, direction) for x in range(len(crossword[0])) for y in range(len(crossword)) for direction in ['HORIZONTAL', 'VERTICAL'] if can_place(word, crossword, x, y, direction)]
            if empty_spots:
                x, y, direction = random.choice(empty_spots)
                crossword = place(word, crossword, x, y, direction)
                count += 1
        
    return crossword

# Interactive function to get user input for words
def get_input_words():
    num_words = int(input("Enter the total number of words: "))
    input_words = []
    for i in range(num_words):
        word = input(f"Enter word {i + 1}: ")
        input_words.append(word)
    return input_words

# Interactive main function
def main():
    # Get input words from the user interactively
    input_words = get_input_words()
    
    max_words = 10  # You can adjust this value as needed
    num_crosswords = 100

    crosswords_and_scores = []  # List to store generated crosswords and their scores

    for _ in range(num_crosswords):
        generated_crossword = generate_crossword(input_words.copy(), max_words)
        resized_crossword = resize_crossword(generated_crossword)
        crossword_quality_score = calculate_crossword_score(resized_crossword)
        crosswords_and_scores.append((resized_crossword, crossword_quality_score))

    # Find the crossword with the highest and lowest scores
    highest_score_crossword, highest_score = max(crosswords_and_scores, key=lambda x: x[1])
    lowest_score_crossword, lowest_score = min(crosswords_and_scores, key=lambda x: x[1])

    # Print the highest and lowest score crosswords
    print("Crossword with Highest Score:")
    print_crossword(highest_score_crossword)
    print(f"Highest Score: {highest_score}")

    print("\nCrossword with Lowest Score:")
    print_crossword(lowest_score_crossword)
    print(f"Lowest Score: {lowest_score}")

if __name__ == "__main__":
    main()
