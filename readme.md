# HIRO AI Mindmap

AI 기반 키워드 확장 기능을 갖춘 마인드맵 웹 애플리케이션입니다. Flask 서버와 순수 HTML/JS 프론트엔드로 구성되어 있으며, Ollama 모델 `exaone3.5:7.8b`를 이용해 입력 키워드와 연관된 하위 키워드를 생성합니다.

## 주요 기능
- 키워드를 노드로 추가하고 연결/해제하여 마인드맵을 구성
- JSON 내보내기/가져오기, PNG 내보내기, 라이트/다크/퍼플 테마 전환
- 생성 개수와 심층 모드를 선택하여 AI 하위 키워드 자동 생성
- `saved_maps` 폴더의 JSON 파일을 로드하는 API 제공

## 설치 및 실행 방법
1. Python 3.8 이상과 [Ollama](https://ollama.ai/)를 설치하고 모델 `exaone3.5:7.8b`를 다운로드합니다.
2. 필요한 패키지를 설치합니다.
   ```bash
   pip install -r requirements.txt
   ```
3. 애플리케이션을 실행합니다.
   ```bash
   python app.py
   ```
4. 브라우저에서 `http://localhost:5000` 으로 접속합니다.

## 사용 방법
- 상단 입력창에 새 키워드를 입력하고 **키워드 추가** 버튼으로 노드를 생성합니다.
- **키워드 연결** / **연결 삭제** 버튼을 사용해 노드 간 링크를 관리합니다.
- 오른쪽 패널의 슬라이더와 옵션을 조정한 뒤 **생성** 버튼을 눌러 AI가 제안하는 하위 키워드를 확인합니다.
- 툴바에서 JSON 내보내기/가져오기, PNG 내보내기, 테마 변경 등을 수행할 수 있습니다.

## API 엔드포인트
- `POST /generate-subkeywords`
  - 입력: `{ "keyword": "중심 키워드", "count": 5, "deep_mode": false }`
  - 반환: 생성된 하위 키워드 배열
- `GET /load-map/<name>`
  - 저장된 JSON 마인드맵을 불러와 반환

## 프로젝트 구조
- `app.py` - Flask 서버와 API 라우트 정의
- `templates/index.html` - 프론트엔드 UI 및 인터랙션 로직
- `static/style.css` - 테마 및 화면 구성 스타일
