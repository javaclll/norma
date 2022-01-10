from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv(".env")

    from main import run
    run()
