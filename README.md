# Sistema de Promoções - Microsserviços Orientados a Eventos

Este projeto é um sistema distribuído orientado a eventos, baseado em microsserviços, para gerenciar e promover promoções de produtos. Os microsserviços comunicam-se exclusivamente por meio de eventos publicados e consumidos em um **broker RabbitMQ**, utilizando uma troca de tópicos.

## Instruções de Configuração

### 1. Inicie o RabbitMQ
Certifique-se de que o daemon do Docker esteja em execução e, em seguida, inicie o broker do RabbitMQ:
```bash
docker-compose up -d
```

### 2. Configure o Ambiente Python
Crie um ambiente virtual e instale as dependências necessárias:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure o Caminho do Python
No diretório raiz do projeto, execute:
```bash
export PYTHONPATH=.
```

### 4. Gere as Chaves Criptográficas
Os microsserviços requerem pares de chaves pública/privada para assinar e verificar eventos. Execute o script utilitário para gerar o diretório keys/:
```bash
python src/utils/generate_key_pair.py
```

## Executando o Sistema

Para ver a arquitetura orientada a eventos em ação, você precisará abrir várias janelas de terminal. Certifique-se de que seu ambiente virtual esteja ativado em cada uma delas e que o caminho do Python está configurado corretamente, (Conforme o ponto 3 da seção anterior).

### Passo 1: Iniciar os Serviços Principais de Backend
Em três terminais separados, inicie os consumidores de backend:
```bash
# Terminal 1: MS de Promoção
python src/promocao.py

# Terminal 2: MS de Classificação
python src/ranking.py

# Terminal 3: MS de Notificação
python src/notificacao.py
```

### Passo 2: Iniciar os Listeners do Cliente

Em um quarto terminal, inicie um cliente de usuário para ouvir as notificações recebidas:
```bash
# Terminal 4: Cliente
python src/client.py
```

### Passo 3: Inicie o Gateway (Interface do Usuário)

Em um terminal final, execute o aplicativo Gateway:
```bash
# Terminal 5: Interface do Usuário do Gateway
python src/gateway.py
```