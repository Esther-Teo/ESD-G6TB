import json
import os

import amqpSetup

monitorBindingKey='#'

def get_inbox_msg():
    amqpSetup.check_setup()
    queue_name = "Inbox"  

    amqpSetup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqpSetup.channel.start_consuming() 

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived inbox message by " + __file__)
    process_msg(body)
    print() 

def process_msg(inboxMsg):
    print("Printing inbox message:")
    try:
        msg = json.loads(inboxMsg)
        print("--JSON:", msg)
    except Exception as e:
        print("--NOT JSON:", e)
        print("--DATA:", inboxMsg)
    print()


if __name__ == "__main__":  
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqpSetup.exchange_name))
    get_inbox_msg()