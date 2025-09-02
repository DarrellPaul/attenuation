import typer

app = typer.Typer()

@app.command()
def total(
    rec_profile: str = "current",
    frequency_hz: float = typer.Option(..., help="Frequency in Hz"),
    
)