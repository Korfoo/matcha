import math


# Function to calculate the Probability
def calculate_probability(rating_1: int, rating_2: int) -> float:

    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating_1 - rating_2) / 400))


def calculate_new_rating(
    rating_player_a: int, rating_player_b: int, K: int, winner: int
):
    player_a_wins = calculate_probability(rating_player_b, rating_player_a)

    player_b_wins = calculate_probability(rating_player_a, rating_player_b)

    # Case -1 When Player A wins
    # Updating the Elo Ratings
    # Player A won
    if winner == 0:
        new_rating_a = rating_player_a + K * (1 - player_a_wins)
        new_rating_b = rating_player_b + K * (0 - player_b_wins)

    # Player B won
    if winner == 1:
        new_rating_a = rating_player_a + K * (0 - player_a_wins)
        new_rating_b = rating_player_b + K * (1 - player_b_wins)

    # Draw
    if winner == 2:
        new_rating_a = rating_player_a + K * (0.5 - player_a_wins)
        new_rating_b = rating_player_b + K * (0.5 - player_b_wins)

    return (int(new_rating_a), int(new_rating_b))
