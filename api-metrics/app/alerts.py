from typing import Tuple, Dict
from ast import Str
import numpy as np 
from main import coletar_dados_prometheus

PODS=['teastore-webui-5d554cc97f-b9xvj', 'teastore-image-5599565ccf-mnl5v',
      'teastore-db-5d9555684f-w64kj', 'teastore-auth-775c7fc4cc-ck64p',
      'teastore-recommender-8589c6d499-g96fp','teastore-persistence-d69d45b4-47bsj',
      'teastore-db-5d9555684f-w64kj'
    ]


def getAlertByPod (name_pod: str, metric: str, type:str, value) -> dict:

    alert_fail=[]
    if(type=="container_memory_working_set_bytes"):
        tp="container_memoryWorking_set_bytes_%s" %(name_pod)
    else:
        tp="%s_%s" %(type,name_pod)
   
    if('container_cpu_usage_seconds_total_teastore-image-5599565ccf-mnl5v'== tp):
        print("são iguais")
    # print(name_pod in PODS)
    if(name_pod in PODS):
        mtc = coletar_dados_prometheus('Pods', '%s'%tp)
        print(mtc)
        if(float(mtc['data']['result'][0]['value'][1]) > float(value)):
            cpuPod={
                'type':metric,
                'pod': name_pod,
                'alert':"failure",
                'time': mtc['data']['result'][0]['value'][0],
                'value':mtc['data']['result'][0]['value'][1]
            }
            # print(cpuPod)
            alert_fail.append(cpuPod)
            return alert_fail
        else:
            cpuPod={
                'type':metric,
                'pod': name_pod,
                'alert':"default",
                'time': mtc['data']['result'][0]['value'][0],
                'value':mtc['data']['result'][0]['value'][1]
            }
            alert_fail.append(cpuPod)
            return alert_fail
    else :
        # return ("Pod %s Não encontrado" %name_pod)
        return None
    