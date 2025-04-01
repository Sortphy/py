from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Status, StatusCode

SERVICE_NAME = "Ordenadores"

def configurar_tracer():
    """Configura um TracerProvider global para os algoritmos de ordenação."""
    resource = Resource.create({"service.name": SERVICE_NAME})
    provider = TracerProvider(resource=resource)

    # Exportador para console (para debugging)
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    # Configuração do Jaeger Exporter
    jaeger_exporter = JaegerExporter(
        agent_host_name="localhost",
        agent_port=6831,
    )
    provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

    trace.set_tracer_provider(provider)
    return trace.get_tracer(__name__)

tracer = configurar_tracer()

def registrar_logs(nome_algoritmo, tamanho_dados, tempo_execucao, comparacoes, trocas):
    """Registra métricas no Jaeger com atributos detalhados."""
    with tracer.start_as_current_span(nome_algoritmo) as span:
        # Adiciona atributos ao span
        span.set_attributes({
            "tamanho_dados": tamanho_dados,
            "tempo_execucao_ms": tempo_execucao,
            "comparacoes": comparacoes,
            "trocas": trocas,
        })
        span.set_status(Status(StatusCode.OK))
        
        # Mantém o log no console para referência
        print(f"\nAlgoritmo: {nome_algoritmo}")
        print(f"Tamanho dos dados: {tamanho_dados}")
        print(f"Tempo de execução: {tempo_execucao:.2f} ms")
        print(f"Comparações: {comparacoes}")
        print(f"Trocas: {trocas}")
        print("-" * 40)