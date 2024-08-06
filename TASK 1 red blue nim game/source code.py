RED_SCORE = 2
BLUE_SCORE = 3

def print_board(red_count, blue_count):
    print(f"Red Marbles: {red_count}")
    print(f"Blue Marbles: {blue_count}")
    print()

def game_over(red_count, blue_count):
    return red_count == 0 or blue_count == 0

def calculate_score(red_count, blue_count):
    return red_count * RED_SCORE + blue_count * BLUE_SCORE

def human_move(red_count, blue_count):
    while True:
        print("Your turn:")
        print_board(red_count, blue_count)
        pile = input("Choose pile (red or blue): ").strip().lower()
        if pile == 'red' and red_count > 0:
            return 'red'
        elif pile == 'blue' and blue_count > 0:
            return 'blue'
        else:
            print("Invalid move! Try again.")

def minmax_move(red_count, blue_count):
    if red_count > blue_count:
        return 'red'
    else:
        return 'blue'

def main():
    num_red = int(input("Enter number of red marbles: "))
    num_blue = int(input("Enter number of blue marbles: "))
    version = input("Enter game version (standard/misere): ").strip().lower()
    first_player = input("Enter first player (human/computer): ").strip().lower()
    depth = int(input("Enter AI search depth (0 for human vs human): "))

    red_count = num_red
    blue_count = num_blue
    current_player = first_player

    print("Welcome to Red-Blue Nim!")
    print_board(red_count, blue_count)

    while not game_over(red_count, blue_count):
        if current_player == 'human':
            pile_choice = human_move(red_count, blue_count)
        else:
            pile_choice = minmax_move(red_count, blue_count)

        if pile_choice == 'red':
            red_count -= 1
        elif pile_choice == 'blue':
            blue_count -= 1

        print(f"{current_player.capitalize()} took 1 {pile_choice} marble.")
        print_board(red_count, blue_count)

        current_player = 'computer' if current_player == 'human' else 'human'

    print("Game Over!")
    final_score = calculate_score(red_count, blue_count)
    print(f"Final Score: {final_score}")

if __name__ == "__main__":
    main()