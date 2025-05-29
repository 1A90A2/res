from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import google.generativeai as genai

# 설정된 요리 종류
cuisines = [
    "",
    "Italian", "Mexican", "Chinese", "Indian", "Japanese",
    "Thai", "French", "Mediterranean", "American", "Greek"
]

# 식이 제한 리스트
dietary_restrictions = [
    "Gluten-Free", "Dairy-Free", "Vegan", "Pescatarian",
    "Nut-Free", "Kosher", "Halal", "Low-Carb", "Organic", "Locally Sourced"
]

# 언어 목록 (언어 이름: 코드)
languages = {
    'English': 'en', 'Spanish': 'es', 'French': 'fr', 'German': 'de',
    'Russian': 'ru', 'Chinese (Simplified)': 'zh-CN', 'Chinese (Traditional)': 'zh-TW',
    'Japanese': 'ja', 'Korean': 'ko', 'Italian': 'it', 'Portuguese': 'pt',
    'Arabic': 'ar', 'Dutch': 'nl', 'Swedish': 'sv', 'Turkish': 'tr',
    'Greek': 'el', 'Hebrew': 'he', 'Hindi': 'hi', 'Indonesian': 'id',
    'Thai': 'th', 'Filipino': 'tl', 'Vietnamese': 'vi'
}

# Flask 앱 초기화
app = Flask(__name__)

# 환경 변수에서 API 키 불러오기
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

# Google Gemini API 설정
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 메인 페이지 렌더링
@app.route('/')
def index():
    return render_template(
        'index.html',
        cuisines=cuisines,
        dietary_restrictions=dietary_restrictions,
        languages=languages
    )

# 레시피 생성 라우트
@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    # 사용자 입력 수집
    ingredients = request.form.getlist('ingredient')
    selected_cuisine = request.form.get('cuisine')
    selected_restrictions = request.form.getlist('restrictions')
    selected_language = request.form.get('language')

    print(f"Selected cuisine: {selected_cuisine}")
    print(f"Selected restrictions: {selected_restrictions}")
    print(f"Selected language: {selected_language}")

    if len(ingredients) != 3:
        return "Kindly provide exactly 3 ingredients."

    # 프롬프트 구성
    prompt = f"Craft a recipe in HTML in {selected_language} using {', '.join(ingredients)}.\n" \
             "Ensure the recipe ingredients appear at the top, followed by the step-by-step instructions.\n"
    
    if selected_cuisine:
        prompt += f"The cuisine should be {selected_cuisine}.\n"
    
    if selected_restrictions:
        prompt += f"The recipe should follow these dietary restrictions: {', '.join(selected_restrictions)}.\n"

    # Gemini API 호출
    try:
        response = model.generate_content(prompt)
        recipe = response.text
    except Exception as e:
        recipe = f"Error generating recipe: {str(e)}"

    return render_template('recipe.html', recipe=recipe)

# 앱 실행
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

