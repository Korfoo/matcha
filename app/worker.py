import logging
import time
import signal

import redis

logger = logging.getLogger(__name__)


def publish_match(player_1_id, player_2_id, room_id):
    pass


def find_matches():
    pass

def terminate(signal,frame):
  sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, terminate)

    while True:
        logger.info("Finding matches...")

        find_matches()
        time.sleep(1)

