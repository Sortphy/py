from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

SERVICE_NAME = "Ordenadores"

def configurar_tracer():
    """Configura um TracerProvider global para os algoritmos de ordenação."""
    resource = Resource.create({"service.name": SERVICE_NAME})
    provider = TracerProvider(resource=resource)

    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    jaeger_exporter = JaegerExporter(
        agent_host_name="localhost",
        agent_port=6831,
    )
    provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

    trace.set_tracer_provider(provider)
    return trace.get_tracer(__name__)

tracer = configurar_tracer()

def registrar_logs(nome_algoritmo, tamanho_dados, tempo_execucao, comparacoes, trocas):
    """Cria um span nomeado com o algoritmo dentro do serviço 'Ordenadores'."""
    with tracer.start_as_current_span(nome_algoritmo):
        print(f"Algoritmo: {nome_algoritmo}")
        print(f"Tamanho dos dados: {tamanho_dados}")
        print(f"Tempo de execução: {tempo_execucao:.2f} ms")
        print(f"Comparações: {comparacoes}")
        print(f"Trocas: {trocas}")
        print("-" * 40)
