"""
Take screenshots of the split view with each dataset for paper figures.
Requires: python http.server running on port 7999
Usage: python scripts/take_screenshots.py
"""
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

BASE_URL = "http://localhost:7999"
DATASETS = {
    "hourclock": "datasets/hourclock.json",
    "surveillance": "datasets/surveillance.json",
    "diehard": "datasets/diehard.json",
}
OUTPUT_DIR = Path("Papers/figures")


async def take_screenshots():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        for name, dataset_path in DATASETS.items():
            print(f"Taking screenshot for {name}...")
            page = await browser.new_page(viewport={"width": 1920, "height": 1080})

            # Load split view
            await page.goto(f"{BASE_URL}/splitview.html")
            await page.wait_for_timeout(1000)

            # Read dataset and send to both iframes via postMessage
            dataset_content = Path(dataset_path).read_text()

            # Upload file via the file input
            file_input = page.locator("#splitInput")
            abs_path = str(Path(dataset_path).resolve())
            await file_input.set_input_files(abs_path)

            # Wait for rendering
            await page.wait_for_timeout(4000)

            # Take full page screenshot
            await page.screenshot(
                path=str(OUTPUT_DIR / f"{name}_split.png"),
                full_page=False,
            )

            # Also take individual view screenshots
            # Graph view
            graph_page = await browser.new_page(viewport={"width": 1200, "height": 800})
            await graph_page.goto(f"{BASE_URL}/graphview.html")
            await graph_page.wait_for_timeout(1000)
            file_input_g = graph_page.locator("#input")
            await file_input_g.set_input_files(abs_path)
            await graph_page.wait_for_timeout(4000)
            await graph_page.screenshot(
                path=str(OUTPUT_DIR / f"{name}_graph.png"),
                full_page=False,
            )
            await graph_page.close()

            # Matrix view
            matrix_page = await browser.new_page(viewport={"width": 900, "height": 900})
            await matrix_page.goto(f"{BASE_URL}/matrixview.html")
            await matrix_page.wait_for_timeout(1000)
            file_input_m = matrix_page.locator("#input")
            await file_input_m.set_input_files(abs_path)
            await matrix_page.wait_for_timeout(3000)
            await matrix_page.screenshot(
                path=str(OUTPUT_DIR / f"{name}_matrix.png"),
                full_page=False,
            )
            await matrix_page.close()

            await page.close()

        await browser.close()

    print(f"Screenshots saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(take_screenshots())
