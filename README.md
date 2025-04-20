# 📸 URL Screenshot to PDF Converter

This Python script captures full-page screenshots of websites listed in a `urls.txt` file, then compiles them into a single PDF. Each page of the PDF includes a clickable URL watermark at the top for easy reference.

## 🧰 Features

- Full-page screenshots using **Playwright**
- Retry mechanism for failed page loads (up to 5 attempts)
- Automatic conversion of screenshots to **PDF**
- **Clickable URL** watermark on each PDF page
- Adjustable image-to-mm conversion using PIL and ReportLab

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/url-screenshot-pdf.git
cd url-screenshot-pdf
```

### 2. Install Dependencies

Make sure you have Python 3.7+ and then run:

```bash
pip install -r requirements.txt
playwright install
```

#### `requirements.txt`

```txt
playwright
pillow
reportlab
```

### 3. Prepare the Input File

Create a `urls.txt` file in the root directory and list your URLs line by line:

```txt
https://example.com
https://another-example.com
```

### 4. Run the Script

```bash
python script.py
```

Output:
- Screenshots are saved in the `screenshots/` folder.
- A file named `retry_watermarked_output.pdf` is generated with the watermarked screenshots.

## 🧾 Example Output

Each page in the resulting PDF:
- Is sized to fit the screenshot exactly
- Displays the URL as a clickable blue watermark at the top

## 🔧 Customization

- Change the output PDF filename: edit the `output_pdf` variable in `main()`.
- Update screenshot resolution or headless behavior via `playwright` options.
- Modify watermark placement or style in the `add_image_with_url_to_pdf()` function.

## 🛡 License

This project is licensed under the [MIT License](LICENSE). Feel free to use and modify as needed.

## ✍️ Author

Created by [sudomofo](https://github.com/sudomofo) – PRs and issues welcome!
