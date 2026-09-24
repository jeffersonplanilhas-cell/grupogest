/* Vitrine de imóveis alimentada por planilha.
   Na versão da imobiliária, CONFIG.csv aponta para a planilha do Google publicada como CSV
   (Arquivo → Compartilhar → Publicar na web → CSV). Mudou a planilha, o site muda sozinho. */
(function () {
  "use strict";
  var CONFIG = {
    csv: "imoveis.csv",
    whatsapp: "",           // só dígitos, com 55 + DDD. Vazio = o WhatsApp deixa a pessoa escolher o contato
    nome: "Imobiliária Exemplo"
  };

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var grid = $("#grid"), count = $("#count"), form = $("#filtros"), dlg = $("#detalhe");
  var todos = [];

  // CSV com aspas, vírgulas dentro de campos e quebras de linha (formato que o Google Planilhas exporta)
  function parseCSV(text) {
    var rows = [], row = [], field = "", q = false;
    for (var i = 0; i < text.length; i++) {
      var c = text[i];
      if (q) {
        if (c === '"' && text[i + 1] === '"') { field += '"'; i++; }
        else if (c === '"') q = false;
        else field += c;
      } else if (c === '"') q = true;
      else if (c === ",") { row.push(field); field = ""; }
      else if (c === "\n" || c === "\r") {
        if (c === "\r" && text[i + 1] === "\n") i++;
        row.push(field); field = "";
        if (row.some(function (x) { return x !== ""; })) rows.push(row);
        row = [];
      } else field += c;
    }
    if (field !== "" || row.length) { row.push(field); if (row.some(function (x) { return x !== ""; })) rows.push(row); }
    var head = rows.shift().map(function (h) { return h.trim().toLowerCase(); });
    return rows.map(function (r) { var o = {}; head.forEach(function (h, j) { o[h] = (r[j] || "").trim(); }); return o; });
  }

  function norm(o) {
    return {
      codigo: o.codigo, finalidade: (o.finalidade || "").toLowerCase().indexOf("loca") === 0 ? "locação" : "venda",
      tipo: o.tipo || "Imóvel", bairro: o.bairro || "", cidade: o.cidade || "",
      preco: Number(String(o.preco).replace(/[^\d.,]/g, "").replace(/\./g, "").replace(",", ".")) || 0,
      quartos: parseInt(o.quartos, 10) || 0, banheiros: parseInt(o.banheiros, 10) || 0, vagas: parseInt(o.vagas, 10) || 0,
      area: parseInt(o.area_m2, 10) || 0, destaque: /^s/i.test(o.destaque || ""),
      titulo: o.titulo || (o.tipo + " em " + o.bairro), descricao: o.descricao || "", foto: o.foto_url || ""
    };
  }

  var brl = function (n) { return "R$ " + n.toLocaleString("pt-BR", { maximumFractionDigits: 0 }); };
  function preco(i) { return i.preco ? brl(i.preco) + (i.finalidade === "locação" ? "/mês" : "") : "Consulte"; }

  function placeholder(i) {
    var hue = { Casa: 24, Apartamento: 210, Terreno: 95, Comercial: 280 }[i.tipo] || 0;
    var svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 260"><rect width="400" height="260" fill="hsl(' + hue + ',32%,88%)"/>' +
      '<path d="M140 170v-56l60-44 60 44v56z" fill="hsl(' + hue + ',30%,70%)"/><rect x="186" y="132" width="28" height="38" fill="hsl(' + hue + ',30%,56%)"/>' +
      '<text x="200" y="215" text-anchor="middle" font-family="system-ui,sans-serif" font-size="18" fill="hsl(' + hue + ',25%,35%)">' + i.codigo + " · foto do imóvel</text></svg>";
    return "data:image/svg+xml;charset=utf-8," + encodeURIComponent(svg);
  }

  function specs(i) {
    var s = [];
    if (i.quartos) s.push(i.quartos + (i.quartos > 1 ? " quartos" : " quarto"));
    if (i.banheiros) s.push(i.banheiros + (i.banheiros > 1 ? " banheiros" : " banheiro"));
    if (i.vagas) s.push(i.vagas + (i.vagas > 1 ? " vagas" : " vaga"));
    if (i.area) s.push(i.area + " m²");
    return s;
  }

  function waLink(i) {
    var msg = "Olá! Tenho interesse no imóvel " + i.codigo + " (" + i.titulo + "), que vi no site da " + CONFIG.nome + ".";
    return "https://wa.me/" + (CONFIG.whatsapp || "") + "?text=" + encodeURIComponent(msg);
  }

  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }

  function card(i) {
    var li = el("li", "card");
    var b = el("button", "card-btn"); b.type = "button"; b.setAttribute("aria-label", i.titulo + ", " + preco(i));
    b.addEventListener("click", function () { abrir(i.codigo); });
    var fig = el("div", "ph"); var img = new Image(); img.alt = ""; img.loading = "lazy"; img.src = i.foto || placeholder(i);
    img.onerror = function () { img.onerror = null; img.src = placeholder(i); };
    fig.appendChild(img); fig.appendChild(el("span", "tag " + (i.finalidade === "venda" ? "t-venda" : "t-loc"), i.finalidade));
    if (i.destaque) fig.appendChild(el("span", "tag t-dest", "destaque"));
    b.appendChild(fig);
    var body = el("div", "cb");
    body.appendChild(el("p", "pr", preco(i)));
    body.appendChild(el("h3", null, i.titulo));
    body.appendChild(el("p", "loc", i.tipo + " · " + i.bairro));
    var ul = el("ul", "sp"); specs(i).forEach(function (s) { ul.appendChild(el("li", null, s)); }); body.appendChild(ul);
    body.appendChild(el("p", "cod", i.codigo));
    b.appendChild(body); li.appendChild(b);
    return li;
  }

  function filtrar() {
    var f = new FormData(form), fin = f.get("fin"), tipo = f.get("tipo"), bairro = f.get("bairro"),
      q = parseInt(f.get("quartos"), 10) || 0, max = Number(String(f.get("max") || "").replace(/\D/g, "")) || 0, ord = f.get("ord");
    var r = todos.filter(function (i) {
      return (!fin || i.finalidade === fin) && (!tipo || i.tipo === tipo) && (!bairro || i.bairro === bairro) &&
        i.quartos >= q && (!max || i.preco <= max);
    });
    r.sort(function (a, b) {
      if (ord === "menor") return a.preco - b.preco;
      if (ord === "maior") return b.preco - a.preco;
      if (ord === "area") return b.area - a.area;
      return (b.destaque - a.destaque) || a.preco - b.preco;
    });
    grid.textContent = "";
    r.forEach(function (i) { grid.appendChild(card(i)); });
    count.textContent = r.length ? r.length + (r.length > 1 ? " imóveis" : " imóvel") : "Nenhum imóvel com esses filtros.";
  }

  function opcoes(sel, vals) {
    vals.forEach(function (v) { var o = el("option", null, v); o.value = v; sel.appendChild(o); });
  }

  function abrir(codigo) {
    var i = todos.filter(function (x) { return x.codigo === codigo; })[0];
    if (!i) return;
    $("#d-img").src = i.foto || placeholder(i);
    $("#d-tag").textContent = i.finalidade;
    $("#d-pr").textContent = preco(i);
    $("#d-tit").textContent = i.titulo;
    $("#d-loc").textContent = i.tipo + " · " + i.bairro + (i.cidade ? ", " + i.cidade : "");
    var ul = $("#d-sp"); ul.textContent = ""; specs(i).forEach(function (s) { ul.appendChild(el("li", null, s)); });
    $("#d-desc").textContent = i.descricao;
    $("#d-cod").textContent = "Código " + i.codigo;
    $("#d-wa").href = waLink(i);
    var link = location.href.split("#")[0] + "#" + i.codigo;
    $("#d-share").onclick = function () {
      var btn = this;
      function ok() { btn.textContent = "Link copiado"; setTimeout(function () { btn.textContent = "Copiar link do imóvel"; }, 1800); }
      if (navigator.share) navigator.share({ title: i.titulo, url: link }).catch(function () {});
      else if (navigator.clipboard) navigator.clipboard.writeText(link).then(ok, function () { prompt("Copie o link:", link); });
      else prompt("Copie o link:", link);
    };
    if (location.hash !== "#" + i.codigo) history.replaceState(null, "", "#" + i.codigo);
    if (dlg.showModal) { if (!dlg.open) dlg.showModal(); } else dlg.setAttribute("open", "");
  }
  function fechar() { if (dlg.close) dlg.close(); else dlg.removeAttribute("open"); }
  dlg.addEventListener("close", function () { history.replaceState(null, "", location.pathname + location.search); });
  $("#d-x").addEventListener("click", fechar);
  dlg.addEventListener("click", function (e) { if (e.target === dlg) fechar(); });

  form.addEventListener("input", filtrar);
  form.addEventListener("change", filtrar);
  form.addEventListener("submit", function (e) { e.preventDefault(); filtrar(); });

  document.querySelectorAll("[data-wa-geral]").forEach(function (a) {
    a.href = "https://wa.me/" + (CONFIG.whatsapp || "") + "?text=" + encodeURIComponent("Olá! Vim pelo site da " + CONFIG.nome + ".");
  });

  fetch(CONFIG.csv, { cache: "no-store" }).then(function (r) {
    if (!r.ok) throw new Error(r.status);
    return r.text();
  }).then(function (t) {
    todos = parseCSV(t).filter(function (o) { return o.codigo; }).map(norm);
    opcoes($("#f-tipo"), Array.from(new Set(todos.map(function (i) { return i.tipo; }))).sort());
    opcoes($("#f-bairro"), Array.from(new Set(todos.map(function (i) { return i.bairro; }))).sort());
    filtrar();
    document.body.classList.add("ok");
    if (location.hash.length > 1) abrir(decodeURIComponent(location.hash.slice(1)));
  }).catch(function () {
    count.textContent = "Não foi possível carregar os imóveis agora. Tente de novo em instantes.";
  });
})();
