from app.retriever import search_assessments
from app.gemini import generate_response
from app.prompts import SYSTEM_PROMPT
from app.intent import detect_intent, needs_clarification

from typing import List, Dict

# Helper function-1
def build_history(messages: List[Dict]) -> str:
    """
    Convert conversation history into text.
    """

    history = ""

    for msg in messages:

        role = msg["role"].capitalize()

        content = msg["content"]

        history += f"{role}: {content}\n"

    return history

#helper function 2
def build_catalog_context(results):

    context = ""

    for item in results:

        context += f"""

Assessment Name:
{item.get("name","")}

Description:
{item.get("description","")}

Job Levels:
{', '.join(item.get("job_levels",[]))}

Keys:
{', '.join(item.get("keys",[]))}

Duration:
{item.get("duration","")}

URL:
{item.get("url","")}

--------------------------------

"""

    return context

# Helper function 3
def build_recommendations(results):

    recommendations = []

    for item in results:

        recommendations.append({

            "name": item["name"],

            "url": item["url"],

            "test_type": item["keys"][0] if item["keys"] else "Unknown"

        })

    return recommendations

# Greeting 
def greeting_response():

    return {

        "reply":
        "Hello! I can help you find the right SHL Individual Test Solutions. Tell me about the role you are hiring for.",

        "recommendations": [],

        "end_of_conversation": False

    }

# Clarification 
def clarification_response():

    return {

        "reply":
"""I'd be happy to help.

Could you please tell me:

• Job Role

• Experience Level

• Skills you want to assess

• Technical, Aptitude or Personality assessment?

Once I have this information I'll recommend suitable SHL assessments.
""",

        "recommendations": [],

        "end_of_conversation": False

    }

# off Topic
def off_topic_response():

    return {

        "reply":
        "I can only help with SHL Individual Test Solution recommendations.",

        "recommendations": [],

        "end_of_conversation": False

    }

# Prompt injection
def prompt_injection_response():

    return {

        "reply":
        "Sorry, I can only answer questions related to SHL Individual Test Solutions.",

        "recommendations": [],

        "end_of_conversation": False

    }

# compare placeholder
def compare_placeholder():

    return {

        "reply":
        "Let me compare those SHL assessments using the catalog.",

        "recommendations": [],

        "end_of_conversation": False

    }

#Refinement Placeholder
def refinement_placeholder():

    return {

        "reply":
        "Updating recommendations based on your latest requirement.",

        "recommendations": [],

        "end_of_conversation": False

    }
# ---------------------------------------
# Recommendation Engine
# ---------------------------------------

def recommendation_response(messages):

    # Latest user query
   combined_query = ""
   for msg in messages:
    if msg["role"] == "user":
        combined_query += msg["content"] + " "

    # Search Top SHL Assessments
    
    results = search_assessments(combined_query, top_k=5)
    if len(results) == 0:

        return {

            "reply":
            "Sorry, I couldn't find any matching SHL assessment.",

            "recommendations": [],

            "end_of_conversation": False

        }

    # Build Conversation History

    history = build_history(messages)

    # Build Catalog Context

    catalog_context = build_catalog_context(results)

    # Gemini Prompt

    prompt = f"""

{SYSTEM_PROMPT}

Conversation History

{history}

----------------------------------------

Retrieved SHL Assessments

{catalog_context}

----------------------------------------

Instructions

Use ONLY the retrieved SHL assessments.

Never invent assessment names.

Never invent URLs.

Recommend between 1 and 5 assessments.

Explain why each assessment fits.

Keep response professional.

"""

    # Gemini Reply

    reply = generate_response(prompt)

    # Recommendation JSON

    recommendations = build_recommendations(results)

    return {

        "reply": reply,

        "recommendations": recommendations,

        "end_of_conversation": False

    }

# ---------------------------------------
# Compare Assessments
# ---------------------------------------

def compare_response(messages):

    user_query = messages[-1]["content"]

    results = search_assessments(user_query, top_k=2)

    if len(results) < 2:

        return {

            "reply":
            "Please mention two SHL assessments you want to compare.",

            "recommendations": [],

            "end_of_conversation": False

        }

    history = build_history(messages)

    catalog = build_catalog_context(results)

    prompt = f"""

{SYSTEM_PROMPT}

Conversation

{history}

Compare ONLY these assessments.

{catalog}

Create a comparison table.

Mention

Purpose

Skills

Duration

Job Level

Best Use Case

Do NOT invent anything.

"""

    reply = generate_response(prompt)

    return {

        "reply": reply,

        "recommendations": build_recommendations(results),

        "end_of_conversation": False

    }

# ---------------------------------------
# Refinement
# ---------------------------------------

def refinement_response(messages):

    combined_query = ""

    for msg in messages:

        if msg["role"] == "user":

            combined_query += msg["content"] + " "

    results = search_assessments(combined_query, top_k=5)

    history = build_history(messages)

    catalog = build_catalog_context(results)

    prompt = f"""

{SYSTEM_PROMPT}

Conversation

{history}

Retrieved Assessments

{catalog}

Update recommendation according to latest user request.

"""

    reply = generate_response(prompt)

    return {

        "reply": reply,

        "recommendations": build_recommendations(results),

        "end_of_conversation": False

    }

# ---------------------------------------
# Main Chat Function
# ---------------------------------------

def chat(messages):

    try:

        if not messages:

            return {
                "reply": "Please enter your requirement.",
                "recommendations": [],
                "end_of_conversation": False
            }

        # Latest User Message
        user_query = messages[-1]["content"]

        # Full Conversation (only user messages)
        combined_query = ""

        for msg in messages:
            if msg["role"] == "user":
                combined_query += msg["content"] + " "

        # --------------------------
        # Detect Intent
        # --------------------------

        intent = detect_intent(user_query)

        print(f"\nDetected Intent : {intent}")

        # --------------------------
        # Greeting
        # --------------------------

        if intent == "greeting":
            return greeting_response()

        # --------------------------
        # Off Topic
        # --------------------------

        if intent == "off_topic":
            return off_topic_response()

        # --------------------------
        # Prompt Injection
        # --------------------------

        if intent == "prompt_injection":
            return prompt_injection_response()

        # --------------------------
        # Compare
        # --------------------------

        if intent == "compare":
            return compare_response(messages)

        # --------------------------
        # Refinement
        # --------------------------

        if intent == "refinement":
            return refinement_response(messages)

        # --------------------------
        # Clarification
        # --------------------------

        if needs_clarification(combined_query):
            return clarification_response()

        # --------------------------
        # Recommendation
        # --------------------------

        response = recommendation_response(messages)

        if len(response["recommendations"]) > 0:
            response["end_of_conversation"] = True
        else:
            response["end_of_conversation"] = False

        return response

    except Exception as e:

        print(e)

        return {
            "reply": "Sorry, something went wrong while processing your request.",
            "recommendations": [],
            "end_of_conversation": False
        }