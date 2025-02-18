import sqlite3

def verificar_placa_no_banco(placa):
    """
    Verifica se uma placa está registrada no banco de dados na tabela parking_veiculo.
    Retorna True se encontrada, False caso contrário.
    """
    try:
        # Conectar ao banco de dados SQLite
        conexao = sqlite3.connect(r"db.sqlite3")
        cursor = conexao.cursor()

        # Pesquisar a placa na tabela 'parking_veiculo'
        cursor.execute("SELECT * FROM parking_veiculo WHERE placa = ?", (placa,))
        resultado = cursor.fetchone()

        # Fechar a conexão
        conexao.close()

        # Retornar True se encontrado, False caso contrário
        return resultado is not None
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return False


