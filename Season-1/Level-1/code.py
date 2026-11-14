'''
Welcome to Secure Code Game Season-1/Level-1!

Follow the instructions below to get started:

1. tests.py is passing but code.py is vulnerable
2. Review the code. Can you spot the bug?
3. Fix the code but ensure that tests.py passes
4. Run hack.py and if passing then CONGRATS!
5. If stuck then read the hint
6. Compare your solution with solution.py
'''

from collections import namedtuple
from decimal import Decimal

Order = namedtuple('Order', 'id, items')
Item = namedtuple('Item', 'type, description, amount, quantity')

# Upper bound for the total value of the products in a single order
MAX_ORDER_TOTAL = Decimal('1e6')

def validorder(order: Order):
    # Decimal gives exact arithmetic: no float rounding (1.1 + 2.2 != 3.3)
    # and no precision loss on huge values (1e19 - 1000 - 1e19 == 0).
    # str() first so a float like 1.1 is not converted with its binary error.
    net = Decimal('0')
    products_total = Decimal('0')

    for item in order.items:
        if item.type == 'payment':
            net += Decimal(str(item.amount))
        elif item.type == 'product':
            cost = Decimal(str(item.amount)) * Decimal(str(item.quantity))
            products_total += cost
            net -= cost
            # Limit the order size regardless of the item/payment order
            if abs(products_total) > MAX_ORDER_TOTAL:
                return 'Total amount payable for an order exceeded'
        else:
            return "Invalid item type: %s" % item.type

    if net != 0:
        return "Order ID: %s - Payment imbalance: $%0.2f" % (order.id, net)
    else:
        return "Order ID: %s - Full payment received!" % order.id
