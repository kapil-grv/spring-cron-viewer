# Cron Expression Describer

A web-based tool to help users understand cron expressions by providing a human-readable description.

## Overview

This Flask-based application accepts a cron expression as input and returns a detailed, easy-to-understand description of the cron schedule. The user interface is minimal and designed for quick use, where users can enter a cron expression and instantly get a description of the scheduled task.

## Features

- **Human-readable description**: Converts complex cron expressions into understandable language.
- **Real-time updates**: As users type a cron expression, the description updates dynamically.
- **Simple and clean UI**: A lightweight frontend with no external dependencies.

## Requirements

- Python 3.x
- Flask (`pip install Flask`)

## Installation

1. Clone this repository or download the `cron_describer.py` file.
   
2. Install dependencies:
   ```bash
   pip install Flask
   ```

3. Run the Flask application:
   ```bash
   python app.py
   ```

4. Visit `http://localhost:5000` in your browser to access the Cron Expression Describer.

## How it Works

The app takes the input cron expression and splits it into its parts (second, minute, hour, day of month, month, day of week). Each part is interpreted and formatted into a human-readable sentence. Special cases for daily, weekly, and monthly cron schedules are also handled.

## API

- **POST `/describe`**: Accepts a cron expression as form data and returns a JSON response with the description.

   **Request Format:**
   - `cron`: A string representing the cron expression (e.g., `0 0 9 * * *`).

   **Response Format:**
   - `description`: A string with the description of the cron expression.

## Example Usage

Input:
```
0 0 9 * * *
```

Output:
```
"at 0 second(s), at 0 minute(s), at 9 AM, daily"
```

## Development

### Frontend (HTML + JavaScript)
- The frontend allows users to input a cron expression and displays the description in real time.
- JavaScript is used to send the cron expression to the Flask backend via a POST request and update the description dynamically.

### Backend (Flask)
- The Flask server processes the input cron expression, interprets it, and returns a description to the frontend.

## License

This project is open-source and available under the MIT License.
