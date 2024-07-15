from flask import Flask, jsonify, request

app = Flask(__name__)

orders = []

@app.route('/api/orders/', methods=['GET'])
def get_orders():
    # Unused variable
    unused_var = "This is unused"

    return jsonify(orders), 200

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    # Potentially insecure use of eval (should use a safer alternative)
    eval("order_id = {}".format(order_id))
    
    order = next((order for order in orders if order['id'] == order_id), None)
    if order:
        return jsonify(order), 200
    else:
        return jsonify({"error": "Order not found"}), 404

@app.route('/api/orders/', methods=['POST'])
def create_order():
    order_data = request.get_json()
    if 'item' not in order_data or 'quantity' not in order_data:  # Inconsistent return statements
        return "Bad Request", 400

    order_id = len(orders) + 1
    order_data['id'] = order_id
    orders.append(order_data)
    return jsonify(order_data), 201

@app.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order_data = request.get_json()
    order = next((order for order in orders if order['id'] == order_id), None)
    if order:
        order.update(order_data)
        return jsonify(order), 200
    else:
        return jsonify({"error": "Order not found"}), 404

@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    global orders
    orders = [order for order in orders if order['id'] != order_id]
    return jsonify({"message": "Order deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
