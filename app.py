print("Starting the Flask app")

from app import create_app

app = create_app()

#Base URL : http://127.0.0.1:5000

if __name__ == "__main__":
    app.run(debug=True)

