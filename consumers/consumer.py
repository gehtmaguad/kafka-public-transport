"""Defines core consumer functionality"""
import logging

import confluent_kafka
from confluent_kafka import Consumer, OFFSET_BEGINNING
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from tornado import gen


logger = logging.getLogger(__name__)
BROKER_URL = "PLAINTEXT://localhost:9092"
SCHEMA_REGISTRY_URL = "http://localhost:8081"


class KafkaConsumer:
    """Defines the base kafka consumer class"""

    def __init__(
        self,
        topic_name_pattern,
        message_handler,
        is_avro=True,
        offset_earliest=False,
        sleep_secs=1.0,
        consume_timeout=0.1,
    ):
        """Creates a consumer object for asynchronous use"""
        self.topic_name_pattern = topic_name_pattern
        self.message_handler = message_handler
        self.sleep_secs = sleep_secs
        self.consume_timeout = consume_timeout
        self.offset_earliest = offset_earliest

        #
        #
        # DONE: Configure the broker properties below. Make sure to reference the project README
        # and use the Host URL for Kafka and Schema Registry!
        #
        #
        self.broker_properties = {
            "bootstrap.servers": BROKER_URL,
            "group.id": "my-consumer",
            "schema.registry.url": SCHEMA_REGISTRY_URL
        }

        # DONE: Create the Consumer, using the appropriate type.
        if is_avro is True:
            self.consumer = AvroConsumer(
                config=self.broker_properties
            )
        else:
            self.consumer = Consumer({
                'bootstrap.servers': self.broker_properties.get('bootstrap.servers'),
                'group.id': self.broker_properties.get('group.id')
            })

        #
        #
        # DONE: Configure the AvroConsumer and subscribe to the topics. Make sure to think about
        # how the `on_assign` callback should be invoked.
        #
        #
        self.consumer.subscribe(
            [self.topic_name_pattern], on_assign=self.on_assign)

    def on_assign(self, consumer, partitions):
        """Callback for when topic assignment takes place"""
        # DONE: If the topic is configured to use `offset_earliest` set the partition offset to
        # the beginning or earliest
        for partition in partitions:
            partition.offset = OFFSET_BEGINNING

        consumer.assign(partitions)

    async def consume(self):
        logger.info("Running consumer.consume")
        """Asynchronously consumes data from kafka topic"""
        while True:
            num_results = 1
            while num_results > 0:
                num_results = self._consume()
            await gen.sleep(self.sleep_secs)

    def _consume(self):
        """Polls for a message. Returns 1 if a message was received, 0 otherwise"""
        #
        #
        # DONE: Poll Kafka for messages. Make sure to handle any errors or exceptions.
        # Additionally, make sure you return 1 when a message is processed, and 0 when no message
        # is retrieved.
        #
        #
        while True:
            message = self.consumer.poll(timeout=1.0)

            if message is None:
                return 0
            elif message.error():
                logger.error("Error on consumed message: %s", message.error())
            else:
                self.message_handler(message)
                return 1

    def close(self):
        """Cleans up any open kafka consumers"""
        #
        #
        # DONE: Cleanup the kafka consumer
        #
        #
        self.consumer.close()
