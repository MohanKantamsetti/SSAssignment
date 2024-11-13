from flask import Flask,request,jsonify,Response
from flask_cors import CORS, cross_origin
import json, jwt, datetime, os
from models import Order
app=Flask(__name__)
cors=CORS(app)

@app.route('/')
@cross_origin()
def home():
    return jsonify({'message':'Welcome to the checkout manager service!', 'status':200})

#Verify the token in the header
def verify_token():
    return True

@app.route('/checkout',methods=['POST'])
@cross_origin()
def checkout():
    if verify_token:
        order=request.json
        order['order_date']=datetime.datetime.now()
        orderid=Order.add_order(order)
        return jsonify({'message':'Order placed successfully!','status':200,'order_id':str(orderid)})
    
@app.route('/orders',methods=['GET'])
@cross_origin()
def get_orders():
    if verify_token:
        orders=Order.get_orders()
        print(orders)
        return jsonify({'message':'Orders fetched!','orders':orders,'status':200})

@app.route('/order/<order_id>',methods=['GET'])
@cross_origin()
def get_order(order_id):
    if verify_token:
        order=Order.get_order(order_id)
        return jsonify({'order':order,'status':200,'message':'Order fetched!'})
    
@app.route('/order/<order_id>',methods=['PUT'])
@cross_origin()
def update_order(order_id):
    if verify_token:
        order=request.json
        Order.update_order(order_id,order)
        return jsonify({'message':'Order updated!','status':200})
    
@app.route('/order/<order_id>',methods=['DELETE'])
@cross_origin()
def delete_order(order_id):
    if verify_token:
        Order.delete_order(order_id)
        return jsonify({'message':'Order deleted!','status':200})

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=5000)