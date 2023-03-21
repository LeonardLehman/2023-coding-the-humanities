# Define exchange rates as a dictionary
exch_rates = {
    ('USD', 'USD'): 1,
    ('USD', 'EUR'): 0.5,
    ('USD', 'AUD'): 1.45,
    ('USD', 'RU'): 0.75,
    ('EUR', 'USD'): 1.95,
    ('EUR', 'EUR'): 1,
    ('EUR', 'AUD'): 3.1,
    ('EUR', 'RU'): 1.49,
    ('AUD', 'USD'): 0.67,
    ('AUD', 'EUR'): 0.31,
    ('AUD', 'AUD'): 1,
    ('AUD', 'RU'): 0.48,
    ('RU', 'USD'): 1.34,
    ('RU', 'EUR'): 0.64,
    ('RU', 'AUD'): 1.98,
    ('RU', 'RU'): 1,
}

# Define a recursive function to find the maximum amount of USD that can be obtained within at most n steps
def max_usd(curr, n, visited):
    # Base case: if n = 0 or we have already visited the current currency, return 0
    if n == 0 or curr in visited:
        return 0
    
    # Mark the current currency as visited
    visited.add(curr)
    
    # Recursively try all possible conversions from the current currency and take the maximum
    max_amt = 0
    max_seq = []
    for next_curr, rate in exch_rates.items():
        if curr == next_curr[0]:
            amt = max_usd(next_curr[1], n-1, visited)
            if amt * rate > max_amt:
                max_amt = amt * rate
                max_seq = [(next_curr, amt)]
            elif amt * rate == max_amt:
                max_seq.append((next_curr, amt))
    
    # Unmark the current currency as visited
    visited.remove(curr)
    
    # Return the maximum amount and the corresponding sequence of steps
    return max_amt, max_seq

# Find the maximum amount of USD that can be obtained within at most 5 steps
max_amt, max_seq = max_usd('USD', 5, set())

# Print the maximum amount and the corresponding sequence of steps
print(f"Maximum amount of USD possible: {max_amt:.4f}")
if max_seq:
    print("Sequence of steps:")
    for step in max_seq:
        print(f"{step[1]:.4f} {step[0][0]} -> {step[1]*exch_rates[step[0]]:.4f} {step[0][1]}")
else:
    print("No sequence of steps found within 5 steps")
