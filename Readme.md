# Freelance Auto-Bidder

Automates the bidding process across freelancing platforms by intelligently matching user preferences, scraping profile data, evaluating project relevance using an LLM, and generating custom bids and cover letters.

## Features
- Auto-login to freelancing platforms using user credentials.
- Scrape user project data from profile.
- Analyze new jobs using LLM and past projects as context.
- Automatically generate appropriate bid rates and cover letters.
- Notify users when a relevant project is found.
- In-built CAPTCHA handling with Tesseract.

## Project Structure
```
freelance-auto-bidder/
├── app.py                  # Flask API to interact with the system
├── login.py                # Login user to freelancing site
├── scrap_project.py        # Scrape user's existing projects
├── main.py                 # Main controller for login and scraping
├── templates/
│   └── index.html          # UI for login input
├── tools/
│   ├── captcha_solver.py   # Solves CAPTCHA using OCR
│   └── tools_dependencies/
│       └── tesseract/      # Embedded Tesseract binaries and data
```

## Setup Instructions
1. Clone the repository.
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the Flask server:
```bash
python app.py
```
4. Open your browser and navigate to `http://localhost:5000` to access the login UI.

## Future Scope
- Multi-platform support for Upwork, Fiverr, etc.
- User dashboard for managing bid history.
- Persistent database support for larger memory context.

## License
This project is under the MIT License.

