import pika 

hostname = "localhost" 
port = 5672 

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=hostname, port=port,
        heartbeat=3600, blocked_connection_timeout=3600, 
))

channel = connection.channel()
 
# Set up exchange 
exchange_name = 'offer_topic'
exchange_type = 'topic'
channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=True)

# ---------- Error queue ----------
queue_name = 'Error'
channel.queue_declare(queue=queue_name, durable=True) 
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='*.error') 

# ----------  Inbox Queue  ----------
queue_name = 'Inbox'
channel.queue_declare(queue=queue_name, durable=True) 
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='#') # KEY NOT CONFIRMED 

# # ----------  Manage_Offers Queue  ----------
# queue_name = 'Manage_Offers'
# channel.queue_declare(queue=queue_name, durable=True) 
# channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='*.offer') 

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







