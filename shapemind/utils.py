import jdatetime
from datetime import date
import typer
from shapemind.db import get_db

def unique_prefixes(ids):
    """
    Given a list of full IDs, return the minimal number of characters 
    required so that all truncated IDs are unique.
    """

    if not ids:
        return 0
    
    max_len = len(ids[0])
    for length in range(1, max_len + 1):
        truncated = [i[:length] for i in ids]
        if len(truncated) == len(set(truncated)):
            return length       
    return max_len # fallback: use full length

def resolve_id(prefix: str) -> str:
    """
    Resolve a user-provided prefix into a full task ID.
    Raises an error if no match or multiple matches exist.
    """

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id FROM tasks WHERE id LIKE ?", (prefix + "%"))
    match_ids = [row["id"] for row in c.fetchall()]
    conn.close()

    if not match_ids:
        typer.echo(f"No task found with id '{prefix}'")
        raise typer.Exit()
    
    if len(match_ids) > 1:
        typer.echo(f"Ambiguous id '{prefix}' matches multiple tasks: {match_ids}")
        raise typer.Exit()
    
    return match_ids[0] # the unique match

def parse_due_date(date_str: str):
    """
    Parse date from Persian calendar input like '1404-07-09'.
    Returns a datetime.date object (Gregorian)
    """

    try:
        jd = jdatetime.date.fromisoformat(date_str)
        return jd.togregorian()
    except ValueError:
        raise ValueError("Invalid Persian date. Use YYYY-MM-DD")
