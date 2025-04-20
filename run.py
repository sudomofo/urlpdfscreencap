import os
import asyncio
from playwright.async_api import async_playwright
from PIL import Image
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas

async def capture_screenshot(url, output_path, retries=5):
    """Capture a full-page screenshot of a URL with retry logic."""
    for attempt in range(1, retries + 1):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                print(f"Attempt {attempt}: Capturing screenshot for: {url}")
                await page.goto(url, timeout=60000)
                await page.screenshot(path=output_path, full_page=True)
                print(f"Screenshot saved: {output_path}")
                await browser.close()
                return  # Exit if successful
        except Exception as e:
            print(f"Attempt {attempt} failed for {url}: {e}")
            if attempt == retries:
                print(f"Skipping {url} after {retries} retries.")
        finally:
            try:
                await browser.close()
            except:
                pass

def add_image_with_url_to_pdf(pdf_path, url_image_pairs):
    """Create a PDF with images and clickable URL watermarks."""
    c = canvas.Canvas(pdf_path)

    for url, image_path in url_image_pairs:
        try:
            # Open the image and get its dimensions
            image = Image.open(image_path)
            img_width_px, img_height_px = image.size

            # Convert pixels to mm (DPI default is 96)
            dpi = 96
            img_width_mm = img_width_px / dpi * 25.4
            img_height_mm = img_height_px / dpi * 25.4

            # Set page size to match image dimensions
            c.setPageSize((img_width_mm * mm, img_height_mm * mm))

            # Draw the image
            c.drawImage(image_path, 0, 0, width=img_width_mm * mm, height=img_height_mm * mm)

            # Add a clickable URL watermark at the top
            c.setFont("Helvetica", 12)
            c.setFillColorRGB(0, 0, 1)  # Set text color to blue
            c.drawString(10, img_height_mm * mm - 15, url)  # Draw the URL
            c.linkURL(url, (10, img_height_mm * mm - 15, img_width_mm * mm - 10, img_height_mm * mm - 5), relative=0)

            # Add the page
            c.showPage()
        except Exception as e:
            print(f"Failed to add image {image_path} to PDF: {e}")

    # Save the PDF
    c.save()

async def main():
    input_file = "urls.txt"  # File containing URLs, one per line
    screenshot_dir = "screenshots"  # Directory to save screenshots
    output_pdf = "retry_watermarked_output.pdf"  # Final PDF file

    # Read URLs from the file
    with open(input_file, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]

    # Ensure the screenshot directory exists
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    # Capture screenshots
    url_image_pairs = []
    for index, url in enumerate(urls, start=1):
        output_path = os.path.join(screenshot_dir, f"screenshot_{index}.png")
        await capture_screenshot(url, output_path, retries=5)
        url_image_pairs.append((url, output_path))

    # Create PDF with images and clickable URL watermarks
    add_image_with_url_to_pdf(output_pdf, url_image_pairs)
    print(f"PDF created: {output_pdf}")

if __name__ == "__main__":
    asyncio.run(main())
