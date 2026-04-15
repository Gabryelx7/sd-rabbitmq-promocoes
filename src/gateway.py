import sys
import uuid
from src.shared.security import load_private_key, create_signed_envelope
from src.shared.messaging import RabbitMQHandler

PRIVATE_KEY_PATH = "keys/gateway_private_key.pem"
private_key = load_private_key(PRIVATE_KEY_PATH)

broker = RabbitMQHandler()
broker.establish_connection()

def menu():
    while True:
        print("\n=== Sistema de Promoções - Gateway ===")
        print("1. Cadastrar uma nova promoção")
        print("2. Sair")

        choice = input("Selecione uma opção: ")

        if choice == '1':
            register_promotion()
        elif choice == '2':
            print("Fechando a conexão...")
            broker.close_connection()
            sys.exit(0)
        else:
            print("Opção inválida. Tente novamente")

def register_promotion():
    print("\n--- Cadastro de Promoção ---")
    
    product_name = input("Nome do Produto: ")
    category = input("Categoria: ")
    price = float(input("Preço: "))

    event_data = {
        "id": str(uuid.uuid4()),
        "produto": product_name,
        "categoria": category,
        "preco": price,
    }

    envelope = create_signed_envelope(event_data, private_key)

    routing_key = "promocao.recebida"
    broker.publish_message(routing_key, envelope)

    print(f"\n[+] Promoção para '{product_name}' recebida!")

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nAbortando...")
        broker.close_connection()
        sys.exit(0)

