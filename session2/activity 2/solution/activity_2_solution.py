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
# WHAT IS NEW HERE: pandas. The preprocessing logic is the same.
# The key insight is: .apply(fn) runs your function on every row
# in one line of code — no manual loops needed.
#
# REQUIRES: pip install pandas
#           The file reviews.csv must be in the same folder as this script.
# =============================================================================

import pandas as pd


# =============================================================================
# PART A — Pipeline from Activity 1.4 (copy-pasted here for self-containment)
# =============================================================================

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

# TODO: Load reviews.csv using pandas.
# The file has two columns: "text" (the review) and "sentiment" (the label).

df = pd.read_csv("reviews.csv")

# STEP B1 — Inspect the dataset
print("=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)
print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Columns: {list(df.columns)}")
print()

# STEP B2 — Show the first 5 rows
print("First 5 rows:")
print(df.head())
print()

# STEP B3 — Count labels
print("Label distribution:")
print(df["sentiment"].value_counts())
print()

# STEP B4 — Check for missing values
print("Missing values per column:")
print(df.isnull().sum())
print()


# =============================================================================
# PART C — Apply the pipeline
# =============================================================================

# pandas tip: df["column"].apply(fn) calls fn(value) for every cell in "column"
# and returns a new Series with the results.

# STEP C1 — Apply pipeline to the "text" column
# TODO: Create a new column "tokens" by applying the pipeline function.

df["tokens"] = df["text"].apply(pipeline)

print("=" * 60)
print("AFTER APPLYING PIPELINE")
print("=" * 60)
print()

# STEP C2 — Inspect the first 5 rows of the new column
for idx, row in df.head(5).iterrows():
    print(f"[{row['sentiment']:8s}] {row['text'][:55]}...")
    print(f"           → {row['tokens']}")
    print()


# =============================================================================
# PART D — Analyse the results
# =============================================================================

# STEP D1 — How many tokens per review on average?
df["n_tokens"] = df["tokens"].apply(len)

print("=" * 60)
print("TOKEN STATISTICS")
print("=" * 60)
print(f"Mean tokens per review : {df['n_tokens'].mean():.1f}")
print(f"Min tokens             : {df['n_tokens'].min()}")
print(f"Max tokens             : {df['n_tokens'].max()}")
print()

# STEP D2 — Which review has the most tokens?
idx_max = df["n_tokens"].idxmax()
print("Longest review (after preprocessing):")
print(f"  Text  : {df.loc[idx_max, 'text']}")
print(f"  Tokens: {df.loc[idx_max, 'tokens']}")
print()

# STEP D3 — Most frequent tokens overall
from collections import Counter

all_tokens = [token for token_list in df["tokens"] for token in token_list]
top_20 = Counter(all_tokens).most_common(20)

print("Top 20 most frequent tokens:")
for token, count in top_20:
    print(f"  {token:20s} {count}")
print()


# =============================================================================
# PART E — Compare positive vs negative vocabulary
# =============================================================================

pos_tokens = [t for tl, s in zip(df["tokens"], df["sentiment"])
              for t in tl if s == "positive"]
neg_tokens = [t for tl, s in zip(df["tokens"], df["sentiment"])
              for t in tl if s == "negative"]

pos_freq = Counter(pos_tokens)
neg_freq = Counter(neg_tokens)

print("=" * 60)
print("TOP TOKENS BY SENTIMENT")
print("=" * 60)
print()
print("Most common in POSITIVE reviews:")
for token, count in pos_freq.most_common(10):
    print(f"  {token:20s} {count}")
print()
print("Most common in NEGATIVE reviews:")
for token, count in neg_freq.most_common(10):
    print(f"  {token:20s} {count}")
print()


# =============================================================================
# PART F — Reflection
# =============================================================================
# Look at the results above and answer:
#
# Q1. Are there tokens that appear in BOTH positive and negative top-10?
#     What does that tell you about their usefulness for classification?
#
# Q2. Do you see any emoticons in the top tokens? 
#     If you ran the pipeline with keep_emoticons=False, would the results
#     change significantly?
#
# Q3. Would you add any words to STOPWORDS after seeing the top tokens?
#     Be careful — would removing them lose sentiment information?
#
# Q4. At the end of this session, we have:
#     raw text → clean token lists ready to be converted to numbers.
#     What is the NEXT step? (Preview of Session 3)

print("=" * 60)
print("NEXT SESSION PREVIEW")
print("=" * 60)
print()
print("We now have clean token lists like:")
sample = df.loc[0, "tokens"]
print(f"  {sample}")
print()
print("Session 3 question: how do we turn this list into NUMBERS")
print("that a machine learning model can actually learn from?")
print()
print("→ Bag of Words  →  TF-IDF  →  Numeric representations")
