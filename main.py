# main.py
from usability_web.app import app
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    # Running from here ensures the environment is loaded
    app.run(debug=True)