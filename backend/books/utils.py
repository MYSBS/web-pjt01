import requests
import openai
import base64
import numpy as np
from pathlib import Path
from typing import Optional
from django.conf import settings
from difflib import ndiff

openai.api_key = settings.OPENAI_API_KEY

def enhance_content(original_text: str) -> tuple[str, str]:
    """
    OpenAI GPT-4o-mini을 통해 원본 텍스트를 다듬고,
    diff(변경점)까지 계산하여 반환.
    """
    # 2) AI에게 다듬은 텍스트 요청 (0.28.x 스타일)
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """너는 세계적으로 유명한 작가야. 사용자가 작성한 글을 더 자연스럽고 풍부하게 다듬어서 멋지게 만들어.
            어떤 문장이라도 문장단위로 대답해. 맞춤법이 틀린 문장도 잘 이해하고 고쳐. 그리고 사용자의 질문에 응답하는게 아니라 질문조차도 멋지게 만드는거야.
            문장이 짧고 어떤 메시지를 담을질 모르겠을 때는 그냥 원문을 그대로 돌려주거나 주어진 단어로 삼행시라도 해서 대답해
            아무리 짧은 문장이여도 답변을 해줘야해. 그리고 최대한 원문과 가깝게 해줘."""},
            {"role": "user",   "content": original_text},
        ],
        temperature=0.8,
    )
    # 응답에서 메시지 콘텐츠 추출
    enhanced = response.choices[0].message.content.strip()

    # 3) diff 계산
    diff_lines = ndiff(
        original_text.splitlines(keepends=True),
        enhanced.splitlines(keepends=True)
    )
    diff_result = "".join(
        f"{'＋' if line.startswith('+') else '－' if line.startswith('-') else '  '}{line[2:]}"
        for line in diff_lines
    )

    return enhanced, diff_result



def extract_keywords(text, max_keywords=10):
    prompt = (
        "다음 사항은 반드시 지키고 다른 문장을 더 넣으면 안되 응답은 한국말로만해" 
        f"다음 텍스트에서 핵심 키워드 {max_keywords}개를 추출해줘:\n\n{text}\n\n"
        "키워드는 쉼표로 구분해서 출력해줘."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    keywords_text = response.choices[0].message['content']
    return [kw.strip() for kw in keywords_text.split(",")]

def get_embedding(text, model="text-embedding-3-small"):
    response = openai.Embedding.create(
        input=[text],
        model=model
    )
    return response["data"][0]["embedding"]




def decode_embedding(embedding_str: str) -> Optional[np.ndarray]:
    try:
        raw = base64.b64decode(embedding_str)
        arr = np.frombuffer(raw, dtype=np.float32)
        # buffer 크기가 float32 단위가 아니면 실패
        if raw and len(raw) % np.dtype(np.float32).itemsize != 0:
            return None
        return arr
    except Exception:
        return None



def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Compute cosine similarity between two vectors.
    """
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))