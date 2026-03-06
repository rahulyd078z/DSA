class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def max_path_sum(root):
    max_sum = float('-inf')  # Initialize global max

    def dfs(node):
        nonlocal max_sum
        if not node:
            return 0  # Base case

        left_gain = max(dfs(node.left), 0)   # Max from left, ignore if negative
        right_gain = max(dfs(node.right), 0) # Max from right, ignore if negative

        current_sum = node.val + left_gain + right_gain  # Path through current node
        max_sum = max(max_sum, current_sum)              # Update global max

        return node.val + max(left_gain, right_gain)     # Return max extending path

    dfs(root)
    return max_sum


# Test Case 1
root1 = TreeNode(1)
root1.left = TreeNode(2)
root1.right = TreeNode(3)
result1 = max_path_sum(root1)
print("Test 1:", result1)  


# Test Case 2
root2 = TreeNode(-10)
root2.left = TreeNode(9)
root2.right = TreeNode(20)
root2.right.left = TreeNode(15)
root2.right.right = TreeNode(7)
result2 = max_path_sum(root2)
print("Test 2:", result2)  
