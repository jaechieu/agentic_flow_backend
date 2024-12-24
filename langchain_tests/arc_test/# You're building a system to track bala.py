# You're building a system to track balances for the OpenAI API credit purchasing system. 
# API users can purchase credit grants, specified by an ID, that are active at a timestamp and that let them use the API.
# Unused credit grant balances expire at a certain time.
# However, there's a kink in our system: requests can arrive out of order because our system is built on a really unstable network. 
# For example, a request to subtract credits can arrive at the system before the request to add credits, even though the request to add credits has a lower timestamp.

# Your task is to implement the Credits class, which should support the following operations:
# - Granting credits, subtracting credits, and getting the credit balance for a user
# - The ability to handle requests that arrive out of order
# - Showing users their balance at a certain time in the past (for audit purposes)

# Some guidelines/hints:
# - Do NOT worry about memory or performance concerns. Write simple, working code. No fancy data structures are needed here.
# - All timestamps can be represented as ints for simplicity and are unique (no two actions will happen at the same timestamp).
# - Subtract from grants expiring soonest first.
# - Hint: Because requests are out of order, you may not want to do computation at the time of a request. You'll need to store the request and then do the computation when you get a request to get the balance.
# - You will need to subtract from multiple grants: ex. if you have two grants of 2 credits each, and you subtract 3 credits, you should subtract 2 from one grant and 1 from the other.
# - The balance is guaranteed to reconcile eventually (i.e. if you subtract more credits than a user has, they will eventually get a grant that will bring their balance back to positive). You can assume that the balance will never go negative.
# - You can assume that the expiration timestamp is always greater than the timestamp of the grant.

# Here's an example class that you'll want to fill in:

"""
from typing import NamedTuple

class ANamedTuple(NamedTuple):
    ""a docstring""
    foo: int
    bar: str
    baz: list

ant = ANamedTuple(1, 'bar', [])
"""

from typing import NamedTuple

class Grant(NamedTuple):
    amount: int
    timestamp: int
    expiration_timestamp: int

class Subtraction(NamedTuple):
    amount: int
    timestamp: int

class Credits:
    def __init__(self):
        self.grants = []
        self.subtracts = []

    def create_grant(self, grant_id: str, amount: int, expiration_timestamp: int, timestamp: int) -> None:
        self.grants.append(Grant(amount, timestamp, expiration_timestamp))
    
    def subtract(self, amount: int, timestamp: int) -> None:
        self.subtracts.append(Subtraction(amount, timestamp))

    def get_balance(self, timestamp: int) -> int:
        grant_start_timestamps = [(grant.timestamp, "1start", grant) for grant in self.grants]
        grant_end_timestamp = [(grant.expiration_timestamp, "2end", grant) for grant in self.grants]
        subtract_timestamps = [(subtract.timestamp, "3subtract", subtract) for subtract in self.subtracts]
        return_timestamp = [(timestamp, "4get_balance")]

        all_events = sorted(grant_start_timestamps + grant_end_timestamp + subtract_timestamps + return_timestamp)

        open_grants = []
        balance = 0
        for event in all_events:
            if event[1] == "1start":
                grant = event[2]
                open_grants.append((grant, grant.amount))
                balance += grant.amount
            elif event[1] == "2end":
                grant = event[2]
                for i in range(len(open_grants)):
                    if open_grants[i][0] == grant:
                        balance -= open_grants.pop(i)[1]
                        break
            elif event[1] == "3subtract":
                subtract = event[2]
                amount_to_subtract = subtract.amount
                while amount_to_subtract:
                    min_grant_by_expiration_date_index = 0
                    min_grant_by_expiration_date = open_grants[0][0]
                    min_grant_by_expiration_date_amount = open_grants[0][1]
                    for i in range(1, len(open_grants)):
                        if open_grants[i][0].expiration_timestamp < min_grant_by_expiration_date.expiration_timestamp:
                            min_grant_by_expiration_date = open_grants[i][0]
                            min_grant_by_expiration_date_index = i
                            min_grant_by_expiration_date_amount = open_grants[i][1]

                    amount_this_grant_can_cover = min(amount_to_subtract, open_grants[min_grant_by_expiration_date_index][1])
                    if amount_this_grant_can_cover == min_grant_by_expiration_date.amount:
                        open_grants.pop(min_grant_by_expiration_date_index)
                    else:
                        open_grants[min_grant_by_expiration_date_index] = (min_grant_by_expiration_date, min_grant_by_expiration_date_amount - amount_this_grant_can_cover)
                    amount_to_subtract -= amount_this_grant_can_cover
                    balance -= amount_this_grant_can_cover
            elif event[1] == "4get_balance":
                return balance
            else:
                raise Exception("Unreachable")

# Make sure you understand these test cases in detail before writing any code.
# Test case 1 - basic subtraction

credits = Credits()
credits.subtract(amount=1, timestamp=30)
credits.create_grant(grant_id="a", amount=1, timestamp=10, expiration_timestamp=100)
assert credits.get_balance(timestamp=10) == 1
assert credits.get_balance(timestamp=30) == 0
assert credits.get_balance(timestamp=20) == 1

# Explanation
# 10: 1 (a)
# 20: 1 (a)
# 30: 0 (a -1)

# Test case 2 - expiration

credits = Credits()
credits.subtract(amount=1, timestamp=30)
credits.create_grant(grant_id="a", amount=2, timestamp=10, expiration_timestamp=100)
assert credits.get_balance(timestamp=10) == 2
assert credits.get_balance(timestamp=20) == 2
assert credits.get_balance(timestamp=30) == 1
assert credits.get_balance(timestamp=100) == 0

# Explanation
# 10: 2 (a)
# 20: 2 (a)
# 30: 1 (a -1)
# 100: 0 (the remainder of a expired)

# Test case 3 - subtracting from soonest expiring grants first
credits = Credits()
credits.create_grant(grant_id="a", amount=3, timestamp=10, expiration_timestamp=60)
assert credits.get_balance(10) == 3
credits.create_grant(grant_id="b", amount=2, timestamp=20, expiration_timestamp=40)
credits.subtract(amount=1, timestamp=30)
credits.subtract(amount=3, timestamp=50)
assert credits.get_balance(10) == 3
assert credits.get_balance(20) == 5
assert credits.get_balance(30) == 4
assert credits.get_balance(40) == 3
assert credits.get_balance(50) == 0

# Explanation
# 10: 3 (a)
# 20: 5 (a=3, b=2)
# 30: 4 (subtract 1 from b, so b=1), since it expires first, a=3
# 40: 3 (b expired)
# 50: 0 (subtract 3 from a)

# Test case 4 - subtract from many grants
credits = Credits()
credits.create_grant(grant_id="a", amount=3, timestamp=10, expiration_timestamp=60)
credits.create_grant(grant_id="b", amount=2, timestamp=20, expiration_timestamp=80)
credits.subtract(amount=4, timestamp=30)
assert credits.get_balance(10) == 3
assert credits.get_balance(20) == 5
assert credits.get_balance(30) == 1
assert credits.get_balance(70) == 1

# Explanation
# 10: 3 (a)
# 20: 5 (a=3, b=2)
# 30: 1 (subtract 3 from a, 1 from b)
# 70: 1 (a expired, b=1)