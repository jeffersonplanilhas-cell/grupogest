/* GrupoGest · comportamento do site
   Sem dependências. Cada módulo só roda se o elemento existir na página. */
(function () {
  "use strict";

  // ── Configuração de contato ────────────────────────────────────────────
  // whatsapp: só dígitos, com 55 + DDD (ex.: "5516999999999"). Vazio = o site não mostra WhatsApp.
  // formEndpoint: URL que recebe POST do formulário (Formspree, Web3Forms ou rota própria).
  //   Vazio = o formulário monta a mensagem e oferece e-mail/cópia, sem enviar nada sozinho.
  var CONFIG = {
    email: "carmojefferson868@gmail.com",
    whatsapp: "",
    formEndpoint: ""
  };

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  function copyText(text, btn, done) {
    function ok() { if (btn) { var t = btn.textContent; btn.textContent = done || "Copiado"; setTimeout(function () { btn.textContent = t; }, 1600); } }
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); ok(); } catch (e) {}
      document.body.removeChild(ta);
    }
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(ok, fallback);
      else fallback();
    } catch (e) { fallback(); }
  }

  // ── Contato: e-mail e WhatsApp onde houver ─────────────────────────────
  $$("[data-email]").forEach(function (el) { el.textContent = CONFIG.email; });
  $$("[data-copy-email]").forEach(function (b) {
    b.addEventListener("click", function () { copyText(CONFIG.email, b); });
  });
  $$("[data-whatsapp-row]").forEach(function (row) {
    if (!CONFIG.whatsapp) { row.hidden = true; return; }
    var a = $("a", row), v = $("[data-whatsapp-num]", row);
    if (a) a.href = "https://wa.me/" + CONFIG.whatsapp;
    if (v) v.textContent = "+" + CONFIG.whatsapp.replace(/^(\d{2})(\d{2})(\d{4,5})(\d{4})$/, "$1 $2 $3-$4");
  });

  // ── 1. Registro do hero: ruído → registro ──────────────────────────────
  (function ledger() {
    var led = $("#ledger"); if (!led) return;
    var hero = led.closest(".hero");
    var ins = $$(".lr-in", led);
    var rules = $$(".lr-rule", led);
    var replay = $("#ledger-replay");
    var seed = 7;
    function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }

    function visibleRows() { return ins.filter(function (el) { return el.offsetParent !== null; }); }

    function scatter() {
      seed = 7 + Math.floor(Math.random() * 1000);
      var H = hero.getBoundingClientRect(), vw = document.documentElement.clientWidth, vh = window.innerHeight;
      // área visível do hero: o ruído acontece onde a pessoa está olhando
      var V = { l: 6, r: vw - 6, t: Math.max(H.top, 64) + 8, b: Math.min(H.bottom, vh) - 12 };
      if (V.b - V.t < 160) V = { l: 6, r: vw - 6, t: H.top + 8, b: H.bottom - 12 };
      var side = $(".hero-side"), S = side ? side.getBoundingClientRect() : null;
      var range = document.createRange();
      visibleRows().forEach(function (el) {
        el.style.transition = "none";
        el.style.transform = "none";
        var r = el.getBoundingClientRect();
        range.selectNodeContents(el);
        var tw = Math.min(range.getBoundingClientRect().width, r.width);
        var sc = 0.95 + rnd() * (vw < 600 ? 0.2 : 0.55), w = Math.min(tw * sc, (V.r - V.l) * 0.94), tx, ty, tries = 0;
        do {
          tx = V.l + rnd() * Math.max(4, V.r - V.l - w);
          ty = V.t + rnd() * Math.max(4, V.b - V.t - 34);
          tries++;
        } while (S && tries < 40 && tx < S.right + 8 && tx + w > S.left - 8 && ty < S.bottom + 8 && ty + 34 > S.top - 8);
        var rot = (rnd() - 0.5) * 12;
        el.style.transform = "translate(" + Math.round(tx - r.left) + "px," + Math.round(ty - r.top) + "px) rotate(" + rot.toFixed(1) + "deg) scale(" + sc.toFixed(2) + ")";
      });
      void led.offsetWidth;
    }

    function order() {
      led.classList.add("is-ordering");
      visibleRows().forEach(function (el, i) {
        var d = i * 55;
        el.style.transition = "transform .95s var(--ease) " + d + "ms, font-variation-settings .95s var(--ease) " + d + "ms, color .95s var(--ease) " + d + "ms";
        el.style.transform = "none";
      });
      rules.forEach(function (el, i) { el.style.setProperty("--d", (900 + i * 70) + "ms"); });
      led.classList.remove("is-noise");
      setTimeout(function () {
        led.classList.remove("is-ordering");
        rules.forEach(function (el) { el.style.removeProperty("--d"); });
      }, 2200);
    }

    function run(delay) {
      if (reduce) { led.classList.remove("is-noise"); led.classList.add("is-ready"); return; }
      led.classList.add("is-noise");
      scatter();
      led.classList.add("is-ready");
      setTimeout(order, delay);
    }

    if (reduce) { led.classList.add("is-ready"); if (replay) replay.hidden = true; return; }

    var started = false;
    function start() { if (started) return; started = true; run(650); }
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { start(); io.disconnect(); } });
      }, { threshold: 0.25, rootMargin: "0px 0px -35% 0px" });
      io.observe(led);
    } else start();
    // se as fontes chegarem depois, a posição final se ajusta sozinha (transform relativo)
    if (replay) replay.addEventListener("click", function () { run(250); });
  })();

  // ── 2. A máquina: entrada → regra → ação e resultado ───────────────────
  (function machine() {
    var root = $("#mach"); if (!root) return;
    var SCRIPT = [
      { ch: "whatsapp", t: "boa tarde! 40 caixas do modelo 42 até sexta, boleto pro financeiro", r: "pedido", ok: "pedido registrado · boleto emitido", man: "alguém redigita o pedido e emite o boleto" },
      { ch: "e-mail", t: "segue o comprovante da parcela de setembro, R$ 1.280", r: "pagamento", ok: "parcela baixada · recibo enviado", man: "alguém confere o extrato e dá baixa" },
      { ch: "site", t: "vocês entregam em Ribeirão Preto?", r: "pergunta", ok: "respondido com a tabela de frete", man: "alguém responde quando vir" },
      { ch: "whatsapp", t: "quero 15 pares do 38, cor café", r: "pedido", ok: "pedido registrado · link de pagamento enviado", man: "alguém anota e manda o link" },
      { ch: "agenda", t: "sexta, 17h: fechamento da semana", r: "resumo", ok: "resumo da semana enviado ao sócio", man: "alguém junta as planilhas" },
      { ch: "whatsapp", t: "paguei no pix agora, R$ 640", r: "pagamento", ok: "pagamento conciliado", man: "alguém confere o banco" },
      { ch: "site", t: "qual o prazo de entrega?", r: "pergunta", ok: "respondido na hora", man: "alguém responde depois" },
      { ch: "e-mail", t: "pedido 1182: 60 caixas do 40, entrega dia 30", r: "pedido", ok: "pedido registrado · separação avisada", man: "alguém redigita no sistema" },
      { ch: "whatsapp", t: "o boleto venceu, pode mandar outro?", r: "pagamento", ok: "2ª via enviada", man: "alguém gera a 2ª via" },
      { ch: "site", t: "vocês emitem nota fiscal?", r: "pergunta", ok: "respondido com o procedimento", man: "alguém responde depois" }
    ];
    var rules = {};
    $$(".rule", root).forEach(function (b) { rules[b.dataset.r] = b.getAttribute("aria-checked") === "true"; });
    var qEl = $("#m-queue"), aEl = $("#m-auto"), mEl = $("#m-man"), nowEl = $("#m-now");
    var aN = $("#m-auto-n"), mN = $("#m-man-n");
    var btnPlay = $("#m-play"), btnStep = $("#m-step"), btnReset = $("#m-reset");
    var idx = 0, doneCount = 0, queue = [], pile = [], timer = null, userPaused = false, visible = false, pageHidden = false;
    var MAX_LOG = 5;

    function el(item, cls, text2) {
      var li = document.createElement("li");
      li.className = "item " + (cls || "");
      var ch = document.createElement("span"); ch.className = "ch mono"; ch.textContent = item.ch;
      var t = document.createElement("span"); t.className = "t"; t.textContent = item.t;
      li.appendChild(ch); li.appendChild(t);
      if (text2) { var r = document.createElement("span"); r.className = "res mono"; r.textContent = text2; li.appendChild(r); }
      li._item = item;
      return li;
    }
    function counts() {
      aN.textContent = doneCount; mN.textContent = pile.length;
    }
    function flip(fromEl, toEl) {
      if (reduce || !fromEl || !fromEl.isConnected || !toEl.animate) return;
      var a = fromEl.getBoundingClientRect(), b = toEl.getBoundingClientRect();
      var dx = a.left - b.left, dy = a.top - b.top;
      toEl.animate([{ transform: "translate(" + dx + "px," + dy + "px)", opacity: .9 }, { transform: "none", opacity: 1 }], { duration: 620, easing: "cubic-bezier(.7,0,.2,1)" });
    }
    function trim(list, max) { while (list.children.length > max) list.removeChild(list.lastElementChild); }

    function arrive() {
      var item = SCRIPT[idx % SCRIPT.length]; idx++;
      var li = el(item, reduce ? "" : "enter");
      qEl.insertBefore(li, qEl.firstChild);
      queue.push(li);
      if (nowEl) nowEl.textContent = item.ch + " · " + item.t;
    }
    function processOldest() {
      var li = queue.shift(); if (!li) return;
      var item = li._item, auto = !!rules[item.r];
      var out;
      if (auto) {
        out = el(item, "auto", item.ok);
        aEl.insertBefore(out, aEl.firstChild);
        doneCount++;
        trim(aEl, MAX_LOG);
      } else {
        out = el(item, "man", item.man);
        mEl.insertBefore(out, mEl.firstChild);
        pile.push(out);
        trim(mEl, MAX_LOG + 1);
      }
      flip(li, out);
      li.remove();
      counts();
    }
    function tick() {
      if (queue.length >= 2) processOldest();
      arrive();
    }
    function drain(rule) {
      var moving = pile.filter(function (p) { return p._item.r === rule; });
      moving.forEach(function (p, i) {
        setTimeout(function () {
          var item = p._item;
          var out = el(item, "auto", item.ok);
          aEl.insertBefore(out, aEl.firstChild);
          flip(p, out);
          if (p.isConnected) p.remove();
          doneCount++;
          pile = pile.filter(function (x) { return x !== p; });
          trim(aEl, MAX_LOG);
          counts();
        }, reduce ? 0 : i * 140);
      });
    }
    function setRunning() {
      var should = !reduce && !userPaused && visible && !pageHidden;
      if (should && !timer) timer = setInterval(tick, 1700);
      if (!should && timer) { clearInterval(timer); timer = null; }
      if (btnPlay) {
        btnPlay.textContent = userPaused ? "Continuar" : "Pausar";
        btnPlay.setAttribute("aria-pressed", userPaused ? "true" : "false");
        btnPlay.hidden = reduce;
      }
    }
    function reset() {
      qEl.innerHTML = ""; aEl.innerHTML = ""; mEl.innerHTML = "";
      idx = 0; doneCount = 0; queue = []; pile = [];
      // estado inicial completo: algo feito, algo parado, algo chegando
      for (var i = 0; i < 4; i++) { arrive(); if (queue.length >= 2) processOldest(); }
      $$(".item", root).forEach(function (n) { n.classList.remove("enter"); n.getAnimations && n.getAnimations().forEach(function (a) { a.finish(); }); });
      counts();
    }

    $$(".rule", root).forEach(function (b) {
      b.addEventListener("click", function () {
        var on = b.getAttribute("aria-checked") !== "true";
        b.setAttribute("aria-checked", on ? "true" : "false");
        rules[b.dataset.r] = on;
        if (on) drain(b.dataset.r);
      });
    });
    if (btnPlay) btnPlay.addEventListener("click", function () { userPaused = !userPaused; setRunning(); });
    if (btnStep) btnStep.addEventListener("click", function () { tick(); });
    if (btnReset) btnReset.addEventListener("click", function () { reset(); });

    reset();
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) { visible = e.isIntersecting; setRunning(); });
      }, { threshold: 0.25 }).observe(root);
    } else { visible = true; setRunning(); }
    document.addEventListener("visibilitychange", function () { pageHidden = document.hidden; setRunning(); });
    setRunning();
  })();

  // ── 3. A conta do trabalho repetido ────────────────────────────────────
  var lastCalc = null;
  (function calc() {
    var P = $("#c-people"), H = $("#c-hours"), R = $("#c-rate"); if (!P) return;
    function brl(n) { return "R$ " + (Math.round(n / 100) * 100).toLocaleString("pt-BR"); }
    function fill(x) { x.style.setProperty("--pct", ((x.value - x.min) / (x.max - x.min) * 100) + "%"); }
    function run() {
      [P, H, R].forEach(fill);
      var p = +P.value, h = +H.value, r = +R.value;
      $("#o-people").textContent = p;
      $("#o-hours").textContent = h + " h";
      $("#o-rate").textContent = "R$ " + r;
      var hours = p * h * 4.33, cost = hours * r;
      var lo = brl(cost * 0.8), hi = brl(cost * 1.2);
      $("#r-range").textContent = lo + " a " + hi;
      $("#r-sub").textContent = "por mês, em cerca de " + Math.round(hours) + " horas de trabalho repetido";
      lastCalc = { hours: Math.round(hours), lo: lo, hi: hi };
    }
    [P, H, R].forEach(function (x) { x.addEventListener("input", run); });
    run();
    var carry = $("#r-carry");
    if (carry) carry.addEventListener("click", function (e) {
      var ta = $("#f-problem"); if (!ta) return;
      e.preventDefault();
      var line = "Fiz a conta no site: cerca de " + lastCalc.hours + " horas por mês em trabalho repetido (entre " + lastCalc.lo + " e " + lastCalc.hi + ").";
      ta.value = ta.value ? ta.value.replace(/^Fiz a conta no site:.*\n?/, "") : "";
      ta.value = line + "\n" + ta.value;
      $("#conversa").scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
      setTimeout(function () { ta.focus(); ta.setSelectionRange(ta.value.length, ta.value.length); }, reduce ? 0 : 500);
    });
  })();

  // ── 4. Formulário: nunca falhar em silêncio ────────────────────────────
  (function form() {
    var f = $("#talk-form"); if (!f) return;
    var name = $("#f-name"), contact = $("#f-contact"), problem = $("#f-problem");
    var note = $("#f-note"), fb = $("#f-fallback"), fbText = $("#f-fallback-text");
    var INTENTS = {
      sites: "Preciso de um site.", automacao: "Quero automatizar uma tarefa.", sistemas: "Preciso de um sistema.",
      integracoes: "Quero integrar ferramentas que já uso.", ecommerce: "Quero melhorar meu e-commerce.",
      dashboards: "Quero enxergar meus números.", processo: "Quero organizar um processo.", ideia: "Tenho uma ideia.",
      diagnostico: "Quero conversar sobre uma solução.", parceria: "Sou de uma agência e quero conversar sobre parceria.",
      clinicas: "Tenho uma clínica e quero organizar a agenda.", contabilidade: "Tenho um escritório contábil e quero automatizar documentos e prazos.",
      imobiliarias: "Trabalho com imóveis e quero parar de perder lead.", comercio: "Quero um site para o meu negócio."
    };
    try {
      var q = new URLSearchParams(location.search);
      var start = [];
      if (INTENTS[q.get("intent")]) start.push(INTENTS[q.get("intent")]);
      if (q.get("fluxo")) start.push(q.get("fluxo").slice(0, 400));
      if (start.length && !problem.value) problem.value = start.join("\n") + "\n";
    } catch (e) {}

    var submit = $("button[type=submit]", f);
    if (CONFIG.formEndpoint && submit) submit.firstChild.textContent = "Enviar mensagem ";
    if (f.dataset.intent && !problem.value && INTENTS[f.dataset.intent]) problem.value = INTENTS[f.dataset.intent] + "\n";
    function compose() {
      return "Olá, GrupoGest.\n\nNome: " + name.value.trim() + "\nResposta por: " + contact.value.trim() + "\n\nO que trava:\n" + problem.value.trim() + "\n\n(mensagem montada no site)";
    }
    function mark(el, bad) { el.setAttribute("aria-invalid", bad ? "true" : "false"); }
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var missing = [name, contact, problem].filter(function (x) { var bad = !x.value.trim(); mark(x, bad); return bad; });
      if (missing.length) { note.textContent = "Faltou preencher: " + missing.map(function (x) { return x.dataset.label; }).join(", ") + "."; missing[0].focus(); return; }
      var msg = compose();
      if (CONFIG.formEndpoint) {
        note.textContent = "Enviando…";
        var data = new FormData(); data.append("nome", name.value); data.append("contato", contact.value); data.append("mensagem", msg); data.append("_subject", "Contato pelo site da GrupoGest");
        fetch(CONFIG.formEndpoint, { method: "POST", body: data, headers: { Accept: "application/json" } })
          .then(function (r) { if (!r.ok) throw new Error(r.status); f.hidden = true; $("#f-sent").hidden = false; })
          .catch(function () { note.textContent = "O envio falhou. A mensagem está abaixo para você mandar por e-mail."; showFallback(msg); });
        return;
      }
      showFallback(msg);
    });
    function showFallback(msg) {
      fbText.value = msg;
      var mail = $("#f-mail"); mail.href = "mailto:" + CONFIG.email + "?subject=" + encodeURIComponent("Contato pelo site da GrupoGest") + "&body=" + encodeURIComponent(msg);
      var wa = $("#f-wa");
      if (CONFIG.whatsapp) { wa.hidden = false; wa.href = "https://wa.me/" + CONFIG.whatsapp + "?text=" + encodeURIComponent(msg); } else wa.hidden = true;
      fb.hidden = false;
      note.textContent = "";
      fb.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "nearest" });
      mail.focus();
    }
    var cp = $("#f-copy"); if (cp) cp.addEventListener("click", function () { copyText(fbText.value, cp, "Mensagem copiada"); });
  })();
})();
