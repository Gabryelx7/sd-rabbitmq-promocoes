import sys
import json
from shared.security import load_public_key, verify_and_extract_envelope
from shared.messaging import RabbitMQHandler

INTERESTS = [
    "promocao.jogo",
    "promocao.destaque"
]

RANKING_PUBLIC_KEY_PATH = "keys/ranking_public_key.pem"
ranking_public_key = load_public_key(RANKING_PUBLIC_KEY_PATH)

def handle_notification(ch, method, properties, body):
    envelope = json.loads(body)
    routing_key = method.routing_key
    
    print("\n" + "-"*40)
    print(f"NOTIFICAÇÃO RECEBIDA: {routing_key}")
    print("="*40)
    if "destaque" in routing_key:
        event_data = verify_and_extract_envelope(envelope, ranking_public_key)
        print(f"Titulo: HOT DEAL")
        print(f"Mensagem: Uma nova promoção em destaque foi publicada!")
        print(f"Produto: {event_data["produto"]}")
        print(f"Preço: {event_data["preco"]}")
    else: # Aqui estão as notificações de fato, não precisa verificar
        for key, value in envelope.items():
            print(f"{key.capitalize()}: {value}")
    print("="*40 + "\n")

if __name__ == "__main__":
    print(f"[*] Iniciando Microsserviço Cliente...")
    print(f"[*] Cliente inscrito nos seguintes tópicos: {INTERESTS}")
    
    broker = RabbitMQHandler()
    
    try:
        broker.establish_connection()
        queue_name = broker.declare_queue()
        broker.bind_keys(queue_name, INTERESTS)
        
        broker.start_consuming(queue_name, handle_notification)
    except KeyboardInterrupt:
        print("\nAbortando...")
        broker.close_connection()
        sys.exit(0)