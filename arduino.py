import serial
import requests
import re  # Para filtrar números

# Configurações da porta serial
serial_port = 'COM3'  # Ajuste conforme necessário
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

print("🚀 Iniciando leitura da porta serial...")

try:
    while True:
        line = arduino.readline().decode('utf-8').strip()
        if line:
            try:
                # Verifica se a linha contém informações para alguma vaga específica
                match = re.search(r"(A\d):\s*([\d.]+)", line)
                if match:
                    codigo_vaga = match.group(1)  # Exemplo: "A1", "A2", "A3", "A4"
                    distancia = float(match.group(2))  # Captura a distância

                    # Lida com os sensores 1, 2 e 3 normalmente
                    if codigo_vaga in vagas:
                        vagas[codigo_vaga] = distancia  # Atualiza a distância na vaga correspondente

                        print(f"📏 {codigo_vaga} - Distância válida: {distancia} cm")

                        # Enviar dados para a API Django
                        response = requests.post(api_url, json={"distancia": distancia, "codigo_vaga": codigo_vaga})

                        if response.status_code == 200:
                            print(f"✅ Dados da {codigo_vaga} enviados com sucesso para a API!")
                        else:
                            print(f"❌ Erro ao enviar dados da {codigo_vaga}: {response.status_code} - {response.text}")

                    # Tratamento especial para o sensor A4
                    elif codigo_vaga == "A4":
                        if distancia > 0 and distancia < 20:
                            print(f"✅ Sensor A4 ativado: Distância {distancia} cm.")
                        else:
                            print(f"⚡ Sensor A4 desativado, distância: ({distancia} cm).")
                else:
                    print(f"⚠️ Formato inválido recebido: {line}")

            except ValueError:
                print(f"⚠️ Dado inválido recebido: {line}")

except KeyboardInterrupt:
    print("🛑 Encerrando...")

finally:
    arduino.close()
