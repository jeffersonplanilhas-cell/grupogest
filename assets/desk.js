/* GrupoGest · a pilha
   Os papéis de um dia de trabalho caem sobre a página. Dá para pegar, arrastar e jogar.
   Quando o sistema liga (botão ou rolagem), cada papel vai para a sua regra e fica registrado.
   Sem JavaScript: os papéis aparecem como lista. Com movimento reduzido: sem física, estados diretos. */
(function () {
  "use strict";
  var hero = document.getElementById("pilha");
  if (!hero) return;
  var desk = hero.querySelector(".desk");
  var papers = Array.prototype.slice.call(desk.querySelectorAll(".paper"));
  var lanes = Array.prototype.slice.call(hero.querySelectorAll(".lane"));
  var toggle = document.getElementById("sys-toggle");
  var status = document.getElementById("sys-status");
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var on = false, touched = false, M = null, engine = null, bodies = [], solids = [], walls = [];
  var raf = 0, visible = true, dragging = null, lastW = 0;


  function active() { return papers.filter(function (p) { return getComputedStyle(p).display !== "none"; }); }
  function rectIn(el) { var h = hero.getBoundingClientRect(), r = el.getBoundingClientRect(); return { x: r.left - h.left, y: r.top - h.top, w: r.width, h: r.height }; }
  function place(p, x, y, a) { p.style.transform = "translate(" + (x - p._w / 2).toFixed(1) + "px," + (y - p._h / 2).toFixed(1) + "px) rotate(" + a.toFixed(4) + "rad)"; }

  // ── onde cada papel fica quando o sistema está ligado ──
  function targets() {
    var list = active(), out = new Map();
    lanes.forEach(function (lane) {
      var t = lane.dataset.t, slot = lane.querySelector(".lane-slot"), r = rectIn(slot);
      var mine = list.filter(function (p) { return p.dataset.t === t; });
      mine.forEach(function (p, i) {
        var s = Math.min(1, r.h / p._h), step = 7;
        var left = r.x + i * step, top = r.y + (r.h - p._h * s) / 2 - i * 2;
        // origem da transformação no centro: compensa a escala para alinhar pela esquerda
        out.set(p, { tx: left - p._w * (1 - s) / 2, ty: top - p._h * (1 - s) / 2, x: left + p._w * s / 2, y: top + p._h * s / 2, s: s });
      });
      var n = lane.querySelector(".lane-n"); if (n) n.textContent = mine.length;
    });
    return out;
  }

  // ── estados ──
  function setOn(v, instant) {
    on = v;
    hero.classList.toggle("is-on", on);
    toggle.setAttribute("aria-pressed", on ? "true" : "false");
    toggle.querySelector(".tl").textContent = on ? "Desligar o sistema" : "Ligar o sistema";
    var list = active();
    if (status) status.textContent = on ? list.length + " papéis · " + lanes.length + " regras · nada esperando alguém" : "sistema desligado · " + list.length + " papéis na pilha";
    if (on) {
      markTops();
      var tg = targets();
      list.forEach(function (p, i) {
        var t = tg.get(p); if (!t) return;
        if (p._body && M) { M.Composite.remove(engine.world, p._body); }
        var to = "translate(" + t.tx.toFixed(1) + "px," + t.ty.toFixed(1) + "px) rotate(0rad) scale(" + t.s.toFixed(3) + ")";
        if (instant || reduce || !p.animate) { p.style.transform = to; return; }
        var from = p.style.transform || to;
        p.animate([{ transform: from }, { transform: to }], { duration: 760, delay: i * 45, easing: "cubic-bezier(.7,0,.2,1)", fill: "backwards" });
        p.style.transform = to;
      });
      stop();
    } else if (M) {
      list.forEach(function (p, i) {
        var b = p._body; if (!b) return;
        var t = p._last || { x: p._w, y: 0 };
        M.Body.setPosition(b, { x: t.x, y: t.y });
        M.Body.setAngle(b, 0);
        M.Body.setVelocity(b, { x: (Math.random() - 0.5) * 10, y: -4 - Math.random() * 6 });
        M.Body.setAngularVelocity(b, (Math.random() - 0.5) * 0.25);
        M.Composite.add(engine.world, b);
      });
      loop();
    } else {
      scatterStatic();
    }
  }

  // posição de cada papel no estado ligado, para desligar a partir dali
  function remember() {
    var tg = targets();
    active().forEach(function (p) { var t = tg.get(p); if (t) p._last = { x: t.x, y: t.y }; });
  }

  // sem física: bagunça estática e determinística
  function markTops() {
    lanes.forEach(function (lane) {
      var mine = active().filter(function (p) { return p.dataset.t === lane.dataset.t; });
      mine.forEach(function (p, i) { p.classList.toggle("is-top", i === mine.length - 1); });
    });
  }
  // área livre da primeira dobra: coluna da direita no desktop, faixa entre o título e os botões no celular
  function freeZone() {
    var W = hero.clientWidth, c = rectIn(hero.querySelector(".pilha-copy")), k = rectIn(hero.querySelector(".pilha-ctl"));
    if (W >= 960) { var L = rectIn(hero.querySelector(".lanes")); return { x: L.x, y: c.y, w: L.w, h: k.y + k.h - c.y }; }
    var top = c.y + c.h + 8;
    return { x: 12, y: top, w: W - 24, h: Math.max(120, k.y - 12 - top) };
  }
  function scatterStatic() {
    var seed = 11, z = freeZone();
    function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
    active().forEach(function (p) {
      var x = z.x + p._w / 2 + rnd() * Math.max(0, z.w - p._w);
      var y = z.y + z.h - p._h / 2 - Math.pow(rnd(), 1.3) * Math.max(0, z.h - p._h);
      place(p, x, y, (rnd() - 0.5) * 0.4);
    });
  }

  function measure() {
    papers.forEach(function (p) { p.style.transform = "none"; p._w = p.offsetWidth; p._h = p.offsetHeight; });
  }

  // ── física ──
  function build() {
    var W = hero.clientWidth, H = hero.clientHeight;
    engine = M.Engine.create({ enableSleeping: true });
    engine.gravity.y = 1.1;
    var t = 200;
    walls = [
      M.Bodies.rectangle(W / 2, H + t / 2, W * 3, t, { isStatic: true }),
      M.Bodies.rectangle(-t / 2, H / 2 - H, t, H * 4, { isStatic: true }),
      M.Bodies.rectangle(W + t / 2, H / 2 - H, t, H * 4, { isStatic: true })
    ];
    solids = Array.prototype.slice.call(hero.querySelectorAll("[data-solid]")).map(function (el) {
      var r = rectIn(el);
      return M.Bodies.rectangle(r.x + r.w / 2, r.y + r.h / 2, r.w, r.h, { isStatic: true, friction: 0.8 });
    });
    M.Composite.add(engine.world, walls.concat(solids));
    var list = active(), n = list.length;
    // faixa onde a pilha cresce: coluna da direita no desktop, largura toda no celular
    var band = { l: 12, w: W - 24 };
    if (W >= 960) { var L = rectIn(hero.querySelector(".lanes")); band = { l: L.x + L.w / 2 - Math.min(460, L.w) / 2, w: Math.min(460, L.w) }; }
    list.forEach(function (p, i) {
      var x = band.l + p._w / 2 + ((i * 0.618034 + 0.13) % 1) * Math.max(10, band.w - p._w);
      var y = -p._h - (i * 55) - Math.random() * 40;
      var b = M.Bodies.rectangle(x, y, p._w, p._h, { friction: 0.85, frictionStatic: 1.2, frictionAir: 0.02, restitution: 0.05, density: 0.0016, angle: (Math.random() - 0.5) * 0.7 });
      b._el = p; p._body = b; bodies.push(b);
      place(p, x, y, b.angle);
    });
    M.Composite.add(engine.world, bodies);
    lastW = W;
  }
  function frame() {
    raf = 0;
    if (!engine || on || !visible) return;
    M.Engine.update(engine, 1000 / 60);
    var awake = false;
    bodies.forEach(function (b) {
      if (!b.isSleeping) awake = true;
      var y = b.position.y;
      if (y > hero.clientHeight + 400) { M.Body.setPosition(b, { x: hero.clientWidth / 2, y: -80 }); M.Body.setVelocity(b, { x: 0, y: 0 }); }
      place(b._el, b.position.x, y, b.angle);
    });
    if (awake || dragging) loop();
  }
  function loop() { if (!raf) raf = requestAnimationFrame(frame); }
  function stop() { if (raf) cancelAnimationFrame(raf); raf = 0; }

  // ── pegar, arrastar e jogar ──
  function point(e) { var h = hero.getBoundingClientRect(); return { x: e.clientX - h.left, y: e.clientY - h.top }; }
  papers.forEach(function (p) {
    p.addEventListener("pointerdown", function (e) {
      if (!M || on || !p._body || e.button > 0) return;
      e.preventDefault();
      touched = true;
      var b = p._body, pt = point(e);
      M.Sleeping.set(b, false);
      var local = M.Vector.rotate(M.Vector.sub(pt, b.position), -b.angle);
      dragging = M.Constraint.create({ pointA: pt, bodyB: b, pointB: local, stiffness: 0.18, damping: 0.08, length: 0 });
      M.Composite.add(engine.world, dragging);
      p.classList.add("is-held");
      try { p.setPointerCapture(e.pointerId); } catch (x) {}
      loop();
    });
    p.addEventListener("pointermove", function (e) { if (dragging && dragging.bodyB === p._body) { dragging.pointA = point(e); loop(); } });
    function up() {
      if (!dragging || dragging.bodyB !== p._body) return;
      M.Composite.remove(engine.world, dragging); dragging = null;
      p.classList.remove("is-held"); loop();
    }
    p.addEventListener("pointerup", up); p.addEventListener("pointercancel", up);
  });

  toggle.addEventListener("click", function () {
    touched = true;
    if (on) remember();
    setOn(!on);
  });

  // quem rola sem clicar vê o sistema ligar sozinho
  var auto = function () {
    if (touched || on) return;
    if (window.scrollY > hero.offsetHeight * 0.22) { setOn(true); window.removeEventListener("scroll", auto); }
  };
  window.addEventListener("scroll", auto, { passive: true });

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible && !on) loop(); }, { threshold: 0 }).observe(hero);
  }
  document.addEventListener("visibilitychange", function () { visible = !document.hidden; if (visible && !on) loop(); });

  var resizeT = 0;
  window.addEventListener("resize", function () {
    clearTimeout(resizeT);
    resizeT = setTimeout(function () {
      if (Math.abs(hero.clientWidth - lastW) < 40) { if (on) setOn(true, true); return; }
      stop(); measure();
      if (engine && M) { M.Composite.clear(engine.world, false); M.Engine.clear(engine); bodies = []; build(); }
      if (on) setOn(true, true); else if (!M) scatterStatic(); else loop();
    }, 200);
  });

  // ── início ──
  measure();
  function fallback() { scatterStatic(); hero.classList.add("is-ready"); }
  if (reduce) { fallback(); return; }
  var s = document.createElement("script");
  s.src = desk.dataset.engine;
  s.async = true;
  s.onload = function () {
    M = window.Matter; if (!M) return;
    if (on) { bodies = []; build(); papers.forEach(function (p) { if (p._body) M.Composite.remove(engine.world, p._body); }); setOn(true, true); return; }
    build(); hero.classList.add("is-ready"); loop();
  };
  s.onerror = function () { hero.classList.add("no-engine"); fallback(); };
  setTimeout(function () { if (!M) fallback(); }, 4000);
  document.head.appendChild(s);
})();
