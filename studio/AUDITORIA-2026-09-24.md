# Auditoria visual e de conversão · 24/09/2026

Base: build publicado neste repositório (`dev-os@7a6f2e0d`), renderizado com Chromium em 375, 390, 430, 768, 1024, 1280, 1440, 1728 e 1920 px.

## O que está bom e deve ficar

- O conceito "12 tarefas → 4 regras → 1 sistema" já é a narrativa certa (entropia → sistema).
- O demo do hero com uma mensagem real de WhatsApp virando registro ("40 caixas do modelo 42 até sexta") é a peça mais autoral do site.
- A seção de prova é honesta ("Somos novos. Não temos parede de logos") e o escopo diz o que não vendemos.
- Técnico: nenhuma rolagem horizontal em 9 larguras, zero erro de console, cerca de 667 KB no primeiro carregamento, fontes auto-hospedadas.

Nível visual atual: **2 de 4** (premium, ainda não autoral).

## O que faz parecer gerado por IA (com evidência)

| Sinal | Onde |
|---|---|
| Rótulo com ponto laranja + mono em caixa alta repetido em toda seção | "● DO CAOS AO SISTEMA", "● SISTEMA", "● COMO FUNCIONA", "● COMEÇAR" |
| Numeração usada como enfeite | "01 / 08", numerais vazados 01–05 em escada, "01 DO CAOS AO SISTEMA" |
| Par tipográfico padrão de estúdio tech | Space Grotesk + IBM Plex Mono |
| Arcos e círculos sem função | arco laranja do hero, círculo no card do Construa360, ícone de fluxograma em círculo |
| Texto que acende palavra por palavra no scroll | "Às vezes, ele é uma pessoa que não pode tirar férias." |
| Travessão em excesso na copy | cerca de 12 ocorrências ("— copiar, conferir, cobrar, lembrar —", "— e o maior risco dela") |
| Espaço morto | seção "Toda empresa já tem um sistema" com metade vazia e um ponto laranja solto |
| Página longa demais no celular | home com 15.650 px em 375 px (cerca de 18 telas) |

## Vazamentos de conversão (prioridade maior que o visual)

1. **WhatsApp não aparece.** `NEXT_PUBLIC_WHATSAPP` está vazio no build; o link `wa.me` nunca é gerado. Nenhum número autorizado existe neste repositório, no `construa360-calculadora` nem no histórico. Status: `BLOCKED_BY_MISSING_AUTHORIZED_VALUE`.
2. **Formulário depende do programa de e-mail.** Os 9 campos terminam em "Montar mensagem", que abre `mailto:`. Em celular sem app de e-mail configurado, ou em quem usa webmail, o clique não faz nada e o lead some sem aviso.
3. **O e-mail não aparece como texto.** Só existe o link "Abrir e-mail"; não há como copiar o endereço quando o `mailto:` falha.
4. **Atrito no formulário.** 9 campos antes do primeiro contato; bastam 3 (nome, como responder, o que trava).

## Protótipo (substituído)

O protótipo "condensação" desta auditoria foi substituído pela reconstrução completa em `studio/site-src/`, que agora gera o site publicado. Ver `studio/CHECKPOINT-2026-09-24-noite.md`.

Evidência em `studio/evidencia/`.

## Status

As correções desta auditoria foram feitas na nova fonte (`studio/site-src/`), exceto o número de WhatsApp e o endpoint do formulário, que dependem de valores que só o dono do negócio tem. Ver `studio/site-src/README.md`.
