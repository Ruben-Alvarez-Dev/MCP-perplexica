# Vane (Perplexica) MCP Server

MCP server para Vane (Perplexica) con descubrimiento automático de puerto.

## Puertos Oficiales

Según la documentación oficial, Vane/Perplexica se ejecuta en:
- **Frontend**: puerto `3000` (Next.js)
- **Backend API**: puerto `3001`
- **SearXNG**: puerto `4000` (motor de búsqueda)

## Quick Start

```bash
cd mcp-vane
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
python3 server.py
```

## Lógica de Descubrimiento

1. **Primero**: Busca en puerto `3001` (backend API oficial)
2. **Si no encuentra**: Escanea puerto `3000` (frontend)
3. **Si sigue sin encontrar**: Puertos alternativos (10301, 8000, 8001, 5000, 8080)
4. **Si sigue sin encontrar**: Pide al usuario el puerto por consola
5. **Fallback**: Usa `http://localhost:3001` si el usuario no responde

## Configuración Manual

Si prefieres configurar manualmente, usa la variable de entorno:
```bash
export VANE_BASE_URL=http://localhost:3001
```

O crea un archivo `.env` en la raíz del proyecto.

## Herramientas

### vane_search
- **query** (string): Consulta de búsqueda
- **mode** (string): "speed", "balanced" (default), o "quality"

## Claude Desktop

```json
{
  "mcpServers": {
    "vane": {
      "command": "uv",
      "args": ["--directory", "/Users/simba/Code/MCP-servers/mcp-vane", "run", "python3", "server.py"]
    }
  }
}
```

## MCP Server

- Puerto: 8082
- SSE: /sse
- HTTP: /mcp