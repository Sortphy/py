from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

# Define a resource with a proper service name
resource = Resource(attributes={
    ResourceAttributes.SERVICE_NAME: "algorithm-benchmarking"  # Replace with your service name
})

# Configure the tracer provider with the resource
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# Add console exporter
trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

# Configure Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

# Add Jaeger exporter
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

# Create a named tracer (more specific than __name__)
tracer = trace.get_tracer("algorithm_performance")

def registrar_logs(nome_algoritmo, tamanho_dados, tempo_execucao, comparacoes, trocas):
    # Create a named span for each algorithm execution
    with tracer.start_as_current_span(f"execute_{nome_algoritmo}"):
        print(f"Algoritmo: {nome_algoritmo}")
        print(f"Tamanho dos dados: {tamanho_dados}")
        print(f"Tempo de execução: {tempo_execucao:.2f} ms")
        print(f"Comparações: {comparacoes}")
        print(f"Trocas: {trocas}")
        print("-" * 40)