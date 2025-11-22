# git-base-team3-test (Dockerfile + gitctf 실행)

Flask 기반 CTF/리서치 앱을 **Dockerfile**로 빌드하고 **gitctf.py exec**로 실행하도록 맞춘 가이드입니다.  
`docker compose`는 사용하지 않습니다.

## 요구사항
- Docker Engine (Docker Desktop 등)
- Python 3 + `gitctf.py` 스크립트
- 열린 포트: 웹 5000 (서비스 포트는 컨테이너 내부 5000으로 고정)

## 빠른 시작 (Dockerfile + gitctf)
1. 환경파일 준비  
   ```bash
   cp .env.example .env
   # SECRET_KEY를 랜덤하게 채우고, 기본은 sqlite로 사용
   ```
2. 빌드 & 실행 (서비스)  
   ```bash
   python3 ./gitctf.py exec service \
     --service-dir . \
     --service-name hspace-service \
     --host-port 5000 \
     --service-port 5000
   ```
3. 접속: http://localhost:5000

## gitctf 실행 예시
- 서비스 실행: 위 “빠른 시작” 명령 사용.
- 익스플로잇 실행 예시(디렉터리 명만 교체):  
  ```bash
  python3 ./gitctf.py exec exploit \
    --exploit-dir ./exploit \
    --service-name hspace-exploit \
    --ip 127.0.0.1 \
    --port 5000 \
    --timeout 60
  ```

## 환경변수 (.env)
- `SECRET_KEY` : 긴 랜덤 문자열 (세션/CSRF 키)
- `DB_ENGINE` : 기본 `sqlite` (별도 DB 컨테이너 없이 동작). 외부 MySQL을 쓸 때만 `mysql`로 변경하고 `DB_HOST` 등 설정.
- `DB_HOST` / `DB_PORT` / `DB_USER` / `DB_PASSWORD` / `DB_NAME` : MySQL 사용 시에만 필요
- `MAX_CONTENT_LENGTH` : 업로드 최대 크기(바이트)

## 프로젝트 구조
- `app.py` : Flask 앱 팩토리
- `models/` : SQLAlchemy 모델
- `routes/` : 블루프린트 라우트
- `services/ctftime.py` : 외부 이벤트 조회
- `static/`, `templates/` : 정적/템플릿 자원
- `docker-entrypoint.sh` : 컨테이너 부팅 시 DB 대기 + 테이블 생성 + 서버 실행

## 주의사항
- `docker-compose.yml`은 사용하지 않습니다(요구사항: Dockerfile + gitctf.py exec 기반).
- MySQL이 필요하다면 외부/별도 컨테이너를 수동으로 올리고 `.env`를 MySQL에 맞게 수정 후 `gitctf.py exec service`를 다시 실행하세요.
