# 1. 빌드용 이미지
FROM node:18-alpine AS build
WORKDIR /app
# 의존성 설치를 위해 package.json 파일 경로 수정
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
# 소스 복사 경로 수정
COPY frontend/. .
RUN npm run build

# 2. 프로덕션용 Nginx 이미지에 빌드 결과 복사
FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
# nginx 설정 파일 경로 수정
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# 3. Nginx 기본 포트 노출
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```dockerfile
# 1. 빌드용 이미지
FROM node:18-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
RUN npm run build

# 2. 프로덕션용 Nginx 이미지에 빌드 결과 복사
FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 3. Nginx 기본 포트 노출
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]