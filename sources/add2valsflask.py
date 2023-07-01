from flask import Flask
from flask import request

app = Flask(__name__)


def sumTwoVals(num1, num2):
    """Sum 2 Values."""
    try:
        sumVal = int(num1) + int(num2)
        return str(sumVal)
    except ValueError:
        return "invalid input"


@app.route("/")
def index():
    num1 = request.args.get("number1", "")
    num2 = request.args.get("number2", "")
    if num1:
        sumVal = sumTwoVals(num1, num2)
    else:
        sumVal = ""
    return (
        """<form action="" method="get">
                <h4>Base Logic For Life - add2vals</h4>
                Number1: <input type="text" name="number1">
                Number2: <input type="text" name="number2">
                <input type="submit" value="Sum the numbers">
            </form>"""
        + "Sum: "
        + sumVal
    )
        
if __name__ == "__main__":
	app.run()