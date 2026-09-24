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

  // ── O mapa: partes de um sistema ───────────────────────────────────────
  (function mapa() {
    var tabs = $$(".st"); if (!tabs.length) return;
    function show(k, focus) {
      tabs.forEach(function (t) {
        var sel = t.dataset.k === k;
        t.setAttribute("aria-selected", sel ? "true" : "false");
        t.tabIndex = sel ? 0 : -1;
        if (sel && focus) t.focus();
      });
      $$(".sp").forEach(function (p) { p.classList.toggle("is-on", p.dataset.k === k); });
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { show(t.dataset.k); });
      t.addEventListener("keydown", function (e) {
        var n = null;
        if (e.key === "ArrowRight" || e.key === "ArrowDown") n = tabs[(i + 1) % tabs.length];
        if (e.key === "ArrowLeft" || e.key === "ArrowUp") n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (e.key === "Home") n = tabs[0];
        if (e.key === "End") n = tabs[tabs.length - 1];
        if (n) { e.preventDefault(); show(n.dataset.k, true); }
      });
    });
    var start = tabs.filter(function (t) { return t.getAttribute("aria-selected") === "true"; })[0] || tabs[0];
    show(start.dataset.k);
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
    function topics() { return $$("input[name=assunto]:checked", f).map(function (c) { return c.value; }); }
    function compose() {
      var t = topics();
      return "Olá, GrupoGest.\n\nNome: " + name.value.trim() + "\nResposta por: " + contact.value.trim() + (t.length ? "\nAssunto: " + t.join(", ") : "") + "\n\nO que trava:\n" + problem.value.trim() + "\n\n(mensagem montada no site)";
    }
    // a mensagem vira um papel e cai na caixa de entrada
    function drop() {
      var slot = $("#tray-slot"); if (!slot) return;
      var old = $(".paper", slot); if (old) old.remove();
      var t = topics();
      var p = document.createElement("div");
      p.className = "paper tray-paper";
      var now = new Date();
      var pc = document.createElement("span"); pc.className = "pc mono"; pc.textContent = "site · " + String(now.getHours()).padStart(2, "0") + ":" + String(now.getMinutes()).padStart(2, "0") + (t.length ? " · " + t.slice(0, 2).join(", ") : "");
      var pt = document.createElement("span"); pt.className = "pt"; var txt = problem.value.trim().replace(/\s+/g, " "); pt.textContent = txt.length > 110 ? txt.slice(0, 108) + "…" : txt;
      var pn = document.createElement("span"); pn.className = "pn mono"; pn.textContent = name.value.trim();
      p.appendChild(pc); p.appendChild(pt); p.appendChild(pn);
      slot.appendChild(p);
      slot.classList.add("has-paper");
      if (reduce || !p.animate) { p.classList.add("is-in"); return; }
      var a = problem.getBoundingClientRect(), b = p.getBoundingClientRect();
      p.animate([
        { transform: "translate(" + (a.left - b.left) + "px," + (a.top - b.top) + "px) rotate(-4deg) scale(.96)", opacity: 0.2 },
        { transform: "translate(" + ((a.left - b.left) * 0.4) + "px," + ((a.top - b.top) * 0.55 - 40) + "px) rotate(6deg)", opacity: 1, offset: 0.45 },
        { transform: "none", opacity: 1 }
      ], { duration: 900, easing: "cubic-bezier(.5,0,.2,1)" }).onfinish = function () { p.classList.add("is-in"); };
    }
    function mark(el, bad) { el.setAttribute("aria-invalid", bad ? "true" : "false"); }
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var missing = [name, contact, problem].filter(function (x) { var bad = !x.value.trim(); mark(x, bad); return bad; });
      if (missing.length) { note.textContent = "Faltou preencher: " + missing.map(function (x) { return x.dataset.label; }).join(", ") + "."; missing[0].focus(); return; }
      var msg = compose();
      drop();
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
