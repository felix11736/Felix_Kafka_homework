from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import csv
from time import sleep

def load_avro_schema_from_file():
    key_schema = avro.load("bitcoin_key.avsc")
    value_schema = avro.load("bitcoin_value.avsc")

    return key_schema, value_schema

def send_record():
    key_schema, value_schema = load_avro_schema_from_file()

    producer_config = {
        "bootstrap.servers": "localhost:9092",
        "schema.registry.url": "http://localhost:8081",
        "acks": "1"
    }

    producer = AvroProducer(producer_config, default_key_schema=key_schema, default_value_schema=value_schema)

    file = open('data/bitcoin_price_Training.csv')

    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        key = {"date": row[0]}
        value = {
            "date": row[0],
            "open": float(row[1]),
            "high": float(row[2]),
            "low": float(row[3]),
            "close": float(row[4]),
            "volume": (row[5]),
            "market_cap": row[6]
        }

        try:
            producer.produce(topic='bitcoin_prices', key=key, value=value)
        except Exception as e:
            print(f"Exception while producing record value - {value}: {e}")
        else:
            print(f"Successfully produced record value - {value}")

        producer.flush()
        sleep(1)

if __name__ == "__main__":
    send_record()
