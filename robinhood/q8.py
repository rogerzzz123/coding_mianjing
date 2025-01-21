"""
https://leetcode.com/discuss/interview-question/5047205/Robinhood-Phonescreen-or-L4

Robinhood is famous for its referral program. It’s exciting to see our users spreading the word across their friends and family. One thing that is interesting about the program is the network effect it creates. We would like to build a dashboard to track the status of the program. Specifically, we would like to learn about how people refer others through the chain of referral.


For the purpose of this question, we consider that a person refers all other people down the referral chain. For example, A refers B, C, and D in a referral chain of A -> B -> C -> D. Please build a leaderboard for the top 3 users who have the most referred users along with the referral count.


Referral rules:


A user can only be referred once.
Once the user is on the RH platform, he/she cannot be referred by other users. For example: if A refers B, no other user can refer A or B since both of them are on the RH platform.
Referrals in the input will appear in the order they were made.
Leaderboard rules:


The user must have at least 1 referral count to be on the leaderboard.
The leaderboard contains at most 3 users.
The list should be sorted by the referral count in descending order.
If there are users with the same referral count, break the ties by the alphabetical order of the user name.
Input


rh_users = ["A", "B", "C"]
| | |
v v v
new_users = ["B", "C", "D"]
Output


["A 3", "B 2", "C 1"]
[execution time limit] 3 seconds (java)


[memory limit] 1 GB


[input] array.string rh_users


A list of referring users.


[input] array.string new_users


A list of user that was referred by the users in the referrers array with the same order.


[output] array.string


An array of 3 users on the leaderboard. Each of the element here would have the "[user] [referral count]" format. For example, "A 4".

"""

from collections import defaultdict
def leaderboard(rh_users, new_users):
    graph=defaultdict(list)
    users=set()
    for rh, new in zip(rh_users, new_users):
        graph[rh].append(new)
        users.add(rh)
        users.add(new)
    
    ref_count={}
    def dfs(node):
        if node in ref_count:
            return ref_count[node]
        count=0
        for nei in graph[node]:
            count=count+1+dfs(nei)
        ref_count[node]=count
        return count
    for user in users:
        if user not in ref_count:
            dfs(user)
    res=[(user, count) for user, count in ref_count.items()]
    res.sort(key=lambda x: (-x[1], x[0]))

    return [f"{user} {count}" for user, count in res[:3]]

rh_users = ["A", "B", "C"]
new_users = ["B", "C", "D"]

# Example Output
print(leaderboard(rh_users, new_users))  # Output: ["A 3", "B 2", "C 1"]