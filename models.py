import pymongo,json,os
db_service  = os.getenv('DB_SERVICE')
db_port     = os.getenv('DB_PORT')
db_user     = os.getenv('DB_USER')
db_pass     = os.getenv('DB_PASSWORD')
db_auth     = os.getenv('DB_NAME')
mongo      = pymongo.MongoClient(host=db_service,port=int(db_port),username=db_user,password=db_pass,authSource=db_auth)
#mongo      = pymongo.MongoClient('localhost',27017)
db=mongo['checkout_db']


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
