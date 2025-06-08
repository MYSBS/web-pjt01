# 1. 베이스 이미지
FROM python:3.9.13-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 의존성 복사 및 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 4. 소스 복사
COPY . /app

# 5. 정적 파일 수집 및 마이그레이션
# (컨테이너 시작 시 실행하도록 entrypoint 스크립트를 추가해도 좋음)
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput

# 6. Gunicorn으로 서비스
CMD ["gunicorn", "mypjt.wsgi:application", "--bind", "0.0.0.0:8000"]