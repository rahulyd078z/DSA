def keyword_sentences(user_query, marketing_keywords_dictionary):
    word_set = set(marketing_keywords_dictionary)
    memo = {}

    def dfs(start):
        # If already computed, return stored result
        if start in memo:
            return memo[start]

        # If reached end of string, one valid sentence (empty tail)
        if start == len(user_query):
            return [""]

        sentences = []

        for end in range(start + 1, len(user_query) + 1):
            word = user_query[start:end]

            if word in word_set:
                # Getting sentences for remaining string
                for tail in dfs(end):
                    if tail:
                        sentences.append(word + " " + tail)
                    else:
                        sentences.append(word)

        memo[start] = sentences
        return sentences

    return dfs(0)


user_query = "climbingtonv5"
marketing_keywords_dictionary = ["climbing", "ton", "v5"]

result = keyword_sentences(user_query, marketing_keywords_dictionary)
print(result)
