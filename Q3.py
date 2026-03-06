def max_profit(max_trades, daily_prices):
    if not daily_prices:
        return 0 # No price to display profit
    
    n = len(daily_prices)
    dp = [[0] * n for _ in range(max_trades + 1)] #DP table

    for k in range(1, max_trades + 1):
        max_diff = -daily_prices[0] #Tracking max difference for profit calculation
        for i in range(1, n):
            dp[k][i] = max(dp[k][i-1], daily_prices[i] + max_diff) #Skip or sell
            max_diff = max(max_diff, dp[k-1][i] - daily_prices[i]) #Update max_diff for next iteration

    return dp[max_trades][n-1]
        
print(max_profit(2, [4000, 3000, 5000, 6000, 2000]))  
