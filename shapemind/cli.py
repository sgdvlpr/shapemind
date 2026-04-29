import typer
from shapemind import tasks, resources
from shapemind.db import init_db
from shapemind.tasks import update_overdue

app = typer.Typer(help="Shapemind CLI - tasks and spaced repetition")

# Register subcommands
app.add_typer(tasks.app, name="task")
app.add_typer(resources.app, name="category")

def main():
    init_db()
    update_overdue()  # auto mark overdue
    app()

if __name__ == "__main__":
    main()
