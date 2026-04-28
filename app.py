from flask import Flask, render_template, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Gauge
import time
import random

# Initialize the Flask app and attach Prometheus metrics
app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('fittrack_app_info', 'FitTrack Application Info', version='1.0.0')

# Custom metrics for tracking business-level data
workouts_logged = Counter(
    'fittrack_workouts_logged_total',
    'Total number of workouts logged',
    ['workout_type']
)
active_users = Gauge(
    'fittrack_active_users',
    'Number of currently active users'
)

# In-memory storage for workout data
workout_log = []

WORKOUT_TYPES = ['Running', 'Weight Training',
                 'Cycling', 'Swimming', 'Yoga', 'HIIT']


@app.route('/')
def dashboard():
    # Count today's workouts and calculate streak
    today_count = len([w for w in workout_log if w['date']
                      == time.strftime('%Y-%m-%d')])
    total_count = len(workout_log)
    streak = min(total_count, 7)
    # Simulate active user count for the dashboard
    active_users.set(random.randint(5, 25))
    return render_template('dashboard.html',
                           today_count=today_count,
                           total_count=total_count,
                           streak=streak)


@app.route('/workouts', methods=['GET', 'POST'])
def workouts():
    if request.method == 'POST':
        # Build a workout entry from the form data
        workout = {
            'type': request.form.get('type', 'Running'),
            'duration': request.form.get('duration', '30'),
            'date': time.strftime('%Y-%m-%d'),
            'time': time.strftime('%H:%M')
        }
        workout_log.append(workout)
        # Increment the Prometheus counter for this workout type
        workouts_logged.labels(workout_type=workout['type']).inc()
    return render_template('workouts.html',
                           workout_types=WORKOUT_TYPES,
                           recent=workout_log[-5:])


@app.route('/progress')
def progress():
    return render_template('progress.html',
                           workouts=workout_log,
                           total=len(workout_log))


@app.route('/healthz')
def health():
    # Health check endpoint for Kubernetes probes
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
