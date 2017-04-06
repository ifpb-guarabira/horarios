#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: skip-file

import csv
import json
from unicodedata import normalize

def csv_to_json(csv_file):
    csv_data = csv.reader(csv_file, delimiter=";")

    n, m = csv_data.next(), csv_data.next()

    turma = n[0]
    linhas = []
    colunas = m[:-1]

    try:
        while True:
            n, m = csv_data.next(), csv_data.next()
            aulas = []

            for i in range(len(colunas) - 1):
                aulas.append({"disciplina" : n[i+1],
                              "professor"  : m[i+1]})

            linhas.append({"horario" : n[0], "aulas" : aulas})

    except:
        pass

    codigo = normalize('NFKD', turma.decode("utf-8")).encode('ASCII', 'ignore').replace(" ","-").lower()

    return {"id" : codigo, "nome" : turma, "linhas" : linhas, "colunas" : colunas}


def professores_in_cursos(cursos):
    professores = set()
    
    for curso in cursos:
        for turma in curso["turmas"]:
            for linha in turma["linhas"]:
                for aula in linha["aulas"]:
                    if aula["professor"]:
                        professores.add(aula["professor"])
    
    professores = list(professores)
    professores.sort()
    
    return professores

def turma_to_professor(t, p):
    codigo = normalize('NFKD', p.decode("utf-8")).encode('ASCII', 'ignore').replace(" ","-").lower()

    result = {"id" : codigo, "nome" : p, "colunas" : t["colunas"], "linhas" : [] }
    
    for l in t["linhas"]:
        linha = {"horario" : l["horario"], "aulas" : []}
        
        for a in l["aulas"]:
            linha["aulas"].append({
                "turma" : t["nome"] if a["professor"] == p else
                          "",
                "disciplina" : a["disciplina"] if a["professor"] == p else
                               a["disciplina"] if a["disciplina"] in ["INTERVALO",
                                   "ALMOÇO", "JANTAR"] else
                               ""
                })

        result["linhas"].append(linha)
    
    return result

def cursos_to_professores(cursos, professores):
    result = []
    turmas = []

    for curso in cursos:
        turmas += curso["turmas"]

    for nome in professores:
        professor = turma_to_professor(turmas[0], nome)

        for t in range(1, len(turmas)):
            for l in range(len(turmas[t]["linhas"])):
                for a in range(len(turmas[t]["linhas"][l]["aulas"])):
                    aula = turmas[t]["linhas"][l]["aulas"][a]

                    if aula["professor"] == nome:
                        professor["linhas"][l]["aulas"][a]["turma"] = turmas[t]["nome"]
                        professor["linhas"][l]["aulas"][a]["disciplina"] = aula["disciplina"]

        result.append(professor)

    return result

cursos = []
turmas = []

turmas.append(csv_to_json(open("_csv/Turmas-IN1.csv")))
turmas.append(csv_to_json(open("_csv/Turmas-IN2.csv")))
turmas.append(csv_to_json(open("_csv/Turmas-IN3.csv")))
turmas.append(csv_to_json(open("_csv/Turmas-IN4.csv")))

cursos.append({"nome" : "Informática", "turmas" : turmas})
turmas = []

turmas.append(csv_to_json(open("_csv/Turmas-ED1.csv")))
turmas.append(csv_to_json(open("_csv/Turmas-ED2.csv")))
turmas.append(csv_to_json(open("_csv/Turmas-ED3.csv")))

cursos.append({"nome" : "Edificações", "turmas" : turmas})
turmas = []

turmas.append(csv_to_json(open("_csv/Turmas-CN1.csv")))

cursos.append({"nome" : "Contabilidade", "turmas" : turmas})
turmas = []

turmas.append(csv_to_json(open("_csv/Turmas-GC1.csv")))
turmas.append(csv_to_json(open("_csv/Turmas-GC2.csv")))
turmas.append(csv_to_json(open("_csv/Turmas-GC3.csv")))
turmas.append(csv_to_json(open("_csv/Turmas-GC4.csv")))

cursos.append({"nome" : "Gestão Comercial", "turmas" : turmas})


professores = professores_in_cursos(cursos)

with open("_data/horarios.json", "w") as file:
    file.write(json.dumps({
        "cursos" : cursos,
        "professores" : cursos_to_professores(cursos, professores)
    }))
