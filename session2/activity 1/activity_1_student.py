# =============================================================================
# SESSION 2 · NLP Applied to Emotion Detection
# Activity 1 — From Raw Text to Tokens
# =============================================================================
#
# This activity is structured in four progressive steps:
#
#   1.1  Text as strings          → lowercase + remove punctuation
#   1.2  Naive tokenisation       → split(), discover its limits
#   1.3  Character-by-char        → full control, emoticon-aware
#   1.4  Complete pipeline        → integrate everything
#
# RULES
# -----
#   - No NLP libraries allowed (no nltk, no spaCy, no transformers).
#   - Only Python built-ins: str methods, lists, loops, dicts.
#   - Every TODO must be completed before moving to the next step.
#   - Think before you code — read the DISCUSSION questions.
# =============================================================================


# =============================================================================
# ACTIVITY 1.1 — Text as Strings: Your First Preprocessing Steps
# =============================================================================
#
# GOAL: Understand that text is just a sequence of characters.
#       Learn to manipulate strings in Python without any NLP library.


# -----------------------------------------------------------------------------
# STEP 1 — Define your sentence
# -----------------------------------------------------------------------------

sentence = "The Battery life on this Phone is AMAZING... it lasts 2 full days! :)"

print("Original sentence:")
print(sentence)
print()


# -----------------------------------------------------------------------------
# STEP 2 — Convert to lowercase
# -----------------------------------------------------------------------------
# Why? "Battery" and "battery" are the same word.
# Mixing cases doubles vocabulary size for no benefit.
#
# TODO 1: Apply .lower() to `sentence` and store the result in `lower_sentence`.
#         Then print it.

# YOUR CODE HERE
lower_sentence = None  # replace with your code

print("Lowercase:")
print(lower_sentence)
print()


# -----------------------------------------------------------------------------
# STEP 3 — Remove basic punctuation
# -----------------------------------------------------------------------------
# We want to keep only letters, digits and spaces.
#
# TODO 2: Complete the loop below. Add a character to `clean_chars` only if it
#         is a letter, a digit, or a space.
#         Hint: use char.isalpha(), char.isdigit(), char == " "
#
#         After running: what happens to ":)"? Is that a problem?

clean_chars = []

for char in lower_sentence:
    pass  # YOUR CODE HERE — replace `pass` with the condition

clean_sentence = "".join(clean_chars)

print("After removing punctuation:")
print(clean_sentence)
print()

print("=" * 60)
print("BEFORE:", sentence)
print("AFTER: ", clean_sentence)
print("=" * 60)
print()

# DISCUSSION — think about these before moving on:
#
# Q1. What information was lost when we removed punctuation?
#     (Hint: look at ":)" and "...")
#
# Q2. In a sentiment analysis task, does removing "!" matter?
#     What about removing "2"?
#
# Q3. We kept digits. Can you think of a sentence where removing digits
#     would change the sentiment?
#     Example: "1-star battery" vs "5-star battery"
#
# Q4. The sentence now has extra spaces where punctuation was.
#     Does that matter for the next step (tokenisation)?


# -----------------------------------------------------------------------------
# BONUS 1.1 — Wrap the cleaning logic in a function
# -----------------------------------------------------------------------------
# TODO 3: Write a function clean_text(text) that applies steps 2 and 3 above
#         to any input string and returns the cleaned version.
#         Test it on the three sentences below.

def clean_text(text):
    """
    Converts text to lowercase and removes all characters
    that are not letters, digits, or spaces.
    """
    # YOUR CODE HERE
    pass


test_sentences = [
    "I LOVE this! Best product ever.",
    "Terrible... absolutely terrible. 0/10.",
    "Not bad :) would buy again!",
]

print("Testing clean_text():")
for s in test_sentences:
    print(f"  IN : {s}")
    print(f"  OUT: {clean_text(s)}")
    print()


# =============================================================================
# ACTIVITY 1.2 — Tokenisation: The Naive Approach
# =============================================================================
#
# GOAL: Split text into tokens using .split().
#       Discover WHY naive tokenisation fails and what it tells us
#       about the relationship between cleaning and tokenisation.
#
# PREREQUISITE: clean_text() must be working before continuing.


# -----------------------------------------------------------------------------
# STEP 1 — Tokenise BEFORE cleaning
# -----------------------------------------------------------------------------
# TODO 4: Split `raw_sentence` into tokens using .split(" ")
#         and store the result in `raw_tokens`. Print the list.

raw_sentence = "I love NLP... and Python! It's amazing :)"

# YOUR CODE HERE
raw_tokens = None  # replace with your code

print("Raw sentence:", raw_sentence)
print("Tokens (no cleaning):", raw_tokens)
print()

# OBSERVE:
#   - "NLP..."   → the word is glued to the punctuation
#   - "Python!"  → exclamation attached to the word
#   - "It's"     → apostrophe inside the token
#   - ":)"       → emoticon becomes a "word"
#
# QUESTION: Which of these are problems? Which might be useful to keep?


# -----------------------------------------------------------------------------
# STEP 2 — Tokenise AFTER cleaning
# -----------------------------------------------------------------------------
# TODO 5: Apply clean_text() to `raw_sentence`, then split on spaces.
#         Store the result in `clean_tokens`. Print and compare.

# YOUR CODE HERE
clean_tokens = None  # replace with your code

print("Tokens (after cleaning):", clean_tokens)
print()

# OBSERVE: the tokens are cleaner — but something is MISSING.
# What happened to ":)"? What happened to "..."?
# Is that acceptable for emotion detection?


# -----------------------------------------------------------------------------
# STEP 3 — Handle multiple spaces
# -----------------------------------------------------------------------------
# After removing punctuation, some words have double spaces between them.
# .split(" ") keeps empty strings as tokens!
# .split() (no argument) splits on ANY whitespace and ignores extras.
#
# TODO 6: Run both versions and compare.

tokens_single_space = clean_text(raw_sentence).split(" ")
tokens_any_space    = clean_text(raw_sentence).split()

print('split(" ") →', tokens_single_space)
print("split()    →", tokens_any_space)
print()

# QUESTION: Which is better? Why?


# -----------------------------------------------------------------------------
# STEP 4 — Test with more sentences
# -----------------------------------------------------------------------------
test_sentences_12 = [
    "Best. Product. Ever.",
    "I can't believe how bad this is!!!",
    "5-star experience, would recommend :)",
    "not bad, not great... just meh",
]

print("Tokenisation test:")
print("-" * 50)
for s in test_sentences_12:
    tokens = clean_text(s).split()
    print(f"Input : {s}")
    print(f"Tokens: {tokens}")
    print()

# FINAL QUESTION:
# Are there cases where cleaning before tokenising loses important
# information for SENTIMENT analysis?
#
# YOUR ANSWER HERE (as a comment):
#


# =============================================================================
# ACTIVITY 1.3 — Tokenisation: Character by Character
# =============================================================================
#
# GOAL: Build a tokeniser from scratch, character by character.
#       This gives us full control over what counts as a token —
#       including emoticons like ":)" that carry emotional information.
#
# KEY INSIGHT: a tokeniser is a state machine.
#   - we accumulate characters into a "buffer"
#   - when we hit a separator, we save the buffer as a token and reset
#   - we decide EXPLICITLY what separates tokens and what stays together


# -----------------------------------------------------------------------------
# STEP 1 — Basic character-by-character tokeniser
# -----------------------------------------------------------------------------
# TODO 7: Complete the function tokenise_basic(text).
# Rules:
#   - Iterate character by character over text.lower()
#   - If the character is a letter or digit → add it to buffer
#   - If the character is a space → save buffer as token (if not empty), reset
#   - At the end of the string → save the last buffer if not empty
#   - Anything else (punctuation) is silently dropped

def tokenise_basic(text):
    """
    Tokenises text character by character, splitting on spaces.
    Removes standalone punctuation.
    """
    tokens = []
    buffer = ""

    for char in text.lower():
        # YOUR CODE HERE
        pass

    # Don't forget the last token!
    # YOUR CODE HERE

    return tokens


sentence_13 = "I love NLP... and Python! It's amazing :)"
print("Basic tokeniser:")
print(tokenise_basic(sentence_13))
print()


# -----------------------------------------------------------------------------
# STEP 2 — Emoticon-aware tokeniser
# -----------------------------------------------------------------------------
# The basic tokeniser loses ":)" completely.
# Let's fix it by detecting emoticons explicitly.

EMOTICONS = {":)", ":(", ":D", ":P", ";)", ":/", ":o", "XD", "<3"}

# TODO 8: Complete tokenise_with_emoticons(text).
# Before reading each character, check if the NEXT TWO characters form
# a known emoticon. If yes: save buffer + save emoticon, advance by 2.
# Otherwise: same logic as tokenise_basic.

def tokenise_with_emoticons(text):
    """
    Tokenises text character by character.
    Detects emoticons from EMOTICONS and keeps them as single tokens.
    """
    tokens = []
    buffer = ""
    i = 0
    text = text.lower()

    while i < len(text):
        # YOUR CODE HERE — check two_chars = text[i:i+2] first
        pass

    if buffer.strip():
        tokens.append(buffer.strip())

    return tokens


print("Emoticon-aware tokeniser:")
test_sentences_13 = [
    "I love NLP... and Python! It's amazing :)",
    "Best. Product. Ever. :D",
    "Terrible experience :( would not recommend",
    "Not bad ;) would buy again!",
]

for s in test_sentences_13:
    basic   = tokenise_basic(s)
    emotion = tokenise_with_emoticons(s)
    print(f"Input  : {s}")
    print(f"Basic  : {basic}")
    print(f"Emotion: {emotion}")
    print()


# DISCUSSION:
# Q1. If ":)" appears 50 times in positive reviews and 2 in negative,
#     what can the model learn? Would it learn the same if split into ":" + ")"?
#
# Q2. What other sequences should stay as one token in emotion detection?
#     (e.g. "!!!", "...", all-caps words, negations like "n't")
#
# Q3. Should "don't" → ["don","t"], ["don't"], or ["do","not"]? Justify.
#
# YOUR ANSWERS HERE (as comments):
#


# -----------------------------------------------------------------------------
# BONUS 1.3 — Make it configurable
# -----------------------------------------------------------------------------
# TODO 9 (optional): Write tokenise(text, keep_emoticons=True) that
#         calls tokenise_with_emoticons when True and tokenise_basic when False.

def tokenise(text, keep_emoticons=True):
    """Configurable tokeniser."""
    # YOUR CODE HERE
    pass


# =============================================================================
# ACTIVITY 1.4 — Complete Normalisation Pipeline
# =============================================================================
#
# GOAL: Integrate everything from 1.1–1.3 into a single coherent pipeline.
#       The key learning here is making CONSCIOUS DESIGN DECISIONS.
#
# At the end you will have: pipeline(text) → raw text → list of tokens


# =============================================================================
# PART A — Constants
# =============================================================================

EMOTICONS_14 = {":)", ":(", ":D", ":P", ";)", ":/", ":o", "XD", "<3",
                ":-)", ":-(", ":-D", ":-P"}

# ⚠️  WARNING: removing "not" can completely flip sentiment.
#     "not good" → if "not" removed → just "good"  ← WRONG
#     Think carefully before adding negations here.

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


# =============================================================================
# PART B — Pipeline functions
# =============================================================================

def lowercase_14(text):
    """Convert text to lowercase."""
    return text.lower()


def tokenise_14(text, keep_emoticons=True):
    """
    Tokenise text character by character.
    Reuse your logic from Activity 1.3.
    """
    # TODO 10: copy / adapt your tokenise_with_emoticons logic here,
    #          using EMOTICONS_14 as the emoticon set.
    #          If keep_emoticons=False, use basic tokenisation (no emoticon check).
    tokens = []
    buffer = ""
    i = 0

    while i < len(text):
        # YOUR CODE HERE
        pass

    if buffer.strip():
        tokens.append(buffer.strip())

    return tokens


def remove_stopwords(tokens, stopwords=STOPWORDS):
    """
    TODO 11: Return a new list containing only tokens NOT in stopwords.
    One line of code is enough (list comprehension).
    """
    # YOUR CODE HERE
    pass


def remove_short_tokens(tokens, min_length=2):
    """
    TODO 12: Return tokens with length >= min_length.
             ALWAYS keep emoticons regardless of length.
    """
    # YOUR CODE HERE
    pass


# =============================================================================
# PART C — The complete pipeline
# =============================================================================

def pipeline(text, keep_emoticons=True, apply_stopwords=True, min_length=2):
    """
    Full preprocessing pipeline:
      raw text
        → lowercase
        → tokenise (with optional emoticon preservation)
        → remove stopwords (optional)
        → remove short tokens
        → list of tokens

    TODO 13: Call the four functions above in the right order.
             Use the parameters to control each step.
    """
    # YOUR CODE HERE
    pass


# =============================================================================
# PART D — Test and inspect
# =============================================================================

test_cases_14 = [
    "The battery life on this phone is absolutely amazing! :)",
    "I can't believe how terrible this product is. Total waste of money.",
    "Not bad, not great... just okay.",
    "Incredible! Best purchase I've made all year :D",
    "Rude staff, cold food. Never coming back.",
]

print("=" * 65)
print("PIPELINE TEST — default settings")
print("=" * 65)

for sentence in test_cases_14:
    tokens = pipeline(sentence)
    print(f"\nInput : {sentence}")
    print(f"Output: {tokens}")

print()

# =============================================================================
# PART E — Design decisions exercise
# =============================================================================
# The same sentence can produce very different results depending on choices.

sentence_14 = "This product is NOT as good as I expected. Very disappointing :("

print("=" * 65)
print("DESIGN DECISIONS — same sentence, different settings")
print("=" * 65)
print(f"\nInput: {sentence_14}\n")

v1 = pipeline(sentence_14, keep_emoticons=True,  apply_stopwords=True)
v2 = pipeline(sentence_14, keep_emoticons=True,  apply_stopwords=False)
v3 = pipeline(sentence_14, keep_emoticons=False, apply_stopwords=True)
v4 = pipeline(sentence_14, keep_emoticons=False, apply_stopwords=False)

print(f"V1 (stopwords=ON,  emoticons=ON ): {v1}")
print(f"V2 (stopwords=OFF, emoticons=ON ): {v2}")
print(f"V3 (stopwords=ON,  emoticons=OFF): {v3}")
print(f"V4 (stopwords=OFF, emoticons=OFF): {v4}")

print()
print("QUESTIONS TO DISCUSS:")
print("  1. Which variant best captures the sentiment of this sentence?")
print("  2. 'not' survived in all variants — is that good or bad?")
print("  3. In V1, is 'disappointing' still in the output? Why?")
print("  4. ':(' is in V1 and V2 but not V3 and V4 — how much does it matter?")
