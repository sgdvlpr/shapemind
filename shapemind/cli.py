import typer
from shapemind import tasks, resources
from shapemind.db import init_db
from shapemind.tasks import update_overdue
from shapemind.config import get_config, set_config

app = typer.Typer(help="Shapemind CLI - tasks and spaced repetition")

# Register subcommands
app.add_typer(tasks.app, name="task")
app.add_typer(resources.app, name="category")

@app.command("config")
def config_command(
        calendar: str = typer.Argument(
            None, 
            help="Set calendar: persian or gregorian",
            autocompletion=lambda: ["persian", "gregorian"]), 
        show: bool = typer.Option(False, "--show", help="Show current configuration")):
    """View or change Shapemind configuration.
    
    Examples:
    shapemind config            # Show current calendar
    shapemind config persian    # Switch to Persian calendar
    shapmeind config gregorian  # Switch to Gregorian calendar
    """

    if show:
        # Show all configuration
        config = get_config()
        typer.echo("\n Shapemind Configuration")
        typer.echo("=" * 30)
        for key, value in config.items():
            typer.echo(f" {key}: {value}")
        typer.echo("")
        return
    
    if calendar is None:
        # Just show current calendar setting
        config = get_config()
        typer.echo(f"Current calendar: {config['calendar']}")
        typer.echo(f"To change: shapemind config [persian|gregorian]")
        return
    
    if calendar not in ("persian", "gregorian"):
        typer.echo(f"Error: '{calendar}' is not valid. Only 'persian' or 'gregorian' is supported.")
        raise typer.Exit(1)
    
    set_config("calendar", calendar)
    typer.echo(f"Calendar switched to {calendar}")

def main():
    init_db()
    update_overdue()  # auto mark overdue
    app()

if __name__ == "__main__":
    main()
