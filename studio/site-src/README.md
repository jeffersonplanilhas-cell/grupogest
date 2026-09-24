# GrupoGest · fonte do site

Esta pasta é a **fonte única** do site publicado em
<https://jeffersonplanilhas-cell.github.io/grupogest/>.
A raiz do repositório é o resultado do build (é ela que o GitHub Pages serve).

```
studio/site-src/
  build.py       templates e conteúdo de todas as páginas
  gg.css         sistema visual (tokens, tipografia, layout)
  gg.js          comportamento: registro do hero, máquina, conta, formulário
  assets/        ícone, fontes (OFL), imagem de prova, imagem de compartilhamento
```

Sem dependências: Python 3 para gerar, nenhum pacote de JavaScript.

## Gerar e publicar

```bash
# prévia local (noindex) em studio/site/
python3 studio/site-src/build.py

# versão de produção direto na raiz do repositório
python3 studio/site-src/build.py --prod --out . --base /grupogest/
git add -A && git commit -m "site: publicar" && git push
```

O GitHub Pages publica a raiz da branch `main`.

## Contato: dois valores pendentes

Em `gg.js`, no objeto `CONFIG`:

- `whatsapp`: só dígitos, com 55 e DDD. Vazio = o site não mostra WhatsApp em lugar nenhum.
- `formEndpoint`: URL que recebe o formulário (Formspree, Web3Forms ou rota própria).
  Vazio = o formulário monta a mensagem e oferece abrir no e-mail ou copiar; nada é enviado sozinho
  e nada falha em silêncio.

Depois de preencher, gere o build de produção de novo.

## Sistema visual

- Duas vozes da mesma família variável (Archivo): **ruído** = larga e leve (`wdth 125`, `wght 280`);
  **sistema** = condensada e pesada (`wdth 64`, `wght 820`).
- Laranja `#FF5500` só aparece quando o sistema age (o quadrado do registro) ou na ação principal.
- Cor de texto sobre fundo claro usa `#C23F00` quando precisa de contraste AA.
- Sem cantos arredondados, sem sombra, sem ornamento. Estrutura por réguas de 1px e 2px.
- Movimento com função: ruído → registro no hero, itens entrando e saindo na máquina.
  Com `prefers-reduced-motion`, tudo aparece no estado final.

## Importante

O repositório `dev-os` publicava um build antigo (Next.js) nesta mesma raiz.
Se esse deploy rodar de novo, ele sobrescreve este site. Publique a partir desta pasta.
