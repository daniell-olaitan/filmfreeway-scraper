# FilmFreeway Festival Scraper

## Overview
This project is a web scraper designed to extract festival details from [FilmFreeway](https://filmfreeway.com/festivals), including festival names, descriptions, deadlines, awards, categories, and important dates using Playwright, Asyncio, and Mistral AI for structured data extraction. The scraper gathers at least **2,200 festival entries** by navigating through paginated results and individual festival pages.

## **Methodology**
### **Data Extraction (Web Scraping)**
- The scraper, built with **Playwright**, fetches festival details directly from the listing page (festival name, deadlines).
- For each festival, it navigates to its **individual page** to extract the **"About"** and **"Awards & Prizes"** sections.

### **AI-Powered Data Processing (mistral-small-latest Model)**
- The extracted text is **fed into Mistral-small-latest**, an AI model prompted to extract:
  - **Festival Info** (A summarized, high-quality description of the festival).
  - **Important Dates**.
  - **Awards** (Categories of awards given).
  - **Categories** (Festival genres or types).
- The AI output is validated against the required JSON schema.

---

## Tech Stack
- **Python >= 3.9**
- **Playwright**
- **MistralAI**
- **JSONL**

---

## Installation & Setup

### **Clone the Repository**
```bash
  git clone https://github.com/daniell-olaitan/filmfreeway-scraper.git
  cd filmfreeway-scraper
```

### **Create a Virtual Environment**
Run the following command to create a virtual environment:

```bash
python -m venv venv
```

### **Activate the Virtual Environment**

- **Windows (Command Prompt)**
```bash
venv\Scripts\activate
```
- **Windows (PowerShell)**
```powershell
venv\Scripts\Activate.ps1
```
- **Mac/Linux**
```bash
source venv/bin/activate
```

### **Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Install Playwright browsers (if not installed):**
```bash
playwright install
```

### **Set Up Environment Variables**
This project uses an `.env` file for API keys and configurations. Create a `.env` file in the project root with the following content:
```env
MISTRAL_API_KEY=your_api_key_here
MISTRAL_MODEL=the_model_you_want_to_use
```

> **Note:** Ensure you replace `your_api_key_here` with your actual Mistral API key and `the_model_you_want_to_use` with the actual model you want to use

---

## Usage

### **Run the Scraper**
To execute the scraper with the default settings:
```bash
python main.py
```

### **Set Logging Level (Optional)**
The scraper allows you to control logging verbosity using a command-line argument:
```bash
python main.py --log-level DEBUG  # OR python main.py -l DEBUG
```
The output will be generated in `festivals.jsonl`.

#### **Available Logging Levels:**
- `DEBUG`: Verbose debugging information
- `INFO` (default): General runtime information
- `WARNING`: Potential issues
- `ERROR`: Errors that prevent execution
- `CRITICAL`: Severe errors causing termination

**Example:**
```bash
python main.py -l WARNING
```

---

## Testing Approach
To ensure completeness and error-free results:
- The script is designed to **resume from the last scraped page** in case of interruptions.
- Extracted festival data is validated against the required schema before saving.
- Handled duplication and edge cases like missing fields.
- Errors are logged, and failed extractions are retried automatically.
- Random samples from the dataset were checked against the website.
- Logs are generated at different levels to track progress and errors.

---

## **Output Format**
The final output is stored in [festivals.jsonl](./festivals.jsonl) and follows the required schema:

```json
{"festival_name": "Flickers' Rhode Island International Film Festival", "festival_info": "...", "deadlines": ["Jan 15, 2023"], "awards": ["Best Short Film"], "categories": ["Film Festival"], "important_dates": ["April 25, 2013"]}
{"festival_name": "8th International Women Filmmakers Festival", "festival_info": "...", "deadlines": ["April 5, 2024"], "awards": ["Best Documentary Award"], "categories": ["Short", "Experimental"], "important_dates": ["Feb 8, 2025"]}
...
```

---

## License
MIT License





### **Setting Up a Virtual Environment**

To ensure dependencies are managed properly and avoid conflicts, it's recommended to use a virtual environment. Follow these steps:

#### **1. Create a Virtual Environment**
Run the following command to create a virtual environment:

```bash
python -m venv venv
```

#### **2. Activate the Virtual Environment**

- **Windows (Command Prompt)**
  ```bash
  venv\Scripts\activate
  ```
- **Windows (PowerShell)**
  ```powershell
  venv\Scripts\Activate.ps1
  ```
- **Mac/Linux**
  ```bash
  source venv/bin/activate
  ```

#### **3. Install Dependencies**
After activating the virtual environment, install the required dependencies:

```bash
pip install -r requirements.txt
```

#### **4. Deactivating the Virtual Environment**
When done, deactivate the virtual environment with:

```bash
deactivate
```

This setup ensures that all required packages are installed in an isolated environment, preventing potential conflicts with system-wide dependencies.