import openai
from django.conf import settings
from books.models import Book
import json
import re

def build_recommend_prompt(user):
    favorite_books = user.favorite_books.values('title', 'author')
    favorite_authors = user.favorite_authors.values_list('author', flat=True)
    favorite_categories = user.favorite_topics.values_list('name', flat=True)

    book_list = [f"{b['title']} ({b['author']})" for b in favorite_books]
    book_candidates = Book.objects.values('id', 'title', 'author')

    book_list_text = "\n".join([
        f"{book['id']}. {book['title']} - {book['author']}" for book in book_candidates
    ])

    prompt = f"""
    **너의 응답은 반드시 JSON형식으로만 응답을 줘야해**
    너는 독서 추천 전문가야. 아래 사용자 정보를 참고해서
    반드시 아래의 보유 도서 리스트 중에서만 3권을 골라 추천해줘!
    절대로 줄글, 설명 없이 JSON 형식만 보내.
    각 항목은 아래 JSON 스키마 그대로 맞춰줘.
    응답 앞뒤에도 설명 붙이지 마!

    [사용자 정보]
    - 관심 책: {', '.join(book_list)}
    - 좋아하는 작가: {', '.join(favorite_authors)}
    - 선호 장르: {', '.join(favorite_categories)}

    [보유 도서 목록]
    {book_list_text}
    
    아래와 같은 JSON 형식으로만 응답해:
    [
        {{
            "id": 책의 id,
            "title": "책 제목",
            "author": "저자",
            "cover": "책 표지 URL",
            "similarity_reason": "유사한 이유",
            "recommend_reason": "추천 이유"
        }}
    ]
    """
    return prompt

def call_gpt_api(prompt):
    openai.api_key = settings.OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model='gpt-4o-mini',
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def parse_gpt_response(result):
    if result.startswith("```json"):
        result = result.removeprefix("```json").strip()
    if result.endswith("```"):
        result = result.removesuffix("```").strip()

    cleaned_result = re.sub(r'[\u200b\u202f\u00a0]', ' ', result)
    cleaned_result = re.sub(r'\s+', ' ', cleaned_result).strip()

    return json.loads(cleaned_result)
