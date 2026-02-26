import json
import os
from .constants import ARQUIVO_RECORDE


def ler_recordes():
    default = {"FACIL": [], "MEDIO": [], "DIFICIL": []}
    if not os.path.exists(ARQUIVO_RECORDE):
        return default

    try:
        with open(ARQUIVO_RECORDE, "r") as f:
            return json.load(f)
    except:
        return default


def salvar_recorde(nv, pts, nome):
    rds = ler_recordes()
    rds[nv].append({"nome": nome, "pontos": pts})
    rds[nv] = sorted(rds[nv], key=lambda x: x['pontos'], reverse=True)[:5]

    with open(ARQUIVO_RECORDE, "w") as f:
        json.dump(rds, f)
