import random
import time
import threading

# Constant
NUM_TICKERS = 1024

class Order:
    def __init__(self, order_type, ticker, quantity, price):
        self.order_type = order_type
        self.ticker = ticker
        self.quantity = quantity
        self.price = price
        self.next = None

class StockEngine:
    def __init__(self):
        self.buy_orders = OrderLList()
        self.sell_orders = OrderLList()

    def add_order(self, order_type, ticker, quantity, price):
        stock_order = Order(order_type, ticker, quantity, price)
        with self.lock:
            if stock_order.order_type == "Buy":
                self.buy_orders.add_order(stock_order)
            else:
                self.sell_orders.add_order(stock_order)

    def match_order(self):
        with self.lock:
            while self.buy_orders.head() and self.sell_orders.head():
                buy_ord = self.buy_orders.head()
                sell_ord = self.sell_orders.head()

                if buy_ord.price >= sell_ord.price:
                    matched_quantity = min(buy_ord.quantity, sell_ord.quantity)
                    print(f"Order completed: {matched_quantity} shares of {buy_ord.ticker} at ${sell_ord.price}")

                    buy_ord.quantity -= matched_quantity
                    if buy_ord.quantity == 0:
                        self.buy_ord.remove_order()

                    sell_ord.quantity -= matched_quantity
                    if sell_ord.quantity == 0:
                        self.sell_ord.remove_order()
                else:
                    break

class OrderLList:
        def __init__(self):
            self.head = None

        def add_order(self, order):
            if not self.head:
                self.head = order
                order.next = None
            if (order.order_type == "Buy" and order.price > self.head.price) or (order.order_type == "Sell" and order.price < self.head.price):
                order.next = self.head
                self.head = order
            else:
                curr_head = self.head
                while curr_head.next and order.order_type == "Buy" and order.price <= curr_head.next.price:
                    curr_head = curr_head.next
                while curr_head.next and order.order_type == "sell" and order.price >= curr_head.next.price:
                    curr_head = curr_head.next
                order.next = curr_head.next
                curr_head.next = order

        def remove_order(self):
            if not self.head:
                return None
            order = self.head
            self.head = self.head.next
            return order
        
        def head(self):
            return self.head

def random_simulation(stock_engine, num_transactions=100):
    for _ in range(num_transactions):
        order_type = random.choice(["Buy", "Sell"])
        ticker = random.randint(0, NUM_TICKERS - 1)
        quantity = random.randint(1, 100)
        price = random.randint(1, 500)
        stock_engine.add_order(order_type, ticker, quantity, price)
        time.sleep(random.uniform(0.1, 1))

if __name__ == "__main__":
    stock_engine = StockEngine()
    simulation_thread = threading.Thread(target=random_simulation, args=(stock_engine,))
    simulation_thread.start()
    simulation_thread.join()
    


"""
Notes

Goal: real-time stock trading engine
function: matches stock buys to stock sells

- Two functions:
AddOrder and MatchOrder

AddOrder
- Takes order type (buy or sell), ticker symbol (ex. AAPL), quantity(10, 100, etc), price (int)
- Support 1024 unique stocks/tickets
- Need to write wrapper around it to randomly execute with different parameter values

MatchOrder
- Matches buy and sell orders
- Condition: Buy price for ticker >= lowest sell price available

Requirements:
- Handle race conditions when multiple threads modify stock order book
- Use lock-free data structures

- Do not use any dictionaries or maps or equivalents

- Match order time complexity should be O(N)

Design
- We want to keep track of the lowest available sell price
- We also want to keep track of the highest available buy price and match these together to reach best market price
- We may be dealing with a lot of insertions and deletions, which would favor a linked list structure
"""
