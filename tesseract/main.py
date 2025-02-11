import cv2
import numpy as np
from PIL import Image
import pytesseract
import re
import serial
from validator import verificar_placa_no_banco

# Configuração do Tesseract (adicione o caminho se necessário)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configuração da comunicação serial com o Arduino
porta_serial = serial.Serial('COM3', 9600)  # Substitua 'COM3' pela porta correta

# Abrir a webcam
cap = cv2.VideoCapture(0)  # Use 0 para a webcam padrão

# Verificar se a webcam foi aberta corretamente
if not cap.isOpened():
    print("Erro ao acessar a webcam")
    exit()

encontrado = False

while not encontrado:
    # Capturar frame da webcam
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar frame")
        break

    # Converter o frame para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicar filtro de limiar
    _, thresh = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY_INV)

    # Aplicar dilatação
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    # Converter o frame pré-processado para o formato PIL
    pil_image = Image.fromarray(dilated)

    # Realizar OCR no frame
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-'
    texto = pytesseract.image_to_string(pil_image, config=custom_config)

    # Limpar o texto detectado de quebras de linha ou espaços indesejados
    texto = texto.strip()

    # Buscar todas as placas detectadas
    placas_detectadas = re.findall(r'[A-Z]{3}[0-9][A-Z][0-9]{2}|[A-Z]{3}-?[0-9]{4}', texto)

    for placa in placas_detectadas:
        print(f"Placa detectada: {placa}")
        
        # Verificar se a placa foi encontrada no banco
        if verificar_placa_no_banco(placa):
            print(f"Placa {placa} encontrada no banco de dados.")
            # Enviar sinal ao Arduino
            porta_serial.write(b'1')  # Envia o byte '1' para o Arduino
            encontrado = True
            break
        else:
            print(f"Placa {placa} não encontrada no banco de dados.")

    # Exibir o frame processado na janela (opcional)
    cv2.imshow("Frame Processado", dilated)

    # Parar manualmente com a tecla 'x'
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

# Liberar a webcam e fechar janelas
cap.release()
cv2.destroyAllWindows()
porta_serial.close()
