# =============================================================================
# SESSION 2 · NLP Applied to Emotion Detection
# Activity 1 — From Raw Text to Tokens  ·  SOLUTION
# =============================================================================
#
#   1.1  Text as strings          → lowercase + remove punctuation
#   1.2  Naive tokenisation       → split(), discover its limits
#   1.3  Character-by-char        → full control, emoticon-aware
#   1.4  Complete pipeline        → integrate everything
# =============================================================================


# =============================================================================
# ACTIVITY 1.1 — Text as Strings
# =============================================================================

sentence = "The Battery life on this Phone is AMAZING... it lasts 2 full days! :)"

print("Original sentence:")
print(sentence)
print()

# --- TODO 1: lowercase ---
lower_sentence = sentence.lower()
print("Lowercase:")
print(lower_sentence)
print()

# --- TODO 2: remove punctuation ---
clean_chars = []
for char in lower_sentence:
    if char.isalpha() or char.isdigit() or char == " ":
        clean_chars.append(char)
clean_sentence = "".join(clean_chars)

print("After removing punctuation:")
print(clean_sentence)
print()
print("=" * 60)
print("BEFORE:", sentence)
print("AFTER: ", clean_sentence)
print("=" * 60)
print()

# --- TODO 3: clean_text function ---
def clean_text(text):
    """
    Converts text to lowercase and removes all characters
    that are not letters, digits, or spaces.
    """
    result = []
    for char in text.lower():
        if char.isalpha() or char.isdigit() or char == " ":
            result.append(char)
    return "".join(result)


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

raw_sentence = "I love NLP... and Python! It's amazing :)"

# --- TODO 4: tokenise before cleaning ---
raw_tokens = raw_sentence.split(" ")
print("Raw sentence:", raw_sentence)
print("Tokens (no cleaning):", raw_tokens)
print()

# --- TODO 5: tokenise after cleaning ---
clean_tokens = clean_text(raw_sentence).split(" ")
print("Tokens (after cleaning):", clean_tokens)
print()

# --- TODO 6: compare split() vs split(" ") ---
tokens_single_space = clean_text(raw_sentence).split(" ")
tokens_any_space    = clean_text(raw_sentence).split()
print('split(" ") →', tokens_single_space)
print("split()    →", tokens_any_space)
print()

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

# ANSWER: Cleaning before tokenising loses emoticons (":)") and
# negations attached to punctuation. For emotion detection this is
# a significant information loss.


# =============================================================================
# ACTIVITY 1.3 — Tokenisation: Character by Character
# =============================================================================

# --- TODO 7: basic char-by-char tokeniser ---
def tokenise_basic(text):
    """
    Tokenises text character by character, splitting on spaces.
    Removes standalone punctuation.
    """
    tokens = []
    buffer = ""

    for char in text.lower():
        if char == " ":
            if buffer:
                tokens.append(buffer)
                buffer = ""
        elif char.isalpha() or char.isdigit():
            buffer += char
        # else: punctuation is silently dropped

    if buffer:
        tokens.append(buffer)

    return tokens


EMOTICONS = {":)", ":(", ":D", ":P", ";)", ":/", ":o", "XD", "<3"}

# --- TODO 8: emoticon-aware tokeniser ---
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


sentence_13 = "I love NLP... and Python! It's amazing :)"
print("Basic tokeniser:")
print(tokenise_basic(sentence_13))
print()

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

# --- TODO 9: configurable tokeniser ---
def tokenise(text, keep_emoticons=True):
    """Configurable tokeniser."""
    if keep_emoticons:
        return tokenise_with_emoticons(text)
    else:
        return tokenise_basic(text)


s_bonus = "Great experience :) would totally recommend!"
print("Configurable tokeniser:")
print(f"keep_emoticons=True : {tokenise(s_bonus, keep_emoticons=True)}")
print(f"keep_emoticons=False: {tokenise(s_bonus, keep_emoticons=False)}")
print()


# =============================================================================
# ACTIVITY 1.4 — Complete Normalisation Pipeline
# =============================================================================

EMOTICONS_14 = {":)", ":(", ":D", ":P", ";)", ":/", ":o", "XD", "<3",
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


def lowercase_14(text):
    return text.lower()


# --- TODO 10: tokenise_14 ---
def tokenise_14(text, keep_emoticons=True):
    """Tokenise character by character, with optional emoticon preservation."""
    tokens = []
    buffer = ""
    i = 0

    while i < len(text):
        if keep_emoticons:
            two_chars = text[i:i+2]
            if two_chars in EMOTICONS_14:
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


# --- TODO 11: remove_stopwords ---
def remove_stopwords(tokens, stopwords=STOPWORDS):
    """Remove tokens that are in the stopword list."""
    return [t for t in tokens if t not in stopwords]


# --- TODO 12: remove_short_tokens ---
def remove_short_tokens(tokens, min_length=2):
    """Remove tokens shorter than min_length, but always keep emoticons."""
    return [t for t in tokens if len(t) >= min_length or t in EMOTICONS_14]


# --- TODO 13: pipeline ---
def pipeline(text, keep_emoticons=True, apply_stopwords=True, min_length=2):
    """
    Full preprocessing pipeline:
      raw text → lowercase → tokenise → remove stopwords → remove short tokens
    """
    text = lowercase_14(text)
    tokens = tokenise_14(text, keep_emoticons=keep_emoticons)
    if apply_stopwords:
        tokens = remove_stopwords(tokens)
    tokens = remove_short_tokens(tokens, min_length=min_length)
    return tokens


# --- Test ---
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

# --- Design decisions ---
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
print("ANSWERS:")
print("  1. V1 is the most compact; V2 retains more context including 'expected'.")
print("     Both V1 and V2 keep ':(' which signals negative emotion directly.")
print("  2. 'not' surviving is GOOD — it negates 'good', preserving the meaning.")
print("  3. 'disappointing' is kept — it is not a stopword and len >= 2.")
print("  4. ':(' adds strong emotional signal; losing it (V3/V4) weakens the output.")
