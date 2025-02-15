# Agent Plan

## Overview

This agent is designed to scrape websites, inspect the HTML, generate and execute code for extracting structured data, and then save the results. The agent will use the `run_code` function from `archive/code_runner.py` to safely execute code in a sandbox.

## Steps

1. **Input Handling & Website Scraping:**
   - Accept a target URL from the user.
   - Use Python's HTTP libraries (e.g., `requests`) to fetch the webpage HTML.
   - Handle errors like timeouts or 404 responses.

2. **HTML Inspection:**
   - Optionally parse the HTML with `BeautifulSoup` for a preliminary inspection.
   - Allow the agent to review the HTML before extraction.

3. **Code Generation for Data Extraction:**
   - Prepare a prompt detailing the task: extract structured data (e.g., JSON) from the HTML.
   - Use **gpt-4o** to generate Python code that performs the data extraction.
   - If needed, employ **Pydantic AI** for the agent framework to enable advanced tool calling.

4. **Executing the Extraction Code:**
   - Run the generated extraction code using `run_code` from `archive/code_runner.py` in a sandbox.
   - Pass the HTML content as input to the extraction code.
   - Capture the output (structured data in JSON or another format) or any errors.
   
   - **Feedback Mechanism:**
     - If the code execution fails (non-zero exit code or error message), capture the error message.
     - Pass the error message along with the previously generated code to **gpt-4o** as feedback.
     - Use the revised code output by **gpt-4o** to attempt a re-execution.
     - Repeat until the code executes successfully or a retry limit is reached.

5. **Saving the Results:**
   - Save the extracted structured data to a file using Python (e.g., with the `json` module).


6. **Agent Orchestration:**
   - Create a main agent module (like `main.py`) to orchestrate the workflow:
     - Accept and process the URL input.
     - Invoke the scraper.
     - Generate and execute code with the help of **gpt-4o**.
     - Save the extraction result.
   - Optionally integrate **pydanticAI** if advanced tool calling is needed.



---

This plan outlines the steps and required modules to build the agent that can scrape websites, generate data extraction code, execute it safely, and save the results. 