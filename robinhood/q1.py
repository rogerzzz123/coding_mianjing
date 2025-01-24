# https://leetcode.com/discuss/interview-question/882324/Robinhood-or-Phone-Screen

# ## A trade is defined as a fixed-width string containing the 4 properties given below separated by commas:


# Symbol (4 alphabetical characters, left-padded by spaces)
# Type (either "B" or "S" for buy or sell)
# Quantity (4 digits, left-padded by zeros)
# ID (6 alphanumeric characters)
# e.g.
# "AAPL,B,0100,ABC123"


# which represents a trade of a buy of 100 shares of AAPL with ID "ABC123"


# Given two lists of trades - called "house" and "street" trades, write code to filter out groups of matches between trades and return a list of unmatched house and street trades sorted alphabetically. 
# There are many ways to match trades, the first and most important way is an exact match (Tests 1-5):


# An exact match is a house_trade+street_trade pair with identical symbol, type, quantity, and ID
# Note: Trades are distinct but not unique


# For example, given the following input:


# // house_trades:
# [
# "AAPL,B,0100,ABC123",
# "AAPL,B,0100,ABC123",
# "GOOG,S,0050,CDC333"
# ]


# // street_trades:
# [
# " FB,B,0100,GBGGGG",
# "AAPL,B,0100,ABC123"
# ]


# We would expect the following output:


# [
# " FB,B,0100,GBGGGG",
# "AAPL,B,0100,ABC123",
# "GOOG,S,0050,CDC333"
# ]
from collections import Counter
def unmatched_trades(house: list, street:list):
    house_count=Counter(house)
    street_count=Counter(street)

    for trade in list(house_count.keys()):
        if trade in street_count:
            num=min(house_count[trade], street_count[trade])
            house_count[trade]-=num
            street_count[trade]-=num
    
    res=[]
    for trade, count in house_count.items():
        if count>0:
            res.extend([trade]*count)
    for trade, count in street_count.items():
        if count>0:
            res.extend([trade]*count)
    return sorted(res)

# Example Input
house_trades = [
    "AAPL,B,0100,ABC123",
    "AAPL,B,0100,ABC123",
    "GOOG,S,0050,CDC333"
]
street_trades = [
    " FB,B,0100,GBGGGG",
    "AAPL,B,0100,ABC123"
]

# Example Output
print(unmatched_trades(house_trades, street_trades))

##Follow-up 1 (Test 6,7,8,9): 
# A "fuzzy" match is a house_trade+street_trade pair with identical symbol, type, and quantity ignoring ID. 
# Prioritize exact matches over fuzzy matches. Prioritize matching the earliest alphabetical house trade with the earliest alphabetical street trade in case of ties.
from collections import defaultdict
def unmatched_with_fuzzy(house, street):

    def fuzzy_key(trade):
        s,t,q,_=trade.split(",")
        return (s,t,q)
    
    h_count=Counter(house)
    s_count=Counter(street)

    # exact match
    for trade in list(h_count.keys()):
        if trade in s_count:
            num=min(h_count[trade], s_count[trade])
            h_count[trade]-=num
            s_count[trade]-=num
    
    h_remain=[]
    s_remain=[]
    for trade, count in h_count.items():
        if count>0:
            h_remain.extend([trade]*count)
    for trade, count in s_count.items():
        if count>0:
            s_remain.extend([trade]*count)

    # fuzzy match
    house_fuzzy = defaultdict(list)
    street_fuzzy = defaultdict(list)
    for trade in h_remain:
        house_fuzzy[fuzzy_key(trade)].append(trade)
    for trade in s_remain:
        street_fuzzy[fuzzy_key(trade)].append(trade)
    
    for fuzzy in list(house_fuzzy.keys()):
        if fuzzy in street_fuzzy:
            house_trades = sorted(house_fuzzy[fuzzy])  # Sort alphabetically
            street_trades = sorted(street_fuzzy[fuzzy])  # Sort alphabetically
            matched = min(len(house_trades), len(street_trades))
            # Remove matched trades
            house_fuzzy[fuzzy] = house_trades[matched:]
            street_fuzzy[fuzzy] = street_trades[matched:]
            if not house_fuzzy[fuzzy]:
                del house_fuzzy[fuzzy]
            if not street_fuzzy[fuzzy]:
                del street_fuzzy[fuzzy]
    unmatched = []
    for trades in house_fuzzy.values():
        unmatched.extend(trades)
    for trades in street_fuzzy.values():
        unmatched.extend(trades)

    # Sort the final result
    return sorted(unmatched)

house_trades = [
    "AAPL,B,0100,ABC123",
    "AAPL,B,0100,DEF456",
    "GOOG,S,0050,XYZ789"
]
street_trades = [
    "AAPL,B,0100,GHJ234",
    " FB,B,0100,GBGGGG",
    "GOOG,S,0050,XYZ789"
]

# Example Output
print(unmatched_with_fuzzy(house_trades, street_trades))


#Follow-up 2: (Test 10) An offsetting match is a house_trade+house_trade or street_trade+street_trade pair where the symbol and quantity of both trades are the same, but the type is different (one is a buy and one is a sell). 
# Prioritize exact and fuzzy matches over offsetting matches. Prioritize matching the earliest alphabetical buy with the earliest alphabetical sell.
from collections import defaultdict

def unmatched_trades_with_offsetting(house: list, street: list) -> list:
    # Helper function to extract fuzzy and offsetting keys
    def fuzzy_key(trade):
        symbol, trade_type, quantity, _ = trade.split(",")
        return (symbol, trade_type, quantity)
    
    def offsetting_key(trade):
        symbol, quantity = trade.split(",")[0], trade.split(",")[2]
        return (symbol, quantity)

    # Step 1: Exact matches
    house_count = defaultdict(int)
    street_count = defaultdict(int)
    for trade in house:
        house_count[trade] += 1
    for trade in street:
        street_count[trade] += 1

    # Remove exact matches
    for trade in list(house_count.keys()):
        if trade in street_count:
            matched = min(house_count[trade], street_count[trade])
            house_count[trade] -= matched
            street_count[trade] -= matched
            if house_count[trade] == 0:
                del house_count[trade]
            if street_count[trade] == 0:
                del street_count[trade]

    # Step 2: Fuzzy matches
    house_remaining = []
    street_remaining = []
    for trade, count in house_count.items():
        house_remaining.extend([trade] * count)
    for trade, count in street_count.items():
        street_remaining.extend([trade] * count)

    house_fuzzy = defaultdict(list)
    street_fuzzy = defaultdict(list)
    for trade in house_remaining:
        house_fuzzy[fuzzy_key(trade)].append(trade)
    for trade in street_remaining:
        street_fuzzy[fuzzy_key(trade)].append(trade)

    # Remove fuzzy matches
    for fuzzy in list(house_fuzzy.keys()):
        if fuzzy in street_fuzzy:
            house_trades = sorted(house_fuzzy[fuzzy])
            street_trades = sorted(street_fuzzy[fuzzy])
            matched = min(len(house_trades), len(street_trades))
            house_fuzzy[fuzzy] = house_trades[matched:]
            street_fuzzy[fuzzy] = street_trades[matched:]
            if not house_fuzzy[fuzzy]:
                del house_fuzzy[fuzzy]
            if not street_fuzzy[fuzzy]:
                del street_fuzzy[fuzzy]

    # Step 3: Offsetting matches
    # Combine house and street for offsetting matches
    house_remaining = []
    street_remaining = []
    for fuzzy, trade in house_fuzzy.items():
        for t in trade:
            house_remaining.append(t)
    for fuzzy, trade in street_fuzzy.items():
        for t in trade:
            street_remaining.append(t)
    print(house_remaining)
    print(street_remaining)
    combined_trades = defaultdict(list)
    for trade in house_remaining:
        combined_trades[offsetting_key(trade)].append(trade)
    for trade in street_remaining:
        combined_trades[offsetting_key(trade)].append(trade)
    print(combined_trades)

    unmatched = []
    print(list(combined_trades.keys()))
    for key in list(combined_trades.keys()):  # Use a copy of keys
        trades = combined_trades[key]

        buys = sorted([t for t in trades if t.split(",")[1] == "B"])
        sells = sorted([t for t in trades if t.split(",")[1] == "S"])
        print(buys)
        print(sells)
        matched = min(len(buys), len(sells))
        print(matched)
        # Collect unmatched trades after performing offsetting matches
        unmatched.extend(buys[matched:])
        unmatched.extend(sells[matched:])

    # Perform offsetting matches
    # for key in list(combined_trades.keys()):
    #     trades = combined_trades[key]
    #     print(trades)
    #     buys = sorted([t for t in trades if t.split(",")[1] == "B"])
    #     sells = sorted([t for t in trades if t.split(",")[1] == "S"])
    #     if len(buys)>0 and len(sells)>0:
    #         matched = min(len(buys), len(sells))
    #         combined_trades[key] = buys[matched:] + sells[matched:]
    #         if not combined_trades[key]:
    #             del combined_trades[key]
    # print(combined_trades)
    # # Step 4: Collect remaining unmatched trades
    # unmatched = []
    # # for trades in house_fuzzy.values():
    # #     unmatched.extend(trades)
    # # for trades in street_fuzzy.values():
    #     # unmatched.extend(trades)
    # for trades in combined_trades.values():
    #     for t in trades:
            # unmatched.append(trades)

    return sorted(unmatched)


house_trades = [
    "AAPL,B,0100,ABC123",
    "AAPL,B,0100,DEF456",
    "GOOG,S,0050,XYZ789",
    "MSFT,S,0020,MSFT123",
    "MSFT,B,0020,MSFT456"
]
street_trades = [
    "AAPL,B,0100,GHJ234",
    " FB,B,0100,GBGGGG",
    "GOOG,S,0050,XYZ789",
    "TSLA,S,0030,TSLA789",
    "TSLA,B,0030,TSLA456"
]

# Output
print(unmatched_trades_with_offsetting(house_trades, street_trades))