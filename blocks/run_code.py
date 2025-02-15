import os
from rizaio import Riza


def run_code(code, input_filename=None):
    if not code:
        message = "Error: code_for_riza.py file not found"
        print(message)
        return None, message
    riza_client = Riza(api_key=os.environ["RIZA_API_KEY"])
    try:
        result = riza_client.command.exec(
            language="python",
            runtime_revision_id="01JKY2FCN25GW3EC8JMFN3KWX9",
            code=code,
        )
    except Exception as e:
        message = f"Exception during execution: {str(e)}"
        print(message)
        return None, message
    if result.exit_code != 0:
        message = f"Code did not execute successfully. Error: {result.stderr}"
        print(message)
        return None, message
    if not result.stdout:
        message = "Code executed successfully but produced no output."
        print(message)
        return "", message
    print(result.stdout)
    return result.stdout, None


if __name__ == "__main__":
    code = "print('Hello World!')"
    run_code(code)
