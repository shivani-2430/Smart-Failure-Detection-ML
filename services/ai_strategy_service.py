import os
import json
from typing import TypedDict

from dotenv import load_dotenv
from google import genai
from google.genai import types

from langgraph.graph import StateGraph, START, END


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Check your .env file."
    )


client = genai.Client(api_key=API_KEY)


# =========================================================
# MODEL
# =========================================================

MODEL_NAME = "gemini-3.6-flash"


# =========================================================
# LANGGRAPH STATE
# =========================================================

class StrategyState(TypedDict):

    project_context: str

    strategic_analysis: str

    mitigation_plan: list

    final_strategy: str


# =========================================================
# COMMON AI RULES
# =========================================================

GROUNDING_RULES = """
You are an AI strategic analysis engine for a project management
and risk assessment system.

STRICT GROUNDING RULES:

1. Use ONLY the project information supplied in PROJECT CONTEXT.
2. Never invent an organization, company, hospital, customer,
   regulation, law, certification, technology, budget, resource,
   requirement, or business fact.
3. Do not assume HIPAA, GDPR, ABDM, ISO, or any other regulation
   unless it is explicitly present in PROJECT CONTEXT.
4. Do not invent project stakeholders or organizational details.
5. Do not claim that a technology is already implemented unless
   PROJECT CONTEXT explicitly says so.
6. If information is unavailable, state that it is unavailable.
7. Base recommendations on the actual risk, feasibility,
   machine-learning prediction, budget, team, timeline,
   technology stack, and project description provided.
8. Do not repeat the entire risk assessment.
9. Produce practical project-specific reasoning.
"""


# =========================================================
# SAFE GEMINI CALL
# =========================================================

def call_gemini(prompt, schema):

    response = client.models.generate_content(

        model=MODEL_NAME,

        contents=prompt,

        config=types.GenerateContentConfig(

            max_output_tokens=1600,

            response_mime_type="application/json",

            response_schema=schema

        )
    )

    # Google GenAI SDK can parse structured JSON directly.
    parsed = getattr(response, "parsed", None)

    if parsed is not None:

        if hasattr(parsed, "model_dump"):
            return parsed.model_dump()

        if isinstance(parsed, dict):
            return parsed

    # Fallback in case SDK does not expose parsed output.
    text = response.text.strip()

    try:
        return json.loads(text)

    except json.JSONDecodeError:

        raise RuntimeError(
            "Gemini returned incomplete structured JSON. "
            f"Raw response:\n{text}"
        )


# =========================================================
# NODE 1
# STRATEGIC ANALYSIS
# =========================================================

def analyze_project(state: StrategyState):

    prompt = f"""
{GROUNDING_RULES}

PROJECT CONTEXT:
{state["project_context"]}

Analyze the current project condition.

Focus on:

- overall project position
- relationship between risk and feasibility
- machine-learning prediction
- execution readiness
- most important strategic concern

Do not invent information.

Return JSON using exactly this structure:

{{
    "analysis": "Professional strategic analysis"
}}
"""

    schema = {
        "type": "OBJECT",
        "properties": {
            "analysis": {
                "type": "STRING"
            }
        },
        "required": ["analysis"]
    }

    result = call_gemini(prompt, schema)

    return {
        "strategic_analysis": result["analysis"]
    }


# =========================================================
# NODE 2
# MITIGATION / IMPROVEMENT ENGINE
# =========================================================

def generate_mitigation(state: StrategyState):

    prompt = f"""
{GROUNDING_RULES}

PROJECT CONTEXT:
{state["project_context"]}

STRATEGIC ANALYSIS:
{state["strategic_analysis"]}

Generate practical mitigation and improvement actions.

Requirements:

- Generate exactly 3 actions.
- Actions must be directly connected to the supplied project information.
- Prioritize the most useful actions first.
- Do not invent regulations, organizations, customers,
  technologies, or business requirements.
- Do not simply repeat the existing risk labels.
- Each action must explain its expected impact.
- If information is unavailable, clearly state that
  additional information is required.

Return JSON using exactly this structure:

{{
    "actions": [
        {{
            "action": "Specific project action",
            "impact": "Expected improvement"
        }},
        {{
            "action": "Specific project action",
            "impact": "Expected improvement"
        }},
        {{
            "action": "Specific project action",
            "impact": "Expected improvement"
        }}
    ]
}}
"""

    schema = {
        "type": "OBJECT",
        "properties": {

            "actions": {

                "type": "ARRAY",

                "items": {

                    "type": "OBJECT",

                    "properties": {

                        "action": {
                            "type": "STRING"
                        },

                        "impact": {
                            "type": "STRING"
                        }

                    },

                    "required": [
                        "action",
                        "impact"
                    ]
                }
            }
        },

        "required": [
            "actions"
        ]
    }

    result = call_gemini(
        prompt,
        schema
    )

    return {
        "mitigation_plan": result["actions"]
    }


# =========================================================
# NODE 3
# FINAL STRATEGIC DECISION
# =========================================================

def generate_final_strategy(state: StrategyState):
    mitigation_text = "\n".join(
        f"{index}. {item['action']} - Expected Impact: {item['impact']}"
        for index, item in enumerate(
            state["mitigation_plan"],
            start=1
        )
    )

    prompt = f"""
{GROUNDING_RULES}

PROJECT CONTEXT:
{state["project_context"]}

STRATEGIC ANALYSIS:
{state["strategic_analysis"]}

MITIGATION PLAN:
{mitigation_text}

Create the final strategic recommendation.

The recommendation must:

- identify one clear primary direction
- explain why that direction is appropriate
- assign HIGH, MEDIUM, or LOW priority
- describe a concrete expected impact
- remain completely grounded in the supplied information

Do not introduce facts that are not present in PROJECT CONTEXT.

Return JSON using exactly this structure:

{{
    "primary_direction": "Clear strategic direction",
    "reasoning": "Why this direction is appropriate",
    "priority": "HIGH",
    "expected_impact": "Specific expected improvement"
}}
"""

    schema = {
        "type": "OBJECT",
        "properties": {
            "primary_direction": {
                "type": "STRING"
            },
            "reasoning": {
                "type": "STRING"
            },
            "priority": {
                "type": "STRING",
                "enum": [
                    "HIGH",
                    "MEDIUM",
                    "LOW"
                ]
            },
            "expected_impact": {
                "type": "STRING"
            }
        },
        "required": [
            "primary_direction",
            "reasoning",
            "priority",
            "expected_impact"
        ]
    }

    result = call_gemini(prompt, schema)

    final_text = (
        f"PRIMARY DIRECTION\n"
        f"{result['primary_direction']}\n\n"
        f"WHY THIS DIRECTION\n"
        f"{result['reasoning']}\n\n"
        f"PRIORITY\n"
        f"{result['priority']}\n\n"
        f"EXPECTED IMPACT\n"
        f"{result['expected_impact']}"
    )

    return {
        "final_strategy": final_text
    }


# =========================================================
# LANGGRAPH WORKFLOW
# =========================================================

workflow = StateGraph(StrategyState)


workflow.add_node(
    "analyze_project",
    analyze_project
)

workflow.add_node(
    "generate_mitigation",
    generate_mitigation
)

workflow.add_node(
    "generate_final_strategy",
    generate_final_strategy
)


workflow.add_edge(
    START,
    "analyze_project"
)

workflow.add_edge(
    "analyze_project",
    "generate_mitigation"
)

workflow.add_edge(
    "generate_mitigation",
    "generate_final_strategy"
)

workflow.add_edge(
    "generate_final_strategy",
    END
)


strategy_agent = workflow.compile()


# =========================================================
# PUBLIC FUNCTION
# =========================================================

def generate_strategy(project_context: str):

    return strategy_agent.invoke(
        {
            "project_context": project_context,
            "strategic_analysis": "",
            "mitigation_plan": "",
            "final_strategy": ""
        }
    )