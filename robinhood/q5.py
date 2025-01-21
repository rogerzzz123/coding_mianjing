"""
Our goal is to build a simplified version of a real Robinhood system that reads prices from a stream and aggregates those prices into historical datapoints aka candlestick charts. We’re looking for clean code, good naming, testing, etc.


Step 1: Parse Prices


Your input will be a comma-separated string of prices and timestamps in the format price:timestamp e.g.


1:0,3:10,2:12,4:19,5:35 is equivalent to


price: 1, timestamp: 0
price: 3, timestamp: 10
price: 2, timestamp: 12
price: 4, timestamp: 19
price: 5, timestamp: 35


You can assume the input is sorted by timestamp and values are non-negative integers.


Step 2: Aggregate Historical Data from Prices


We calculate historical data across fixed time intervals. In this case, we’re interested in intervals of 10, so the first interval will be [0, 10). For each interval, you’ll build a datapoint with the following values.


Start time
First price
Last price
Max price
Min price


Important: If an interval has no prices, use the previous datapoint’s last price for all prices. If there are no prices and no previous datapoints, skip the interval.


You should return a string formatted as {start,first,last,max,min}. For the prices shown above, the expected datapoints are


{0,1,1,1,1}{10,3,4,4,2}{20,4,4,4,4}{30,5,5,5,5}


[execution time limit] 3 seconds (cs)


[input] string prices_to_parse


[output] string


[C#] Syntax Tips


// Prints help message to the console
// Returns a string
string helloWorld(string name) {
Console.Write("This prints to the console when you Run Tests");
return "Hello, " + name;
}


C#
Mono v6.12.0.122
14151611121391067845
}
else
{
if (i > 0 && list[i-1] != null)
{
AggregatePrice aggPrice = new AggregatePrice(list[i-1].lastPrice, i10);
str.Append("{");
str.Append(GetAggregatedPrice(i10, aggPrice));
str.Append("}");
}


TESTS
CUSTOM TESTS
RESULTS
Tests passed: 0/3. Compilation error.
Test 1
Input:
prices_to_parse: "1:0,2:1,3:2,4:3,5:4,6:5,7:6,8:7,9:8,10:9,11:10,12:11,13:12,14:13,15:14,16:15,17:16,18:17,19:18,20:19"
Output:
undefined
Expected Output:
"{0,1,10,10,1}{10,11,20,20,11}"
Console Output:
Empty
Test 2
Test 3

"""

def aggregated_price(prices_input):
    prices=[]
    for entry in prices_input.split(","):
        price, ts=map(int, entry.split(':'))
        prices.append((price, ts))
    
    res=[]
    interval_size=10
    curr=0
    i=0
    n=len(prices)
    prev_price=None

    while i<n or (prev_price is not None and curr <= prices[-1][1]):
        interval_price=[]
        while i<n and prices[i][1]<curr+interval_size:
            interval_price.append(prices[i][0])
            i+=1
        
        if interval_price:
            first_price=interval_price[0]
            last_price=interval_price[-1]
            max_price=max(interval_price)
            min_price=min(interval_price)
            prev_price=last_price
        
        elif prev_price is not None:
            first_price=last_price=max_price=min_price=prev_price
        else:
            curr+=interval_size
            continue

        res.append(f"{{{curr},{first_price},{last_price},{max_price},{min_price}}}")
        curr+=interval_size
    
    return ''.join(res)

prices_to_parse = "1:0,3:10,2:12,4:19,5:35"
# print(prices_to_parse)
op=aggregated_price(prices_to_parse)
print(op)
