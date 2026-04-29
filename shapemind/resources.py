from rich.console import Console
from rich.table import Table
from rich.text import Text
import uuid
import typer
from datetime import datetime, timezone
from shapemind.db import get_db

console = Console()
app = typer.Typer(help="Resource management")

# ----------------Helper functions----------------------
def _now_iso():
    return datetime.now(timezone.utc).isoformat()

def short_id():
    return uuid.uuid4().hex[:8]

#-----------------------CATEGORY------------------------
@app.command("add")
def add_category(name: str):
    conn = get_db()
    id = short_id()
    try:
        conn.execute(
            "INSERT INTO categories (id, name, created_at, updated_at) VALUES (?, ?, ?, ?)", 
            (id, name, _now_iso(), _now_iso())
        )
        conn.commit()
        typer.echo(f"Added category '{name}' [ID: {id}]")
    except Exception as e:
        typer.echo(f"Error: {e} ")
    finally:
        conn.close()

@app.command("list")
def list_categories():
    conn = get_db()
    rows = conn.execute("SELECT * FROM categories ORDER BY updated_at DESC").fetchall()
    conn.close()

    if not rows:
        typer.echo("No categories found.")
        return
    table = Table(title = "Categories")
    table.add_column("ID", style="dim")
    table.add_column("Name", style="bold")
    table.add_column("Updated at", style="cyan")
    table.add_column("Created_at", style="cyan")

    for r in rows:
        table.add_row(r["id"], r["name"], r["updated_at"], r["created_at"])
    
    console.print(table)

@app.command("rename")
def rename_category(id: str, new_name: str):
    conn = get_db()
    now = _now_iso()
    c = conn.cursor()
    c.execute("UPDATE categories SET name=?, updated_at=? WHERE id=?", (new_name, now, id))
    
    if c.rowcount == 0:
        typer.echo(f"No category found with ID {id}")
    else:
        conn.commit()
        typer.echo(f"Renamed category {id} -> {new_name}")
    
    conn.close()

@app.command("delete")
def delete_category(id: str):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM categories WHERE id=?", (id,))
    
    if c.rowcount == 0:
        typer.echo(f"No category found with ID {id}")
    else:
        conn.commit()
        typer.echo(f"Deleted category {id}")
    
    conn.close()

