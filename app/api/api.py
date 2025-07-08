import time
from flask import Flask
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.metrics import set_meter_provider  # Important!
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

app = Flask(__name__)

# Define OTEL resource (service name)
resource = Resource.create(attributes={"service.name": "dataiku-time-service"})

# Setup Prometheus metric reader + meter provider
reader = PrometheusMetricReader()
provider = MeterProvider(resource=resource, metric_readers=[reader])
set_meter_provider(provider)

# Instrument Flask app (includes HTTP metrics!)
FlaskInstrumentor().instrument_app(app)

@app.errorhandler(404)
def not_found(e):
    return {'error': 'Not Found'}, 404

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run()