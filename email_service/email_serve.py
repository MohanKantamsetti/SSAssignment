import pika.exceptions
from smtp_config import smtp_mail, smtp_pass
import smtplib, ssl, json
import pika, os, time
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def send_email(to, message):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    fro = smtp_mail
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(fro, smtp_pass)
            server.sendmail(fro, to, message)
            server.quit()
            logger.info(f"Email sent to {to}")
            return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False

def callback(ch, method, properties, body):
    order_data = json.loads(body)
    message = f"Subject: Order {order_data['order_id']} - {order_data['order_status']}\n\n"
    message += f"Order Details:\n"
    message += f"order_payment : {order_data['order_payment']['transaction_id']}\n"
    message += f"order_shipment : {order_data['order_shipment']['shipment_id']}\n"
    message += f"order_tracking : {order_data['order_tracking']}\n"
    message += "\n\nThank you for shopping with us!"
    send_email(order_data['customer_email'], message)
    logger.debug(f"Email sent for order {order_data['order_id']}")

def consume_orders():
    retries=5
    while retries > 0:
        try:
            logger.debug('Starting to consume orders')
            user = os.getenv('RABBITMQ_USER')
            password = os.getenv('RABBITMQ_PASSWORD')
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='rabbitmq', 
                credentials=pika.PlainCredentials(user, password)
            ))
            channel = connection.channel()
            logger.debug('Connection made successfully')
            channel.queue_declare(queue='order_queue')
            channel.basic_consume(queue='order_queue',
                                  on_message_callback=callback,
                                  auto_ack=True)
            logger.debug(' [*] Waiting for messages')
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            logger.debug(f"Retrying in 5 seconds")
            retries -= 1
            time.sleep(5)

if __name__ == '__main__':
    consume_orders()