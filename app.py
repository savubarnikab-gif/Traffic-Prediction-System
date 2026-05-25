from flask import Flask, render_template, request
from traffic_model import predict_traffic
import psycopg2

app = Flask(__name__)

# PostgreSQL Connection
try:

    conn = psycopg2.connect(
        host="localhost",
        database="traffic_db",
        user="postgres",
        password="admin"
    )

    cursor = conn.cursor()

    print("Database Connected Successfully")

except Exception as e:

    print("Database Connection Failed")
    print(e)

    conn = None
    cursor = None

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# Prediction Route
@app.route('/predict', methods=['POST'])
def predict():

    try:

        # Form Data
        hour = int(request.form['hour'])
        lat = float(request.form['lat'])
        longi = float(request.form['long'])
        alert = request.form['alert']
        speed = float(request.form['speed'])

        # ML Prediction
        result = predict_traffic(
            hour,
            lat,
            longi,
            alert,
            speed
        )

        # Route Suggestion
        if result == "Heavy":
            suggestion = "Choose Alternative Route"

        elif result == "Medium":
            suggestion = "Traffic Moderate - Drive Carefully"

        else:
            suggestion = "Best Route Available"

        # Save to PostgreSQL
        if cursor is not None:

            cursor.execute(
                """
                INSERT INTO traffic_predictions
                (
                    hour,
                    lat,
                    longi,
                    alert,
                    speed,
                    prediction,
                    suggestion
                )

                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    hour,
                    lat,
                    longi,
                    alert,
                    speed,
                    result,
                    suggestion
                )
            )

            conn.commit()

        return render_template(
            'index.html',
            prediction=result,
            suggestion=suggestion
        )

    except Exception as e:

        return f"""
        <h2>Error Occurred</h2>
        <p>{e}</p>
        """

# Run Flask App
if __name__ == '__main__':

    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False
    )