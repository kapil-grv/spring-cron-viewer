from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

def describe_cron_expression(cron_expression):
    parts = cron_expression.split()
    if len(parts) != 6:
        return "Invalid cron expression"

    second, minute, hour, day_of_month, month, day_of_week = parts

    # Helper function to format a part
    def interpret_part(part, unit, include_at=True):
        if part == '*':
            return f"{'every ' if include_at else ''}{unit}"
        elif ',' in part:
            return f"at {part.replace(',', ', ')} {unit}"
        elif '-' in part:
            start, end = part.split('-')
            return f"from {start} to {end} {unit}"
        elif '/' in part:
            base, interval = part.split('/')
            return f"every {interval} {unit} starting from {base}"
        elif part.isdigit():
            return f"at {part} {unit}"
        return part

    description = []

    if second != '*':
        description.append(interpret_part(second, 'second(s)', False))
    if minute != '*':
        description.append(interpret_part(minute, 'minute(s)', False))
    if hour != '*':
        hour_description = interpret_part(hour, 'hour(s)', False)
        if hour_description.startswith("at "):
            # Convert 24-hour format to 12-hour format with AM/PM
            hour_value = int(hour.split(',')[0])
            if hour_value > 12:
                hour_value -= 12
                period = "PM"
            elif hour_value == 12:
                period = "PM"
            elif hour_value == 0:
                hour_value = 12
                period = "AM"
            else:
                period = "AM"
            description.append(f"at {hour_value} {period}")
        else:
            description.append(hour_description)

    # Special case for daily schedules
    if day_of_month == '*' and month == '*' and day_of_week == '*':
        if not description:
            description.append("every day")
        else:
            description.append("daily")

    # Special case for weekly schedules
    if day_of_month == '*' and month == '*' and day_of_week != '*':
        description.append(f"on {day_of_week} of every week")

    # Special case for monthly schedules
    if day_of_month != '*' and month != '*' and day_of_week == '*':
        description.append(f"on day {day_of_month} of every month")

    # Combine all parts
    return ', '.join(description)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cron Expression Describer</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                color: #333;
            }
            .container {
                max-width: 800px;
                margin: auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
                color: #2c3e50;
            }
            form {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            input[type="text"] {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 16px;
            }
            .result {
                margin-top: 20px;
                padding: 15px;
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            #description {
                font-weight: bold;
            }
        </style>
        <script>
            function describeCron() {
                const cronInput = document.getElementById('cron');
                const descriptionElement = document.getElementById('description');
                const cronExpression = cronInput.value;

                fetch('/describe', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: new URLSearchParams(`cron=${cronExpression}`)
                })
                .then(response => response.json())
                .then(data => {
                    descriptionElement.innerText = data.description;
                })
                .catch(error => {
                    descriptionElement.innerText = 'Error describing cron expression';
                });
            }

            document.addEventListener('DOMContentLoaded', () => {
                const cronInput = document.getElementById('cron');
                cronInput.addEventListener('input', describeCron);
            });
        </script>
    </head>
    <body>
        <div class="container">
            <h1>Cron Expression Describer</h1>
            <form>
                <label for="cron">Enter Cron Expression:</label>
                <input type="text" id="cron" name="cron" placeholder="e.g. 0 0 9 * * *" required>
            </form>
            <div class="result">
                <p id="description"></p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/describe', methods=['POST'])
def describe():
    cron_expression = request.form['cron']
    description = describe_cron_expression(cron_expression)
    return jsonify(description=description)

if __name__ == '__main__':
    app.run(debug=True)
