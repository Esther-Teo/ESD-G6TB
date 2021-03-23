import pika 

hostname = "localhost" 
port = 5672 

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=hostname, port=port,
        heartbeat=3600, blocked_connection_timeout=3600, # these parameters to prolong the expiration time (in seconds) of the connection
))

channel = connection.channel()
 
# Set up exchange 
exchange_name = 'inbox_topic'
exchange_type = 'topic'
channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=True)

# ----------  Inbox Queue  ----------
# Declare Inbox queue
queue_name = 'Inbox'
channel.queue_declare(queue=queue_name, durable=True) 
# bind 'Inbox' to 'inbox_topic' exchange
# any routing_key (since #)
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='#') 

# ----------  Manage_Offers Queue  ----------
queue_name = 'Manage_Offers'
channel.queue_declare(queue=queue_name, durable=True) 
# bind 'Manage_Offers' to 'inbox_topic' exchange
# any routing_key that ends with '.offer'
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='*.offer') 

"""
This function in this module sets up a connection and a channel to a local AMQP broker,
and declares a 'topic' exchange to be used by the microservices in the solution.
"""
def check_setup():
    global connection, channel, hostname, port, exchangename, exchangetype

    if not is_connection_open(connection):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    if channel.is_closed:
        channel = connection.channel()
        channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype)

def is_connection_open(connection):
    try:
        connection.process_data_events()
        return True
    except pika.exceptions.AMQPError as e:
        print("AMQP Error:", e)
        print("...creating a new connection.")
        return False







