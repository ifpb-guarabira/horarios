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

open("_data/horarios.json", "w").write(json.dumps({"cursos" : cursos}))
