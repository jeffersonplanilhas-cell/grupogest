#!/usr/bin/env python3
"""Gera o site da GrupoGest a partir destes templates.

Uso:
  python3 build.py                 # prévia em ../site (noindex)
  python3 build.py --prod --out DIR  # versão para publicar (indexável)

Tudo que é texto aqui veio do site publicado ou descreve algo que existe.
"""
import argparse, datetime, json, os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://jeffersonplanilhas-cell.github.io/grupogest/"
EMAIL = "carmojefferson868@gmail.com"

# ────────────────────────────── conteúdo ──────────────────────────────

SOLUCOES = {
  "sites": {
    "nome": "Sites e landing pages", "curto": "Sites",
    "title": "Site para empresa e landing page · GrupoGest",
    "desc": "Site próprio para comércio, clínica, escritório ou prestador de serviço. Rápido, com contato em todas as dobras e encontrável no Google. Escopo e preço fechados.",
    "tag": "presença digital própria",
    "h1": "Seu negócio já existe. Falta ele existir fora do Instagram.",
    "lede": "Perfil em rede social é aluguel: o alcance é de outro, a lista é de outro, a busca no Google não te encontra. Um site próprio é endereço, prova e canal de contato que continua funcionando quando o algoritmo muda.",
    "cta": "Quero um site", "preco": "R$ 690 a R$ 1.500",
    "dores": ["O cliente procura no Google pelo seu nome e acha um link quebrado, um domínio estacionado ou nada.",
              "O contato depende de alguém ver a mensagem no direct.",
              "Não dá para mandar uma proposta com um link que represente a empresa."],
    "construimos": [("Página que carrega rápido", "HTML e CSS enxutos, imagem otimizada, sem construtor pesado. Abre em segundos no 4G do cliente."),
                    ("Contato sem atrito", "WhatsApp, telefone e formulário no lugar certo, em todas as dobras, não escondido no rodapé."),
                    ("Encontrável", "Título, descrição, dados estruturados, endereço e mapa. O básico do SEO local feito direito."),
                    ("Publicado e no ar", "Domínio, hospedagem, HTTPS e a conferência final em celular real antes de entregar.")],
    "etapas": [("Conversa", "o que o site precisa fazer"), ("Estrutura", "conteúdo e seções"), ("Construção", "página e responsivo"), ("Revisão", "você aprova"), ("No ar", "domínio + HTTPS")],
    "aplica": ["Comércio local", "Clínicas e consultórios", "Escritórios (contábil, advocacia)", "Prestadores de serviço", "Construtoras e reformas"],
    "evidencia": [("Front-end e landing pages", "Landing page de lead magnet construída e testada internamente (HTML/CSS/JS)."),
                  ("Diagnóstico técnico de site", "Rotina própria de checagem de DNS, HTTP, viewport mobile, WhatsApp e formulário, usada para achar o que está quebrado antes de propor.")],
    "investimento": "Escopo fechado, preço fechado. Faixa conforme número de páginas e conteúdo.",
  },
  "automacao": {
    "nome": "Automação", "curto": "Automação",
    "title": "Automação de processos com n8n e Python · GrupoGest",
    "desc": "Mapeamento e automação de processo repetitivo: lead, atendimento, agendamento, cobrança e rotina administrativa. Com log, tratamento de erro e documentação.",
    "tag": "n8n, Python, APIs",
    "h1": "Existe trabalho manual que sua equipe não deveria mais estar fazendo.",
    "lede": "Copiar dado de um sistema para outro, responder a mesma pergunta cinquenta vezes, lembrar de cobrar, digitar planilha. Tudo isso é regra, e regra é coisa de máquina. A gente mapeia o processo, automatiza o que é repetitivo e deixa a decisão com a pessoa.",
    "cta": "Quero automatizar um processo", "preco": "a partir de R$ 150",
    "dores": ["Lead chega e esfria porque ninguém viu a mensagem a tempo.",
              "A mesma informação é digitada em três lugares diferentes.",
              "Cobrança, confirmação e lembrete dependem de alguém lembrar."],
    "construimos": [("Mapa do processo", "Antes de automatizar: o que acontece hoje, quem faz, quanto tempo leva, onde trava. Sem isso, automação só acelera a bagunça."),
                    ("Fluxo em n8n ou Python", "Gatilho, condição, ação, registro. Cada passo visível, com log: dá para auditar o que rodou e quando."),
                    ("Tratamento de erro", "O que acontece quando a API do outro lado cai. Repetição, fila e alerta, não silêncio."),
                    ("Entrega com manual", "Você fica com o fluxo, a documentação e o acesso. Não é uma caixa-preta que só a gente abre.")],
    "etapas": [("Gatilho", "formulário, mensagem, planilha, API"), ("Qualificação", "regra que separa o que importa"), ("Ação", "registrar, notificar, responder"), ("Registro", "CRM, planilha ou banco"), ("Acompanhamento", "lembrete e follow-up")],
    "aplica": ["Clínicas (agenda e confirmação)", "Escritórios contábeis (documento e prazo)", "Imobiliárias (lead e visita)", "Comercial (lead, CRM, follow-up)", "Pós-venda e recompra"],
    "evidencia": [("n8n + Postgres + webhooks + API de IA", "Pipeline construído e validado ponta a ponta em ambiente próprio."),
                  ("Automação em Python", "CLIs e rotinas com testes automatizados rodando na operação interna todo dia.")],
    "investimento": "Três degraus, escopo fechado em cada um: micro-automação (uma tarefa repetitiva) a partir de R$ 150; processo inteiro (gatilho, regra, ação e registro) a partir de R$ 500; implantação com integração e acompanhamento mensal é orçada por escopo. O degrau certo sai do diagnóstico, não do chute.",
  },
  "sistemas": {
    "nome": "Sistemas sob medida", "curto": "Sistemas",
    "title": "Desenvolvimento de sistema sob medida · GrupoGest",
    "desc": "Sistema web e API sob medida em Python/FastAPI e PostgreSQL, com testes automatizados e deploy contínuo. Para quando a planilha virou o gargalo da operação.",
    "tag": "web, API e aplicativo",
    "h1": "Quando a planilha vira o gargalo, o próximo passo é um sistema.",
    "lede": "Planilha compartilhada é ótima até o dia em que duas pessoas editam junto, o histórico some e ninguém sabe qual versão vale. Sistema resolve o que planilha não resolve: acesso por usuário, regra que não pode ser burlada, histórico e dado confiável.",
    "cta": "Quero desenvolver um sistema", "preco": "escopo fechado, sob orçamento",
    "dores": ["Versões diferentes da mesma planilha circulando por WhatsApp.",
              "Ninguém sabe quem mudou o quê, nem quando.",
              "A regra do negócio está na cabeça de uma pessoa, não no sistema."],
    "construimos": [("Modelo de dados primeiro", "O que é uma obra, um cliente, um lançamento. Errar aqui custa caro depois; acertar aqui faz o resto ficar simples."),
                    ("API testada", "Back-end em Python/FastAPI com suíte de testes automatizados rodando a cada alteração. Regressão aparece antes de chegar em você."),
                    ("Interface de trabalho", "Tela feita para quem usa oito horas por dia: teclado, atalho, estado claro de carregamento, erro e sucesso."),
                    ("Deploy e continuidade", "Integração contínua, ambiente de produção e um caminho combinado para evoluir o sistema depois da entrega.")],
    "etapas": [("Escopo", "o que entra na primeira versão"), ("Modelo", "dados e regras"), ("API", "com testes"), ("Telas", "uso real"), ("Produção", "deploy e evolução")],
    "aplica": ["Gestão interna de operação", "Cadastro e histórico de clientes", "Controle de obra, estoque ou serviço", "Portal para cliente final", "Substituição de planilha crítica"],
    "evidencia": [("Back-end Python/FastAPI + PostgreSQL", "Construa360, SaaS próprio de gestão de obras: mais de 400 testes automatizados, integração contínua e deploy em nuvem. Em pré-lançamento."),
                  ("Aplicativo Expo/React Native", "Aplicativo do Construa360 construído com build configurado. Ainda não publicado em loja, e não vendemos publicação em loja como especialidade.")],
    "investimento": "Sistema não tem tabela: depende de quantas regras existem. A conversa começa pelo diagnóstico.",
  },
  "integracoes": {
    "nome": "Integrações", "curto": "Integrações",
    "title": "Integração entre sistemas e APIs · GrupoGest",
    "desc": "Integração entre CRM, ERP, e-commerce, WhatsApp e planilhas com fila, tratamento de erro e monitoramento. Seus sistemas trocando dado sem digitação manual.",
    "tag": "APIs, CRM, WhatsApp, ERP",
    "h1": "Seus sistemas já existem. Falta um falar com o outro.",
    "lede": "Quase toda empresa já paga por três ou quatro ferramentas que não se conhecem. O trabalho manual de copiar dado entre elas custa mais caro que a integração, só que esse custo está escondido na folha, não na fatura.",
    "cta": "Quero integrar ferramentas", "preco": "escopo fechado, sob orçamento",
    "dores": ["O pedido entra num sistema e alguém redigita no outro.",
              "O relatório só existe depois que uma pessoa junta tudo na mão.",
              "A ferramenta nova não conversa com a antiga e ninguém quer trocar."],
    "construimos": [("Levantamento de contrato", "O que cada API entrega, o que ela exige, qual limite de chamada, o que acontece em caso de falha."),
                    ("Ponte com fila", "Integração que não perde evento quando o outro lado cai: fila, repetição e registro do que passou."),
                    ("Sincronização com regra", "Quem manda em cada campo quando os dois lados mudam. Definido antes, não descoberto no conflito."),
                    ("Monitoramento", "Alerta quando a integração para. Integração silenciosa quebrada é pior que integração nenhuma.")],
    "etapas": [("Sistema A", "origem do evento"), ("Ponte", "tradução e regra"), ("Fila", "repetição segura"), ("Sistema B", "destino"), ("Log", "o que passou e quando")],
    "aplica": ["CRM e formulário de site", "WhatsApp e atendimento", "ERP e e-commerce", "Meio de pagamento e financeiro", "Planilha e banco de dados"],
    "evidencia": [("Integração de meio de pagamento", "Checkout com Mercado Pago (Pix e cartão) e cálculo de frete via Melhor Envio em projeto próprio de e-commerce."),
                  ("Webhooks e APIs de terceiros", "Fluxos n8n com webhook, banco e API externa validados ponta a ponta.")],
    "investimento": "O preço depende de quantos sistemas e de quão bem documentada é a API de cada lado. O levantamento é a primeira etapa.",
  },
  "ecommerce": {
    "nome": "E-commerce", "curto": "E-commerce",
    "title": "E-commerce em Next.js com Pix e cartão · GrupoGest",
    "desc": "Loja própria em Next.js com Mercado Pago (Pix e cartão), frete Melhor Envio, confirmação por webhook e painel de pedidos. Venda online tratada como operação.",
    "tag": "loja própria e marketplace",
    "h1": "Vender online é operação, não só vitrine.",
    "lede": "A loja bonita que não calcula frete direito, não confirma pagamento e não avisa o cliente gera mais trabalho do que venda. O que faz diferença é o que acontece depois do botão comprar.",
    "cta": "Quero melhorar meu e-commerce", "preco": "escopo fechado, sob orçamento",
    "dores": ["Carrinho abandonado no frete porque o cálculo está errado ou lento.",
              "Pagamento confirmado e ninguém no estoque ficou sabendo.",
              "Catálogo desatualizado porque atualizar dá trabalho demais."],
    "construimos": [("Catálogo e carrinho", "Loja em Next.js com banco próprio: rápida, indexável e sem depender de plugin de terceiro para o essencial."),
                    ("Pagamento de verdade", "Pix e cartão via Mercado Pago, com confirmação por webhook: o pedido muda de estado quando o dinheiro entra, não quando alguém confere."),
                    ("Frete calculado", "Cotação via Melhor Envio no checkout, com peso e dimensão do produto."),
                    ("Painel de pedidos", "Onde a operação vê o que vendeu, o que pagou e o que precisa sair hoje.")],
    "etapas": [("Catálogo", "produto e estoque"), ("Carrinho", "frete calculado"), ("Pagamento", "Pix ou cartão"), ("Webhook", "confirmação automática"), ("Expedição", "pedido na fila")],
    "aplica": ["Varejo local que quer vender fora da loja", "Atacado e distribuição", "Produto digital", "Catálogo B2B com preço por cliente"],
    "evidencia": [("Loja completa em Next.js", "Projeto próprio com Supabase, Drizzle, Mercado Pago (Pix e cartão) e Melhor Envio, construído e testado internamente.")],
    "investimento": "Somos honestos sobre plataforma: construímos loja própria em Next.js. Não nos apresentamos como especialistas em Shopify, Nuvemshop ou WordPress; se for esse o caminho, dizemos antes.",
  },
  "dashboards": {
    "nome": "Dados e indicadores", "curto": "Dados",
    "title": "Dashboard e indicadores para PME · GrupoGest",
    "desc": "Painéis e planilhas que respondem à pergunta certa: fonte única, atualização automática e leitura em segundos. Indicador que muda decisão, não gráfico de enfeite.",
    "tag": "indicador que gera decisão",
    "h1": "Relatório que ninguém abre não é informação. É trabalho.",
    "lede": "Dashboard bom responde uma pergunta que muda uma decisão nesta semana. O resto é enfeite. A gente começa pela pergunta, não pelo gráfico.",
    "cta": "Quero enxergar meus números", "preco": "planilha estruturada a partir de R$ 450",
    "dores": ["O número só existe depois que alguém passa a tarde juntando planilha.",
              "Cada área tem um total diferente para a mesma coisa.",
              "Ninguém sabe dizer o que está caindo antes do fim do mês."],
    "construimos": [("Pergunta antes do gráfico", "Que decisão esse número muda? Se não muda nenhuma, ele não entra no painel."),
                    ("Fonte única", "Um lugar onde o dado é verdade. Os outros leem de lá, e acaba o total divergente."),
                    ("Atualização automática", "O painel se atualiza sozinho a partir do banco ou da planilha. Ninguém monta relatório na mão."),
                    ("Leitura em 10 segundos", "Hierarquia clara: o que está fora do esperado aparece primeiro, o detalhe fica um clique abaixo.")],
    "etapas": [("Fonte", "banco, planilha ou API"), ("Consolidação", "regra de cálculo única"), ("Indicador", "o que muda decisão"), ("Painel", "leitura rápida"), ("Alerta", "quando sai do esperado")],
    "aplica": ["Comercial (funil e conversão)", "Financeiro (caixa e recebíveis)", "Operação (produtividade e prazo)", "Diretoria (visão semanal)"],
    "evidencia": [("Painel operacional próprio", "Painel da nossa operação comercial lê um banco SQLite real e é gerado por script, sem servidor."),
                  ("Planilhas geradas por código", "Planilhas Excel estruturadas via openpyxl, com validação em aplicativo real antes de publicar.")],
    "investimento": "Planilha estruturada sob medida a partir de R$ 450; painel conectado a banco é orçado por escopo.",
  },
}
ORDEM = ["sites", "automacao", "sistemas", "integracoes", "ecommerce", "dashboards"]

# ────────────────────────────── partes comuns ──────────────────────────────

def head(p, title, desc, path, noindex, extra=""):
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<link rel="canonical" href="{BASE_URL}{path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:url" content="{BASE_URL}{path}">
<meta property="og:image" content="{BASE_URL}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0d1321">
<link rel="icon" href="{p}assets/icon.svg" type="image/svg+xml">
<link rel="preload" href="{p}assets/fonts/archivo-latin-wdth-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/gg.css">
<script>document.documentElement.classList.add('js')</script>
{extra}</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
"""

def header(p, home=False, current=""):
    h = "" if home else f"{p}"
    def cur(k): return ' aria-current="page"' if current == k else ""
    cta = "#conversa" if home else f"{p}contato/"
    return f"""<header class="top">
  <div class="wrap">
    <a class="brand" href="{p}" aria-label="GrupoGest, início"><img src="{p}assets/icon.svg" alt="" width="26" height="26"><b aria-hidden="true">Grupo<i>Gest</i></b></a>
    <nav aria-label="Principal">
      <a href="{h}#maquina">O sistema</a>
      <a href="{h}#capacidade">O que construímos</a>
      <a href="{h}#prova">Prova</a>
      <a href="{p}parcerias/"{cur('parcerias')}>Agências</a>
    </nav>
    <a class="btn small" href="{cta}">Conversar <span class="arr" aria-hidden="true">→</span></a>
  </div>
</header>
"""

def footer(p, noindex):
    sol = "\n".join(f'      <a href="{p}solucoes/{k}/">{SOLUCOES[k]["nome"]}</a>' for k in ORDEM)
    return f"""<section class="agency" aria-label="Para agências">
  <div class="wrap">
    <p>Tem agência, consultoria ou estúdio? <span>A gente vira seu braço técnico, no seu nome, com preço fechado antes de você vender.</span></p>
    <a class="link" href="{p}parcerias/">Parceria para agências <span aria-hidden="true">→</span></a>
  </div>
</section>
<footer class="foot">
  <div class="wrap">
    <div class="fb">
      <a class="brand" href="{p}" aria-label="GrupoGest, início"><img src="{p}assets/icon.svg" alt="" width="26" height="26"><b aria-hidden="true">Grupo<i>Gest</i></b></a>
      <p>Trabalho manual vira sistema que roda sozinho: sites, sistemas, automações e integrações sob medida.</p>
      <p class="mono">Franca/SP · atendimento em todo o Brasil</p>
    </div>
    <nav aria-label="Site">
      <span class="mono">site</span>
      <a href="{p}">Início</a>
      <a href="{p}#maquina">O sistema</a>
      <a href="{p}#capacidade">O que construímos</a>
      <a href="{p}#prova">Prova</a>
      <a href="{p}contato/">Contato</a>
    </nav>
    <nav aria-label="Soluções">
      <span class="mono">soluções</span>
{sol}
    </nav>
    <nav aria-label="Agências">
      <span class="mono">agências</span>
      <a href="{p}parcerias/">Parceria white-label</a>
    </nav>
    <nav aria-label="Contato">
      <span class="mono">contato</span>
      <a href="{p}contato/">Descrever o problema</a>
      <span data-email>{EMAIL}</span>
    </nav>
    <div class="legal mono"><span>© 2026 GrupoGest</span><span>Este site foi construído pela própria GrupoGest.</span></div>
  </div>
</footer>
<script src="{p}assets/gg.js" defer></script>
</body>
</html>
"""

def talk(p, heading="Conte o que trava.", intent="", hid="conversa", h1=False, crumb="", lede=None):
    di = f' data-intent="{intent}"' if intent else ""
    tag = "h1" if h1 else "h2"
    lede = lede or "Três linhas bastam. A gente responde com o que dá para fazer, em quanto tempo e por quanto, ou diz com franqueza que não é com a gente."
    return f"""<section class="talk{' talk-page' if h1 else ''}" id="{hid}" aria-labelledby="{hid}-h">
  <div class="wrap grid talk-grid">
    <div class="talk-copy">
      {crumb}<{tag} class="h2" id="{hid}-h">{heading}</{tag}>
      <p class="lede">{lede}</p>
      <div class="ways">
        <div class="way" data-whatsapp-row><div><div class="k mono">whatsapp</div><div class="v" data-whatsapp-num></div></div><a class="ctl on-ink" href="#" rel="noopener">Abrir conversa</a></div>
        <div class="way"><div><div class="k mono">e-mail</div><div class="v" data-email>{EMAIL}</div></div><button class="ctl on-ink" type="button" data-copy-email>Copiar</button></div>
      </div>
      <p class="mono form-note">resposta por e-mail em até 1 dia útil</p>
    </div>
    <form class="form" id="talk-form" novalidate{di}>
      <div class="row2">
        <label for="f-name">Seu nome<input id="f-name" name="nome" autocomplete="name" required data-label="nome"></label>
        <label for="f-contact">WhatsApp ou e-mail para a resposta<input id="f-contact" name="contato" autocomplete="email" inputmode="email" required data-label="como responder"></label>
      </div>
      <label for="f-problem">O que trava hoje<textarea id="f-problem" name="problema" required data-label="o que trava" placeholder="O que acontece, quem faz, onde trava. Sem formalidade."></textarea></label>
      <div class="form-foot">
        <button class="btn primary" type="submit">Montar a mensagem <span class="arr" aria-hidden="true">→</span></button>
        <p class="mono form-note" id="f-note" aria-live="polite"></p>
      </div>
      <div class="fallback" id="f-fallback" hidden>
        <p>Sua mensagem está pronta. Escolha como enviar:</p>
        <div class="acts">
          <a class="btn primary" id="f-wa" href="#" hidden rel="noopener">Enviar pelo WhatsApp</a>
          <a class="btn" id="f-mail" href="#">Abrir no e-mail</a>
          <button class="ctl on-ink" type="button" id="f-copy">Copiar mensagem</button>
        </div>
        <label for="f-fallback-text" class="mono">Se o e-mail não abrir no seu aparelho, copie e envie para <span data-email>{EMAIL}</span>
          <textarea id="f-fallback-text" readonly></textarea></label>
      </div>
      <p class="sent" id="f-sent" hidden>Mensagem enviada. A gente responde em até 1 dia útil.</p>
    </form>
  </div>
</section>
"""

# ────────────────────────────── home ──────────────────────────────

LEDGER = [
  ("cadê o boleto do mês?", "cobrança · sai sozinha", False),
  ("40 caixas do modelo 42 até sexta", "pedido · registrado", False),
  ("ela pagou? confere o extrato", "pagamento · baixa automática", False),
  ("manda de novo aquela planilha", "dados · fonte única", True),
  ("qual versão vale?", "histórico · uma versão só", False),
  ("quem ficou de ligar pro cliente?", "retorno · lembrete na hora", True),
  ("remarca a Ana pra quinta, 15h", "agenda · confirmada", False),
  ("junta os números pro sócio", "painel · sexta, 17h", False),
  ("copia do WhatsApp pro sistema", "integração · sem redigitar", True),
  ("o site saiu do ar?", "monitor · alerta automático", True),
]

RULES = [
  ("pedido", "Pedido completo", "registra no sistema e emite a cobrança", True),
  ("pagamento", "Pagamento e cobrança", "confere, dá baixa ou manda a 2ª via", False),
  ("pergunta", "Pergunta frequente", "responde na hora, com a informação certa", False),
  ("resumo", "Sexta, 17h", "junta os números e envia o resumo", False),
]

CAPS = [
  ("sites", "Sites e landing pages", "O cliente procura sua empresa e acha um link quebrado, um perfil ou nada.", "Site rápido, encontrável no Google, com contato em todas as dobras.", "Landing de lead magnet construída e testada", "R$ 690 a R$ 1.500"),
  ("automacao", "Automação", "Alguém copia, confere e lembra todo dia o que uma regra faria melhor.", "Fluxo em n8n ou Python, com registro do que rodou e tratamento de erro.", "Pipeline n8n + PostgreSQL + webhooks validado", "a partir de R$ 150"),
  ("integracoes", "Integrações", "O pedido entra num sistema e alguém redigita no outro.", "Ponte com fila, repetição e alerta quando a integração para.", "Mercado Pago e Melhor Envio integrados em loja própria", "sob orçamento"),
  ("sistemas", "Sistemas sob medida", "A planilha virou o sistema da empresa, e o maior risco dela.", "Web, API e aplicativo com acesso por usuário, regra e histórico.", "Construa360: FastAPI, PostgreSQL, 400+ testes, app Expo", "sob orçamento"),
  ("ecommerce", "E-commerce", "A loja vende, mas pagamento, frete e expedição dependem de alguém conferir.", "Loja em Next.js com Pix, cartão, frete calculado e confirmação por webhook.", "Loja própria completa em Next.js", "sob orçamento"),
  ("dashboards", "Dados e indicadores", "O número da semana só existe depois de uma tarde juntando planilha.", "Painel que se atualiza sozinho, a partir de uma fonte única.", "Painel operacional próprio gerado por script", "planilha a partir de R$ 450"),
]

PROOF = [
  ("Construa360", "produto próprio · pré-lançamento", "Gestão de obras: equipe, ponto, financeiro e suprimentos. Python/FastAPI, PostgreSQL, mais de 400 testes automatizados e app em Expo/React Native. Não é case de cliente."),
  ("Calculadora de prejuízo na obra", "landing pública do Construa360", "Estima a perda mensal de uma obra a partir de índices da literatura brasileira. Roda inteira no navegador, sem rastreamento, com a metodologia aberta."),
  ("Loja em Next.js", "projeto interno", "Catálogo, carrinho e checkout com Pix e cartão via Mercado Pago, frete pelo Melhor Envio e confirmação de pagamento por webhook."),
  ("Pipeline de automação", "validado e arquivado", "n8n, PostgreSQL e webhooks: gatilho, regra, banco e API externa testados ponta a ponta, com registro do que rodou e quando."),
  ("A operação da GrupoGest", "em uso diário", "Prospecção, CRM e finanças num sistema que construímos para nós: banco de dados, rotinas com testes e painel gerado por script."),
]

STEPS = [
  ("Encontrar o atrito", "Uma conversa sobre onde o tempo some: o que se repete, quem faz, o que trava.", "primeira conversa sobre o caso"),
  ("Entender o processo", "Desenhamos como o trabalho acontece hoje, passo a passo, antes de falar de ferramenta.", "mapa do processo atual"),
  ("Definir as regras", "O que entra, o que decide, o que acontece. Daí saem escopo, prazo e preço fechados.", "escopo e preço por escrito"),
  ("Construir", "Entrega em partes, com você acompanhando, e testado antes de chegar em você.", "versões para você validar"),
  ("Colocar para rodar", "No ar, com acesso, documentação e o combinado de como evoluir. Sem dependência artificial.", "sistema rodando e documentado"),
]

def home(p, noindex):
    ld = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "GrupoGest",
          "description": "A GrupoGest transforma trabalho manual em sistema que roda sozinho: sites, sistemas, automações e integrações sob medida, com escopo e preço fechados antes de começar.",
          "url": BASE_URL.rstrip("/"), "email": EMAIL, "areaServed": "BR",
          "address": {"@type": "PostalAddress", "addressLocality": "Franca", "addressRegion": "SP", "addressCountry": "BR"},
          "knowsAbout": ["automação de processos", "integração de sistemas", "sistemas sob medida", "desenvolvimento web"]}
    extra = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
    rows = "\n".join(
        f'        <li class="lrow{" is-hidden-mobile" if hid else ""}"><span class="lr-in">{a}</span><span class="lr-rule mono">{b}</span></li>'
        for a, b, hid in LEDGER)
    rules = "\n".join(
        f'''          <button class="rule" type="button" role="switch" aria-checked="{"true" if on else "false"}" data-r="{k}"><span class="sw" aria-hidden="true"></span><span class="rt">{t}</span><span class="ra">{a}</span></button>'''
        for k, t, a, on in RULES)
    caps = "\n".join(f'''      <li><a class="caprow" href="{p}solucoes/{k}/">
        <h3>{n}</h3>
        <p><span class="c-k mono">quando</span>{q}</p>
        <p class="c-deliv"><span class="c-k mono">a gente entrega</span>{e}</p>
        <p class="c-proof"><span class="c-k mono">já construímos</span>{pr}</p>
        <p><span class="c-k mono">investimento</span><span class="price">{pv}</span><span class="go mono">ver detalhes →</span></p>
      </a></li>''' for k, n, q, e, pr, pv in CAPS)
    proof = "\n".join(f'''        <li class="pitem"><h3>{n}</h3><span class="st mono">{s}</span><p>{d}</p></li>''' for n, s, d in PROOF)
    steps = "\n".join(f'''      <li class="step"><span class="sn mono">{i + 1} de 5</span><h3>{t}</h3><p>{d}</p><p class="out mono"><b>sai daqui:</b> {o}</p></li>''' for i, (t, d, o) in enumerate(STEPS))
    return head(p, "GrupoGest · do caos ao sistema",
                "A GrupoGest transforma trabalho manual em sistema que roda sozinho: sites, sistemas, automações e integrações sob medida, com escopo e preço fechados antes de começar.",
                "", noindex, extra) + header(p, home=True) + f"""<main id="conteudo">

<section class="hero" aria-labelledby="hero-h">
  <div class="wrap grid hero-grid">
    <p class="mono where">Franca/SP · sistemas, sites, automação e integrações para empresas de todo o Brasil</p>
    <h1 class="h1" id="hero-h"><span>Trabalho manual vira sistema</span><span class="soft">que roda sozinho.</span></h1>
    <div class="hero-side">
      <p class="hero-lede">A gente encontra o que sua equipe repete todo dia (copiar, conferir, cobrar, lembrar) e constrói o que faz isso por ela. Com registro de tudo e preço fechado antes de começar.</p>
      <div class="cta-row">
        <a class="btn primary" href="#conversa">Conversar sobre a demanda <span class="arr" aria-hidden="true">→</span></a>
        <a class="link" href="#maquina">Ver o sistema funcionando</a>
      </div>
    </div>
    <div class="ledger" id="ledger">
      <div class="ledger-head mono"><span>registro · exemplo</span><span class="wide-only">o que chega → a regra que resolve</span></div>
      <ol class="lrows" aria-label="Exemplos de pedidos do dia a dia e a regra que resolve cada um">
{rows}
      </ol>
      <div class="ledger-foot mono"><span>cada frase repetida vira uma regra</span><button type="button" id="ledger-replay">embaralhar</button></div>
    </div>
  </div>
</section>

<section class="machine" id="maquina" aria-labelledby="maq-h">
  <div class="wrap">
    <div class="grid">
      <h2 class="thesis" id="maq-h">Toda empresa já tem um sistema. <span>Às vezes, ele é uma pessoa que não pode tirar férias.</span></h2>
      <p class="lede machine-lede">Ligue e desligue as regras. Cada mensagem que chega é resolvida pelo sistema ou fica esperando alguém.</p>
    </div>
    <div class="mach" id="mach">
      <div class="mcol m-in"><header class="mono"><b>entrada</b><span>chegando agora</span></header><ol class="mlist" id="m-queue" aria-label="Mensagens chegando"></ol></div>
      <p class="now mono" id="m-now" aria-live="off"></p>
      <div class="mcol m-rules"><header class="mono"><b>regra</b><span>ligue para o sistema assumir</span></header>
        <div class="rules">
{rules}
        </div>
      </div>
      <div class="mcol is-auto"><header class="mono"><b>feito pelo sistema</b><span class="n" id="m-auto-n">0</span></header><ol class="mlist" id="m-auto" aria-label="Feito pelo sistema"></ol></div>
      <div class="mcol is-man"><header class="mono"><b>esperando alguém</b><span class="n" id="m-man-n">0</span></header><ol class="mlist" id="m-man" aria-label="Esperando alguém"></ol></div>
    </div>
    <div class="mach-bar">
      <button class="ctl" type="button" id="m-play" aria-pressed="false">Pausar</button>
      <button class="ctl" type="button" id="m-step">Processar próxima</button>
      <button class="ctl" type="button" id="m-reset">Recomeçar</button>
      <span class="note mono">exemplo ilustrativo de uma distribuidora que vende pelo WhatsApp</span>
    </div>
  </div>
</section>

<section class="cap" id="capacidade" aria-labelledby="cap-h">
  <div class="wrap">
    <div class="grid cap-head">
      <h2 class="h2" id="cap-h">O que a gente constrói, a partir do que trava.</h2>
      <p class="lede">Site, sistema, automação e integração são ferramentas. O trabalho começa pelo problema e só depois escolhe qual delas resolve, inclusive quando a resposta é não construir nada.</p>
    </div>
    <ol class="caps">
{caps}
    </ol>
  </div>
</section>

<section class="proof" id="prova" aria-labelledby="prova-h">
  <div class="wrap grid proof-grid">
    <div class="proof-copy">
      <p class="kicker"><b>prova de método</b></p>
      <h2 class="h2" id="prova-h">Somos novos. Levamos execução a sério.</h2>
      <p class="lede">Não temos parede de logos e não vamos inventar uma. Cada item abaixo existe, com o estado real ao lado.</p>
      <ol class="plist">
{proof}
      </ol>
    </div>
    <figure class="proof-shot" style="margin:0">
      <div class="shot">
        <div class="shot-bar mono"><span>construa360 · calculadora de prejuízo invisível</span><span class="wide-only">captura real</span></div>
        <img src="{p}assets/img/construa360-calculadora.jpg" alt="Resultado da calculadora de prejuízo invisível do Construa360: perda estimada por mês e a origem de cada parcela" width="720" height="861" loading="lazy" decoding="async">
      </div>
      <figcaption class="shot-cap mono">Landing pública do Construa360, produto próprio, com valores de exemplo digitados. O cálculo roda no navegador de quem visita; nenhum dado sai de lá sem a pessoa escolher.</figcaption>
    </figure>
  </div>
</section>

<section class="method" id="metodo" aria-labelledby="met-h">
  <div class="wrap">
    <p class="kicker"><b>como funciona</b></p>
    <h2 class="h2" id="met-h" style="margin-top:14px">Do primeiro papo ao sistema rodando.</h2>
    <p class="lede" style="margin-top:18px">Entender antes de construir. IA e automação entram onde ajudam de verdade: a regra vem primeiro, a ferramenta depois.</p>
    <ol class="steps">
{steps}
    </ol>
    <div class="prices" role="list">
      <div class="pcell" role="listitem"><span class="pv"><small>micro-automação</small>R$ 150+</span><p>Uma tarefa repetitiva que vira regra.</p></div>
      <div class="pcell" role="listitem"><span class="pv"><small>processo completo</small>R$ 500+</span><p>Entrada, regra, ação e registro de um processo inteiro.</p></div>
      <div class="pcell" role="listitem"><span class="pv"><small>site ou landing page</small>R$ 690–1.500</span><p>Escopo fechado, conforme páginas e conteúdo.</p></div>
      <div class="pcell" role="listitem"><span class="pv"><small>sob medida</small>orçamento</span><p>Sistemas, integrações e produtos, com escopo fechado depois do diagnóstico.</p></div>
    </div>
    <p class="prices-note mono">preço fechado antes de começar · o degrau certo sai do diagnóstico, não do chute</p>
  </div>
</section>

<section class="cost" id="conta" aria-labelledby="conta-h">
  <div class="wrap grid cost-grid">
    <div class="cost-copy">
      <p class="kicker"><b>antes de conversar</b></p>
      <h2 class="h2" id="conta-h">Quanto custa o trabalho repetido hoje?</h2>
      <p class="lede">Mexa nos números da sua operação. A conta roda aqui no navegador; nada é enviado.</p>
      <p class="mono method-note">conta: pessoas × horas por semana × 4,33 semanas × custo da hora. Mostramos uma faixa de 20% para cima e para baixo, porque quase ninguém mede esse tempo com precisão.</p>
    </div>
    <div class="calc">
      <div class="field"><label class="mono" for="c-people">pessoas que fazem esse trabalho</label><div class="inrow"><input type="range" id="c-people" min="1" max="15" value="2"><output for="c-people" id="o-people">2</output></div></div>
      <div class="field"><label class="mono" for="c-hours">horas por semana, cada uma</label><div class="inrow"><input type="range" id="c-hours" min="1" max="30" value="6"><output for="c-hours" id="o-hours">6 h</output></div></div>
      <div class="field"><label class="mono" for="c-rate">custo da hora (salário + encargos)</label><div class="inrow"><input type="range" id="c-rate" min="15" max="150" step="5" value="35"><output for="c-rate" id="o-rate">R$ 35</output></div></div>
      <div class="calc-out" aria-live="polite">
        <span class="big" id="r-range">R$ 1.500 a R$ 2.200</span>
        <span class="sub" id="r-sub">por mês, em cerca de 52 horas de trabalho repetido</span>
      </div>
      <a class="btn" href="#conversa" id="r-carry">Levar esse número para a conversa <span class="arr" aria-hidden="true">→</span></a>
    </div>
  </div>
</section>

{talk(p)}
</main>
""" + footer(p, noindex)

# ────────────────────────────── páginas internas ──────────────────────────────

def crumbs_html(crumbs, cls="crumb mono"):
    cr = ' <span aria-hidden="true">/</span> '.join(crumbs)
    return f'<nav class="{cls}" aria-label="Você está em">{cr}</nav>'

def page_head(p, crumbs, tag, h1, lede, meta="", aside=""):
    return f"""<section class="page-head" aria-labelledby="ph-h">
  <div class="wrap grid ph-grid">
    <div class="ph-main">
      {crumbs_html(crumbs)}
      <h1 class="page-h1" id="ph-h">{h1}</h1>
      <p class="page-lede">{lede}</p>
      <div class="page-meta">{meta}<span class="mono">{tag}</span></div>
    </div>
    <aside class="ph-aside">{aside}</aside>
  </div>
</section>
"""

def block(title, kicker, body):
    return f"""<section class="block">
  <div class="wrap grid block-grid">
    <div class="bh"><span class="mono">{kicker}</span><h2>{title}</h2></div>
    <div class="bb">{body}</div>
  </div>
</section>
"""

def block_full(title, kicker, body):
    return f"""<section class="block">
  <div class="wrap">
    <div class="bh bh-row"><span class="mono">{kicker}</span><h2>{title}</h2></div>
    <div class="bf">{body}</div>
  </div>
</section>
"""

def solucao(k, p, noindex):
    s = SOLUCOES[k]
    pains = "".join(f"<li>{d}</li>" for d in s["dores"])
    builds = "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in s["construimos"])
    flow = "".join(f"<li><b>{t}</b><span class=\"mono\">{d}</span></li>" for t, d in s["etapas"])
    aplica = "".join(f"<li>{a}</li>" for a in s["aplica"])
    evid = "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in s["evidencia"])
    others = "".join(f'<a href="{p}solucoes/{o}/">{SOLUCOES[o]["nome"]} →</a>' for o in ORDEM if o != k)
    meta = f'<a class="btn primary" href="#conversa">{s["cta"]} <span class="arr" aria-hidden="true">→</span></a><span class="mono"><b>{s["preco"]}</b></span>'
    aside = f'<span class="mono aside-k">onde isso costuma doer</span><ol class="pains">{pains}</ol>'
    body = page_head(p, [f'<a href="{p}">início</a>', f'<a href="{p}#capacidade">soluções</a>', f'<span>{s["nome"]}</span>'], s["tag"], s["h1"], s["lede"], meta, aside)
    body += block("O que construímos", "a solução", f'<ol class="builds">{builds}</ol>')
    body += block_full("Como funciona", "etapas", f'<ol class="flow">{flow}</ol>')
    body += block("Onde se aplica e o que já existe", "aplicação e prova", f'<div class="two-lists"><div class="tl"><h3>Onde se aplica</h3><ul>{aplica}</ul></div><div><h3 class="tl" style="font-variation-settings:\'wdth\' 74,\'wght\' 760;font-size:1.15rem;padding-bottom:10px;margin-bottom:0">Nossa evidência</h3><ol class="evidence" style="border-top-width:2px">{evid}</ol></div></div>')
    body += block("Investimento", "quanto custa", f'<div class="price-line"><span class="pv">{s["preco"]}</span><p>{s["investimento"]}</p></div>')
    body += block("Outras frentes", "soluções", f'<div class="others">{others}</div>')
    return (head(p, s["title"], s["desc"], f"solucoes/{k}/", noindex) + header(p) +
            f'<main id="conteudo">\n{body}{talk(p, "Vamos olhar o seu caso?", intent=k)}</main>\n' + footer(p, noindex))

def contato(p, noindex):
    depois = [("Você descreve o problema.", "Três linhas bastam."),
              ("A gente responde com perguntas ou já com um caminho.", "Em até 1 dia útil, por e-mail."),
              ("Se fizer sentido, vem escopo, prazo e preço fechados.", "Por escrito, antes de começar."),
              ("Se não for com a gente, a gente diz.", "E indica o caminho.")]
    flow = "".join(f"<li><b>{t}</b><span class=\"mono\">{d}</span></li>" for t, d in depois)
    body = talk(p, "Vamos resolver isso.", h1=True,
                crumb=crumbs_html([f'<a href="{p}">início</a>', "<span>contato</span>"], "crumb mono on-ink"),
                lede="Não precisa vir com solução pronta nem com termo técnico. Conte o que está travando em três linhas; descobrir o que construir é trabalho nosso.")
    body += block_full("O que acontece depois", "próximos passos", f'<ol class="flow">{flow}</ol>')
    return (head(p, "Contato · GrupoGest", "Descreva seu problema em três linhas. Respondemos dizendo se resolvemos, como resolveríamos e quanto custa, ou que não é com a gente.", "contato/", noindex) +
            header(p) + f'<main id="conteudo">\n{body}</main>\n' + footer(p, noindex))

def parcerias(p, noindex):
    ganha = [("Você vende mais escopo", "Deixa de recusar projeto que trava na parte técnica. A engenharia entra e você mantém o contrato, a marca e a relação com o cliente."),
             ("Preço fechado antes da venda", "A gente devolve escopo, prazo e preço fechados. Você precifica sua margem com segurança, não no chute."),
             ("White-label de verdade", "Falamos com você. Se quiser a gente na reunião com o cliente, vamos no seu nome, do seu jeito."),
             ("Time que documenta", "Entrega com acesso, código e documentação. Se a parceria acabar, nada fica refém da gente.")]
    faz = ["Back-end e API (Python/FastAPI, PostgreSQL)", "Automação de processo (n8n, Python, webhooks)", "Integração entre sistemas e APIs", "Aplicação web em Next.js e e-commerce próprio", "Sistemas internos e painéis de dados", "Correção e manutenção de projeto existente"]
    nao = ["Tráfego pago e gestão de anúncios", "SEO com promessa de posição", "Publicação em App Store/Play como especialidade", "Especialista em Shopify, Nuvemshop ou WordPress", "Design de marca e identidade visual completa"]
    pratica = [("Briefing", "Você manda o que o cliente pediu. Fazemos as perguntas técnicas que faltaram, de preferência antes de você fechar."),
               ("Escopo", "Devolvemos escopo, prazo e preço fechados em até 3 dias úteis. Você aplica sua margem."),
               ("Execução", "Ponto de contato único, entrega em partes, repositório acessível a você."),
               ("Entrega", "No seu nome. Código, acesso e documentação passam para você ou para o cliente, o que vocês combinarem."),
               ("Depois", "Manutenção e evolução podem ser contratadas por demanda. Sem mensalidade obrigatória.")]
    builds = "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in ganha)
    flow = "".join(f"<li><b>{t}</b><span>{d}</span></li>" for t, d in pratica)
    lists = ('<div class="tl no"><ul>' + "".join(f"<li>{x}</li>" for x in nao) +
             '</ul></div><p class="lede" style="margin-top:22px">Preferimos perder um projeto a entregar algo fora da nossa competência no seu nome. É o seu cliente que fica na conta, não o nosso.</p>')
    aside = '<span class="mono aside-k">o que fazemos bem</span><ol class="pains">' + "".join(f"<li>{x}</li>" for x in faz) + '</ol>'
    meta = f'<a class="btn primary" href="#conversa">Mandar um projeto para orçar <span class="arr" aria-hidden="true">→</span></a><a class="link" href="{p}#prova">Ver o que já construímos</a>'
    body = page_head(p, [f'<a href="{p}">início</a>', "<span>parcerias</span>"], "para agências, consultorias e estúdios",
                     "Seu cliente precisa de tecnologia. A gente vira seu braço técnico.",
                     "Você já tem a relação comercial, o contexto e a confiança do cliente. O que costuma faltar é quem construa, com prazo, teste e documentação. É essa parte que a gente faz, por baixo, no seu nome.", meta, aside)
    body += block("O que você ganha", "para a agência", f'<ol class="builds">{builds}</ol>')
    body += block("O que não vendemos", "escopo honesto", lists)
    body += block_full("Como funciona na prática", "do briefing à entrega", f'<ol class="flow">{flow}</ol>')
    body += talk(p, "Manda um projeto para a gente orçar.", intent="parceria")
    return (head(p, "Parceria técnica e white-label para agências · GrupoGest", "Somos o braço técnico de agências e consultorias: back-end, automação, integração e sistemas sob medida, em white-label, com prazo e preço fechados antes de você vender.", "parcerias/", noindex) +
            header(p, current="parcerias") + f'<main id="conteudo">\n{body}</main>\n' + footer(p, noindex))


# ────────────────────────────── landing pages de campanha (/lp/) ──────────────────────────────

EVID_AUTOMACAO = [("n8n + Postgres + webhooks + API de IA", "Pipeline construído e validado ponta a ponta em ambiente próprio."),
                  ("Automação em Python", "CLIs e rotinas com testes automatizados rodando na operação interna todo dia.")]
LPS = {
  "automacao-clinicas": {
    "title": "Automação de agendamento para clínicas · GrupoGest",
    "desc": "Confirmação automática, lembrete com remarcação e recuperação de horários vagos para clínicas e consultórios.",
    "seg": "clínicas e consultórios", "intent": "clinicas",
    "h1": "Cada falta na agenda é uma hora que não volta.",
    "lede": "Confirmação, lembrete e recuperação de horário são regra, e regra pode rodar sozinha, 24 horas por dia, sem sobrecarregar a recepção.",
    "cta": "Quero organizar minha agenda",
    "entra": [("Confirmação no ato", "O paciente marca e já recebe data, horário e endereço. Menos ligação, menos engano."),
              ("Lembrete com remarcação", "24h antes, com opção de remarcar em vez de simplesmente faltar."),
              ("Recuperação de horário", "Faltou? A automação oferece novas datas na hora, enquanto o interesse ainda existe.")],
    "evid": EVID_AUTOMACAO, "sol": "automacao",
  },
  "automacao-contabilidade": {
    "title": "Automação para escritório contábil · GrupoGest",
    "desc": "Recebimento de documento, validação, cobrança de pendência e painel de prazos automatizados para escritórios contábeis.",
    "seg": "escritórios contábeis", "intent": "contabilidade",
    "h1": "Documento, prazo e cobrança não deveriam depender de memória.",
    "lede": "Escritório contábil vive de prazo. A parte que some no meio é sempre a mesma: o cliente que não mandou o documento e ninguém cobrou a tempo.",
    "cta": "Quero ver isso no meu escritório",
    "entra": [("Entrada organizada", "Documento que chega por e-mail ou WhatsApp é validado, nomeado e arquivado no lugar certo."),
              ("Cobrança automática", "Faltou documento perto do prazo? O cliente recebe a cobrança sem alguém precisar lembrar."),
              ("Painel de pendências", "Um lugar para ver quem está em dia e quem vai virar problema no dia 20.")],
    "evid": EVID_AUTOMACAO, "sol": "automacao",
  },
  "automacao-imobiliarias": {
    "title": "CRM e automação de leads para imobiliárias · GrupoGest",
    "desc": "Centralização de leads de portais, site e WhatsApp, distribuição por regra e follow-up automático para imobiliárias.",
    "seg": "imobiliárias e corretores", "intent": "imobiliarias",
    "h1": "O lead do portal esfria em minutos. Sua resposta leva horas.",
    "lede": "Quem responde primeiro costuma agendar a visita. Isso é problema de processo, não de esforço do corretor.",
    "cta": "Quero não perder mais lead",
    "entra": [("Lead centralizado", "Portal, site e WhatsApp caindo num lugar só, com origem registrada."),
              ("Distribuição por regra", "Bairro, faixa de preço ou rodízio: o corretor certo recebe na hora."),
              ("Follow-up que não esquece", "Visita agendada, retorno cobrado, contato reativado no prazo certo.")],
    "evid": EVID_AUTOMACAO, "sol": "automacao",
  },
  "parceria-white-label": {
    "title": "Parceria técnica white-label para agências · GrupoGest",
    "desc": "Desenvolvimento white-label para agências e consultorias: back-end, automação, integração e sistemas com escopo e prazo fechados.",
    "seg": "agências e consultorias", "intent": "parceria",
    "h1": "Seu cliente precisa de tecnologia. A gente vira seu braço técnico.",
    "lede": "Você mantém a relação, a marca e o contrato. A engenharia roda por baixo, no seu nome, no seu prazo.",
    "cta": "Quero conversar sobre parceria",
    "entra": [("White-label de verdade", "Falamos com você, não com seu cliente, a não ser que você peça e esteja na sala."),
              ("Escopo fechado", "Você precifica com segurança porque recebe prazo e preço fechados antes de vender."),
              ("O que fazemos", "Back-end, automação, integração, e-commerce e sistema sob medida. O que não sabemos, dizemos antes.")],
    "evid": None, "sol": "sistemas",
  },
  "site-comercio-local": {
    "title": "Site para comércio e negócio local · GrupoGest",
    "desc": "Site próprio para comércio local: rápido, encontrável no Google e com WhatsApp em toda dobra. Escopo e preço fechados, de R$ 690 a R$ 1.500.",
    "seg": "comércio e serviço local", "intent": "comercio",
    "h1": "Seu negócio já existe. Agora dê a ele um endereço próprio.",
    "lede": "Rede social é aluguel: alcance de outro, regra de outro. Site é seu: aparece no Google, funciona no celular e leva ao WhatsApp em um toque.",
    "cta": "Quero meu site",
    "entra": [("Encontrável no Google", "Nome, serviço, cidade, endereço e mapa configurados como o buscador espera."),
              ("Contato em um toque", "WhatsApp e telefone visíveis em toda dobra, testados em celular de verdade."),
              ("Escopo e preço fechados", "Você sabe o que vai receber e quanto custa antes de começar. De R$ 690 a R$ 1.500.")],
    "evid": None, "sol": "sites",
  },
}

def lp(k, p):
    d = LPS[k]
    evid = d["evid"] or SOLUCOES[d["sol"]]["evidencia"]
    entra = "".join(f"<li><b>{t}</b> {x}</li>" for t, x in d["entra"])
    ev = "".join(f"<li><h3>{t}</h3><p>{x}</p></li>" for t, x in evid)
    aside = f'<span class="mono aside-k">o que entra</span><ol class="pains lp-entra">{entra}</ol>'
    meta = f'<a class="btn primary" href="#conversa">{d["cta"]} <span class="arr" aria-hidden="true">→</span></a><a class="link" href="{p}#maquina">Ver como é construído</a>'
    body = page_head(p, [f'<a href="{p}">início</a>', f'<span>{d["seg"]}</span>'], d["seg"], d["h1"], d["lede"], meta, aside)
    body += block("Nossa evidência", "o que já construímos", f'<ol class="evidence">{ev}</ol><p class="lede" style="margin-top:22px">Não temos parede de logos nem depoimento. Somos uma equipe nova e não inventamos cliente: o que mostramos é o que construímos e validamos.</p>')
    body += talk(p, "Quer ver isso rodando na sua operação?", intent=d["intent"])
    return (head(p, d["title"], d["desc"], f"lp/{k}/", True) + header(p) +
            f'<main id="conteudo">\n{body}</main>\n' + footer(p, True))

def not_found(p, noindex=True):
    body = f"""<section class="page-head" aria-labelledby="ph-h">
  <div class="wrap grid ph-grid">
    <div class="ph-main">
      <p class="mono muted">erro 404</p>
      <h1 class="page-h1" id="ph-h">Essa página não existe. O problema que te trouxe aqui, sim.</h1>
      <p class="page-lede">Link quebrado é justamente um dos motivos pelos quais as empresas nos procuram.</p>
      <div class="page-meta"><a class="btn" href="{p}">Voltar ao início</a><a class="link" href="{p}contato/">Falar com a gente <span aria-hidden="true">→</span></a></div>
    </div>
    <aside class="ph-aside"><span class="mono aside-k">talvez você procurasse</span><ol class="pains">{"".join(f'<li><a href="{p}solucoes/{o}/">{SOLUCOES[o]["nome"]}</a></li>' for o in ORDEM)}</ol></aside>
  </div>
</section>
"""
    return (head(p, "Página não encontrada · GrupoGest", "Essa página não existe. O problema que te trouxe aqui, sim.", "404.html", True) + header(p) +
            f'<main id="conteudo">\n{body}</main>\n' + footer(p, True))

# ────────────────────────────── build ──────────────────────────────

def write(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prod", action="store_true", help="versão indexável para publicar")
    ap.add_argument("--out", default=os.path.join(ROOT, "..", "site"))
    ap.add_argument("--base", default="/site/", help="caminho absoluto do site no servidor (usado pela página 404)")
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    noindex = not a.prod
    write(os.path.join(out, "index.html"), home("", noindex))
    write(os.path.join(out, "contato", "index.html"), contato("../", noindex))
    write(os.path.join(out, "parcerias", "index.html"), parcerias("../", noindex))
    for k in ORDEM:
        write(os.path.join(out, "solucoes", k, "index.html"), solucao(k, "../../", noindex))
    for k in LPS:
        write(os.path.join(out, "lp", k, "index.html"), lp(k, "../../"))
    write(os.path.join(out, "404.html"), not_found(a.base))
    assets = os.path.join(out, "assets")
    os.makedirs(os.path.join(assets, "fonts"), exist_ok=True)
    os.makedirs(os.path.join(assets, "img"), exist_ok=True)
    shutil.copy(os.path.join(ROOT, "gg.css"), assets)
    shutil.copy(os.path.join(ROOT, "gg.js"), assets)
    shutil.copy(os.path.join(ROOT, "assets", "og.png"), os.path.join(out, "og.png"))
    for f in os.listdir(os.path.join(ROOT, "assets")):
        src = os.path.join(ROOT, "assets", f)
        if os.path.isdir(src):
            for g in os.listdir(src): shutil.copy(os.path.join(src, g), os.path.join(assets, f))
        else:
            shutil.copy(src, assets)
    if a.prod:
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        urls = [("", "1", "monthly"), ("parcerias/", "0.8", "monthly"), ("contato/", "0.7", "yearly")] + [(f"solucoes/{k}/", "0.9", "monthly") for k in ORDEM]
        sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
            f"<url>\n<loc>{BASE_URL}{u}</loc>\n<lastmod>{now}</lastmod>\n<changefreq>{c}</changefreq>\n<priority>{pr}</priority>\n</url>\n" for u, pr, c in urls) + "</urlset>\n"
        write(os.path.join(out, "sitemap.xml"), sm)
    print("site gerado em", out, "(noindex)" if noindex else "(produção)")

if __name__ == "__main__":
    main()
