from dotenv import load_dotenv
import sys

if __name__ == "__main__":
    load_dotenv(".env")

    if sys.argv[1] == "clean":
        from core.redis import redis_client
        redis_client.flushall()

    elif sys.argv[1] == "start":
        from main import run
        run()
