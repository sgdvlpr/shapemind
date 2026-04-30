from rich.console import Console
from rich.table import Table
from rich.text import Text
import uuid
import typer
from typing import List
from datetime import date, timedelta

console = Console()

from shapemind.db import get_db
from shapemind.utils import unique_prefixes, resolve_id
from shapemind.date_utils import parse_date, format_date, get_today_str

app = typer.Typer(help="Task management")

@app.command("add")
def add(title: str, due: str = typer.Option("today", "--due")):
    """
    Add a task with a title and due date.
    --due accepts:
    - "today" or "tomorrow"
    - Persian date in YYYY-MM-DD
    """
    
    due_date = parse_date(due)
    due_str = due_date.isoformat()  # "YYYY-MM-DD"
    id = uuid.uuid4().hex[:8] # short random ID

    conn = get_db()
    conn.execute("INSERT INTO tasks (id, title, due, status) VALUES (?, ?, ?, ?)", (id, title, due_str, "todo"))
    conn.commit()
    conn.close()

    # Show date for user feedback
    display_date = format_date(due_date)
    typer.echo(f"Added task: {title} (due {str(display_date)}) [ID: {id}]")

@app.command("ls")
def list(
    on: str = typer.Option(None, "--on", help="Tasks due exactly on this date"),
    before: str = typer.Option(None, "--before", help="Tasks due before this date"),
    after: str = typer.Option(None, "--after", help="Tasks due after this date"),
    status: str = typer.Option(None, "--status", help="Filter by status: todo / done /overdue"),
    sort: str = typer.Option("asc", "--sort", help="Sort by due date: asc or desc")           
):
    """
    List tasks filtered by date and/or status.
    """
    
    conn = get_db()
    c = conn.cursor()

    # Determine which filter is used
    query = "SELECT * FROM tasks"
    conditions = []
    params = []

    # Date filter
    if on:
        conditions.append("due = ?") 
        params.append(parse_date(on).isoformat())
    elif before:
        conditions.append("due < ?") 
        params.append(parse_date(before).isoformat())
    elif after:
        conditions.append("due > ?") 
        params.append(parse_date(after).isoformat())

    # Status filter
    if status:
        if status not in ("todo", "done", "overdue"):
            typer.echo("Invalid status. Use: todo / done / overdue")
            raise typer.Exit()
        conditions.append("status = ?")
        params.append(status)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Add ORDER By for sorting
    sort_order = "ASC" if sort.lower() == "asc" else "DESC"
    query += f" ORDER BY due {sort_order}"

    c.execute(query, params)    
    rows = c.fetchall()
    conn.close()

    if not rows:
        typer.echo("No tasks found.")
        return
    
    full_ids = [row["id"] for row in rows]
    prefix_len = unique_prefixes(full_ids)

    table = Table(title="📋 Your Tasks", header_style="bold cyan")
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("Title", style="bold", width=40)
    table.add_column("Due", style="cyan")
    table.add_column("Status", style="bold")

    for row in rows:
        display_id = row["id"][:prefix_len]
        gregorian_due = date.fromisoformat(row["due"])
        display_date = format_date(gregorian_due)
        
        # Apply colors based on status
        if row["status"] == "overdue":
            status_text = Text(row["status"], style="bold red")
        elif row["status"] == "done":
            status_text = Text(row["status"], style="bold green")
        else:
            status_text = Text(row["status"], style="yellow")
        
        table.add_row(display_id, row["title"], str(display_date), status_text)

    console.print(table)

@app.command("delete")
def delete(task_ids: List[str] = typer.Argument(None), all: bool = typer.Option(False, "--all", help="Delete ALL tasks")):
    """Delete one or more tasks by ID, or delete all tasks with --all
    """
    conn = get_db()
    c = conn.cursor()
    if all:
        confirm = typer.confirm("⚠️ Are you sure you want to delete ALL tasks?")
        if confirm:
            c.execute("DELETE FROM tasks")
            typer.echo("All tasks deleted.")
        else:
            typer.echo("Aborted.")
    elif task_ids:
        # Resolve prefixes into full IDs
        resolved_ids = [resolve_id(id) for id in task_ids]

        # delete multiple IDs
        placeholders = ",".join("?" for _ in resolved_ids)
        c.execute(f"DELETE FROM tasks WHERE id IN ({placeholders})", resolved_ids)    
        typer.echo(f"Deleted tasks: {', '.join(map(str, resolved_ids))}")
    else:
        typer.echo("Please provide task IDs or use --all.")
    
    conn.commit()
    conn.close()

@app.command("update")
def update(
    id: str = typer.Argument(..., help="ID of the task to update"),
    title: str = typer.Option(None, "--title", help="New title"),
    due: str = typer.Option(None, "--due", help="New due date (today / tomorrow or YYYY-MM-DD)"),
    status: str = typer.Option(None, "--status", help="New status: todo / done")
):
    """Update a task's title, due date, or status"""
    conn = get_db()
    c = conn.cursor()

    # Fetch current task
    c.execute("SELECT * FROM tasks WHERE id LIKE ?", (id + "%",))
    row = c.fetchone()
    if not row:
        typer.echo(f"Task {id} not found.")
        conn.close()
        raise typer.Exit()
    
    # Determine new values
    new_title = title if title else row["title"]

    if due:
        if due == "today":
            new_due = date.today()
        elif due == "tomorrow":
            new_due = date.today() + timedelta(days=1)
        else:
            new_due = parse_date(due)
    else:
        new_due = date.fromisoformat(row["due"])
    
    if status:
        if status not in ("todo", "done"):
            typer.echo("Invalid status. Use: todo / done")
            conn.close()
            raise typer.Exit()
        new_status = status
    else:
        new_status = row["status"]
    
    # Update in DB
    c.execute("UPDATE tasks SET title=?, due=?, status=? WHERE id LIKE ?", (new_title, new_due.isoformat(), new_status, id + "%"))
    conn.commit()
    conn.close()

    display_date = format_date(new_due)
    typer.echo(f"Task {id} updated. Title: '{new_title}', Due: '{str(display_date)}', Status: {new_status}")

def update_overdue():
    """Mark all tasks whose due date has passed as 'overdue'."""
    conn = get_db()
    today_str = date.today().isoformat()
    conn.execute("UPDATE tasks SET status='overdue' WHERE status='todo' AND due < ?", (today_str,))
    conn.commit()
    conn.close()
