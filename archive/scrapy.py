import json
import os
from pydantic_ai import Agent
from bs4 import BeautifulSoup
import httpx
from rizaio import Riza


agent = Agent(
    "openai:gpt-4o",
    system_prompt=open("system_prompt.txt").read(),
)


@agent.tool_plain
def save_body_html(url):
    """Extracts and returns the <body> content from an HTML page with all <script> tags removed.

    This function retrieves HTML from a URL, parses it, locates the <body> tag, removes any
    <script> elements within it, and returns the cleaned body content as a string.

    Args:
        url (str): The URL to retrieve and process HTML from

    Returns:
        str: The HTML string containing just the <body> content with scripts removed
        None: If no <body> tag is found in the input HTML or if URL fetch fails

    Example:
        >>> extract_body_html("https://example.com")
        '<body>Content</body>'
    """
    response = httpx.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve URL: {url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    body = soup.find("body")
    if body:
        for script in body.find_all("script"):
            script.decompose()
        return str(body)
    else:
        print("No <body> tag found in the HTML.")
        return None


@agent.tool_plain
async def generate_code(site_html):
    """Generates Python code to scrape data from HTML using an AI agent.

    This function uses an AI agent to analyze the provided HTML and generate
    Python code that can extract structured data from it. The agent is configured
    using instructions from 'generate_code_prompt.txt'.

    Args:
        site_html (str): The HTML content to generate scraping code for

    Returns:
        str: The generated Python code for scraping the HTML
    """
    code_agent = Agent(
        "openai:gpt-4o",
        system_prompt=open("generate_code_prompt.txt").read(),
    )

    code = await code_agent.run(site_html)
    return code


@agent.tool_plain
def run_code(code, input_data):
    """Executes Python code using the Riza service and returns the output.

    Args:
        code (str): The Python code to execute
        input_data (str): Data to pass to the code via stdin

    Returns:
        str: The stdout output from executing the code, or error messages if execution failed
    """

    riza_client = Riza(api_key=os.environ["RIZA_API_KEY"])
    result = riza_client.command.exec(
        language="python",
        runtime_revision_id="01JKY2FCN25GW3EC8JMFN3KWX9",
        stdin=input_data,
        code=code,
    )
    if result.exit_code != 0:
        print("Code did not execute successfully. Error:")
        print(result.stderr)
    elif result.stdout == "":
        print(
            "Code executed successfully but produced no output. "
            "Ensure your code includes print statements to get output."
        )
    return result.stdout


@agent.tool_plain
def save_file(data, filename):
    """Saves data to a file.

    This function takes data and saves it to a file. For JSON data, it will
    serialize the Python object to JSON format.

    Args:
        data: The data to save to the file
        filename (str): The path where the file should be saved

    Example:
        >>> data = {"key": "value"}
        >>> save_file(data, "output.json")
        >>> text = "Hello world"
        >>> save_file(text, "output.txt")
    """
    path = "files/" + filename
    with open(path, "w") as f:
        json.dump(data, f)


@agent.tool_plain
def load_file(filename):
    """Loads data from a file.

    This function reads data from a file and returns it. For JSON files, it will
    deserialize into a Python object. For other files, returns the raw text content.

    Args:
        filename (str): The path to the file to load

    Returns:
        Union[dict, str]: The data from the file - either a dict for JSON or raw text
    """
    path = "files/" + filename
    with open(path, "r") as f:
        if filename.endswith(".json"):
            return json.load(f)
        return f.read()


def log_messages(messages):
    """Convert agent messages to JSON-serializable format and save to file."""
    serialized = [
        {
            "role": m.role if hasattr(m, "role") else "unknown",
            "content": m.content if hasattr(m, "content") else str(m),
        }
        for m in messages
    ]
    with open("all_messages.json", "w") as f:
        json.dump(serialized, f, indent=2)


if __name__ == "__main__":
    url = "https://www.nba.com/stats/teams/boxscores"
    result = agent.run_sync(url)
    log_messages(result.all_messages())
    print(agent.data)
