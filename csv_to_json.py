#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: skip-file

import csv
import json

def csv_to_json(csv_file):
    csv_data = csv.reader(csv_file, delimiter=";")

    n, m = csv_data.next(), csv_data.next()

    turma = n[0]
    horarios = [[], [], [], [], []]

    try:
        while True:
            n, m = csv_data.next(), csv_data.next()

            for i in range(5):
                if n[i+1] and n[i+1] not in ("ALMOÇO", "JANTAR", "INTERVALO"):
                    horarios[i].append({"disciplina" : n[i+1],
                                        "professor"  : m[i+1]})

                else:
                    horarios[i].append(None)

    except:
        pass

    return {"turma" : turma, "horarios" : horarios}

cursos = []
turmas = []

turmas.append(csv_to_json(open("data/csv/Turmas-IN1.csv")))
turmas.append(csv_to_json(open("data/csv/Turmas-IN2.csv")))
turmas.append(csv_to_json(open("data/csv/Turmas-IN3.csv")))
turmas.append(csv_to_json(open("data/csv/Turmas-IN4.csv")))

cursos.append({"curso" : "Informática", "turmas" : turmas})
turmas = []

turmas.append(csv_to_json(open("data/csv/Turmas-ED1.csv")))
turmas.append(csv_to_json(open("data/csv/Turmas-ED2.csv")))
turmas.append(csv_to_json(open("data/csv/Turmas-ED3.csv")))

cursos.append({"curso" : "Edificações", "turmas" : turmas})
turmas = []

turmas.append(csv_to_json(open("data/csv/Turmas-CN1.csv")))

cursos.append({"curso" : "Contabilidade", "turmas" : turmas})
turmas = []

turmas.append(csv_to_json(open("data/csv/Turmas-GC1.csv")))
turmas.append(csv_to_json(open("data/csv/Turmas-GC2.csv")))
turmas.append(csv_to_json(open("data/csv/Turmas-GC3.csv")))
turmas.append(csv_to_json(open("data/csv/Turmas-GC4.csv")))

cursos.append({"curso" : "Gestão Comercial", "turmas" : turmas})

open("data/horarios.json", "w").write(json.dumps({"cursos" : cursos}))
