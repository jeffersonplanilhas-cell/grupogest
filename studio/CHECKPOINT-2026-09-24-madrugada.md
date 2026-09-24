# Checkpoint · a pilha no ar · 24/09/2026 (madrugada)

Substitui `CHECKPOINT-2026-09-24-noite.md`.

- **Branch:** `claude/vibrant-fermi-yrknqg`, com `main` avançada até o mesmo commit (fast-forward).
- **Fonte:** `studio/site-src/` (única). Gera a raiz do repositório, que o GitHub Pages serve a partir de `main`.
- **Build:** `python3 studio/site-src/build.py --prod --out . --base /grupogest/`
- **Deploy:** workflow "pages build and deployment" do GitHub, disparado pelo push em `main`.

## O que é o site agora

Não é mais uma página com hero e seções. O início é a demonstração do que a GrupoGest vende:

1. **Entrada.** Os papéis de um dia de trabalho numa distribuidora (pedido pelo WhatsApp, comprovante por e-mail, planilha `estoque_v3_FINAL(2).xlsx`) caem sobre a página com física de verdade. Dá para pegar, arrastar e jogar. 16 papéis no desktop, 8 no celular.
2. **Transformação.** "Ligar o sistema" manda cada papel para a sua regra (pedidos, pagamentos, agenda, perguntas, números) e carimba o último. Quem só rola a página vê o sistema ligar sozinho.
3. **Mapa.** "Por dentro de um sistema": seis partes (entrada, regra, ponte, registro, painel, na rua), cada uma com o que a gente constrói, o que já existe e quanto custa.
4. **Memória.** No formulário, a mensagem do visitante vira um papel carimbado que cai na caixa de entrada da GrupoGest, com os assuntos marcados em chips.

Tese, prova, método e conta do trabalho repetido continuam, no mesmo sistema visual.

## Medido nesta build (produção, servida localmente em `/grupogest/`)

| | celular | desktop |
|---|---|---|
| Lighthouse desempenho / acessibilidade / boas práticas / SEO | 99 / 100 / 100 / 100 | 100 / 100 / 100 / 100 |
| LCP | 2,1 s | 0,6 s |
| CLS | 0 | 0 |
| TBT | 0 ms | 0 ms |

- Peso do início: 287 KiB. JavaScript próprio: 7,8 KB comprimido. Motor de física (Matter.js 0.20.0, MIT): 25 KB comprimido, carregado só pela pilha e nunca com movimento reduzido.
- axe-core 4.13: 0 violações em 6 páginas × 2 larguras.
- 15 páginas × 10 larguras (375, 390, 430, 768, 834, 1024, 1280, 1440, 1728, 1920): sem rolagem horizontal, sem erro de console, alvos de toque ≥ 24 px.
- 524 links e âncoras internas resolvem.
- 34 testes funcionais passam: queda e arraste dos papéis, ligar e desligar, cada papel na regra certa, ligar ao rolar, abas do mapa por teclado, conta, validação e montagem da mensagem, cópia, intenções antigas (`?intent=`), celular com toque, movimento reduzido e sem JavaScript.

## Correções encontradas pelo QA desta rodada

- Com movimento reduzido (ou sem o motor de física), a pilha estática cobria o botão principal. Agora ela ocupa só a área livre.
- A pilha deslocava o layout ao iniciar (CLS 0,86 no celular). O estado inicial agora vem da classe `js` do `<head>`: CLS 0.
- Links do menu, do rodapé e das landing pages apontavam para `#maquina`, que não existe mais.
- O texto de prova dizia "cerca de 11 KB" de JavaScript próprio; o medido é 7,8 KB. Corrigido para "cerca de 8 KB".
- E-mail quebrando no meio no rodapé; tese com metade da tela vazia no desktop (virou composição diagonal).

## Verificação ao vivo

O ambiente desta sessão bloqueia `jeffersonplanilhas-cell.github.io` (403 no proxy), então a página publicada não foi aberta daqui. O que foi verificado: o push em `main` e a conclusão do workflow de Pages no GitHub. Para verificar a página ao vivo numa próxima sessão, adicione `jeffersonplanilhas-cell.github.io` aos domínios permitidos do ambiente.

## Pendências reais

1. **WhatsApp:** preencher `CONFIG.whatsapp` em `studio/site-src/gg.js`. Nenhum número autorizado existe nos arquivos (`BLOCKED_BY_MISSING_AUTHORIZED_VALUE`). Enquanto vazio, o site não mostra WhatsApp.
2. **Formulário:** preencher `CONFIG.formEndpoint` para envio direto. Enquanto vazio, o formulário monta a mensagem e oferece e-mail e cópia; nada falha em silêncio.
3. **dev-os:** o deploy antigo publicava um build Next.js nesta mesma raiz. Se rodar de novo, sobrescreve este site.
