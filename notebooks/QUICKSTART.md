# Inicio rápido: C1 a C4

1. Selecciona en VS Code el entorno Python del proyecto, con las dependencias
   de `requirements.txt` instaladas.
2. Configura `OPENAI_API_KEY` localmente, en el entorno o en `.env`. No
   incluyas la clave en notebooks ni en archivos compartidos.
3. Inicializa SQLite y Chroma desde la raíz del proyecto:

   ```bash
   docker compose up -d chroma
   docker compose --profile init run --build --rm db-init
   ```

   Para consultar el servicio Docker desde los notebooks, configura
   `CHROMA_HOST=localhost` y `CHROMA_PORT=8000` en el entorno o `.env`.
   Sin `CHROMA_HOST`, se usa la colección local en
   `data/chroma_security_knowledge/`, que debe inicializarse por separado.
4. Abre `C1_baseline_llm_only.ipynb`, `C2_llm_rag.ipynb`,
   `C3_llm_rag_secure_prompt.ipynb` y `C4_llm_rag_full_defense.ipynb`.
   Cada uno explica sus pasos en inglés.
5. Por defecto cada notebook procesa cuatro registros. Usa el mismo valor de
   `N_RECORDS` en todos; para la evaluación completa usa `None`.
   Mantén también iguales `STRUCTURED_OUTPUT` y `RECOVER_MARKDOWN`: ambos están
   activados por defecto. El primero requiere un modelo compatible con salidas
   estructuradas de OpenAI.

Para ejecutarlos todos por lotes:

```bash
python notebooks/run_experiments.py
```

Los resultados se guardan en `results/c1_results.json` hasta
`results/c4_results.json`. El ejecutor también guarda HTML y
`results/experiment_summary.json`. Cada ejecución sobrescribe los archivos
correspondientes; guarda una copia si necesitas conservar resultados anteriores.
El resumen distingue salidas válidas directamente de las recuperadas de
Markdown; no mide precisión ni éxito de ataque.

**Costes y privacidad:** cada registro realiza una llamada al proveedor del
modelo. El conjunto completo puede generar costes y enviar datos externos;
utiliza únicamente registros autorizados.

Para comprender las diferencias y limitaciones, consulta
[README_EXPERIMENTAL_CONFIGS.md](README_EXPERIMENTAL_CONFIGS.md).
