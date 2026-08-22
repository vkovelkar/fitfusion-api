from tools.fitness.analyze import analyze_fitness
from tools.fitness.recommend import recommend_fitness
from tools.fitness.workout import workout_plan
from tools.fitness.plan import generate_complete_plan


# =========================================================
# TOOL HANDLER REGISTRY
# =========================================================

TOOL_HANDLERS = {
    "fitness.analyze": analyze_fitness,
    "fitness.recommend": recommend_fitness,
    "fitness.workout_plan": workout_plan,
    "fitness.complete_plan": generate_complete_plan
}


# =========================================================
# GENERIC TOOL EXECUTION
# =========================================================

def execute_tool(tool_name, arguments):

    handler = TOOL_HANDLERS.get(tool_name)

    if handler is None:
        return {
            "error": f"Unknown tool: {tool_name}"
        }

    return handler(arguments)