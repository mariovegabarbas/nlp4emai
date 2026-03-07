# =============================================================================
# SESSION 2 · NLP Applied to Emotion Detection
# Activity 2 — Scaling Up: pandas Preprocessing Pipeline
# =============================================================================
#
# GOAL
# ----
# Apply the pipeline from Activity 1.4 to a real dataset using pandas.
# Load a CSV of reviews, process every row, inspect the results.
#
# WHAT IS NEW HERE: pandas.
# The preprocessing logic is the same as Activity 1.4.
# The key insight: .apply(fn) runs your function on every row
# in one line of code — no manual loops needed.
#
# REQUIRES: pip install pandas
#           reviews.csv must be in the same folder as this script.
# =============================================================================

import pandas as pd
from collections import Counter


# =============================================================================
# PART A — Pipeline from Activity 1.4
# =============================================================================
# Nothing to implement here — this is the pipeline you already built.
# Read through it and make sure you understand each function before continuing.

EMOTICONS = {":)", ":(", ":D", ":P", ";)", ":/", ":o", "XD", "<3",
             ":-)", ":-(", ":-D", ":-P"}

STOPWORDS = {
    "a", "an", "the",
    "in", "on", "at", "to", "for", "of", "with", "by", "from",
    "and", "but", "or", "so",
    "is", "are", "was", "were", "be", "been", "being",
    "do", "does", "did",
    "have", "has", "had",
    "will", "would", "could", "should",
    "i", "you", "he", "she", "it", "we", "they",
    "me", "him", "her", "us", "them",
    "my", "your", "his", "its", "our", "their",
    "this", "that", "these", "those",
    "just", "also", "very",
}
# NOTE: "not", "never", "no" are deliberately NOT in STOPWORDS.


def tokenise(text, keep_emoticons=True):
    tokens = []
    buffer = ""
    i = 0
    while i < len(text):
        if keep_emoticons:
            two_chars = text[i:i+2]
            if two_chars in EMOTICONS:
                if buffer.strip():
                    tokens.append(buffer.strip())
                    buffer = ""
                tokens.append(two_chars)
                i += 2
                continue
        char = text[i]
        if char == " ":
            if buffer.strip():
                tokens.append(buffer.strip())
            buffer = ""
        elif char.isalpha() or char.isdigit():
            buffer += char
        i += 1
    if buffer.strip():
        tokens.append(buffer.strip())
    return tokens


def pipeline(text, keep_emoticons=True, apply_stopwords=True, min_length=2):
    text = text.lower()
    tokens = tokenise(text, keep_emoticons=keep_emoticons)
    if apply_stopwords:
        tokens = [t for t in tokens if t not in STOPWORDS]
    tokens = [t for t in tokens if len(t) >= min_length or t in EMOTICONS]
    return tokens


# =============================================================================
# PART B — Load the dataset
# =============================================================================

# TODO 1: Load reviews.csv into a pandas DataFrame called `df`.
#         Hint: pd.read_csv("reviews.csv")
#         The file has two columns: "text" and "sentiment".

# YOUR CODE HERE
df = None  # replace with your code

# STEP B1 — Inspect the dataset
# TODO 2: Print the shape, column names, first 5 rows,
#         label distribution and missing value count.
#         Use: df.shape, df.columns, df.head(),
#              df["sentiment"].value_counts(), df.isnull().sum()

print("=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)

# YOUR CODE HERE


# =============================================================================
# PART C — Apply the pipeline
# =============================================================================
# pandas tip: df["column"].apply(fn) calls fn(value) for every cell
# and returns a new Series with the results. No loop needed.

# TODO 3: Create a new column "tokens" by applying the pipeline function
#         to the "text" column.
#         Hint: df["tokens"] = df["text"].apply(...)

# YOUR CODE HERE

print("=" * 60)
print("AFTER APPLYING PIPELINE")
print("=" * 60)

# TODO 4: Print the first 5 rows showing original text + token list.
#         Use df.head(5).iterrows() or df.head().apply(...).
#         Format: [sentiment]  text preview...
#                            → [token, list]

# YOUR CODE HERE


# =============================================================================
# PART D — Analyse the results
# =============================================================================

# TODO 5: Create a new column "n_tokens" with the number of tokens per review.
#         Hint: df["tokens"].apply(len)
#         Then print mean, min and max number of tokens.

# YOUR CODE HERE

print("=" * 60)
print("TOKEN STATISTICS")
print("=" * 60)

# YOUR CODE HERE (print mean / min / max)


# TODO 6: Find and print the review with the most tokens.
#         Hint: df["n_tokens"].idxmax()

# YOUR CODE HERE


# TODO 7: Count all tokens across the whole dataset and print the top 20.
#         Hint: flatten all token lists into a single list, then use Counter.
#         all_tokens = [token for token_list in df["tokens"] for token in token_list]

# YOUR CODE HERE

print("Top 20 most frequent tokens:")
# YOUR CODE HERE


# =============================================================================
# PART E — Compare positive vs negative vocabulary
# =============================================================================

# TODO 8: Collect all tokens from positive reviews into `pos_tokens`
#         and all tokens from negative reviews into `neg_tokens`.
#         Hint: zip(df["tokens"], df["sentiment"])
#         Then use Counter to find the top 10 for each.

# YOUR CODE HERE

print("=" * 60)
print("TOP TOKENS BY SENTIMENT")
print("=" * 60)

# YOUR CODE HERE (print top 10 positive and top 10 negative)


# =============================================================================
# PART F — Reflection
# =============================================================================
# Look at the output above and answer these questions in the comments:
#
# Q1. Are there tokens in BOTH positive and negative top-10?
#     What does that tell you about their usefulness for classification?
#
# Q2. Do you see any emoticons in the top tokens?
#     If you ran the pipeline with keep_emoticons=False,
#     would the results change significantly?
#
# Q3. Would you add any words to STOPWORDS after seeing the top tokens?
#     Be careful — would removing them lose sentiment information?
#
# Q4. At the end of this session we have:
#     raw text → clean token lists, ready to be converted to numbers.
#     What is the NEXT step? (Preview of Session 3)
#
# YOUR ANSWERS HERE:
#
# Q1:
# Q2:
# Q3:
# Q4:

print("=" * 60)
print("NEXT SESSION PREVIEW")
print("=" * 60)
print()
print("We now have clean token lists like:")
print(f"  {df.loc[0, 'tokens']}")
print()
print("Session 3 question: how do we turn this list into NUMBERS")
print("that a machine learning model can actually learn from?")
print()
print("→ Bag of Words  →  TF-IDF  →  Numeric representations")
