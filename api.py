from flask import Flask,request,jsonify,Response
from flask_cors import CORS, cross_origin
import json, jwt, datetime, os
from models import Order, Payment, Cart
app=Flask(__name__)
cors=CORS(app)

@app.route('/')
@cross_origin()
def home():
    return jsonify({'message':'Welcome to the checkout manager service!', 'status':200})

#Verify the token in the header
def verify_token():
    return True

#Payment API
@app.route('/payment',methods=['POST'])
@cross_origin()
def payment():
    if verify_token:
        payment=request.json
        payment['payment_date']=datetime.datetime.now()
        paymentid=Payment.add_payment(payment)
        if paymentid:
            return jsonify({'message':'Payment successful!','payment_id':str(paymentid)}),200
        return jsonify({'message':'Payment failed!','status':400}),400

@app.route('/payment/<payment_id>',methods=['GET'])
@cross_origin()
def get_payment(payment_id):
    if verify_token:
        payment=Payment.get_payment(payment_id)
        if payment:
            return jsonify({'payment':payment,'status':200,'message':'Payment fetched!'}),200
        return jsonify({'message':'Payment not found!','status':404}),404

#cart API
@app.route('/cart',methods=['POST'])
@cross_origin()
def add_to_cart():
    if verify_token:
        cart=request.json
        cart['cart_date']=datetime.datetime.now()
        cartid=Cart.add_to_cart(cart)
        if cartid:
            return jsonify({'message':'Item added to cart!','cart_id':str(cartid)}),200
        return jsonify({'message':'Failed to add item to cart!','status':400}),400    

@app.route('/cart',methods=['GET'])
@cross_origin()
def get_cart():
    if verify_token:
        cart=Cart.get_cart()
        if not cart:
            return jsonify({'message':'Cart not found!','status':404}),404
        return jsonify({'message':'Cart fetched!','cart':cart,'status':200})

#delete all items from cart    
@app.route('/cart/<cartid>',methods=['DELETE'])
@cross_origin()
def clear_cart(cartid):
    if verify_token:
        Cart.clear_cart(cartid)
        return jsonify({'message':'Cart cleared!','status':200})        

#delete item from cart
@app.route('/cart',methods=['DELETE'])
@cross_origin()
def delete_item():
    request_data=request.json
    if verify_token:
        return jsonify({'message':'Item deleted from cart!','status':200})

#order API
@app.route('/orders',methods=['POST'])
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
    
@app.route('/order/<order_id>',methods=['PATCH'])
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