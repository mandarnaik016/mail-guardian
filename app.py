import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from rich.console import Console
from rich.table import Table

from utils.helper import colorize, process_email
from utils.logger import logger

EML_DIR = Path("./eml")
MAX_WORKERS = 4


def main():
    table = Table(title="Email Classifications")
    table.add_column("Subject", justify="left", style="cyan")
    table.add_column("Spam", justify="right")
    table.add_column("Phishing", justify="right")
    table.add_column("Time (s)", justify="right")

    start = time.perf_counter()
    times = []
    processed = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(process_email, path): path for path in EML_DIR.glob("*.eml")
        }
        for future in as_completed(futures):
            try:
                result = future.result()
                if not result:
                    continue
                response, elapsed = result
                times.append(elapsed)
                processed += 1
                table.add_row(
                    response["subject"],
                    colorize(response["spam"]),
                    colorize(response["phishing"]),
                    f"{elapsed:.2f}",
                )
            except Exception:  # NOQA
                logger.exception("Failed: %s", futures[future].name)

    console = Console()
    console.print(table)
    console.print(f"\nProcessed: {processed}")
    console.print(f"Total time: {time.perf_counter() - start:.2f}s")
    console.print(
        f"Average request time: {sum(times) / len(times):.2f}s"
        if times
        else "Average request time: N/A"
    )


if __name__ == "__main__":
    main()
