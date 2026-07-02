import re


# -------------------------------
# Clarification Intent
# -------------------------------

def needs_clarification(query: str):

    query = query.lower().strip()

    # अगर बहुत छोटा input है
    if len(query.split()) == 1:
        if query.lower() in ["hi","hello","hey"]:
            return False
        return True

    # Role keywords
    roles = [
        "developer",
        "engineer",
        "manager",
        "analyst",
        "tester",
        "sales",
        "executive",
        "java",
        "python",
        "data scientist",
        "leader",
        "leadership"
    ]

    # Experience keywords
    experience = [
        "year",
        "years",
        "fresher",
        "entry",
        "mid",
        "senior",
        "graduate",
        "experienced"
    ]

    # Assessment type
    assessment = [
        "technical",
        "aptitude",
        "personality",
        "coding",
        "behavior"
    ]

    role_found = any(x in query for x in roles)
    exp_found = any(x in query for x in experience)
    assess_found = any(x in query for x in assessment)

    # कम से कम दो जानकारी मिल गई तो clarification नहीं चाहिए
    score = role_found + exp_found + assess_found

    return score < 2

# -------------------------------
# Compare Intent
# -------------------------------

def is_compare(query: str) -> bool:

    query = query.lower()

    compare_words = [
        "compare",
        "difference",
        "vs",
        "versus",
        "better than"
    ]

    return any(word in query for word in compare_words)


# -------------------------------
# Refinement Intent
# -------------------------------

def is_refinement(query: str) -> bool:

    query = query.lower()

    refinement_words = [
        "actually",
        "instead",
        "also",
        "include",
        "add",
        "remove",
        "change",
        "update",
        "only",
        "without"
    ]

    return any(word in query for word in refinement_words)


# -------------------------------
# Greeting Intent
# -------------------------------

def is_greeting(query: str) -> bool:

    query = query.lower().strip()

    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good evening",
        "good afternoon"
    ]

    return query in greetings


# -------------------------------
# Off-topic Intent
# -------------------------------

def is_off_topic(query: str) -> bool:

    query = query.lower()

    off_topic = [
        "ipl",
        "cricket",
        "football",
        "movie",
        "weather",
        "politics",
        "prime minister",
        "president",
        "bitcoin",
        "share market",
        "youtube",
        "instagram",
        "facebook"
    ]

    return any(word in query for word in off_topic)


# -------------------------------
# Prompt Injection Detection
# -------------------------------

def is_prompt_injection(query: str) -> bool:

    query = query.lower()

    injection_patterns = [
        "ignore previous",
        "forget previous",
        "system prompt",
        "reveal prompt",
        "developer message",
        "act as",
        "pretend",
        "jailbreak",
        "bypass",
        "ignore instructions"
    ]

    return any(pattern in query for pattern in injection_patterns)


# -------------------------------
# Main Intent Classifier
# -------------------------------

def detect_intent(query: str):

    if is_prompt_injection(query):
        return "prompt_injection"

    if is_off_topic(query):
        return "off_topic"

    if is_greeting(query):
        return "greeting"

    if is_compare(query):
        return "compare"

    if is_refinement(query):
        return "refinement"

    if needs_clarification(query):
        return "clarification"

    return "recommendation"


# -------------------------------
# Test
# -------------------------------

if __name__ == "__main__":

    while True:

        query = input("\nUser : ")

        print("Intent :", detect_intent(query))