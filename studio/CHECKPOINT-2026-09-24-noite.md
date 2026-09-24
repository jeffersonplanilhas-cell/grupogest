# Checkpoint · reconstrução do site · 24/09/2026 (noite)

> Substituído por `CHECKPOINT-2026-09-24-madrugada.md`. O push e o deploy desta lista já foram feitos.

- **Branch:** `claude/vibrant-fermi-yrknqg`
- **Fonte:** `studio/site-src/` (única). Gera a raiz do repositório, que o GitHub Pages serve.
- **Build:** `python3 studio/site-src/build.py --prod --out . --base /grupogest/`
- **Push:** recusado pelo GitHub (403, o app do Claude não tem escrita no repositório). Commits locais prontos.

## O que mudou

- **Visual:** sistema próprio com duas vozes tipográficas (ruído largo e leve, sistema condensado e pesado), laranja só quando o sistema age, réguas no lugar de cards. Sai Space Grotesk + Plex Mono, rótulos com ponto, numeração decorativa, arcos e travessões.
- **Experiência:** hero em que frases reais da rotina viram um registro com a regra de cada uma; máquina interativa (regras ligam e desligam, pilha manual esvazia); capacidade como tabela problema → entrega → prova → preço; conta do trabalho repetido que leva o número à mensagem.
- **Conversão:** formulário de 3 campos que nunca falha em silêncio (monta a mensagem, oferece e-mail e cópia); e-mail visível e copiável; WhatsApp e endpoint isolados em `CONFIG` e ocultos enquanto vazios; links antigos com `?intent=` continuam pré-preenchendo.
- **Páginas:** início, contato, parcerias, 6 soluções, 5 landing pages de campanha e 404, todas no mesmo sistema. Build antigo do Next.js removido.
- **Responsivo:** composições próprias no celular (registro com 6 linhas, máquina 2×2, capacidade só com dor e preço). Início no celular: ~9.900 px (antes 15.650).
- **Desempenho:** primeiro carregamento ~194 KB (antes ~667 KB), JS 18 KB (antes ~130 KB). Lighthouse celular 99 (antes 81), LCP 2,0 s (antes 4,8 s), CLS 0.
- **Acessibilidade:** axe sem violações além do logotipo (isento pela WCAG 1.4.3); foco visível; `role="switch"` nas regras; movimento reduzido e sem JavaScript mostram a página completa.

## Testes

- 16 páginas × 10 larguras (375 a 1920): sem rolagem horizontal, sem erro de console, alvos ≥ 24 px.
- 1.044 links e âncoras internas resolvem.
- 23 testes funcionais (formulário, máquina, conta, registro, intenções, movimento reduzido, sem JS).

## Pendências reais

1. **Push/deploy:** dar ao app do Claude permissão de escrita em `jeffersonplanilhas-cell/grupogest` e enviar a branch para `main`.
2. **WhatsApp:** preencher `CONFIG.whatsapp` em `studio/site-src/gg.js` (número não existe em nenhum arquivo autorizado).
3. **Formulário:** preencher `CONFIG.formEndpoint` para o envio direto.
4. **dev-os:** o deploy antigo publica um build Next.js nesta mesma raiz e sobrescreveria este site. Desativar ou apontar para `studio/site-src`.
