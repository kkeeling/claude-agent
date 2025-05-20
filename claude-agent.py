#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "rich",
#   "click",
#   "halo",
#   "python-dotenv"
# ]
# ///

import os
import sys
import subprocess
import json
import click
from rich.console import Console
from rich.syntax import Syntax
from rich import print as rprint
from halo import Halo
from dotenv import load_dotenv

# Initialize rich console
console = Console()

# Load environment variables from .env file
load_dotenv()

# Validate Claude executable path early
def validate_claude_path():
    claude_executable = os.getenv("CLAUDE_PATH")
    if not claude_executable:
        console.print("[bold red]Error: CLAUDE_PATH environment variable not set.[/bold red]")
        console.print("[bold red]Please create a .env file with CLAUDE_PATH=/path/to/claude[/bold red]")
        console.print("[bold red]See .env.example for reference.[/bold red]")
        sys.exit(1)
        
    # Check if the executable exists and is executable
    if not os.path.isfile(claude_executable) or not os.access(claude_executable, os.X_OK):
        console.print(f"[bold red]Error: Claude executable not found or not executable at {claude_executable}[/bold red]")
        console.print("[bold red]Please check your CLAUDE_PATH environment variable.[/bold red]")
        sys.exit(1)
    
    return claude_executable

# Validate CLAUDE_PATH before anything else
claude_executable = validate_claude_path()

@click.command()
@click.argument('working_directory', required=False)
@click.option('--claude-md', help='Path to CLAUDE.md file containing Claude rules (optional)')
def main(working_directory, claude_md):
    """Process todo list from a markdown file using Claude Code."""
    
    # If no working directory provided, prompt for it
    if not working_directory:
        working_directory = click.prompt("Please enter a working directory path", 
                                         type=click.Path(exists=True, file_okay=False, dir_okay=True))
    
    # Normalize and validate the working directory
    working_directory = os.path.abspath(working_directory)
    if not os.path.isdir(working_directory):
        console.print(f"[bold red]Error: {working_directory} is not a valid directory.[/bold red]")
        sys.exit(1)
    
    # Check for todo.md file
    todo_file_path = os.path.join(working_directory, "todo.md")
    if not os.path.isfile(todo_file_path):
        console.print(f"[bold red]Error: Cannot find todo.md in {working_directory}[/bold red]")
        sys.exit(1)
        
    # Use the claude_prompt.md from the project root (script directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_file_path = os.path.join(script_dir, "claude_prompt.md")
    if not os.path.isfile(prompt_file_path):
        console.print(f"[bold red]Error: Cannot find claude_prompt.md in {script_dir}[/bold red]")
        sys.exit(1)
    
    # Read the prompt template
    with open(prompt_file_path, 'r') as f:
        prompt_template = f.read()
        
    # Handle Claude rules from CLAUDE.md file
    if claude_md:
        claude_md_path = os.path.abspath(claude_md)
        if os.path.isfile(claude_md_path):
            with open(claude_md_path, 'r') as f:
                claude_rules = f.read()
            console.print(f"[bold green]Using Claude rules from:[/bold green] [yellow]{claude_md_path}[/yellow]")
        else:
            console.print(f"[bold yellow]Warning: CLAUDE.md file not found at {claude_md_path}[/bold yellow]")
            claude_rules = ""
    else:
        # Ask if user wants to provide a CLAUDE.md file
        if click.confirm("Do you want to provide a CLAUDE.md file with custom rules?", default=False):
            claude_md_path = click.prompt(
                "Please enter the path to your CLAUDE.md file",
                type=click.Path(exists=True, file_okay=True, dir_okay=False)
            )
            with open(claude_md_path, 'r') as f:
                claude_rules = f.read()
            console.print(f"[bold green]Using Claude rules from:[/bold green] [yellow]{claude_md_path}[/yellow]")
        else:
            claude_rules = ""
            console.print("[bold yellow]No Claude rules provided, proceeding without custom rules.[/bold yellow]")
    
    # Prepare the prompt with the working directory and rules
    if claude_rules:
        prompt = prompt_template.replace("{{working_folder}}", working_directory).replace("{{claude_rules}}", claude_rules)
    else:
        # Remove the claude rules section entirely if no rules are provided
        prompt = prompt_template.replace("{{working_folder}}", working_directory).replace("{{claude_rules}}", "")
    
    # Define the allowed tools for Claude
    allowed_tools = [
        # Standard Claude Code tools
        "Bash",
        "Edit",
        "View",
        "GlobTool",
        "GrepTool",
        "LSTool",
        "BatchTool",
        "AgentTool",
        "WebFetchTool",
        "Write",
        # Add any other tools you might need
    ]

    # Execute the Claude command with stream-json output format
    try:
        spinner = Halo(text=f'Starting Claude Code to process todos from: {working_directory}', spinner='dots')
        spinner.start()

        # Claude executable was already validated at the beginning of the script
        
        cmd = [
            claude_executable,
            "--print",  # Explicitly use --print instead of -p for clarity
            "--verbose",  # Required when using --output-format=stream-json
            "--output-format", "stream-json",
            "--allowedTools",
        ] + allowed_tools + ["--", prompt]  # Use -- to separate flags from the prompt

        # Start the process and read output as it comes
        spinner.stop()
        console.print(f"[bold blue]🤖 Starting Claude Code to process todos from:[/bold blue] [yellow]{working_directory}[/yellow]")
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line buffered
        )

        # Process and display JSON output in real-time
        console.print("\n[bold green]📊 Streaming Claude output:[/bold green]")
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break

            syntax = Syntax(line, "json", theme="monokai", line_numbers=False)
            console.print(syntax)

        # Check for any errors
        stderr = process.stderr.read()
        if stderr:
            console.print(f"[bold red]⚠️ Error output from Claude:[/bold red]\n{stderr}")

        # Get return code
        return_code = process.wait()
        if return_code == 0:
            console.print(f"[bold green]✅ Claude Code completed successfully[/bold green]")
        else:
            console.print(
                f"[bold red]❌ Claude Code failed with exit code: {return_code}[/bold red]"
            )
            sys.exit(return_code)

    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]❌ Error executing Claude Code: {str(e)}[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]❌ Unexpected error: {str(e)}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()