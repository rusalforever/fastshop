from kafka import KafkaConsumer
import time
import json


def read_queue():
    consumer = KafkaConsumer(
        'product-topic',
        bootstrap_servers='localhost:29092',
        auto_offset_reset='earliest',  # Читати з початку, якщо немає збереженого офсету
        group_id='my-group',           # Група споживачів для координування читання
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Десеріалізація JSON
    )

    # Безперервне читання і виведення повідомлень
    while True:
        for message in consumer:
            data = message.value
            print(json.dumps(data, indent=4, ensure_ascii=False))
            # Send product to Hotline
        time.sleep(1)


if __name__ == '__main__':
    read_queue()
