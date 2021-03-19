import json
import os

import amqp_setup

monitorBindingKey='#'

def getInboxMsg():
    amqp_setup.check_setup()
    queue_name = "Inbox"  

    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() 

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived inbox message by " + __file__)
    processMsg(body)
    print() 

def processMsg(inboxMsg):
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
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    getInboxMsg()