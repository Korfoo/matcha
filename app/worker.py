import json
import logging
import time

import redis

logger = logging.getLogger(__name__)

matchmaking_pool = redis.Redis(host="redis", port=6379, db=1)

def publish_match(player_1_id, player_2_id, room_id):
    pass


def find_matches():
    """
    Loop over all players and look for potential opponents. Publish a match when 2 opponents have been found within eachothers ELO-range.

    The longer a player is queueing the bigger his ELO-range will be. This should reduce matchmaking time and can be tuned with variables in the config.
    It's important that a when a possible opponent is found that the player is also in the opponents player's ELO-range, this gives more balanced matches.
    It's also possible to cap out the ELO-range as to not get extreme ELO differences between players.
    """

    for player in matchmaking_pool.zscan_iter("matchmaking_time"):
        # Player id is the key
        player_id = player[0]

        # Using the player ID we can retrieve it's ELO.
        player_elo = matchmaking_pool.zscore("matchmaking_pool", player_id)
        
        # When the player has stopped queueing it won't be present
        if not player_elo:
            continue

        # The time at which the player queued is the value in the table. 
        # Taking the difference between queue time and current time is the time the player has been in the queue.
        player_queue_time = player[1]
        player_time_in_queue = int(time.time()) - int(player_queue_time)

        # TODO: remove magic numbers, extract to config
        player_elo_range = min(50 * (1 + 25 / 100) ** int(player_time_in_queue / 10), 500)

        # Search all other players whose ELO is within the calculated range
        possible_opponents = []

        for opponent in matchmaking_pool.zrangebyscore(
            "matchmaking_pool",
            int(player_elo - player_elo_range),
            int(player_elo + player_elo_range),
            withscores=True,
        ):
            # Now we go the opposite direction, using the ID we retrieve the opponent's time in the queue.
            opponent_id = opponent[0]

            opponent_queue_time = matchmaking_pool.zscore(
                "matchmaking_time", opponent_id
            )

            # When the player has stopped queueing it won't be present
            if not opponent_queue_time:
                continue

            opponent_time_in_queue = int(time.time()) - int(opponent_queue_time)

            # TODO: remove magic numbers, extract to config
            opponent_elo_range = min(50 * (1 + 25 / 100) ** int(opponent_time_in_queue / 10),500)

            opponent_elo = opponent[1]

            # Make sure the player's ELO is also in the opponent's ELO-range
            if (opponent_elo - opponent_elo_range) <= player_elo <= (opponent_elo + opponent_elo_range) and player_id != opponent_id:
                possible_opponent = {
                    "id": opponent_id,
                    "time_in_queue": opponent_time_in_queue,
                }
                possible_opponents.append(possible_opponent)

        if possible_opponents:
            logger.info(f"{len(possible_opponents)} possible opponents")
            # Sort opponents by time in queue from longest to shortest
            possible_opponents.sort(key=lambda x: x["time_in_queue"], reverse=True)

            # Remove both players from matchmaking pool
            matchmaking_pool.zrem("matchmaking_time", player_id)
            matchmaking_pool.zrem("matchmaking_time", possible_opponents[0]["id"])
            matchmaking_pool.zrem("matchmaking_pool", player_id)
            matchmaking_pool.zrem("matchmaking_pool", possible_opponents[0]["id"])

            # Return the opponent that has been queueing the longest
            return possible_opponents[0]["id"]


def terminate(signal,frame):
  sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, terminate)

    while True:
        logger.info("Finding matches...")

        find_matches()
        time.sleep(10)

