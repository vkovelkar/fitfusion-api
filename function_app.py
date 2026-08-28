import azure.functions as func
import json
import logging

from tools.registry import TOOLS
from tools.router import execute_tool

app = func.FunctionApp()


# =========================================================
# ARGUMENT VALIDATION
# =========================================================

def validate_arguments(tool_name, arguments):

    tool = TOOLS[tool_name]
    schema = tool["input_schema"]

    # -----------------------------------------------------
    # ARGUMENTS MUST BE AN OBJECT
    # -----------------------------------------------------

    if not isinstance(arguments, dict):
        return {
            "error": "Arguments must be a JSON object"
        }

    # -----------------------------------------------------
    # REQUIRED FIELDS
    # -----------------------------------------------------

    required_fields = schema.get("required", [])

    for field in required_fields:

        if field not in arguments:

            return {
                "error": f"Missing required argument: {field}"
            }

    # -----------------------------------------------------
    # PROPERTY VALIDATION
    # -----------------------------------------------------

    properties = schema.get("properties", {})

    for field, value in arguments.items():

        # Ignore unknown fields for now.
        # We can enforce strict schemas later.

        if field not in properties:
            continue

        field_schema = properties[field]

        # -------------------------------------------------
        # TYPE VALIDATION
        # -------------------------------------------------

        expected_type = field_schema.get("type")

        if expected_type == "string":

            if not isinstance(value, str):

                return {
                    "error": (
                        f"Invalid type for '{field}'. "
                        "Expected string."
                    )
                }

        elif expected_type == "number":

            if (
                not isinstance(value, (int, float))
                or isinstance(value, bool)
            ):

                return {
                    "error": (
                        f"Invalid type for '{field}'. "
                        "Expected number."
                    )
                }

        # -------------------------------------------------
        # ENUM VALIDATION
        # -------------------------------------------------

        if "enum" in field_schema:

            allowed_values = field_schema["enum"]

            if value not in allowed_values:

                return {
                    "error": (
                        f"Invalid value for '{field}': {value}. "
                        f"Allowed values: {allowed_values}"
                    )
                }

    return None


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
    # VALIDATE REQUEST BODY TYPE
    # -----------------------------------------------------

    if not isinstance(data, dict):

        return func.HttpResponse(
            json.dumps({
                "error": "Request body must be a JSON object"
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
    # VALIDATE TOOL ARGUMENTS AGAINST SCHEMA
    # -----------------------------------------------------

    validation_error = validate_arguments(
        tool_name,
        arguments
    )

    if validation_error:

        return func.HttpResponse(
            json.dumps(validation_error),
            status_code=400,
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

    # -----------------------------------------------------
    # VALIDATE FITNESS ANALYSIS ARGUMENTS
    # -----------------------------------------------------

    validation_error = validate_arguments(
        "fitness.analyze",
        data
    )

    if validation_error:

        return func.HttpResponse(
            json.dumps(validation_error),
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