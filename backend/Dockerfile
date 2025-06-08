# FROM python:3.9.13

# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# RUN python manage.py collectstatic --noinput

# COPY . .
# CMD ["gunicorn", "mypjt.wsgi:application", "--bind", "0.0.0.0:8000"]

FROM python:3.9.13

# 시스템 종속성 설치 (필요시)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 의존성 설치 단계 (캐시 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 정적 파일 수집
RUN python manage.py collectstatic --noinput  # 올바른 위치

CMD ["gunicorn", "mypjt.wsgi:application", "--bind", "0.0.0.0:8000"]
