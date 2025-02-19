import serial
import requests
import re
import cv2
import numpy as np
from PIL import Image
import pytesseract
import threading
from validator import verificar_placa_no_banco

# Configuração da porta serial
serial_port = 'COM3'
baud_rate = 9600
arduino = serial.Serial(serial_port, baud_rate, timeout=1)

# URL da API Django
api_url = "http://127.0.0.1:8000/api/atualizar_monitoramento/"

# Mapeamento dos sensores para as vagas
vagas = {
    "A1": None,
    "A2": None,
    "A3": None
}

# Configuração do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def monitoramento_vagas():
    """ Função para monitorar sensores do Arduino e enviar dados para a API """
    while True:
        line = arduino.readline().decode('utf-8').strip()
        if line:
            match = re.search(r"(A\d):\s*([\d.]+)", line)
            if match:
                codigo_vaga = match.group(1)
                distancia = float(match.group(2))

                if codigo_vaga in vagas:
                    vagas[codigo_vaga] = distancia
                    print(f"📏 {codigo_vaga} - Distância válida: {distancia} cm")

                    # Enviar dados para a API Django
                    response = requests.post(api_url, json={"distancia": distancia, "codigo_vaga": codigo_vaga})
                    if response.status_code == 200:
                        print(f"✅ Dados da {codigo_vaga} enviados com sucesso para a API!")
                    else:
                        print(f"❌ Erro ao enviar dados da {codigo_vaga}: {response.status_code}")

                # Controle da cancela (Sensor A4)
                elif codigo_vaga == "A4":
                    if 0 < distancia < 10:
                        print(f"✅ Sensor A4 ativado: Distância {distancia} cm.")
                        arduino.write(b"servo_on\n")  # Envia comando para abrir a cancela
                    else:
                        print(f"⚡ Sensor A4 desativado: {distancia} cm.")

def reconhecimento_placa():
    """ Função para capturar e reconhecer placas via webcam """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro ao acessar a webcam")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        pil_image = Image.fromarray(thresh)

        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-'
        texto = pytesseract.image_to_string(pil_image, config=custom_config).strip()

        # Detectar placa no texto extraído
        match_mercosul = re.search(r'[A-Z]{3}[0-9][A-Z][0-9]{2}', texto)
        match_antigo = re.search(r'[A-Z]{3}-?[0-9]{4}', texto)

        placa = match_mercosul.group() if match_mercosul else match_antigo.group() if match_antigo else None

        if placa:
            print(f"🔍 Placa detectada: {placa}")

            if verificar_placa_no_banco(placa):
                print(f"✅ Placa {placa} AUTORIZADA! Abrindo cancela...")
                arduino.write(b"servo_on\n")  # Enviar comando para abrir a cancela
                arduino.flush()
            else:
                print(f"❌ Placa {placa} NÃO AUTORIZADA! Acesso negado.")
        

        cv2.imshow("Reconhecimento de Placa", thresh)
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Criar e iniciar as threads
thread1 = threading.Thread(target=monitoramento_vagas)
thread2 = threading.Thread(target=reconhecimento_placa)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
