from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML template for the calculator
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Basic Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
        .calculator { padding: 20px; border: 1px solid #ccc; border-radius: 5px; }
        input { margin: 5px; padding: 5px; }
        .result { margin-top: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="calculator">
        <h2>Basic Calculator</h2>
        <form method="post">
            <input type="number" name="num1" placeholder="Enter first number" required step="any">
            <select name="operation">
                <option value="add">Addition (+)</option>
                <option value="subtract">Subtraction (-)</option>
                <option value="multiply">Multiplication (×)</option>
                <option value="divide">Division (÷)</option>
            </select>
            <input type="number" name="num2" placeholder="Enter second number" required step="any">
            <input type="submit" value="Calculate">
        </form>
        {% if result is not none %}
            <div class="result">
                Result: {{ num1 }} {{ op_symbol }} {{ num2 }} = {{ result }}
            </div>
        {% endif %}
        {% if error %}
            <div class="result" style="color: red;">
                Error: {{ error }}
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None
    error = None
    num1 = None
    num2 = None
    op_symbol = None
    
    if request.method == 'POST':
        try:
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            operation = request.form['operation']
            
            if operation == 'add':
                result = num1 + num2
                op_symbol = '+'
            elif operation == 'subtract':
                result = num1 - num2
                op_symbol = '-'
            elif operation == 'multiply':
                result = num1 * num2
                op_symbol = '×'
            elif operation == 'divide':
                if num2 == 0:
                    error = "Cannot divide by zero"
                else:
                    result = num1 / num2
                    op_symbol = '÷'
        except ValueError:
            error = "Please enter valid numbers"
    
    return render_template_string(HTML_TEMPLATE, result=result, error=error, 
                               num1=num1, num2=num2, op_symbol=op_symbol)

if __name__ == '__main__':
    app.run(host="0.0.0", debug=True)