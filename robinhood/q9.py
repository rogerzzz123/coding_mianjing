"""
Given a stream of incoming "buy" and "sell" orders (as lists of limit price, quantity, and side, like
["155", "3", "buy"]), determine the total quantity (or number of "shares") executed.

A "buy" order can be executed if there is a corresponding "sell" order with a price that is less than or
equal to the price of the "buy" order.
Similarly, a "sell" order can be executed if there is a corresponding "buy" order with a price that is
greater than or equal to the price of the "sell" order.
It is possible that an order does not execute immediately if it isn't paired to a counterparty. In that 
case, you should keep track of that order and execute it at a later time when a pairing order is found.
You should ensure that orders are filled immediately at the best possible price. That is, an order 
should be executed when it is processed, if possible. Further, "buy" orders should execute at the 
lowest possible price and "sell" orders at the highest possible price at the time the order is handled.

Note that orders can be partially executed.

--- Sample Input ---

orders = [
  ['150', '5', 'buy'],    # Order A
  ['190', '1', 'sell'],   # Order B
  ['200', '1', 'sell'],   # Order C
  ['100', '9', 'buy'],    # Order D
  ['140', '8', 'sell'],   # Order E
  ['210', '4', 'buy'],    # Order F
]

Sample Output
9

[execution time limit] 3 seconds (java)

[input] array.array.string orders

[output] integer

[Java] Syntax Tips

// Prints help message to the console
// Returns a string
// 
// Globals declared here will cause a compilation error,
// declare variables inside the function instead!
Order Book

Buys: ['100', '9', 'buy']

Sells: , ['200', '1', 'sell']

Total Shares: 5 + 3 + 1 = 9
"""

def total_executed(orders):
    sell_heap=[]
    buy_heap=[]
    res=0

    for price, quantity, action in orders:
        price=int(price)
        quantity=int(quantity)
        if action =='buy':
            while sell_heap and quantity>0 and sell_heap[0][0]<=price:
                sell_price, sell_quantity=heapq.heappop(sell_heap)
                num_executed=min(quantity, sell_quantity)
                res+=num_executed
                quantity-=num_executed
                sell_quantity-=num_executed
                if sell_quantity>0:
                    heapq.heappush(sell_heap, sell_quantity)
            if quantity>0:
                heapq.heappush(buy_heap, (-price, quantity))
