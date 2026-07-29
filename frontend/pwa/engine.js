/*
 * PC 플리핑 매니저 — PWA(서버 없이 브라우저 단독 실행) 엔진
 * backend/scoring.py + backend/compatibility.py + backend/parts_db.py + backend/database.py를
 * 그대로 JS로 이식하고, SQLite 대신 localStorage에 저장한다.
 * frontend/index.html의 UI 코드는 손대지 않고, api() 호출만 이 파일의 localApi()로 라우팅한다.
 */

// ── 공통: 한글 별칭 정규화 + 부분일치 검색 (compatibility.py 이식) ──
let KOREAN_ALIASES = [];
function normalize(s) {
  s = (s || "").toLowerCase();
  for (const [ko, en] of KOREAN_ALIASES) s = s.split(ko).join(en);
  return s.replace(/[^a-z0-9가-힣]/g, "");
}
function longestMatch(nameNorm, normalizedMap) {
  let bestVal = null, bestLen = 0;
  for (const key in normalizedMap) {
    if (key && nameNorm.includes(key) && key.length > bestLen) {
      bestVal = normalizedMap[key];
      bestLen = key.length;
    }
  }
  return bestVal;
}
function buildNormalizedMap(mapping) {
  const out = {};
  for (const k in mapping) out[normalize(k)] = mapping[k];
  return out;
}
function findSocket(name, mapN) { return longestMatch(normalize(name), mapN); }
function findScoreT(name, mapN) { const v = longestMatch(normalize(name), mapN); return v != null ? v : 0; }

let CPU_SOCKET_MAP_N = {}, MOTHERBOARD_SOCKET_MAP_N = {}, MOTHERBOARD_DDR_MAP_N = {};
let CPU_TDP_N = {}, GPU_TDP_N = {};

function checkCompatibility(parts) {
  const issues = [], warnings = [];
  const cpu = parts.find(p => p.category === "cpu");
  const motherboard = parts.find(p => p.category === "motherboard");
  const ram = parts.find(p => p.category === "ram");
  const psu = parts.find(p => p.category === "psu");
  const gpu = parts.find(p => p.category === "gpu");

  if (cpu && motherboard) {
    const cpuName = `${cpu.brand} ${cpu.model}`.toLowerCase();
    const mbName = `${motherboard.brand} ${motherboard.model}`.toLowerCase();
    const cpuSocket = (cpu.specs && cpu.specs.socket) || findSocket(cpuName, CPU_SOCKET_MAP_N);
    const mbSocket = (motherboard.specs && motherboard.specs.socket) || findSocket(mbName, MOTHERBOARD_SOCKET_MAP_N);
    const compatiblePairs = new Set(["LGA1151|LGA1151v2", "LGA1151v2|LGA1151"]);
    if (cpuSocket && mbSocket) {
      if (cpuSocket !== mbSocket && !compatiblePairs.has(`${cpuSocket}|${mbSocket}`)) {
        issues.push({ type: "socket_mismatch", severity: "error", message: `CPU 소켓(${cpuSocket})과 메인보드 소켓(${mbSocket})이 호환되지 않습니다.`, parts: ["cpu", "motherboard"] });
      } else if (compatiblePairs.has(`${cpuSocket}|${mbSocket}`)) {
        warnings.push({ type: "socket_warning", message: `CPU(${cpuSocket})와 메인보드(${mbSocket})는 일부 호환되나 바이오스 업데이트가 필요할 수 있습니다.` });
      }
    } else if (!cpuSocket) {
      warnings.push({ type: "unknown_cpu_socket", message: `CPU 소켓 정보를 확인할 수 없습니다: ${cpu.model}` });
    }
  }

  if (ram && motherboard) {
    const ramDdr = (ram.specs && ram.specs.ddr_type) || "";
    const mbName = `${motherboard.brand} ${motherboard.model}`.toLowerCase();
    const mbDdr = (motherboard.specs && motherboard.specs.ddr_type) || findSocket(mbName, MOTHERBOARD_DDR_MAP_N) || "";
    if (ramDdr && mbDdr && !mbDdr.includes(ramDdr)) {
      issues.push({ type: "ram_incompatible", severity: "error", message: `RAM 규격(${ramDdr})이 메인보드(${mbDdr})와 호환되지 않습니다.`, parts: ["ram", "motherboard"] });
    }
  }

  if (psu && (cpu || gpu)) {
    const psuWatt = (psu.specs && psu.specs.wattage) || 0;
    const cpuPower = (cpu ? findScoreT(`${cpu.brand} ${cpu.model}`, CPU_TDP_N) : 0) || 65;
    const gpuPower = (gpu ? findScoreT(`${gpu.brand} ${gpu.model}`, GPU_TDP_N) : 0) || 0;
    const basePower = 80;
    const recommendedWatt = Math.round((cpuPower + gpuPower + basePower) * 1.2);
    if (psuWatt > 0 && psuWatt < recommendedWatt) {
      issues.push({ type: "psu_insufficient", severity: "error", message: `파워 용량(${psuWatt}W)이 부족합니다. 권장: ${recommendedWatt}W 이상`, parts: ["psu"], recommended_watt: recommendedWatt });
    } else if (psuWatt > 0) {
      warnings.push({ type: "psu_info", message: `파워 ${psuWatt}W (권장 최소: ${recommendedWatt}W) — 적합합니다.` });
    }
  }

  return { compatible: issues.length === 0, issues, warnings };
}

// ── scoring.py 이식 ──
const PURPOSE_WEIGHTS = {
  gaming: { cpu: 0.35, gpu: 0.65 }, work: { cpu: 0.65, gpu: 0.35 },
  streaming: { cpu: 0.55, gpu: 0.45 }, office: { cpu: 0.70, gpu: 0.30 },
};
const PURPOSE_LABELS = { gaming: "게임", work: "작업", streaming: "스트리밍", office: "사무" };
const REQUIRED_SLOTS = ["cpu", "motherboard", "ram", "storage", "psu", "case"];
const RARITY_CUTS = {
  cpu: [[45000, "legendary"], [28000, "epic"], [15000, "rare"]],
  gpu: [[30000, "legendary"], [16000, "epic"], [9000, "rare"]],
};
const PSU_RARITY = { titanium: "legendary", platinum: "epic", gold: "rare" };

let CPU_KEYS = {}, GPU_KEYS = {}, CPU_SORTED = [], GPU_SORTED = [];

function buildKeys(entries) {
  const keys = {};
  for (const e of entries) {
    const key = e.key, score = e.score || 0;
    if (!key) continue;
    const noClock = key.replace(/(\s+\d+)*\s*[\d.]+\s*[gm]hz$/, "").trim();
    const noCores = noClock.replace(/\s+(dual|triple|quad|six|eight|ten|twelve|sixteen)([- ]?core)?$/, "").trim();
    const variants = new Set([key, noClock, noCores]);
    for (let v of variants) {
      v = normalize(v);
      if (v && (!(v in keys) || score > keys[v])) keys[v] = score;
    }
  }
  return keys;
}
function findBench(name, keys) { const v = longestMatch(normalize(name), keys); return v != null ? v : 0; }
const _cpuBenchCache = new Map();
function cpuBench(name) {
  if (_cpuBenchCache.has(name)) return _cpuBenchCache.get(name);
  const v = findBench(name, CPU_KEYS); _cpuBenchCache.set(name, v); return v;
}
const _gpuBenchCache = new Map();
function gpuBench(name) {
  if (_gpuBenchCache.has(name)) return _gpuBenchCache.get(name);
  const v = findBench(name, GPU_KEYS); _gpuBenchCache.set(name, v); return v;
}
function bisectLeft(arr, x) {
  let lo = 0, hi = arr.length;
  while (lo < hi) { const mid = (lo + hi) >> 1; if (arr[mid] < x) lo = mid + 1; else hi = mid; }
  return lo;
}
function percentile(score, sortedScores) {
  if (score <= 0 || !sortedScores.length) return 0;
  const idx = bisectLeft(sortedScores, score);
  return Math.round((idx / sortedScores.length) * 100 * 10) / 10;
}
function relativePerf(score, sortedScores) {
  if (score <= 0 || !sortedScores.length) return 0;
  const anchor = sortedScores[Math.max(0, Math.floor(sortedScores.length * 0.99) - 1)];
  if (anchor <= 0) return 0;
  return Math.round(Math.min(100, (score / anchor) * 100) * 10) / 10;
}

function partPerformance(category, brand, model, specs) {
  specs = specs || {};
  const name = `${brand} ${model}`.trim();
  if (category === "cpu") {
    const score = cpuBench(name);
    return finishRarity("cpu", score, percentile(score, CPU_SORTED));
  }
  if (category === "gpu") {
    const score = gpuBench(name);
    return finishRarity("gpu", score, percentile(score, GPU_SORTED));
  }
  if (category === "psu") {
    const text = `${specs.efficiency || ""} ${name}`.toLowerCase();
    for (const eff in PSU_RARITY) {
      if (text.includes(eff)) return { score: 0, percentile: null, rarity: PSU_RARITY[eff] };
    }
    return { score: 0, percentile: null, rarity: "common" };
  }
  return { score: 0, percentile: null, rarity: "common" };
}
function finishRarity(category, score, pct) {
  let rarity = "common";
  for (const [cut, tier] of RARITY_CUTS[category]) { if (score >= cut) { rarity = tier; break; } }
  return { score, percentile: pct, rarity };
}
function gradeOf(score) {
  if (score >= 90) return "S";
  if (score >= 78) return "A";
  if (score >= 62) return "B";
  if (score >= 45) return "C";
  return "D";
}

function scoreBuild(parts, purpose, purchaseCost) {
  purpose = purpose || "gaming";
  const cats = {};
  for (const p of parts) (cats[p.category] = cats[p.category] || []).push(p);

  let cpuPct = 0, gpuPct = 0, cpuRel = 0, gpuRel = 0, cpuBenchV = 0, gpuBenchV = 0;
  if (cats.cpu) {
    const c = cats.cpu[0];
    cpuBenchV = cpuBench(`${c.brand} ${c.model}`.trim());
    cpuPct = percentile(cpuBenchV, CPU_SORTED);
    cpuRel = relativePerf(cpuBenchV, CPU_SORTED);
  }
  if (cats.gpu) {
    const g = cats.gpu[0];
    gpuBenchV = gpuBench(`${g.brand} ${g.model}`.trim());
    gpuPct = percentile(gpuBenchV, GPU_SORTED);
    gpuRel = relativePerf(gpuBenchV, GPU_SORTED);
  }

  function performanceFor(w) {
    if (gpuRel > 0 && cpuRel > 0) return cpuRel * w.cpu + gpuRel * w.gpu;
    if (cpuRel > 0) return cpuRel * 0.8;
    if (gpuRel > 0) return gpuRel * 0.5;
    return 0;
  }
  const performance = performanceFor(PURPOSE_WEIGHTS[purpose] || PURPOSE_WEIGHTS.gaming);
  const purposeScores = {};
  for (const pk in PURPOSE_WEIGHTS) purposeScores[pk] = Math.round(performanceFor(PURPOSE_WEIGHTS[pk]));

  let bottleneck = null, balance;
  if (cpuRel > 0 && gpuRel > 0) {
    const gap = Math.abs(cpuRel - gpuRel);
    balance = Math.max(0, 100 - gap * 1.5);
    if (gap > 25) {
      const weaker = cpuRel < gpuRel ? "CPU" : "GPU";
      bottleneck = `${weaker} 병목 주의 — CPU 성능 ${cpuRel.toFixed(0)} vs GPU 성능 ${gpuRel.toFixed(0)} (오늘날 상위권 대비)`;
    }
  } else {
    balance = (cpuRel || gpuRel) ? 50 : 0;
  }

  const compat = checkCompatibility(parts);
  const compatScore = Math.max(0, 100 - 45 * compat.issues.length - 5 * compat.warnings.length);

  const have = new Set(Object.keys(cats));
  if (have.has("ssd") || have.has("hdd")) have.add("storage");
  const filled = REQUIRED_SLOTS.filter(s => have.has(s)).length;
  const completeness = Math.round((filled / REQUIRED_SLOTS.length) * 100);
  const missing = REQUIRED_SLOTS.filter(s => !have.has(s));

  let value = null;
  if (purchaseCost && purchaseCost > 0 && performance > 0 && completeness >= 50) {
    const costMan = purchaseCost / 10000;
    value = Math.round(Math.min(100, (performance / Math.max(costMan, 1)) * 60));
  }

  function overallOf(perf, bal) {
    if (value !== null) return Math.round(perf * 0.40 + bal * 0.15 + compatScore * 0.15 + completeness * 0.10 + value * 0.20);
    return Math.round(perf * 0.50 + bal * 0.20 + compatScore * 0.15 + completeness * 0.15);
  }
  const overall = overallOf(performance, balance);

  const upgrades = [];
  if (cpuRel > 0 && gpuRel > 0 && Math.abs(cpuRel - gpuRel) > 10) {
    const stronger = Math.max(cpuRel, gpuRel);
    const weakerName = cpuRel < gpuRel ? "CPU" : "GPU";
    const gain = overallOf(stronger, 100) - overall;
    if (gain > 0) upgrades.push({ message: `${weakerName}를 상대 성능 ${stronger.toFixed(0)} 수준으로 업그레이드하면 밸런스가 맞습니다.`, gain });
  }
  const slotLabel = { cpu: "CPU", motherboard: "메인보드", ram: "RAM", storage: "저장장치", psu: "파워", case: "케이스" };
  for (const slot of missing) {
    upgrades.push({ message: `${slotLabel[slot] || slot} 슬롯을 채우면 완성도가 올라갑니다.`, gain: Math.round((100 / REQUIRED_SLOTS.length) * 0.25) });
  }
  const ramParts = cats.ram || [];
  const ramGb = ramParts.reduce((s, p) => s + ((p.specs && p.specs.capacity_gb) || 0), 0);
  if (ramParts.length && ramGb > 0 && ramGb < 16) {
    upgrades.push({ message: `RAM ${ramGb}GB → 16GB 이상으로 늘리면 게임/멀티태스킹 체감이 좋아집니다.`, gain: 0 });
  }

  return {
    overall, grade: gradeOf(overall), purpose, purpose_label: PURPOSE_LABELS[purpose] || purpose,
    breakdown: { performance: Math.round(performance), balance: Math.round(balance), compatibility: compatScore, completeness, value },
    cpu: { benchmark: cpuBenchV, percentile: cpuPct },
    gpu: { benchmark: gpuBenchV, percentile: gpuPct },
    purpose_scores: purposeScores, bottleneck, upgrades, missing_slots: missing,
    compat_issues: compat.issues, compat_warnings: compat.warnings,
  };
}

// ── parts_db.py 이식 (자동완성 DB, 23,512개) ──
const KO2EN = { "CPU": "cpu", "그래픽카드": "gpu", "메인보드": "motherboard", "RAM": "ram", "저장장치": "ssd", "파워": "psu", "케이스": "case", "쿨러": "cooler", "기타": "etc" };
function splitBrand(name) {
  const m = name.match(/^\s*(\S+)\s+(.+)$/);
  return m ? [m[1], m[2]] : ["", name.trim()];
}
function parseSpecs(category, name, s) {
  const specs = { summary: s };
  if (s.startsWith("벤치")) return specs;
  const parts = s.split("·").map(p => p.trim());
  if (category === "cpu") {
    for (const p of parts) {
      let m;
      if ((m = p.match(/^(\d+)코어/))) specs.cores = parseInt(m[1]);
      else if ((m = p.match(/^([\d.]+)GHz/))) specs.boost_clock_ghz = parseFloat(m[1]);
      else if ((m = p.match(/^(\d+)W/))) specs.tdp_w = parseInt(m[1]);
    }
  } else if (category === "gpu") {
    if (parts.length) specs.chipset = parts[0].replace(/\s*\d+GB$/, "").trim();
    for (const p of parts.slice(1)) { const m = p.match(/^(\d+)GB/); if (m) specs.vram_gb = parseInt(m[1]); }
  } else if (category === "motherboard") {
    if (parts.length >= 1 && parts[0]) specs.socket = parts[0];
    if (parts.length >= 2 && parts[1]) specs.form_factor = parts[1];
    for (const p of parts.slice(2)) { if (p.toUpperCase().startsWith("DDR")) specs.ddr_type = p.toUpperCase(); }
  } else if (category === "ram") {
    if (parts.length) { const m = parts[0].match(/^(\d)-(\d+)/); if (m) { specs.ddr_type = `DDR${m[1]}`; specs.speed_mhz = parseInt(m[2]); } }
    if (parts.length >= 2) { const m = parts[1].match(/^(\d+)x(\d+)/); if (m) { specs.modules = parseInt(m[1]); specs.capacity_gb = parseInt(m[1]) * parseInt(m[2]); } }
  } else if (category === "ssd" || category === "hdd") {
    for (const p of parts) {
      let m;
      if ((m = p.match(/^([\d.]+)\s*(GB|TB)/i))) { const cap = parseFloat(m[1]); specs.capacity_gb = m[2].toUpperCase() === "TB" ? Math.round(cap * 1000) : Math.round(cap); }
      else if (p.toUpperCase() === "SSD" || p.toUpperCase() === "HDD") specs.storage_type = p.toUpperCase();
      else if (p) specs.form_factor = p;
    }
  } else if (category === "psu") {
    for (const p of parts) {
      let m;
      if ((m = p.match(/^(\d+)\s*W/i))) specs.wattage = parseInt(m[1]);
      else if (["bronze", "silver", "gold", "platinum", "titanium", "plus"].includes(p.toLowerCase())) specs.efficiency = p.charAt(0).toUpperCase() + p.slice(1).toLowerCase();
    }
  }
  return specs;
}
let PARTS_DATABASE = [];
function loadPartsDB(raw) {
  const db = [];
  for (const koCat in raw) {
    const baseCat = KO2EN[koCat] || "etc";
    for (const item of raw[koCat]) {
      const name = item.n || "", s = item.s || "";
      let cat = baseCat;
      if (koCat === "저장장치" && s.toUpperCase().includes("HDD")) cat = "hdd";
      const [brand, model] = splitBrand(name);
      db.push({ category: cat, brand, model, name, specs: parseSpecs(cat, name, s) });
    }
  }
  PARTS_DATABASE = db;
}
function searchPartsDB(query, category) {
  query = (query || "").toLowerCase().trim();
  let results = PARTS_DATABASE;
  if (category) {
    results = (category === "ssd" || category === "hdd")
      ? results.filter(p => p.category === "ssd" || p.category === "hdd")
      : results.filter(p => p.category === category);
  }
  if (query) {
    const tokens = query.split(/\s+/).filter(Boolean);
    results = results.filter(p => {
      const text = `${p.name} ${p.specs.summary || ""}`.toLowerCase();
      return tokens.every(t => text.includes(t));
    });
  }
  return results.slice(0, 30);
}

// ── database.py 이식: localStorage 저장소 ──
const STORAGE_KEY = "pcfm_store_v1";
function loadStore() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {}
  return { seq: { parts: 0, pcs: 0, ledger: 0 }, parts: [], pcs: [], ledger: [] };
}
let STORE = loadStore();
function persist() { localStorage.setItem(STORAGE_KEY, JSON.stringify(STORE)); }
function nextId(table) { STORE.seq[table] = (STORE.seq[table] || 0) + 1; return STORE.seq[table]; }
function nowIso() { return new Date().toISOString(); }
function getPart(id) { return STORE.parts.find(p => p.id === id); }
function getPcRaw(id) { return STORE.pcs.find(p => p.id === id); }
function getPcOr404(id) { const pc = getPcRaw(id); if (!pc) throw new Error("PC not found"); return pc; }

function partDict(p) {
  const perf = partPerformance(p.category, p.brand || "", p.model || "", p.specs || {});
  return {
    id: p.id, category: p.category, brand: p.brand, model: p.model,
    specs: p.specs || {}, condition: p.condition, owned: !!p.owned,
    purchase_price: p.purchase_price, market_price: p.market_price,
    pc_id: p.pc_id, rarity: perf.rarity, percentile: perf.percentile,
  };
}
function pcDict(pc, purpose) {
  purpose = purpose || "gaming";
  const parts = STORE.parts.filter(p => p.pc_id === pc.id);
  const cost = (pc.whole && pc.purchase_price) ? pc.purchase_price : parts.reduce((s, p) => s + (p.purchase_price || 0), 0);
  const partsData = parts.map(p => ({ category: p.category, brand: p.brand || "", model: p.model || "", specs: p.specs || {} }));
  return {
    id: pc.id, name: pc.name, status: pc.status, whole: !!pc.whole,
    purchase_price: pc.purchase_price, sold_price: pc.sold_price,
    created_at: pc.created_at, completed_at: pc.completed_at, sold_at: pc.sold_at,
    parts: parts.map(partDict), cost, score: scoreBuild(partsData, purpose, cost || null),
  };
}

// ── main.py 라우트 이식 ──
function getStats() {
  const total = STORE.parts.length;
  const warehouse = STORE.parts.filter(p => p.pc_id == null && p.owned).length;
  const wishlist = STORE.parts.filter(p => !p.owned).length;
  const building = STORE.pcs.filter(p => p.status === "building").length;
  const done = STORE.pcs.filter(p => p.status === "done").length;
  const sold = STORE.pcs.filter(p => p.status === "sold").length;
  const buyTotal = STORE.ledger.filter(e => e.type === "buy").reduce((s, e) => s + (e.price || 0), 0);
  const sellTotal = STORE.ledger.filter(e => e.type === "sell").reduce((s, e) => s + (e.price || 0), 0);
  return { total, warehouse, wishlist, building, done, sold, buy_total: buyTotal, sell_total: sellTotal, net: sellTotal - buyTotal };
}
function listParts(params) {
  let list = STORE.parts.slice();
  if (params.has("owned")) { const o = params.get("owned") === "true"; list = list.filter(p => !!p.owned === o); }
  if (params.get("in_warehouse") === "true") list = list.filter(p => p.pc_id == null);
  list.sort((a, b) => b.id - a.id);
  return list.map(partDict);
}
function createPart(data) {
  const ts = nowIso();
  const p = {
    id: nextId("parts"), category: data.category, brand: data.brand || "", model: data.model,
    specs: data.specs || {}, condition: data.condition || "used", owned: data.owned !== false,
    purchase_price: data.purchase_price ?? null, market_price: data.market_price ?? null,
    pc_id: data.pc_id ?? null, created_at: ts, updated_at: ts,
  };
  STORE.parts.push(p); persist();
  return partDict(p);
}
function updatePart(id, data) {
  const p = getPart(id); if (!p) throw new Error("Part not found");
  for (const k in data) { if (data[k] !== undefined && data[k] !== null) p[k] = data[k]; }
  p.updated_at = nowIso(); persist();
  return partDict(p);
}
function deletePartH(id) {
  const idx = STORE.parts.findIndex(p => p.id === id);
  if (idx < 0) throw new Error("Part not found");
  STORE.parts.splice(idx, 1); persist();
  return { ok: true };
}
function sellPartH(id, data) {
  const p = getPart(id); if (!p) throw new Error("Part not found");
  if (p.pc_id != null) throw new Error("PC에 장착된 부품입니다. 먼저 탈착하세요.");
  const name = `${p.brand || ""} ${p.model || ""}`.trim();
  const margin = data.price - (p.purchase_price || 0);
  STORE.ledger.push({ id: nextId("ledger"), type: "sell", item: `[부품판매] ${name}`, price: data.price, pc_id: null, date: nowIso() });
  const idx = STORE.parts.findIndex(x => x.id === id);
  STORE.parts.splice(idx, 1); persist();
  return { ok: true, margin };
}
function listPcs(params) {
  let list = STORE.pcs.slice();
  if (params.get("status")) list = list.filter(p => p.status === params.get("status"));
  list.sort((a, b) => b.id - a.id);
  return list.map(pc => pcDict(pc, params.get("purpose") || "gaming"));
}
function createPc(data) {
  const p = { id: nextId("pcs"), name: (data && data.name) || "새 PC", status: "building", whole: false, purchase_price: null, sold_price: null, created_at: nowIso(), completed_at: null, sold_at: null };
  STORE.pcs.push(p); persist();
  return pcDict(p);
}
function updatePc(id, data) {
  const pc = getPcOr404(id);
  if (data.name !== undefined && data.name !== null) pc.name = data.name;
  persist();
  return pcDict(pc);
}
function deletePcFull(id) {
  getPcOr404(id);
  STORE.parts = STORE.parts.filter(p => p.pc_id !== id);
  STORE.pcs = STORE.pcs.filter(p => p.id !== id);
  persist();
  return { ok: true };
}
function attachPart(pcId, partId) {
  const pc = getPcOr404(pcId);
  const part = getPart(partId);
  if (!part) throw new Error("PC or Part not found");
  if (part.pc_id != null && part.pc_id !== pcId) throw new Error("이미 다른 PC에 장착된 부품입니다.");
  part.pc_id = pcId; persist();
  return pcDict(pc);
}
function detachPart(pcId, partId) {
  const part = STORE.parts.find(p => p.id === partId && p.pc_id === pcId);
  if (!part) throw new Error("Part not found on this PC");
  part.pc_id = null; persist();
  return pcDict(getPcOr404(pcId));
}
function completePc(id) { const pc = getPcOr404(id); pc.status = "done"; pc.completed_at = nowIso(); persist(); return pcDict(pc); }
function reopenPc(id) { const pc = getPcOr404(id); pc.status = "building"; pc.completed_at = null; persist(); return pcDict(pc); }
function sellPcH(id, data) {
  const pc = getPcOr404(id);
  pc.status = "sold"; pc.sold_price = data.price; pc.sold_at = nowIso();
  STORE.ledger.push({ id: nextId("ledger"), type: "sell", item: pc.name, price: data.price, pc_id: id, date: nowIso() });
  persist();
  return pcDict(pc);
}
function dismantlePc(id) {
  getPcOr404(id);
  STORE.parts.forEach(p => { if (p.pc_id === id) p.pc_id = null; });
  STORE.pcs = STORE.pcs.filter(p => p.id !== id);
  persist();
  return { ok: true };
}
function wholeIntake(data) {
  const ts = nowIso();
  const pc = { id: nextId("pcs"), name: data.name, status: "done", whole: true, purchase_price: data.purchase_price, sold_price: null, created_at: ts, completed_at: ts, sold_at: null };
  STORE.pcs.push(pc);
  (data.parts || []).forEach(wp => {
    STORE.parts.push({ id: nextId("parts"), category: wp.category, brand: wp.brand || "", model: wp.model, specs: wp.specs || {}, condition: "used", owned: true, purchase_price: null, market_price: null, pc_id: pc.id, created_at: ts, updated_at: ts });
  });
  STORE.ledger.push({ id: nextId("ledger"), type: "buy", item: `[통매입] ${data.name}`, price: data.purchase_price, pc_id: pc.id, date: ts });
  persist();
  return pcDict(pc);
}
function pcScore(id, params) {
  const pc = getPcOr404(id);
  const parts = STORE.parts.filter(p => p.pc_id === id);
  const cost = (pc.whole && pc.purchase_price) ? pc.purchase_price : parts.reduce((s, p) => s + (p.purchase_price || 0), 0);
  const partsData = parts.map(p => ({ category: p.category, brand: p.brand || "", model: p.model || "", specs: p.specs || {} }));
  return scoreBuild(partsData, params.get("purpose") || "gaming", cost || null);
}
function listLedger() {
  const entries = STORE.ledger.slice().sort((a, b) => (b.date || "").localeCompare(a.date || "") || b.id - a.id);
  const buyTotal = entries.filter(e => e.type === "buy").reduce((s, e) => s + (e.price || 0), 0);
  const sellTotal = entries.filter(e => e.type === "sell").reduce((s, e) => s + (e.price || 0), 0);
  return { entries, buy_total: buyTotal, sell_total: sellTotal, net: sellTotal - buyTotal };
}
function createLedger(data) {
  const e = { id: nextId("ledger"), type: data.type, item: data.item, price: data.price, pc_id: null, date: data.date || nowIso() };
  STORE.ledger.push(e); persist();
  return e;
}
function deleteLedger(id) {
  const idx = STORE.ledger.findIndex(e => e.id === id);
  if (idx < 0) throw new Error("Entry not found");
  STORE.ledger.splice(idx, 1); persist();
  return { ok: true };
}
function backupData() {
  return {
    exported_at: nowIso(),
    parts: STORE.parts.map(p => ({ id: p.id, category: p.category, brand: p.brand, model: p.model, specs: p.specs, condition: p.condition, owned: p.owned, purchase_price: p.purchase_price, market_price: p.market_price, pc_id: p.pc_id, created_at: p.created_at })),
    pcs: STORE.pcs.map(pc => ({ id: pc.id, name: pc.name, status: pc.status, whole: pc.whole, purchase_price: pc.purchase_price, sold_price: pc.sold_price, created_at: pc.created_at, completed_at: pc.completed_at, sold_at: pc.sold_at })),
    ledger: STORE.ledger.map(e => ({ id: e.id, type: e.type, item: e.item, price: e.price, pc_id: e.pc_id, date: e.date })),
  };
}
function importBackup(data) {
  const next = { seq: { parts: 0, pcs: 0, ledger: 0 }, parts: [], pcs: [], ledger: [] };
  (data.parts || []).forEach(p => {
    next.parts.push({ id: p.id, category: p.category, brand: p.brand || "", model: p.model || "", specs: p.specs || {}, condition: p.condition || "used", owned: p.owned !== false, purchase_price: p.purchase_price ?? null, market_price: p.market_price ?? null, pc_id: p.pc_id ?? null, created_at: p.created_at || nowIso(), updated_at: p.created_at || nowIso() });
    next.seq.parts = Math.max(next.seq.parts, p.id || 0);
  });
  (data.pcs || []).forEach(pc => {
    next.pcs.push({ id: pc.id, name: pc.name, status: pc.status || "building", whole: !!pc.whole, purchase_price: pc.purchase_price ?? null, sold_price: pc.sold_price ?? null, created_at: pc.created_at || nowIso(), completed_at: pc.completed_at ?? null, sold_at: pc.sold_at ?? null });
    next.seq.pcs = Math.max(next.seq.pcs, pc.id || 0);
  });
  (data.ledger || []).forEach(e => {
    next.ledger.push({ id: e.id, type: e.type, item: e.item, price: e.price, pc_id: e.pc_id ?? null, date: e.date || nowIso() });
    next.seq.ledger = Math.max(next.seq.ledger, e.id || 0);
  });
  STORE = next;
  persist();
}

// ── 엔진 데이터 로딩 (parts_db.json / benchmark_db.json / compat_tables.json) ──
let ENGINE_READY = null;
function loadEngine() {
  if (ENGINE_READY) return ENGINE_READY;
  ENGINE_READY = (async () => {
    const [partsRaw, bench, compatTables] = await Promise.all([
      fetch("parts_db.json").then(r => r.json()),
      fetch("benchmark_db.json").then(r => r.json()),
      fetch("compat_tables.json").then(r => r.json()),
    ]);
    KOREAN_ALIASES = compatTables.KOREAN_ALIASES || [];
    CPU_SOCKET_MAP_N = buildNormalizedMap(compatTables.CPU_SOCKET_MAP);
    MOTHERBOARD_SOCKET_MAP_N = buildNormalizedMap(compatTables.MOTHERBOARD_SOCKET_MAP);
    MOTHERBOARD_DDR_MAP_N = buildNormalizedMap(compatTables.MOTHERBOARD_DDR_MAP);
    CPU_TDP_N = buildNormalizedMap(compatTables.CPU_TDP);
    GPU_TDP_N = buildNormalizedMap(compatTables.GPU_TDP);
    CPU_KEYS = buildKeys(bench.cpu || []);
    GPU_KEYS = buildKeys(bench.gpu || []);
    CPU_SORTED = Object.values(CPU_KEYS).sort((a, b) => a - b);
    GPU_SORTED = Object.values(GPU_KEYS).sort((a, b) => a - b);
    loadPartsDB(partsRaw);
  })();
  return ENGINE_READY;
}

// ── frontend/index.html의 api() 가 호출하는 REST 경로를 그대로 흉내내는 라우터 ──
async function localApi(path, opt) {
  opt = opt || {};
  await loadEngine();
  const method = (opt.method || "GET").toUpperCase();
  const body = opt.json;
  const qIdx = path.indexOf("?");
  const rawPath = qIdx === -1 ? path : path.slice(0, qIdx);
  const params = new URLSearchParams(qIdx === -1 ? "" : path.slice(qIdx + 1));
  const segs = rawPath.split("/").filter(Boolean);

  try {
    if (rawPath === "/stats" && method === "GET") return getStats();
    if (rawPath === "/parts" && method === "GET") return listParts(params);
    if (rawPath === "/parts" && method === "POST") return createPart(body);
    if (segs[0] === "parts" && segs.length === 2 && method === "PUT") return updatePart(+segs[1], body);
    if (segs[0] === "parts" && segs.length === 2 && method === "DELETE") return deletePartH(+segs[1]);
    if (segs[0] === "parts" && segs[2] === "sell" && method === "POST") return sellPartH(+segs[1], body);
    if (rawPath === "/pcs" && method === "GET") return listPcs(params);
    if (rawPath === "/pcs" && method === "POST") return createPc(body);
    if (segs[0] === "pcs" && segs[1] === "whole" && method === "POST") return wholeIntake(body);
    if (segs[0] === "pcs" && segs[2] === "parts" && method === "POST") return attachPart(+segs[1], +segs[3]);
    if (segs[0] === "pcs" && segs[2] === "parts" && method === "DELETE") return detachPart(+segs[1], +segs[3]);
    if (segs[0] === "pcs" && segs[2] === "complete" && method === "POST") return completePc(+segs[1]);
    if (segs[0] === "pcs" && segs[2] === "reopen" && method === "POST") return reopenPc(+segs[1]);
    if (segs[0] === "pcs" && segs[2] === "sell" && method === "POST") return sellPcH(+segs[1], body);
    if (segs[0] === "pcs" && segs[2] === "dismantle" && method === "POST") return dismantlePc(+segs[1]);
    if (segs[0] === "pcs" && segs[2] === "score" && method === "GET") return pcScore(+segs[1], params);
    if (segs[0] === "pcs" && segs.length === 2 && method === "GET") return pcDict(getPcOr404(+segs[1]), params.get("purpose") || "gaming");
    if (segs[0] === "pcs" && segs.length === 2 && method === "PUT") return updatePc(+segs[1], body);
    if (segs[0] === "pcs" && segs.length === 2 && method === "DELETE") return deletePcFull(+segs[1]);
    if (rawPath === "/ledger" && method === "GET") return listLedger();
    if (rawPath === "/ledger" && method === "POST") return createLedger(body);
    if (segs[0] === "ledger" && segs.length === 2 && method === "DELETE") return deleteLedger(+segs[1]);
    if (rawPath === "/db/search" && method === "GET") return searchPartsDB(params.get("q") || "", params.get("category") || "");
    if (rawPath === "/backup" && method === "GET") return backupData();
    if (rawPath.startsWith("/prices/")) throw new Error("PWA(로컬 전용) 버전에서는 실시간 시세 조회를 지원하지 않습니다 — 판매가를 직접 입력해주세요.");
  } catch (e) {
    throw e;
  }
  throw new Error("알 수 없는 API: " + path);
}
