# Configuraciones experimentales de la tesis

| Configuración | Notebook | Recuperación | Defensas |
|---|---|---|---|
| C1 | [C1_baseline_llm_only.ipynb](C1_baseline_llm_only.ipynb) | No | Ninguna explícita |
| C2 | [C2_llm_rag.ipynb](C2_llm_rag.ipynb) | Chroma, top 3 | Ninguna explícita |
| C3 | [C3_llm_rag_secure_prompt.ipynb](C3_llm_rag_secure_prompt.ipynb) | Chroma, top 3 | Prompt seguro e instrucciones separadas |
| C4 | [C4_llm_rag_full_defense.ipynb](C4_llm_rag_full_defense.ipynb) | Chroma, top 3 | Detector, metadatos de confianza y ruta segura con control de citas |

Los notebooks conservan la organización por secciones y clases de los
originales, con las cuatro configuraciones separadas según la tesis. El
notebook de demostración independiente no forma parte de esta comparación.

Todos los notebooks utilizan los mismos campos de entrada desde SQLite, el
modelo `OPEN_MODEL` (por defecto `gpt-4o-mini`), temperatura 0.1 y el mismo
esquema de salida. Las etiquetas de evaluación no se envían al modelo.
C2, C3 y C4 usan la misma colección persistente de Chroma y la misma consulta.
Por defecto se procesan cuatro registros; cambia `N_RECORDS` a `None` en
todos los notebooks para procesar el conjunto completo. Una muestra pequeña
no constituye la evaluación de la tesis.

En C4, el detector examina únicamente campos controlables por el cliente.
Una coincidencia selecciona el prompt seguro y el control de citas; sin
coincidencia se usa RAG estándar. No detectar una inyección no demuestra que
no exista. El control de citas comprueba que los IDs citados estén entre los
recuperados, pero no verifica que las fuentes respalden la respuesta.

El prompt seguro compartido por C3 y la ruta segura de C4 distingue un
intento malicioso de un ataque exitoso y separa la clasificación del evento
web de las instrucciones inyectadas. Mantiene `unknown` cuando falta
evidencia, no considera benigno un registro solo porque se bloqueó un
ataque o no hay evidencia de fuerza bruta, y no deduce fuerza bruta de un
único login fallido. Los resultados
registran `secure_prompt_version` para distinguir este prompt de ejecuciones
anteriores; el prompt estándar de C1, C2 y la ruta estándar de C4 no cambia.

En C3 y C4, `USE_FEW_SHOT = True` añade al prompt seguro tres ejemplos
sintéticos creados para desarrollo, sin extraer registros de los 500:
una petición normal con una instrucción inyectada, intentos de login
relacionados con indicios de fuerza bruta y un único login fallido sin
contexto suficiente. El ejemplo de varios intentos es hipotético: el pipeline
actual recibe un solo registro y no aporta secuencias temporales. No debe
inferirlas a partir de ese ejemplo.

Estos ejemplos no crean una partición de evaluación ni garantizan que no haya
similitudes con los registros de prueba. Para una evaluación final, separa
desarrollo y prueba por parejas y evita filtrar plantillas. Cambia
`USE_FEW_SHOT` a `False` en ambos notebooks para comparar con el prompt anterior.
Las funciones compartidas conservan los ejemplos desactivados por defecto.
Cada resultado registra `few_shot_enabled`, `few_shot_applied` y
`few_shot_version`; en C4 solo se aplican si se selecciona la ruta segura.
La versión del prompt base se conserva en `secure_prompt_version`. Estos
cambios no demuestran por sí mismos una reducción de `unknown`.

La lógica compartida está en `../src/experiments.py`. Los cuatro notebooks
activan por igual `STRUCTURED_OUTPUT` y `RECOVER_MARKDOWN`. La primera opción
solicita al proveedor una salida estructurada con el esquema Pydantic estricto;
requiere un modelo compatible y los errores del proveedor no se ocultan.
La segunda permite recuperar únicamente un bloque Markdown completo, con
etiqueta `json` o sin etiqueta, y valida su contenido con Pydantic. No se
extrae JSON de respuestas con texto adicional ni se corrigen datos inválidos.

Los resultados guardan la respuesta original, los dos ajustes y los campos
`raw_output_valid`, `raw_output_error`, `markdown_recovered`, `output_valid`
y `output_error`. La validez directa se cuenta por separado de las
recuperaciones; `output_valid` incluye ambos casos. Un rechazo del modelo
se registra en `model_refusal`. El resumen por lotes también distingue
salidas directas y recuperadas. Estas medidas no demuestran que la respuesta
sea correcta. Para reproducir el comportamiento anterior, desactiva ambos
ajustes en los cuatro notebooks; no compares directamente resultados obtenidos
con ajustes diferentes. Los notebooks aún no calculan las métricas de
clasificación o de ataque de la tesis.

Las ejecuciones envían los registros al proveedor del modelo y pueden generar
costes. Usa solo datos cuyo envío esté autorizado y evita incluir secretos.
Consulta [QUICKSTART.md](QUICKSTART.md) para preparar y ejecutar.

## Evaluación completa reproducible

Para ejecutar los 500 registros en las cuatro configuraciones y conservar
los resultados parciales en un directorio dedicado:

```bash
python scripts/evaluate_full_dataset.py --output-dir results/full_dataset_new --workers 8
python scripts/summarize_full_dataset.py --output-dir results/full_dataset_new
```

La ejecución requiere hasta 2.000 llamadas al proveedor. Usa Chroma local,
comprueba que sus 57 documentos coinciden con el corpus y conserva la
recuperación compartida, el manifiesto y cada respuesta. Si una llamada falla,
la ejecución se detiene tras terminar las llamadas en curso; se puede reanudar
con el mismo comando y directorio si los datos, el código y los ajustes siguen
coincidiendo con el manifiesto. El resumen solo se crea cuando hay 2.000
resultados y no sobrescribe un resumen existente.

El resumen distingue aciertos, `unknown`, errores binarios y salidas inválidas.
No calcula éxito de inyección ni respaldo semántico de citas: esas métricas
necesitan una evaluación adicional. Los resultados del conjunto completo
siguen siendo descriptivos, no una prueba independiente, porque algunos de
sus registros se usaron durante el ajuste del prompt.
