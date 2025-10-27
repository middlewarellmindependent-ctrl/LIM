import logging

# Criar um logger específico para a sua aplicação
logger = logging.getLogger("my_app")
logger.setLevel(logging.INFO)  # Define o nível mínimo de log

# Criar um manipulador para escrever no arquivo
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)

# Definir o formato do log
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Adicionar o manipulador ao logger
logger.addHandler(file_handler)

# Desativar logs desnecessários de bibliotecas externas
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("watchfiles").setLevel(logging.ERROR)
