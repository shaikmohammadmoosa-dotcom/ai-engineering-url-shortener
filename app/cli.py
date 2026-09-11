import click
import httpx

BASE_URL = "http://localhost:8000"


@click.group()
def cli():
    """AI-Assisted URL Shortener CLI Tool"""
    pass


@cli.command()
@click.argument("url")
@click.option("--custom", default=None, help="Custom short code")
@click.option("--ttl", default=30, help="TTL in days")
def shorten(url: str, custom: str, ttl: int):
    """Shorten a target URL"""
    payload = {"target_url": url, "custom_code": custom, "ttl_days": ttl}
    try:
        response = httpx.post(f"{BASE_URL}/shorten", json=payload)
        if response.status_code == 201:
            data = response.json()
            click.echo(f"Success! Short URL: {data['short_url']}")
        else:
            click.echo(f"Error ({response.status_code}): {response.json().get('detail')}")
    except Exception as e:
        click.echo(f"Failed to connect to service: {e}")


@cli.command()
@click.argument("code")
def analytics(code: str):
    """View analytics for a short code"""
    try:
        response = httpx.get(f"{BASE_URL}/analytics/{code}")
        if response.status_code == 200:
            data = response.json()
            click.echo(f"Short Code    : {data['short_code']}")
            click.echo(f"Target URL    : {data['target_url']}")
            click.echo(f"Click Count   : {data['click_count']}")
            click.echo(f"Created At    : {data['created_at']}")
            click.echo(f"Last Accessed : {data['last_accessed']}")
        else:
            click.echo(f"Error ({response.status_code}): {response.json().get('detail')}")
    except Exception as e:
        click.echo(f"Failed to connect to service: {e}")


if __name__ == "__main__":
    cli()