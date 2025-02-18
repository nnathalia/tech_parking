import cv2
import numpy as np
from PIL import Image
import pytesseract
import re
from validator import verificar_placa_no_banco

# Configuração do Tesseract (adicione o caminho se necessário)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Abrir a webcam
cap = cv2.VideoCapture(0)  # Use 0 para a webcam padrão

# Verificar se a webcam foi aberta corretamente
if not cap.isOpened():
    print("Erro ao acessar a webcam")
    exit()

while True:
    # Capturar frame da webcam
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar frame")
        break

    # Converter o frame para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicar equalização de histograma para melhorar contraste
    clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # Aplicar filtro de limiar adaptativo
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Aplicar filtro mediano para reduzir ruídos
    filtered = cv2.medianBlur(thresh, 3)

    # Aplicar dilatação
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(filtered, kernel, iterations=1)

    # Converter o frame pré-processado para o formato PIL
    pil_image = Image.fromarray(dilated)

    # Realizar OCR no frame
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-'
    texto = pytesseract.image_to_string(pil_image, config=custom_config)

    # Limpar o texto detectado de quebras de linha ou espaços indesejados
    texto = texto.strip()

    # Validar placas no texto reconhecido
    match_mercosul = re.search(r'[A-Z]{3}[0-9][A-Z][0-9]{2}', texto)
    match_antigo = re.search(r'[A-Z]{3}-?[0-9]{4}', texto)

    placa = None
    if match_mercosul:
        placa = match_mercosul.group()
        print(f"Placa Mercosul detectada: {placa}")
    elif match_antigo:
        placa = match_antigo.group()
        print(f"Placa Antiga detectada: {placa}")
        
    # Verificar se a placa foi encontrada no banco
    if placa:
        if verificar_placa_no_banco(placa):
            print(f"Placa {placa} encontrada no banco de dados.")
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
