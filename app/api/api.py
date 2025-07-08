import time
from flask import Flask, request, g

from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.metrics import get_meter_provider, set_meter_provider

from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server

from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Set up Prometheus reader and HTTP server
reader = PrometheusMetricReader()
start_http_server(port=8000)  # Prometheus will scrape from here

# OpenTelemetry setup
resource = Resource(attributes={SERVICE_NAME: "flask-service"})
provider = MeterProvider(metric_readers=[reader], resource=resource)
set_meter_provider(provider)
meter = get_meter_provider().get_meter("flask-meter")

# Define metrics
request_counter = meter.create_counter(
    "http_server_requests_total",
    description="Total number of HTTP requests"
)

request_duration = meter.create_histogram(
    "http_server_duration_ms",
    unit="ms",
    description="HTTP request duration in milliseconds"
)

exception_counter = meter.create_counter(
    "http_server_exceptions_total",
    description="Total number of exceptions"
)

# Create Flask app
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    duration_ms = (time.time() - g.start_time) * 1000
    labels = {
        "method": request.method,
        "path": request.path,
        "status_code": response.status_code,
    }
    request_counter.add(1, labels)
    request_duration.record(duration_ms, labels)
    return response

@app.teardown_request
def teardown_request(exc):
    if exc:
        labels = {
            "method": request.method,
            "path": request.path,
            "exception": type(exc).__name__,
        }
        exception_counter.add(1, labels)

@app.errorhandler(404)
def not_found(e):
    return {'error': 'Not Found'}, 404

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}