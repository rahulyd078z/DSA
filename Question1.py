from collections import defaultdict
from math import gcd

def max_points_on_line(points):
    # Function to compute reduced slope between two points
    def get_slope(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

       
        if dx == 0:
            return ('inf', 0)

        # horizontal line normalization
        if dy == 0:
            return (0, 1)

        g = gcd(dy, dx)
        dy //= g
        dx //= g

        # keep dx positive 
        if dx < 0:
            dx *= -1
            dy *= -1

        return (dy, dx)

    n = len(points)
    if n <= 2:
        return n

    max_points = 0

    for i in range(n):
        slopes = defaultdict(int)
        duplicates = 1

        for j in range(n):
            if i == j:
                continue
            if points[i] == points[j]:
                duplicates += 1
            else:
                slope = get_slope(points[i], points[j])
                slopes[slope] += 1

        current_max = duplicates
        if slopes:
            current_max = duplicates + max(slopes.values())

        max_points = max(max_points, current_max)

    return max_points


# Test case 1
customer_locations = [[1,1], [2,2], [3,3]]
print(max_points_on_line(customer_locations))  # Output: 3

#Test case 2
customer_locations = [[1,1], [3,2], [5,3], [4,1], [2,3], [1,4]]
print(max_points_on_line(customer_locations))  # Output: 4
