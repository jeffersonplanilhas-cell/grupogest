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

## Protótipo: `studio/condensacao/`

Conceito de direção de arte, não publicado. A tipografia faz o argumento: Archivo variável vai de largo e leve ("Trabalho manual") a condensado e pesado ("vira sistema."), e a coluna 12 → 4 → 1 repete essa compressão.

- Hero com a condensação animada uma vez (estado final estático com `prefers-reduced-motion`).
- Mecanismo: a mensagem entra, os dados voam para a ficha, o ruído apaga e o carimbo fecha. Três exemplos: pedido, pagamento, agenda.
- Calculadora "quanto custa o trabalho repetido", no mesmo padrão da calculadora do Construa360 (roda no navegador, mostra faixa, metodologia aberta).
- Prova em tabela com o estado real de cada item.
- Contato com WhatsApp, e-mail copiável e formulário de 3 campos.
- Sem rótulos com ponto, sem numeração decorativa, sem arcos, sem travessões na copy.
- Verificado em 9 larguras: sem rolagem horizontal, as duas linhas do título cabem dentro da margem de 16 px, home com cerca de 5.600 px em 390 px.

Nível visual do protótipo: **3 de 4** (autoral).

Evidência em `studio/evidencia/`.

## Como portar no dev-os

1. Definir `NEXT_PUBLIC_WHATSAPP` (só dígitos, com 55 e DDD) no ambiente de build e publicar de novo.
2. Trocar o `mailto:` do formulário por um endpoint de formulário (Web3Forms, Formspree ou uma rota própria) e mostrar o e-mail como texto com botão de copiar.
3. Reduzir o formulário para 3 campos obrigatórios.
4. Substituir Space Grotesk + IBM Plex Mono por Archivo (wdth 62–125) + Martian Mono via `next/font/google`.
5. Portar hero, mecanismo e calculadora como componentes; remover rótulos com ponto, numerais decorativos, arcos e o texto que acende no scroll.
6. Revisar a copy trocando travessões por vírgula, parênteses ou ponto.
