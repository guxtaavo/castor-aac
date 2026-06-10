#!/usr/bin/env python3
import sys
import time

sys.path.append("/home/pi/catkin_ws/src/huskylens_2/scripts/DFRobot_HuskylensV2/python/smbus2/")
from dfrobot_huskylensv2 import *

ALGORITHM = ALGORITHM_FACE_RECOGNITION
KNOWLEDGE_ID = 1

huskylens = HuskylensV2_I2C()

if not huskylens.knock():
    print("Erro: HuskyLens não encontrada.")
    sys.exit(1)

huskylens.switchAlgorithm(ALGORITHM)
time.sleep(1)

# Carrega banco anterior
huskylens.loadKnowledges(ALGORITHM, KNOWLEDGE_ID)
time.sleep(0.5)

nome_pessoa = input("Digite o nome da pessoa que será cadastrada: ")

print("Modo: Face Recognition")
print("Coloque o rosto da pessoa na frente da câmera.")
print("Quando uma face for detectada, ela será cadastrada automaticamente.")

face_detectada = False
tempo_inicio = None
tempo_estavel = 3.0

while True:
    huskylens.getResult(ALGORITHM)

    if huskylens.available(ALGORITHM):
        result = huskylens.getCachedCenterResult(ALGORITHM)

        if result is not None:
            if not face_detectada:
                print("Face detectada. Mantenha o rosto parado...")
                tempo_inicio = time.time()
                face_detectada = True

            tempo_passado = time.time() - tempo_inicio
            print(f"Cadastrando em {max(0, tempo_estavel - tempo_passado):.1f} s", end="\r")

            if tempo_passado >= tempo_estavel:
                face_id = huskylens.learn(ALGORITHM)

                print()

                if face_id:
                    huskylens.setNameByID(ALGORITHM, face_id, nome_pessoa)
                    huskylens.saveKnowledges(ALGORITHM, KNOWLEDGE_ID)

                    print("Face cadastrada com sucesso!")
                    print(f"ID: {face_id}")
                    print(f"Nome registrado: {nome_pessoa}")
                    print(f"Conhecimento salvo no slot {KNOWLEDGE_ID}")
                else:
                    print("Falha ao cadastrar face.")

                break
    else:
        if face_detectada:
            print()
            print("Face perdida. Tentando novamente...")
        face_detectada = False
        tempo_inicio = None

    time.sleep(0.1)