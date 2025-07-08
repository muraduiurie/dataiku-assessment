import time
from flask import Flask
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Set Prometheus exporter to expose metrics
metric_reader = PrometheusMetricReader()
provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter("flask-app")

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

# Create custom metrics
request_counter = meter.create_counter(
    "app_request_count",
    description="Total number of requests"
)

request_latency = meter.create_histogram(
    "app_request_latency",
    unit="ms",
    description="Request latency in milliseconds"
)

@app.errorhandler(404)
def not_found(e):
    request_counter.add(1, {"endpoint": "not_found", "status_code": 404})
    return {'error': 'Not Found'}, 404

@app.route('/api/time')
def get_current_time():
    start_time = time.time()
    response = {'time': time.time()}
    latency_ms = (time.time() - start_time) * 1000

    request_counter.add(1, {"endpoint": "get_current_time", "status_code": 200})
    request_latency.record(latency_ms, {"endpoint": "get_current_time"})

    return response

# Expose Prometheus metrics endpoint at /metrics
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':
    app.run(debug=True, port=8000)