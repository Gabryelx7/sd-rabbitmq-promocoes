import time
import threading
from src.shared.messaging import RabbitMQHandler

# Function to run the consumer in the background
def run_consumer():
    consumer = RabbitMQHandler()
    consumer.establish_connection()
    
    # Declare a queue and bind it to a test topic
    queue_name = consumer.declare_queue()
    consumer.bind_keys(queue_name, ["test.topic.*"])
    
    def callback(ch, method, properties, body):
        print(f"\n[X] Consumer received message on routing key: {method.routing_key}")
        print(f"[X] Payload: {body.decode('utf-8')}")
        
    consumer.start_consuming(queue_name, callback)

# Start consumer thread
print("Starting consumer thread...")
thread = threading.Thread(target=run_consumer, daemon=True)
thread.start()

# Give the consumer a second to connect and bind the queue
time.sleep(1)

# Publish a test message
print("\nPublishing message...")
publisher = RabbitMQHandler()
publisher.establish_connection()

test_payload = {"test": "success", "message": "Hello RabbitMQ!"}
publisher.publish_message("test.topic.test1", test_payload)

# Wait a moment to see the output, then close
time.sleep(1)
publisher.close_connection()
print("\nTest complete.")