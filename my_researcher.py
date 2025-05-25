import asyncio
import typer
import os
import subprocess
from typing import Any
import markdown
from gpt_researcher import GPTResearcher

app = typer.Typer()


async def submit_query(researcher: GPTResearcher):
    # Conduct research on the given query
    await researcher.conduct_research()
    # Write the report
    return await researcher.write_report()


def write_html_report(report: Any, output_path: str):
    md = markdown.markdown(str(report))
    with open(output_path, "w") as f:
        f.write(md)
        print(f"Report written to {output_path}")


def write_report(report: Any, output_path: str):
    with open(output_path, "w") as f:
        f.write(str(report))
        print(f"Report written to {output_path}")


@app.command()
def main(
    query: str = typer.Option(None, help="The query string"),
    input_prompt: str = typer.Option(None, help="Filename for input prompt"),
    output_file: str = typer.Option(None, help="Filename for output file"),
    report_type: str = typer.Option("detailed_report", help="Type of report"),
    output_format: str = typer.Option(
        "md", help="Output format: md | html | json | yaml"
    ),
):
    queries_dir = "queries"
    if not os.path.exists(queries_dir):
        os.makedirs(queries_dir)
        print(f"Created directory: {queries_dir}")

    if not query and input_prompt:
        try:
            input_prompt_path = os.path.join(queries_dir, input_prompt)
            with open(input_prompt_path, "r") as f:
                query = f.read()
        except Exception as e:
            print(f"Error reading input prompt file: {e}")
            raise
    elif not query:
        print("No query provided.")
        return

    output_dir = "output"
    format_dir = os.path.join(output_dir, output_format)
    if not os.path.exists(format_dir):
        os.makedirs(format_dir)
        print(f"Created directory: {format_dir}")

    if not output_file:
        output_file = "report"

    output_file_path = os.path.join(format_dir, f"{output_file}.{output_format}")

    try:
        researcher = GPTResearcher(query=query, report_type=report_type)
        report = asyncio.run(submit_query(researcher))

        if output_format == "md":
            write_report(report, output_file_path)
        elif output_format == "html":
            write_html_report(report, output_file_path)
        else:
            print(f"Unsupported output format: {output_format}")
            return
    except Exception as e:
        print(f"An error occurred during report generation: {e}")
        raise

    print("Program complete.")
    try:
        subprocess.run(["open", output_file_path])
        subprocess.run(["vim", output_file_path])
    except Exception as e:
        print(f"Error opening the output file: {e}")
        raise


if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print(f"A critical error occurred: {e}")
        raise
