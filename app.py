from flask import Flask, render_template_string, request

app = Flask(__name__)

# 網頁的 HTML 範本
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>BMI 計算器</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; border: 1px solid #ccc; border-radius: 10px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        input[type="number"] { width: 100%; padding: 8px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .result { margin-top: 20px; padding: 10px; background-color: #f8f9fa; border-left: 5px solid #007bff; }
    </style>
</head>
<body>
    <h2>BMI 體重指數計算器</h2>
    <form method="POST">
        <div class="form-group">
            <label>身高 (公分):</label>
            <input type="number" name="height" step="0.1" required value="{{ height }}">
        </div>
        <div class="form-group">
            <label>體重 (公斤):</label>
            <input type="number" name="weight" step="0.1" required value="{{ weight }}">
        </div>
        <button type="submit">計算 BMI</button>
    </form>

    {% if bmi %}
    <div class="result">
        <h3>計算結果：</h3>
        <p>您的 BMI 為: <strong>{{ bmi }}</strong></p>
        <p>體重狀態: <strong>{{ status }}</strong></p>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def bmi_calculator():
    bmi = None
    status = ""
    height = ""
    weight = ""
    
    if request.method == "POST":
        try:
            height = float(request.form["height"])
            weight = float(request.form["weight"])
            
            # BMI 公式 = 體重(kg) / 身高(m)平方
            height_in_meters = height / 100
            bmi_value = weight / (height_in_meters ** 2)
            bmi = round(bmi_value, 2)
            
            # 判斷體重狀態
            if bmi < 18.5:
                status = "體重過輕"
            elif 18.5 <= bmi < 24:
                status = "健康體位"
            else:
                status = "體重過重/肥胖"
        except (ValueError, ZeroDivisionError):
            status = "輸入資料有誤，請重新輸入。"

    return render_template_string(HTML_TEMPLATE, bmi=bmi, status=status, height=height, weight=weight)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
