
![Projeto de IOT - Estacionamento Inteligente (1)](https://github.com/user-attachments/assets/24c1c955-0ef6-4267-8b3c-374c3a3c5914)


O **Tech Parking** consiste em um sistema inteligente de estacionamento que integra hardware e software para o monitoramento e gerenciamento das vagas disponíveis. Por meio de sensores conectados a um microcontrolador, como o Arduino, o sistema detecta a presença de veículos nas vagas e atualiza essas informações em tempo real em uma interface web desenvolvida com Django.

Este projeto foi desenvolvido como atividade acadêmica da disciplina de Internet das Coisas (IoT) do curso de Análise e Desenvolvimento de Sistemas (ADS) do Instituto Federal de Rondônia.



## Funcionalidades

- Monitoramento em tempo real da ocupação das vagas de estacionamento.
- Interface web para visualização do status das vagas.
- Integração com hardware (sensores e microcontrolador) para detecção de veículos.
- Armazenamento de dados utilizando SQLite.

## Tecnologias Utilizadas

- Python
- Django
- SQLite
- Arduino 
- Sensores de presença

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

- `tech_parking/`: Diretório principal do projeto Django.
- `parking/`: Aplicativo Django responsável pela lógica de estacionamento.
- `arduino.py`: Script para comunicação entre o microcontrolador e o servidor Django.
- `validator.py`: Módulo para validação de dados recebidos dos sensores.
- `db.sqlite3`: Banco de dados SQLite utilizado pelo Django.
- `requirements.txt`: Lista de dependências do projeto.

## Instalação

1.Clone o repositório:

```bash
git clone https://github.com/nnathalia/tech_parking.git
cd tech_parking
```

2.Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate (No Windows: venv\Scripts\activate)
```

3.Instale as dependências:

```bash
pip install -r requirements.txt
```

4.Aplique as migrações do banco de dados:

```bash
python manage.py migrate
```

5.Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

## Autores
- Nathalia Mariano — [GitHub](https://github.com/nnathalia)
- Amanda Alves — [GitHub](https://github.com/aalvesz)
- Gilvan Alves — [GitHub](https://github.com/Gilvan1254)
- Caian Henrique 


## Licença
Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.







