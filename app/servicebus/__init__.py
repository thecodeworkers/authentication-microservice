from pika import BlockingConnection, ConnectionParameters, BasicProperties
from ..constants import SERVICEBUS_HOST
from ..utils import contains
import uuid
import json

class ServiceBus():
    def __init__(self):
        self.__connection = BlockingConnection(ConnectionParameters(host=SERVICEBUS_HOST))
        self.__channel = self.__connection.channel()
        self.__queues = []

    def add_queue(self, queue_name, emitter):
        event_object = {
            'queue_name': queue_name,
            'emitter': emitter
        }

        self.__queues.append(event_object)

    def receive(self, channel_name, send=''):
        self.__channel_name = channel_name
        self.__start_one_channel(self.__on_response)

        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.__publish_channel(self.__channel, self.__channel_name, self.corr_id, send, self.callback_queue)
        
        while self.response is None:
            self.__connection.process_data_events()

        return self.response

    def send(self):
        self.__start_multiple_channel()

    def status(self):
        return len(self.__channel.consumer_tags)

    def start(self):
        self.__channel.start_consuming()

    def stop(self):
        self.__channel.stop_consuming()

    def close_connection(self):
        self.__connection.close()

    def __start_one_channel(self, on_event):
        result = self.__queue_declaration('', True)
        self.callback_queue = result.method.queue

        self.__consume_channel(self.callback_queue, on_event, True)

    def __start_multiple_channel(self):
        self.__channel.basic_qos(prefetch_count=1)

        for queue in self.__queues:
            result = self.__queue_declaration(queue['queue_name'])
            callback_queue = result.method.queue

            self.__consume_channel(callback_queue, self.__on_request)

    def __on_request(self, ch, method, props, body):
        request = contains(self.__queues, lambda queue: queue['queue_name'] == method.routing_key)
        request = request['emitter']() if request != None else None

        self.__publish_channel(ch, props.reply_to, props.correlation_id, request)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body.decode('utf8'))

    def __queue_declaration(self, queue, exclusive=False):
        result = self.__channel.queue_declare(queue=queue, exclusive=exclusive)
        return result

    def __consume_channel(self, callback_queue, on_event, auto_ack=False):
        self.__channel.basic_consume(
            queue=callback_queue,
            on_message_callback=on_event,
            auto_ack=auto_ack
        )

    def __publish_channel(self, channel, routing_key, correlation_id, body, reply_to=None):
        channel.basic_publish(
            exchange='',
            routing_key=routing_key,
            properties=BasicProperties(
                reply_to=reply_to, 
                correlation_id=correlation_id,
                content_type='application/json'
            ),
            body=json.dumps(body)
        )
