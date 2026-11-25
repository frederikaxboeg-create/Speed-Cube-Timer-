// Gemmer appens filer på telefonen, så den virker uden internet.
// Hæv versionsnummeret, når filerne ændres, så telefonen henter de nye.
const CACHE = "cubetimer-v5";
const FILES = ["./", "index.html", "manifest.json", "icon-180.png", "icon-192.png", "icon-512.png", "cstimer_module.js"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  // Selve siden: hent altid den nyeste, når der er net. Uden net: brug den gemte.
  if (e.request.mode === "navigate") {
    e.respondWith(
      fetch(e.request, { cache: "no-cache" })
        .then(res => {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put("index.html", copy));
          return res;
        })
        .catch(() => caches.match("index.html"))
    );
    return;
  }
  // Ranglister: vis den gemte med det samme, og hent en nyere i baggrunden.
  if (new URL(e.request.url).pathname.includes("/ranks/")) {
    e.respondWith(caches.open(CACHE).then(async c => {
      const hit = await c.match(e.request);
      const net = fetch(e.request).then(r => { if (r.ok) c.put(e.request, r.clone()); return r; }).catch(() => hit);
      return hit || net;
    }));
    return;
  }
  e.respondWith(
    caches.match(e.request, { ignoreSearch: true }).then(hit => hit || fetch(e.request))
  );
});
