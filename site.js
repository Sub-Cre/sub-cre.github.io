/* Animaciones del sitio. Todo el contenido es legible sin JavaScript; esto solo lo anima. */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var css = function (name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); };
  var ease = function (p) { return p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2; };
  var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };

  /* ---------- formato de números en español ---------- */
  function fmt(v, dec, miles) {
    var s = v.toFixed(dec).split(".");
    var ent = s[0];
    if (miles) ent = ent.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    return dec ? ent + "," + s[1] : ent;
  }
  function parseNum(txt) {
    var m = txt.match(/\d+(?:[.,]\d+)*/g);
    if (!m) return null;
    var raw = m[m.length - 1];
    var idx = txt.lastIndexOf(raw);
    var dec = raw.indexOf(",") > -1 ? raw.split(",")[1].length : 0;
    var val = parseFloat(raw.replace(/\./g, "").replace(",", "."));
    return { raw: raw, idx: idx, dec: dec, miles: raw.indexOf(".") > -1, val: val };
  }
  function countUp(el, dur, from) {
    var txt = el.textContent, n = parseNum(txt);
    if (!n || !n.val || reduce) return;
    var pre = txt.slice(0, n.idx), post = txt.slice(n.idx + n.raw.length), t0 = null;
    from = from || 0;
    function step(ts) {
      if (t0 === null) t0 = ts;
      var p = ease(clamp((ts - t0) / dur));
      el.textContent = pre + fmt(from + (n.val - from) * p, n.dec, n.miles) + post;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  function onView(el, cb, threshold) {
    if (!("IntersectionObserver" in window)) { cb(); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { io.disconnect(); cb(); } });
    }, { threshold: threshold || 0.4 });
    io.observe(el);
  }

  /* ---------- barra de progreso de lectura ---------- */
  var bar = document.querySelector(".progress");
  if (bar) {
    var upd = function () {
      var h = document.documentElement.scrollHeight - innerHeight;
      bar.style.setProperty("--p", h > 0 ? (scrollY / h).toFixed(4) : 0);
    };
    addEventListener("scroll", upd, { passive: true });
    upd();
  }

  /* ---------- cifras que se cuentan al aparecer ---------- */
  document.querySelectorAll(".r-metric b, .case td").forEach(function (el) {
    onView(el, function () { countUp(el, 1000); }, 0.8);
  });

  /* ---------- Fig. 1: calidad antes / después ---------- */
  var q = document.getElementById("quality");
  if (q) {
    var rows = q.querySelectorAll(".q-row"), btns = q.querySelectorAll(".seg button"), avg = q.querySelector("[data-avg]");
    var estado = "antes";
    var setState = function (s) {
      if (s === estado) return;
      var sum = 0, prevSum = 0;
      rows.forEach(function (r) {
        var a = parseFloat(r.dataset[estado]), b = parseFloat(r.dataset[s]);
        prevSum += a; sum += b;
        r.querySelector(".q-fill").style.setProperty("--w", b + "%");
        var v = r.querySelector(".q-val");
        v.textContent = Math.round(b) + " %";
        countUp(v, 900, Math.round(a));
      });
      avg.textContent = Math.round(sum / rows.length) + " %";
      countUp(avg, 900, Math.round(prevSum / rows.length));
      q.classList.toggle("done", s === "despues");
      btns.forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.state === s)); });
      estado = s;
    };
    btns.forEach(function (b) { b.addEventListener("click", function () { setState(b.dataset.state); }); });
    onView(q, function () { setTimeout(function () { setState("despues"); }, reduce ? 0 : 500); }, 0.5);
  }

  /* ---------- Fig. 0: registros desordenados que se fusionan y se ordenan por ciudad ---------- */
  var cv = document.getElementById("sorter-canvas");
  if (!cv) return;
  var ctx = cv.getContext("2d");
  var CIUDADES = [["Santa Cruz", "Sta. Cruz", 552], ["La Paz", "La Paz", 426], ["Cochabamba", "Cbba.", 347],
                  ["El Alto", "El Alto", 195], ["Sucre", "Sucre", 175], ["Tarija", "Tarija", 103]];
  var UNIDAD = 6, POR_FILA = 6, DUPS = Math.round(218 / UNIDAD);
  var CRUDOS = ["SCZ", "sta. cruz", "+591 7123 4567", "7123-4567", "1.250,50", "Bs 980,00", "05/03/2024",
                "2024-03-05", "MARIA  GUTIERREZ", "ana.lopez@GMAIL.COM", "cbba", "pendiente", "591-712-34567", "la paz "];
  var T_MERGE = 900, T_SORT = 1900, SORT_DUR = 1300, STAGGER = 700, T_LABEL = 3700, T_END = 4700;

  var seed = 7;
  var rnd = function () { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
  var dots = [], dups = [], tags = [], W = 0, H = 0, t0 = null, running = false, done = false;

  CIUDADES.forEach(function (c, ci) {
    var n = Math.round(c[2] / UNIDAD);
    for (var j = 0; j < n; j++) dots.push({ c: ci, j: j, rx: rnd(), ry: rnd(), ph: rnd() * 6.28 });
  });
  dots.forEach(function (d, i) { d.order = i / dots.length; });
  for (var k = 0; k < DUPS; k++) dups.push({ rx: rnd(), ry: rnd(), ph: rnd() * 6.28, twin: Math.floor(rnd() * dots.length) });
  CRUDOS.forEach(function (s) { tags.push({ s: s, rx: rnd(), ry: rnd() }); });

  function size() {
    var r = cv.getBoundingClientRect(), dpr = Math.min(devicePixelRatio || 1, 2);
    W = r.width; H = r.height;
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  function layout() {
    var colW = W / CIUDADES.length, maxRows = Math.ceil(dots.filter(function (d) { return d.c === 0; }).length / POR_FILA);
    var s = Math.min(12, (colW * 0.62) / POR_FILA, (H - 64) / maxRows);
    return { colW: colW, s: s, base: H - 48, r: Math.max(1.6, s * 0.34) };
  }
  function target(d, L) {
    var cx = L.colW * (d.c + 0.5), row = Math.floor(d.j / POR_FILA), k = d.j % POR_FILA;
    return [cx + (k - (POR_FILA - 1) / 2) * L.s, L.base - 8 - row * L.s];
  }
  function scatter(o, t) {
    return [12 + o.rx * (W - 24) + Math.sin(t * 0.0012 + o.ph) * 4, 10 + o.ry * (H - 70) + Math.cos(t * 0.001 + o.ph) * 4];
  }
  function circle(x, y, r, color, a) {
    if (a <= 0) return;
    ctx.globalAlpha = a; ctx.fillStyle = color;
    ctx.beginPath(); ctx.arc(x, y, r, 0, 6.2832); ctx.fill();
  }

  var ledger = document.querySelectorAll(".ledger b"), ledSpans = document.querySelectorAll(".ledger span");
  var led = { dup: false, uni: false };
  function ledgerReset() {
    ledger[1].textContent = "–"; ledger[2].textContent = "–";
    ledSpans.forEach(function (s) { s.classList.remove("on"); });
    led.dup = led.uni = false;
  }
  function ledgerAt(t) {
    if (!led.dup && t >= T_MERGE) { led.dup = true; ledSpans[1].classList.add("on"); ledger[1].textContent = "218"; countUp(ledger[1], 900); }
    if (!led.uni && t >= T_LABEL - 300) { led.uni = true; ledSpans[1].classList.remove("on"); ledSpans[2].classList.add("on"); ledger[2].textContent = "1.798"; countUp(ledger[2], 900); }
  }

  function draw(t) {
    var L = layout(), accent = css("--accent"), muted = css("--ink-soft"), warm = css("--warm"), ink = css("--ink"), rule = css("--rule");
    ctx.clearRect(0, 0, W, H);

    // fragmentos de texto crudo que desaparecen al ordenar
    var ta = 1 - clamp((t - T_SORT + 300) / 700);
    if (ta > 0) {
      ctx.font = "11px 'IBM Plex Mono', Consolas, monospace"; ctx.textAlign = "left";
      tags.forEach(function (g, i) {
        var p = scatter(g, t + i * 500);
        ctx.globalAlpha = 0.55 * ta; ctx.fillStyle = muted;
        ctx.fillText(g.s, Math.min(p[0], W - ctx.measureText(g.s).width - 6), p[1]);
      });
    }

    // eje base
    var la = clamp((t - T_SORT) / 800);
    ctx.globalAlpha = la; ctx.strokeStyle = rule; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(0, L.base + 0.5); ctx.lineTo(W, L.base + 0.5); ctx.stroke();

    // duplicados: viajan hacia su gemelo y se fusionan
    dups.forEach(function (d) {
      var p = ease(clamp((t - T_MERGE) / 1000)), a = scatter(d, t), b = scatter(dots[d.twin], t);
      circle(a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p, L.r, warm, t < T_MERGE ? 0.9 : 1 - p);
    });

    // registros únicos: se ordenan por ciudad
    dots.forEach(function (d) {
      var p = ease(clamp((t - T_SORT - d.order * STAGGER) / SORT_DUR)), a = scatter(d, t), b = target(d, L);
      var x = a[0] + (b[0] - a[0]) * p, y = a[1] + (b[1] - a[1]) * p;
      circle(x, y, L.r, muted, (1 - p) * 0.75);
      circle(x, y, L.r, accent, p);
    });

    // etiquetas por ciudad
    var lb = clamp((t - T_LABEL) / 500);
    if (lb > 0) {
      ctx.textAlign = "center";
      CIUDADES.forEach(function (c, ci) {
        var cx = L.colW * (ci + 0.5);
        var n = Math.round(c[2] * ease(clamp((t - T_LABEL) / 800)));
        ctx.globalAlpha = lb; ctx.fillStyle = muted;
        ctx.font = "13px 'IBM Plex Sans', system-ui, sans-serif";
        ctx.fillText(L.colW < 95 ? c[1] : c[0], cx, L.base + 20);
        ctx.fillStyle = ink; ctx.font = "500 13px 'IBM Plex Mono', Consolas, monospace";
        ctx.fillText(fmt(n, 0, true), cx, L.base + 38);
      });
    }
    ctx.globalAlpha = 1;
  }

  function frame(ts) {
    if (t0 === null) t0 = ts;
    var t = ts - t0;
    ledgerAt(t);
    draw(t);
    if (t < T_END) requestAnimationFrame(frame);
    else { running = false; done = true; }
  }
  function start() {
    if (running) return;
    size();
    if (reduce) { done = true; draw(T_END); return; }
    ledgerReset(); t0 = null; running = true; done = false;
    requestAnimationFrame(frame);
  }

  size(); draw(0);
  var go = function () { onView(cv, start, 0.12); };
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(go); else go();
  document.getElementById("replay").addEventListener("click", start);
  addEventListener("resize", function () { if (!running) { size(); draw(done ? T_END : 0); } });
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () { if (!running) draw(done ? T_END : 0); });
})();
