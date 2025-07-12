#!/bin/bash

# Exit on any error
set -e

# Instalar los navegadores de Playwright (requerido en Railway y similares)
echo "Instalando navegadores de Playwright..."
playwright install

# (Opcional) Si usas Chromium específicamente:
# playwright install chromium

echo "Setup completo."
