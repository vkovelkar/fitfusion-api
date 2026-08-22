import azure.functions as func
import json
import logging

from tools.registry import TOOLS
from tools.router import execute_tool

app = func.FunctionApp()


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route(
    route="health",
    methods=["GET"],
    auth_level=func.AuthLevel.ANONYMOUS
)
def health(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("Health check requested.")

    response = {
        "status": "healthy",
        "service": "FitFusion API"
    }

    return func.HttpResponse(
        json.dumps(response),
        status_code=200,
        mimetype="application/json"
    )


# =========================================================
# TOOL DISCOVERY
# =========================================================

@app.route(
    route="tools",
    methods=["GET"],
    auth_level=func.AuthLevel.ANONYMOUS
)
def list_tools(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("Tool discovery requested.")

    response = {
        "tools": list(TOOLS.values()),
        "count": len(TOOLS)
    }

    return func.HttpResponse(
        json.dumps(response),
        status_code=200,
        mimetype="application/json"
    )


# =========================================================
# GENERIC TOOL EXECUTION
# =========================================================

@app.route(
    route="tools/execute",
    methods=["POST"],
    auth_level=func.AuthLevel.ANONYMOUS
)
def execute(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("Tool execution requested.")

    try:
        data = req.get_json()

    except ValueError:
        return func.HttpResponse(
            json.dumps({
                "error": "Invalid JSON request body"
            }),
            status_code=400,
            mimetype="application/json"
        )

    # -----------------------------------------------------
    # VALIDATE TOOL REQUEST
    # -----------------------------------------------------

    if "tool" not in data:
        return func.HttpResponse(
            json.dumps({
                "error": "Missing required field: tool"
            }),
            status_code=400,
            mimetype="application/json"
        )

    if "arguments" not in data:
        return func.HttpResponse(
            json.dumps({
                "error": "Missing required field: arguments"
            }),
            status_code=400,
            mimetype="application/json"
        )

    tool_name = data["tool"]
    arguments = data["arguments"]

    # -----------------------------------------------------
    # CHECK TOOL EXISTS
    # -----------------------------------------------------

    if tool_name not in TOOLS:
        return func.HttpResponse(
            json.dumps({
                "error": "Unknown tool",
                "tool": tool_name,
                "available_tools": list(TOOLS.keys())
            }),
            status_code=404,
            mimetype="application/json"
        )

    # -----------------------------------------------------
    # EXECUTE TOOL
    # -----------------------------------------------------

    result = execute_tool(
        tool_name,
        arguments
    )

    # -----------------------------------------------------
    # RETURN ERROR FROM TOOL
    # -----------------------------------------------------

    if "error" in result:

        return func.HttpResponse(
            json.dumps(result),
            status_code=400,
            mimetype="application/json"
        )

    # -----------------------------------------------------
    # SUCCESS RESPONSE
    # -----------------------------------------------------

    response = {
        "tool": tool_name,
        "result": result
    }

    return func.HttpResponse(
        json.dumps(response),
        status_code=200,
        mimetype="application/json"
    )


# =========================================================
# FITNESS ANALYSIS
# BACKWARD-COMPATIBLE REST ENDPOINT
# =========================================================

@app.route(
    route="fitness/analyze",
    methods=["POST"],
    auth_level=func.AuthLevel.ANONYMOUS
)
def analyze_fitness(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("Fitness analysis requested.")

    try:
        data = req.get_json()

    except ValueError:
        return func.HttpResponse(
            json.dumps({
                "error": "Invalid JSON request body"
            }),
            status_code=400,
            mimetype="application/json"
        )

    result = execute_tool(
        "fitness.analyze",
        data
    )

    if "error" in result:

        return func.HttpResponse(
            json.dumps(result),
            status_code=400,
            mimetype="application/json"
        )

    return func.HttpResponse(
        json.dumps(result),
        status_code=200,
        mimetype="application/json"
    )