import random
import time
from rich.live import Live
from rich.table import Table
from rich.console import Console

console=Console()

def generate_table() -> Table:
    """Make a new table."""
    table = Table()
    table.add_column("ID")
    table.add_column("Value")
    table.add_column("Status")

    for row in range(random.randint(2, 6)):
        value = random.random() * 100
        table.add_row(f"{row}", f"{value:3.2f}", "[red]ERROR" if value < 50 else "[green]SUCCESS")
    return table

with Live(generate_table(), refresh_per_second=4) as live:
    with console.status("working"):
        estado=True
        # for _ in range(40):
        #     print(f'iteracion {_}')
        cant=0

        while estado:

            time.sleep(5)
            live.update(generate_table())
            
            cant+=1
            estado= False if cant==100 else True