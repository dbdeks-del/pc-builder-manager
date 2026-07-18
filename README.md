# 🖥️ PC 플리핑 매니저 (PC Builder Manager)

중고 부품을 **매입 → 조립 → 검사 → 판매**해서 수익을 내는 흐름을 게임처럼 관리하는 도구입니다.
기존 [PC-Manager](https://github.com/dbdeks-del/PC-Manager)(조립실·장부)와 PC Builder Manager(호환성·병목·시세 분석)를 하나로 합쳤습니다.

## 실행 방법

1. **Python 3.10 이상 설치** — https://www.python.org/downloads/
   설치할 때 **"Add Python to PATH"** 체크 필수.
2. 저장소 클론:
   ```
   git clone https://github.com/dbdeks-del/pc-builder-manager.git
   ```
3. `start.bat` **더블클릭**.
   - 첫 실행 시 필요한 라이브러리를 자동 설치합니다(인터넷 필요).
   - backend 서버(http://localhost:8000)가 켜지고 브라우저가 자동으로 열립니다.
4. 종료하려면 실행 창에서 아무 키나 누르세요.

## 5개 구역 (게임 루프)

| 구역 | 하는 일 |
|---|---|
| 📦 **창고** | 부품 매입·보관. 이름 입력하면 **30,123개 DB에서 자동완성**, 부품마다 벤치마크 기반 **등급**(일반/레어/에픽/전설) 표시 |
| 🛠️ **조립실** | 창고 부품을 **드래그**해서 슬롯에 장착. 장착 즉시 호환성 검사 + 점수 게이지 반영. "본체 통째 매입"도 지원 |
| 🧪 **검사실** | **종합점수 0~100 + S/A/B/C/D 등급**. 성능·밸런스·호환성·완성도·가성비 항목별 게이지, 목적별(게임/작업/스트리밍/사무) 점수, 병목 경고 |
| 💰 **판매장** | 다나와·번개장터·중고나라 **실시간 중고 시세**로 권장 판매가 계산 → 판매가 입력하면 마진 자동 표시 → 판매 확정 시 장부 기록 |
| 📒 **장부** | 구매/판매 내역과 총 수지. 가격은 "12만", "9만5천" 표기도 인식 |

## 종합점수 계산

- **성능**: CPU(PassMark 계열 5,055개) / GPU(G3DMark 2,408개) 벤치마크 백분위를 목적별 가중치로 합산
- **밸런스**: CPU-GPU 백분위 격차가 크면 감점 + 병목 경고
- **호환성**: 소켓/DDR 세대/파워 용량 검사 결과로 감점
- **완성도**: 필수 슬롯(CPU·보드·RAM·저장장치·파워·케이스) 충족률
- **가성비**: 성능 대비 투입 비용 (빌드가 절반 이상 완성됐을 때만)

## 부품 DB 갱신 (더 모으고 싶을 때)

`parts_db.json`(30,123개)은 3개 소스를 병합한 것입니다:
1. GitHub [docyx/pc-part-dataset](https://github.com/docyx/pc-part-dataset) — PCPartPicker 스크랩 최신본
2. `benchmark_db.json` — PassMark 계열 CPU 5,055개/GPU 2,408개 (**GTX 750 Ti, HD 7970, FX-8350, Core 2 Quad 같은 10년+ 구형이 전부 여기 있음**)
3. 기존 DB 보존분 + 구형 메인보드 큐레이션(AM3+/FM2+/H61/G41 등)

최신본으로 다시 빌드하려면:

```
cd backend
python build_parts_db.py            # 인터넷 필요
python build_parts_db.py --offline  # 다운로드 생략, 로컬 소스만 재병합
```

## PC-Manager에서 데이터 가져오기

기존 PC-Manager의 `data.json`(부품/PC/장부)을 그대로 이전할 수 있습니다:

```
cd backend
python migrate_pc_manager.py <PC-Manager 폴더>\data.json
```

원본 data.json은 수정되지 않습니다. 중복 저장되므로 **1회만** 실행하세요.

## 구조

- `backend/` — FastAPI 서버
  - `main.py` — API (부품/PC/장부 CRUD, 점수, 시세)
  - `scoring.py` — 종합점수 엔진 (`benchmark_db.json` 사용)
  - `compatibility.py` — 소켓/DDR/파워 호환성 + 병목 분석
  - `crawler.py` — 다나와·번개장터·중고나라 시세 크롤러
  - `parts_db.py` — 부품 카탈로그 검색 (`parts_db.json`, 23,512개)
  - `migrate_pc_manager.py` — PC-Manager 데이터 이전 스크립트
- `frontend/index.html` — 웹 UI (단일 파일)
- `start.bat` — 원클릭 실행 스크립트

데이터는 `backend/pc_builder.db`(SQLite)에 저장됩니다.
