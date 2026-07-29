// PC 플리핑 매니저 오프라인 PWA — 앱 셸 + 데이터 파일을 캐시해서
// 첫 로드 이후로는 인터넷/서버 연결 없이 완전히 동작하게 한다.
const CACHE_NAME = "pcfm-pwa-v3";
const ASSETS = [
  "./",
  "./index.html",
  "./engine.js",
  "./manifest.json",
  "./parts_db.json",
  "./benchmark_db.json",
  "./compat_tables.json",
  "./icon-192.png",
  "./icon-512.png",
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))))
  );
  self.clients.claim();
});

// 캐시 우선(cache-first) — 오프라인에서도 무조건 뜨는 게 목적이라
// 네트워크 우선보다 안전하다. 캐시에 없을 때만 네트워크로 가고, 성공하면 캐시에 채워둔다.
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  e.respondWith(
    caches.match(e.request).then((cached) => {
      if (cached) return cached;
      return fetch(e.request)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(e.request, copy));
          return res;
        })
        .catch(() => cached);
    })
  );
});
