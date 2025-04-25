

# Verification Suite 
# *   **Purpose:** Combined script for linting, console log analysis, and render testing.
# *   **Usage:** `python _20_user-scripts/verification-suite.py --url [URL]`
# *   **Arguments:**
#     *   `--url`: Required target URL.
#     *   `--log-prompt`: Optional custom prompt for console log analysis.
#     *   `--no-console`: Disable console log analysis.
# *   **Output:** Combined results (Console Analysis, Render Test, Lint (`npm run lint`)).
# *   **Workflow:** Run after code changes; address *new* errors/warnings before completing the task set.



import argparse
import asyncio
import os
import pathlib
import subprocess
import shutil
import google.generativeai as genai
# type: ignore
from playwright.async_api import async_playwright, Error as PlaywrightError
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Default Prompts ---
DEFAULT_LOG_PROMPT = """\
## Log Analysis:
    Analyze the provided console logs and generate a concise summary outline.
    - At top of summary, provide total number of console log lines received. Include discrete counts for each type (e.g., "A Total; B Errors, C Warnings, D Info, E Debug, F Logs").
    - Identify and list all critical errors (JavaScript exceptions, failed network requests).
    - For each critical error, provide a brief log snippet and mention any immediately preceding/subsequent logs that might indicate the cause.
    - Specifically list any 404 Not Found errors, including the requested asset URL.
    - Summarize recurring warnings or informational messages. Use counts for frequency (e.g., "Warning X appeared 15 times").
    - Note any significant deviations from expected log patterns or messages that seem anomalous.
    - Use ranges where applicable (e.g., "Processed items 100-200").
    - Be concise. **Ensure the total length of your summary is significantly shorter than the original logs.**
    - Do not provide recommendations, insights, implications, solutions, or explanations.
"""

# --- Constants ---
GEMINI_API_KEY_ENV_VAR = "GEMINI_API_KEY"
GEMINI_MODEL_NAME = "gemini-2.5-flash-preview-04-17"

async def check_render(url: str) -> str:
    """Check if page renders successfully by verifying root element visibility."""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                is_visible = await page.locator('div#root').is_visible()
                
                if is_visible:
                    return "Render Check: PASSED - Root element (div#root) found."
                else:
                    return "Render Check: FAILED - Root element (div#root) not found."
                    
            except PlaywrightError as e:
                return f"Render Check: FAILED - Playwright error: {str(e)}"
            finally:
                await browser.close()
                
    except Exception as e:
        return f"Render Check: FAILED - Unexpected error: {str(e)}"

async def analyze_page(url: str, log_prompt: str, no_console: bool) -> str:
    """Navigates to a URL, captures logs, and sends to Gemini for analysis."""
    logs = []
    analysis_result = "Analysis could not be completed."

    try:
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                if not no_console:
                    page.on("console", lambda msg: logs.append(f"[{msg.type}] {msg.text}"))

                await page.goto(url, wait_until="load", timeout=60000)
                await browser.close()

            except PlaywrightError as e:
                print(f"Playwright error: {e}", file=sys.stderr)
                return f"Error during browser automation: {e}"
            except Exception as e:
                print(f"Unexpected error during Playwright operation: {e}", file=sys.stderr)
                return f"Unexpected error during browser automation: {e}"

        log_text = "\n".join(logs) if logs and not no_console else "Console log analysis disabled."
        combined_log_prompt = f"{log_prompt}\n\n{log_text}".replace('\\n', '\n')

        api_key = os.getenv(GEMINI_API_KEY_ENV_VAR)
        if not api_key:
            print(f"Error: Gemini API key not found in environment variable '{GEMINI_API_KEY_ENV_VAR}'", file=sys.stderr)
            return f"Error: Missing API Key. Set the '{GEMINI_API_KEY_ENV_VAR}' environment variable."

        genai.configure(api_key=api_key)

        try:
            model = genai.GenerativeModel(GEMINI_MODEL_NAME)
            content = []
            if not no_console:
                content.append(combined_log_prompt)
            
            if not content:
                analysis_result = "Analysis skipped (console analysis disabled)"
            else:
                response = await model.generate_content_async(content)
                if response.parts:
                    analysis_result = "".join(part.text for part in response.parts if hasattr(part, 'text'))
                elif hasattr(response, 'text'):
                    analysis_result = response.text
                else:
                    analysis_result = "Received an empty or unexpected response format from Gemini."
                    print("Warning: Unexpected Gemini response format.", file=sys.stderr)

        except Exception as e:
            print(f"Error calling Gemini API: {e}", file=sys.stderr)
            error_detail = str(e)
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                error_detail += f"\nResponse: {e.response.text}"
            analysis_result = f"Error during Gemini API call: {error_detail}"

    finally:
        pass

    return analysis_result

async def main():
    parser = argparse.ArgumentParser(description="Analyze a webpage using Playwright and Gemini.")
    parser.add_argument("--url", required=True, help="URL of the webpage to analyze.")
    parser.add_argument("--log-prompt", default="", help="Custom prompt to append to default for console log analysis.")
    parser.add_argument("--no-console", action="store_true", help="Disable console log capture and analysis")

    args = parser.parse_args()

    log_prompt = DEFAULT_LOG_PROMPT
    if args.log_prompt:
        log_prompt += f"\n\n**Critically:**\n{args.log_prompt}"

    print("Starting verification suite...")
    
    # Run all tasks in parallel
    analysis_task = asyncio.create_task(analyze_page(args.url, log_prompt, args.no_console))
    render_task = asyncio.create_task(check_render(args.url))
    
    def run_lint():
        try:
            project_root = str(pathlib.Path(__file__).parent.parent)
            os.chdir(project_root)
            
            npm_cmd = "npm.cmd" if os.name == 'nt' else "npm"
            npm_path = shutil.which(npm_cmd)
            
            if not npm_path:
                return ("npm not found in PATH", "")
            
            result = subprocess.run(
                [npm_path, "run", "lint"],
                capture_output=True,
                text=True,
                cwd=project_root
            )
            return (result.stdout, result.stderr)
        except Exception as e:
            return (f"Error running npm lint: {str(e)}", "")
    
    lint_task = asyncio.get_event_loop().run_in_executor(None, run_lint)
    
    # Wait for all tasks to complete
    analysis_result, render_result, lint_result = await asyncio.gather(
        analysis_task, 
        render_task, 
        lint_task
    )
    
    # Print results
    print(analysis_result)
    print("\n## Render Check:")
    print(render_result)
    print("\n## Lint Analysis:")
    lint_stdout, lint_stderr = lint_result
    print(lint_stdout)
    if lint_stderr:
        print(lint_stderr, file=sys.stderr)
    
    print("--- End ---")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred in the main execution: {e}", file=sys.stderr)
        sys.exit(1)