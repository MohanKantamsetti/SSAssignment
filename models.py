import pymongo,json,os
import pika
db_service  = os.getenv('DB_SERVICE')
db_port     = os.getenv('DB_PORT')
db_user     = os.getenv('DB_USER')
db_pass     = os.getenv('DB_PASSWORD')
db_auth     = os.getenv('DB_NAME')
mongo      = pymongo.MongoClient(host=db_service,port=int(db_port),username=db_user,password=db_pass,authSource=db_auth)
#mongo      = pymongo.MongoClient('localhost',27017)
db=mongo['checkout_db']
class Payment:
    def __init__(self):
        pass
    def add_payment(self,payment):
        payment={
            'payment_id':self.get_paymentid()+1,
            'payment_amount':payment['payment_amount'],
            'payment_date':payment['payment_date'],
            'payment_status':payment['payment_status'],
            'payment_method':payment['payment_method'],
            'payment_notes':payment['payment_notes'],
        }
        res=db.payments.insert_one(payment)
        return res.inserted_id
    
    def get_payment(paymentid):
        paymentid=int(paymentid)
        payment=db.payments.find_one({'payment_id':paymentid})
        if not payment.__sizeof__==0:
            payment['_id']=str(payment['_id']) #convert the object id to string
            return payment
        else:
            return []

class Cart:
    def __init__(self):
        pass
    def add_to_cart(self,cart):
        cart={
            'cart_id':self.get_cartid()+1,
            'cart_items':cart['cart_items'],
            'cart_total':cart['cart_total'],
            'cart_date':cart['cart_date'],
        }
        res=db.carts.insert_one(cart)
        return res.inserted_id
    
    def get_cart(cart_id):
        cart_id=int(cart_id)
        cart=db.carts.find_one({'cart_id':cart_id})
        if not cart.__sizeof__==0:
            cart['_id']=str(cart['_id']) #convert the object id to string
            return cart
        else:
            return []
    
    def clear_cart(self,cart_id):
        return db.carts.delete_one({'cart_id':cart_id})

class Order:
    @staticmethod
    def add_order(order):
        order={
            'order_id':Order.get_orderid()+1,
            'customer_name':order['customer_name'],
            'customer_email':order['customer_email'],
            'customer_phone':order['customer_phone'],
            'order_items':order['order_items'],
            'order_total':order['order_total'],
            'order_date':order['order_date'],
            'order_status':order['order_status'],
            'order_address':order['order_address'],
            'order_payment':order['order_payment'],
            'order_shipment':order['order_shipment'],
            'order_tracking':order['order_tracking'],
            'order_notes':order['order_notes'],
        }
        res=db.orders.insert_one(order)
        order_notification={
            'order_id':order['order_id'],
            'order_status':order['order_status'],
            'customer_email':order['customer_email'],
            'order_address':order['order_address'],
            'order_payment':order['order_payment'],
            'order_shipment':order['order_shipment'],
            'order_tracking':order['order_tracking'],
        }
        publish_order(order_notification)
        return res.inserted_id
    @staticmethod
    def get_orders():
        all_orders=[]
        orders=db.orders.find()
        for order in orders:
            order['_id']=str(order['_id'])
            all_orders.append(order)
        return all_orders
    
    @staticmethod
    def get_orderid():
        order_id=0
        orderid=db.orders.find().sort('order_id',-1).limit(1)
        for i in orderid:
            order_id=i['order_id']
        return order_id

    @staticmethod
    def get_order(order_id):
        order_id=int(order_id)
        order=db.orders.find_one({'order_id':order_id})
        if not order.__sizeof__==0:
            order['_id']=str(order['_id']) #convert the object id to string
            return order
        else:
            return []
    @staticmethod
    def update_order(order_id,order):
        return db.orders.update_one({'order_id':order_id},{'$set':order})
    @staticmethod
    def delete_order(order_id):
        return db.orders.delete_one({'order_id':order_id})

#rabbitmq connection
def publish_order(order):
    #auth
    user=os.getenv('RABBITMQ_USER')
    password=os.getenv('RABBITMQ_PASSWORD')
    connection=pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',credentials=pika.PlainCredentials(user,password)))
    channel=connection.channel()
    channel.queue_declare(queue='order_queue')
    channel.basic_publish(exchange='',routing_key='order_queue',body=json.dumps(order))
    connection.close()