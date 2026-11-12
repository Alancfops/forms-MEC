#!/usr/bin/env bash
# Gera o .docx do levantamento a partir de conteudo.py (2 passadas: a 2ª preenche as páginas do sumário)
set -e
cd "$(dirname "$0")"
OUT="$(cd ../.. && pwd)/docs/requisitos/Levantamento de requisitos - Projeto Fabiana.docx"
TMP=$(mktemp -d)
python3 build.py "$TMP/p.docx"
soffice --headless --convert-to pdf --outdir "$TMP" "$TMP/p.docx" >/dev/null 2>&1
python3 pages.py "$TMP/p.pdf"
python3 build.py "$OUT" pages.json
rm -rf "$TMP"
