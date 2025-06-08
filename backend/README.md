PJT 07 (2025.05.02.)
---



- 참여자 : 서울 2반 김미진, 서울 2반 박소현 
- 선택주제 : 도서
- 프로젝트 개요 및 목적
  : 비동기 통신을 이용한 웹 페이지 구현

---



1. 과제 설명 및 역할 분담
   
   - 유저 팔로우 기능 비동기 구현
     : 버튼 텍스트와 팔로워 팔로잉 수 실시간 갱신
     
     - button.addEventListener('click', e.preventDefault()) : 기본 이동 제어
     - fetch/axios.post + CSRF 헤더(X-CSRFToken) + credentials: 'same-origin' : csrf 와 함께 POST 요청
     
     
   
   - 쓰레드 좋아요 기능 비동기 구현
     : 좋아요 추가 취소 요청 및 좋아요 수 실시간 갱신
     
     - likeForm.addEventListener('submit', ()) : 좋아요 구현
     
     
   
   - 게시글 댓글 기능 비동기 구현
     : 댓글 제출 시 댓글 객체 DOM 추가 반영
     
     - commentForm.addEventListener('submit', ()) : 댓글 생성 
     - commentList.addEventListener('submit', ()) : 댓글 삭제
     
     
   
   -  도서 장르 필터링 비동기 구현
     
     : 특정 카테고리 클릭 시 선택된 장르의 도서 카드만 렌더링
     
     - addEventListener('click', …) + e.preventDefault() : 기본 이동 제어
     
     - axios.get(url, { params: { category } }) : 새로고침 없이 지정 장르 도서 카드 json 형태로 비동기 요청

 

---



2. 개인
   - 개인 역할
     
     - 유저 팔로우 기능 비동기 구현
       : 버튼 텍스트와 팔로워 팔로잉 수 실시간 갱신
     
     - 도서 장르 필터링 비동기 구현 
       : 특정 카테고리 클릭 시 선택된 장르의 도서 카드만 렌더링
     
     
   
   - 느낀점
     
     - 비동기 통신을 이용한 웹 페이지 구현을 통한 응답성 향상
     
     - 협업을 통해 백엔드 개발의 전반적인 구조를 익히고, 책임 분담의 중요성을 느낌

        