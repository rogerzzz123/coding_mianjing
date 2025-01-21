"""
https://www.1point3acres.com/bbs/thread-1076537-1-1.html

Portfolio Value Optimization
You have some securities available to buy that each has a price Pi.
Your friend predicts for each security the stock price will be Si at some future date.
But based on volatility of each share, you only want to buy up to Ai shares of each security i.
Given M dollars to spend, calculate the maximum value you could potentially
achieve based on the predicted prices Si (and including any cash you have remaining).

Pi = Current Price
Si = Expected Future Price
Ai = Maximum units you are willing to purchase
M = Dollars available to invest
Example 1:
Input:
M = $140 available
N = 4 Securities
P1=15, S1=45, A1=3 (AAPL)
P2=40, S2=50, A2=3 (BYND)
P3=25, S3=35, A3=3 (SNAP)
P4=30, S4=25, A4=4 (TSLA)

Output: $265 (no cash remaining) 
3 shares of apple -> 45(15 *3), 135(45 *3)
3 shares of snap -> 75, 105
0.5 share of bynd -> 20, 25
"""
def pvo(M,securities):
    ratios=[]
    for price, future_price, max_shares in securities:
        ratios.append((future_price/price, price, future_price, max_shares))
    
    ratios.sort(reverse=True, key=lambda x: x[0])
    res=0
    for r, p, fp, max_shares in ratios:
        max_cost=p*max_shares
        if max_cost<=M:
            res+=fp*max_shares
            M-=max_cost
        else:
            res+=fp * (M/p)
            M=0
            break
    
    return res

M = 140
securities = [
    (15, 45, 3),  # AAPL
    (40, 50, 3),  # BYND
    (25, 35, 3),  # SNAP
    (30, 25, 4)   # TSLA
]
print(pvo(M, securities)) 

