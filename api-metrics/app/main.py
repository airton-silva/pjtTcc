from cgi import print_arguments
from prometheus_client import start_http_server, Summary, Counter, Histogram
from typing import Tuple, Dict
# from flask import Flask, Response, request, jsonify
# import random
# import time
# from routes import myDatasource

from json import loads
from requests import get



    # from json import loads
    # from requests import get

    # return loads(get(request_prometheus_api).text) 


PROMETHEUS_KUBE_PROMETHEUS = 'http://200.129.62.190:30000/api/v1/query?query='
API_PROMETHEUS = 'http://200.129.62.190:30000/api/v1/'
# API_PROMETHEUS = data_source()

def data_source (url: str):
    print (url)
    return url


METRICAS = {
    'rede': {
        'recebido': 'container_network_receive_bytes_total',
        'receive': 'sum (rate (container_network_receive_bytes_total{kubernetes_io_hostname=~"^.*$"}[1m]))',
        'sent': '- sum (rate (container_network_receive_bytes_total{kubernetes_io_hostname=~"^.*$"}[1m]))',

    },

    'Request': {
        'request_duration_seconds_count':'sum(rate(http_request_duration_seconds_bucket{job="kube-state-metrics"}))',
        'http_requests_total': 'request_duration_seconds_count{kubernetes_io_hostname="dti-d610", pod="teastore-webui-5d9c74d9d6-9lrw5"}',

    },

    'CPU':{
        'consumo_percent_cpu': 'sum (rate (container_cpu_usage_seconds_total{id="/",kubernetes_io_hostname="dti-d610"}[1m])) / sum (machine_cpu_cores{kubernetes_io_hostname="dti-d610"}) * 100', # consumo em percentagem
        'container_cpu_usage_seconds_total':'container_cpu_usage_seconds_total',
        'machine_cpu_cores':"machine_cpu_cores",
        'consume_cpu_by_container':'sum (rate (container_cpu_usage_seconds_total{image!="",name!~"^k8s_.*",kubernetes_io_hostname=~"^.*$",namespace=~"^(boutique|default|kube-node-lease|kube-public|kube-system|monitoring|simple-bank|teashop)$"}[1m])) by (kubernetes_io_hostname, name, image)',
        'consumo_total_cpu':'sum (rate (container_cpu_usage_seconds_total{id="/",kubernetes_io_hostname=~"^.*$"}[1m]))',

    },
    'Memory':{
        # 'usage_bytes_total':'container_memory_usage_bytes{kubernetes_io_hostname="dti-d610", pod="teastore-webui-5d9c74d9d6-9lrw5"}',
        'machine_memory_bytes': 'sum (machine_memory_bytes{kubernetes_io_hostname=~\'^.*$\'})', # memoria da maquina 
        'container_memoryWorking_set_bytes':'sum (container_memory_working_set_bytes{id="/",kubernetes_io_hostname="dti-d610"})', # consumo de memória in bytes
        'consumo_percent_memory': 'sum (container_memory_working_set_bytes{id="/",kubernetes_io_hostname="dti-d610"}) / sum (machine_memory_bytes{kubernetes_io_hostname="dti-d610"}) * 100', # consumo em percentagem
    },
    'FileSystem':{
        'consumo_percent_filesystem': 'sum (container_fs_usage_bytes{device=~"^/dev/[sv]d[a-z][1-9]$",id="/",kubernetes_io_hostname="dti-d610"}) / sum (container_fs_limit_bytes{device=~"^/dev/[sv]d[a-z][1-9]$",id="/",kubernetes_io_hostname="dti-d610"}) * 100',
        'consumo_total_filesystem': 'sum (container_fs_usage_bytes{device=~\"^/dev/[sv]d[a-z][1-9]$\",id=\"/\",kubernetes_io_hostname=~\"^.*$\"})',
        'container_fs_limit_bytes' : 'sum (container_fs_limit_bytes{device=~"^/dev/[sv]d[a-z][1-9]$",id="/",kubernetes_io_hostname=~\"^.*$\"})',
        # 'container_fs_reads_bytes_total_teastore-webui-5d9c74d9d6-9lrw5': 'sum(rate(container_fs_reads_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-webui-5d9c74d9d6-9lrw5"}[1m]))'
    },

    'Pods':{
        'kube_pod_labels':'kube_pod_labels',
        'cpu_usage_seconds_total':'sum(rate(container_cpu_usage_seconds_total{kubernetes_io_hostname="dti-d610", pod="teastore-webui-5d9c74d9d6-9lrw5"}[1m]))',
        'container_spec_cpu_period':'container_spec_cpu_period{kubernetes_io_hostname="dti-d610", pod="teastore-webui-5d9c74d9d6-9lrw5"}',
        
        # teastore-webui-5d9c74d9d6-9lrw5 -
        'container_network_transmit_bytes_total_teastore-webui-5d9c74d9d6-9lrw5': 'container_network_transmit_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-webui-5d9c74d9d6-9lrw5"}',
        'container_network_receive_bytes_total_teastore-webui-5d9c74d9d6-9lrw5' : 'container_network_receive_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-webui-5d9c74d9d6-9lrw5"}',
        'container_cpu_usage_seconds_total_teastore-webui-5d9c74d9d6-9lrw5':'sum(rate(container_cpu_usage_seconds_total{kubernetes_io_hostname="dti-d610", pod="teastore-webui-5d9c74d9d6-9lrw5"}[1m]))', 
        'container_memoryWorking_set_bytes_teastore-webui-5d9c74d9d6-9lrw5':'sum(rate(container_memory_working_set_bytes{kubernetes_io_hostname="dti-d610", pod="teastore-webui-5d9c74d9d6-9lrw5"}[1m]))',
        'container_fs_writes_bytes_total_teastore-webui-5d9c74d9d6-9lrw5': 'sum(rate(container_fs_writes_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-webui-5d9c74d9d6-9lrw5"}[1m]))',
        'container_fs_reads_bytes_total_teastore-webui-5d9c74d9d6-9lrw5': 'sum(rate(container_fs_reads_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-webui-5d9c74d9d6-9lrw5"}[1m]))',
        # teastore-db-5d9555684f-w64kj - 
        'container_network_transmit_bytes_total_teastore-db-5d9555684f-w64kj': 'container_network_transmit_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-db-5d9555684f-w64kj"}',
        'container_network_receive_bytes_total_teastore-db-5d9555684f-w64kj' : 'container_network_receive_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-db-5d9555684f-w64kj"}',
        'container_cpu_usage_seconds_total_teastore-db-5d9555684f-w64kj':'sum(rate(container_cpu_usage_seconds_total{kubernetes_io_hostname="dti-d610", pod="teastore-db-5d9555684f-w64kj"}[1m]))', 
        'container_memoryWorking_set_bytes_teastore-db-5d9555684f-w64kj':'sum(rate(container_memory_working_set_bytes{kubernetes_io_hostname="dti-d610", pod="teastore-db-5d9555684f-w64kj"}[1m]))',
        'container_fs_writes_bytes_total_teastore-db-5d9555684f-w64kj': 'sum(rate(container_fs_writes_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-db-5d9555684f-w64kj"}[1m]))',
        'container_fs_reads_bytes_total_teastore-db-5d9555684f-w64kj': 'sum(rate(container_fs_reads_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-db-5d9555684f-w64kj"}[1m]))',
        # teastore-image-74cc7d64c5-6bppm
        'container_network_transmit_bytes_total_teastore-image-74cc7d64c5-6bppm': 'container_network_transmit_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-image-74cc7d64c5-6bppm"}',
        'container_network_receive_bytes_total_teastore-image-74cc7d64c5-6bppm' : 'container_network_receive_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-image-74cc7d64c5-6bppm"}',
        'container_cpu_usage_seconds_total_teastore-image-74cc7d64c5-6bppm':'sum(rate(container_cpu_usage_seconds_total{kubernetes_io_hostname="dti-d610", pod="teastore-image-74cc7d64c5-6bppm"}[1m]))', 
        'container_memoryWorking_set_bytes_teastore-image-74cc7d64c5-6bppm':'sum(rate(container_memory_working_set_bytes{kubernetes_io_hostname="dti-d610", pod="teastore-image-74cc7d64c5-6bppm"}[1m]))',
        'container_fs_writes_bytes_total_teastore-image-74cc7d64c5-6bppm': 'sum(rate(container_fs_writes_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-image-74cc7d64c5-6bppm"}[1m]))',
        'container_fs_reads_bytes_total_teastore-image-74cc7d64c5-6bppm': 'sum(rate(container_fs_reads_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-image-74cc7d64c5-6bppm"}[1m]))',
        # teastore-persistence-6cc5b44f9d-wm8hn
        'container_network_transmit_bytes_total_teastore-persistence-6cc5b44f9d-wm8hn': 'container_network_transmit_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-persistence-6cc5b44f9d-wm8hn"}',
        'container_network_receive_bytes_total_teastore-persistence-6cc5b44f9d-wm8hn' : 'container_network_receive_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-persistence-6cc5b44f9d-wm8hn"}',
        'container_cpu_usage_seconds_total_teastore-persistence-6cc5b44f9d-wm8hn':'sum(rate(container_cpu_usage_seconds_total{kubernetes_io_hostname="dti-d610", pod="teastore-persistence-6cc5b44f9d-wm8hn"}[1m]))', 
        'container_memoryWorking_set_bytes_teastore-persistence-6cc5b44f9d-wm8hn':'sum(rate(container_memory_working_set_bytes{kubernetes_io_hostname="dti-d610", pod="teastore-persistence-6cc5b44f9d-wm8hn"}[1m]))',
        'container_fs_writes_bytes_total_teastore-persistence-6cc5b44f9d-wm8hn': 'sum(rate(container_fs_writes_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-persistence-6cc5b44f9d-wm8hn"}[1m]))',
        'container_fs_reads_bytes_total_teastore-persistence-6cc5b44f9d-wm8hn': 'sum(rate(container_fs_reads_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-persistence-6cc5b44f9d-wm8hn"}[1m]))',

        # teastore-auth-7947675f98-rbk99
        'container_network_transmit_bytes_total_teastore-auth-7947675f98-rbk99': 'container_network_transmit_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-auth-7947675f98-rbk99"}',
        'container_network_receive_bytes_total_teastore-auth-7947675f98-rbk99' : 'container_network_receive_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-auth-7947675f98-rbk99"}',
        'container_cpu_usage_seconds_total_teastore-auth-7947675f98-rbk99':'sum(rate(container_cpu_usage_seconds_total{kubernetes_io_hostname="dti-d610", pod="teastore-auth-7947675f98-rbk99"}[1m]))', 
        'container_memoryWorking_set_bytes_teastore-auth-7947675f98-rbk99':'sum(rate(container_memory_working_set_bytes{kubernetes_io_hostname="dti-d610", pod="teastore-auth-7947675f98-rbk99"}[1m]))',
        'container_fs_writes_bytes_total_teastore-auth-7947675f98-rbk99': 'sum(rate(container_fs_writes_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-auth-7947675f98-rbk99"}[1m]))',
        'container_fs_reads_bytes_total_teastore-auth-7947675f98-rbk99': 'sum(rate(container_fs_reads_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-auth-7947675f98-rbk99"}[1m]))',

        # teastore-recommender-794c699f5-v69gm
        'container_network_transmit_bytes_total_teastore-recommender-794c699f5-v69gm': 'container_network_transmit_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-recommender-794c699f5-v69gm"}',
        'container_network_receive_bytes_total_teastore-recommender-794c699f5-v69gm' : 'container_network_receive_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-recommender-794c699f5-v69gm"}',
        'container_cpu_usage_seconds_total_teastore-recommender-794c699f5-v69gm':'sum(rate(container_cpu_usage_seconds_total{kubernetes_io_hostname="dti-d610", pod="teastore-recommender-794c699f5-v69gm"}[1m]))', 
        'container_memoryWorking_set_bytes_teastore-recommender-794c699f5-v69gm':'sum(rate(container_memory_working_set_bytes{kubernetes_io_hostname="dti-d610", pod="teastore-recommender-794c699f5-v69gm"}[1m]))',
        'container_fs_writes_bytes_total_teastore-recommender-794c699f5-v69gm': 'sum(rate(container_fs_writes_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-recommender-794c699f5-v69gm"}[1m]))',
        'container_fs_reads_bytes_total_teastore-recommender-794c699f5-v69gm': 'sum(rate(container_fs_reads_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-recommender-794c699f5-v69gm"}[1m]))',

        # teastore-registry-8bbbc8d7f-5kj9
        'container_network_transmit_bytes_total_teastore-registry-8bbbc8d7f-5kj9': 'container_network_transmit_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-registry-8bbbc8d7f-5kj9"}',
        'container_network_receive_bytes_total_teastore-registry-8bbbc8d7f-5kj9' : 'container_network_receive_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-registry-8bbbc8d7f-5kj9"}',
        'container_cpu_usage_seconds_total_teastore-registry-8bbbc8d7f-5kj9':'sum(rate(container_cpu_usage_seconds_total{kubernetes_io_hostname="dti-d610", pod="teastore-registry-8bbbc8d7f-5kj9"}[1m]))', 
        'container_memoryWorking_set_bytes_teastore-registry-8bbbc8d7f-5kj9':'sum(rate(container_memory_working_set_bytes{kubernetes_io_hostname="dti-d610", pod="teastore-registry-8bbbc8d7f-5kj9"}[1m]))',
        'container_fs_writes_bytes_total_teastore-registry-8bbbc8d7f-5kj9': 'sum(rate(container_fs_writes_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-registry-8bbbc8d7f-5kj9"}[1m]))',
        'container_fs_reads_bytes_total_teastore-registry-8bbbc8d7f-5kj9': 'sum(rate(container_fs_reads_bytes_total{kubernetes_io_hostname="dti-d610", pod="teastore-registry-8bbbc8d7f-5kj9"}[1m]))',

   
    },
    'histogram':{
        'request_duration_seconds_count':'sum(rate(http_request_duration_seconds_bucket{job="kube-state-metrics"}[1m])) by (le)',
    },
    'process':{
        'container_processes':'container_processes{kubernetes_io_hostname="dti-d610"}',
    },
    'namespace':{
        'kube_namespace_labels':'kube_namespace_labels',
    },
    'node':{
        'kube_node_info':'kube_node_info',
    },

}  
def gerarQueryPreferences (identify: str, type: str, metric: str, pod: str) :
    create_query = f"{identify}: rate ({type}"+'{"kubernetes_io_hostname="dti-d610", pod="'+f"{pod}"+'"})'
    return create_query
# usage_seconds_total_norm':'rate(container_cpu_usage_seconds_total{kubernetes_io_hostname="dti-d610", pod="teastore-webui-5d9c74d9d6-9lrw5"})

def gerarMetadata () -> dict:
    url = API_PROMETHEUS+'metadata'
    dados = requisitar_prometheus(url)
    dados_processados = processar_dados(dados)

    return dados_processados  

def buscar(query: str)-> dict:
    """Busca metricas no Prometheus.

    """
    url = PROMETHEUS_KUBE_PROMETHEUS + query
    print(url)
    dados = requisitar_prometheus(url)
    dados_processados = processar_dados(dados)
    return dados_processados
    

def search_metric(query: str, metric: str, tmp : str = '') -> dict:
    """Busca metricas no Prometheus.

    """
    url = API_PROMETHEUS+'query_range?query='+METRICAS[query][metric]+ tmp
    print(url)
    dados = requisitar_prometheus(url)
    dados_processados = processar_dados(dados)
    # print(dados_processados)
    return dados_processados


def getTargets(query: str):
    url = API_PROMETHEUS + query
    dados = requisitar_prometheus(url)
    dados_processados = processar_dados(dados)
    return dados_processados


def coletar_dados_prometheus(metrica: str, type: str, intervalo_prometheus: str = '') -> dict:
    
    requisicao_prometheus_api = criar_requisicao_prometheus(metrica, type, intervalo_prometheus)
    print(requisicao_prometheus_api)
    dados = requisitar_prometheus(requisicao_prometheus_api)
    dados_processados = processar_dados(dados)
    return dados_processados

def criar_requisicao_prometheus(metrica: str, type: str, intervalo_prometheus: str) -> str:
  # URL do Kube Prometheus 
    url = PROMETHEUS_KUBE_PROMETHEUS + METRICAS[metrica][type] + intervalo_prometheus
    
    
    return url
    # return PROMETHEUS_KUBE_PROMETHEUS + METRICAS.get(metrica) + intervalo_prometheus


def requisitar_prometheus(request_prometheus_api: str) -> dict:
    """Coletar dados no prometheus através de um GET.

        Args:
            request_prometheus_api (str): A URL de consulta ao Prometheus
            para uma determinada métrica.

        Returns:
            Dado bruto do Prometheus seguindo a estruturação do json (dict).
    """
    from json import loads
    from requests import get

    return loads(get(request_prometheus_api).text) 

def processar_dados(dados: dict) -> dict:

    from numpy import array
   
    
    if dados.get('status') == 'success':
        dados_processados = {
            'status': dados.get('status'),
            'data': array(dados.get('data')).tolist()
        }
    else:
        dados_processados = {
            'status': dados.get('status'),
            'data': dados.get('data')
        }
    # print(dados_processados)
    return dados_processados


# def gerar_response(status, metric, type, msg= False):
#     body ={}
#     body['status'] = status
#     body['metric'] = metric
#     body['type'] = type
#     if msg:
#         body['msg'] = msg
#     return jsonify(body, status=200)



# def get_request_prometheus_api():
#     return loads(get('http://localhost:9090/api/v1/query?query=sum(rate(http_requests_total[1m]))').text)


# def getHistogram(t):
#     REQUEST_TIME_HIST = Histogram('request_latency_seconds', 'Histogram')
   


# COUNTER = Counter('requests_greater_than_half_sec_total',
#                   'number of waits greater than half a second')


# @REQUEST_TIME_HIST.time()
# def process_request(t):
#     """A dummy function that takes some time."""
#     time.sleep(t)