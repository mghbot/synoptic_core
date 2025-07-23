"""Command-line interface for Synoptic Core."""

import click
import json
from rich.console import Console
from rich.table import Table

from synoptic_core import SynopticEngine
from synoptic_core.models.rule import Rule

console = Console()


@click.group()
@click.version_option()
def cli():
    """Synoptic Core - Symbolic Logic Engine."""
    pass


@cli.command()
@click.argument('text')
@click.option('--rules', '-r', type=click.Path(exists=True), help='Path to JSON rules file')
@click.option('--output-format', '-o', type=click.Choice(['simple', 'verbose', 'json']), 
              default='simple', help='Output format')
@click.option('--encoding', '-e', default='utf-8', help='Text encoding')
def process(text, rules, output_format, encoding):
    """Process text through the symbolic logic engine."""
    
    try:
        # Initialize engine
        engine = SynopticEngine()
        
        # Load custom rules if provided
        custom_rules = None
        if rules:
            with open(rules, 'r') as f:
                rules_data = json.load(f)
                custom_rules = [Rule.from_dict(r) for r in rules_data]
        
        # Process text
        result = engine.process(text, custom_rules)
        
        # Display output based on format
        if output_format == 'json':
            console.print_json(result.to_json())
        elif output_format == 'verbose':
            display_verbose_output(result)
        else:
            display_simple_output(result)
            
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise click.Abort()


def display_simple_output(result):
    """Display results in simple format."""
    console.print("\n[bold]Logic Statements:[/bold]")
    for stmt in result.statements:
        console.print(f"  • {stmt.format()}")


def display_verbose_output(result):
    """Display results in verbose format with table."""
    table = Table(title="Logic Statements")
    
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    table.add_column("Subject", style="green")
    table.add_column("Predicate", style="yellow")
    table.add_column("Object", style="blue")
    table.add_column("Confidence", style="red")
    
    for i, stmt in enumerate(result.statements):
        table.add_row(
            str(i + 1),
            stmt.statement_type,
            stmt.subject,
            stmt.predicate,
            stmt.object,
            f"{stmt.confidence:.2f}"
        )
    
    console.print(table)


@cli.command()
def list_rules():
    """List available built-in rules."""
    engine = SynopticEngine()
    rules = engine.rule_engine.get_builtin_rules()
    
    table = Table(title="Built-in Rules")
    table.add_column("Name", style="cyan")
    table.add_column("Pattern", style="green")
    table.add_column("Description", style="yellow")
    
    for rule in rules:
        table.add_row(rule.name, rule.pattern, rule.description)
    
    console.print(table)


if __name__ == "__main__":
    cli()