"""Genera la página profesional (index + casos de estudio) en el repo sub-cre.github.io."""
import time
from html import escape
from pathlib import Path

SITE = Path(r"C:\Users\PCs\OneDrive\Desktop\CV's\analista\github\sub-cre.github.io")
REPO = "https://github.com/Sub-Cre/portafolio-analisis-datos/tree/main/"
EMAIL = "oscararnez1234@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/oscar-a-639b09183"
GITHUB = "https://github.com/Sub-Cre/portafolio-analisis-datos"
VER = str(int(time.time()))
WORKANA = "https://www.workana.com/freelancer/303a6967c8c3074f16680fe3aebb4022"

PROYECTOS = [
    dict(
        slug="limpieza-base-clientes", carpeta="03-limpieza-base-clientes", img="limpieza.jpg",
        titulo="Limpieza y estandarización de una base de clientes",
        corto="Limpieza de una base de clientes",
        pregunta="¿Cómo dejar una base exportada del CRM sin duplicados y con formatos estándar?",
        tecnica="Pandas, regex, union-find, pytest",
        metrica="37 → 97 %", metrica_label="campos en formato estándar", n="2.016 registros",
        resumen="Una base cargada por distintas personas y formularios: teléfonos en seis formatos, ciudades escritas de cinco maneras, montos con coma o punto decimal y el mismo cliente repetido. Armé un pipeline que la deja lista para usar y que se puede volver a correr con la exportación del mes siguiente.",
        contexto=[
            "Es el pedido más común que veo en proyectos freelance: una empresa quiere hacer una campaña, migrar a otro CRM o simplemente contar cuántos clientes tiene, y la base no lo permite. Arreglarla a mano en Excel funciona una vez, pero el mes siguiente llega otra exportación con los mismos problemas.",
            "Por eso lo resolví como un pipeline: cada regla de limpieza es una función de Python con pruebas, y el proceso completo se ejecuta con un comando.",
        ],
        datos="2.016 registros con nombre, correo, teléfono, ciudad, fecha de registro y monto de compras. La base se generó por simulación con 1.800 clientes distintos más 216 duplicados con variaciones, para poder medir si el pipeline encuentra exactamente a los clientes que existen.",
        pasos=[
            "Estandaricé cada campo: nombres con mayúsculas consistentes, correos en minúscula y validados, teléfonos al formato +591 7XXXXXXX, ciudades contra un catálogo, fechas a AAAA-MM-DD y montos a número decimal.",
            "Si un valor no se puede interpretar, queda vacío. El pipeline no completa datos que no estaban.",
            "Detecté duplicados con union-find: dos registros son el mismo cliente si comparten correo, teléfono o nombre y ciudad, aunque el vínculo sea indirecto.",
            "De cada grupo conservé el registro más completo y rellené sus vacíos con los datos de los duplicados.",
            "Separé en una hoja aparte los 56 clientes sin contacto válido o con fecha ilegible, para que los revise una persona.",
        ],
        resultados=[("Registros de entrada", "2.016"), ("Clientes únicos", "1.798"), ("Duplicados fusionados", "218"),
                    ("Campos en formato estándar, antes", "37 %"), ("Campos en formato estándar, después", "97 %"),
                    ("Pruebas automáticas", "37")],
        hallazgos=[
            "El pipeline encontró 1.798 de los 1.800 clientes. Las 2 fusiones de más son clientes distintos que en la simulación recibieron el mismo correo, el mismo criterio que usaría un CRM.",
            "Lo que falta para llegar al 100 % en correo y teléfono son datos que venían vacíos o inválidos de origen. Quedan señalados, no inventados.",
        ],
        codigo_archivo="src/limpieza.py", lang="python",
        codigo='''def normalizar_telefono(valor):
    """Cualquier formato de celular boliviano -> '+591 7XXXXXXX'."""
    if _vacio(valor):
        return None
    dig = re.sub(r"\\D", "", str(valor))
    if len(dig) == 11 and dig.startswith("591"):
        dig = dig[3:]
    if len(dig) == 8 and dig[0] in "67":
        return f"+591 {dig}"
    return None''',
    ),
    dict(
        slug="analisis-sql-ecommerce", carpeta="04-analisis-sql-ecommerce", img="sql.jpg",
        titulo="Retención y segmentación de clientes de un e-commerce en SQL",
        corto="Retención y segmentación en SQL",
        pregunta="¿El negocio crece porque los clientes vuelven o solo porque llegan clientes nuevos?",
        tecnica="SQL, CTEs, funciones de ventana",
        metrica="16 %", metrica_label="de cada cohorte vuelve al mes siguiente", n="6.965 pedidos",
        resumen="Una tienda online con 4.000 clientes y dos años de pedidos. Todo el análisis está escrito en SQL: ventas mensuales, ranking de productos, retención por cohorte, segmentación RFM y recompra por canal de adquisición.",
        contexto=[
            "Los ingresos de la tienda crecieron 143 % de un año a otro. La pregunta del dueño era si ese crecimiento se sostiene solo, o si depende de seguir comprando tráfico.",
            "Escribí cinco consultas sobre una base relacional de cuatro tablas. Python solo ejecuta las consultas y dibuja los gráficos, así el análisis se puede llevar a PostgreSQL o MySQL casi sin cambios.",
        ],
        datos="Base SQLite con las tablas clientes (4.000), productos (60), pedidos (6.965) y detalle_pedido (17.479). Datos simulados con tasas de recompra distintas por canal y popularidad desigual de productos.",
        pasos=[
            "KPIs mensuales con variación respecto al mes anterior usando LAG().",
            "Top 3 productos por categoría con RANK() OVER (PARTITION BY categoria) y su peso dentro de la categoría.",
            "Retención por cohorte: el mes de la primera compra de cada cliente y en qué meses posteriores volvió a comprar.",
            "Segmentación RFM con NTILE(5) para recencia y monto. La frecuencia va con umbrales fijos, porque la mayoría compra una sola vez y NTILE repartiría esos empates al azar.",
            "Recompra y valor de vida por canal de adquisición.",
        ],
        resultados=[("Ingresos 2025", "$1,22 M"), ("Crecimiento vs 2024", "+143 %"), ("Retención al mes 1", "16 %"),
                    ("Retención al mes 3", "11 %"), ("Campeones + Leales", "11 % de clientes, 26 % de ingresos"),
                    ("Recompra: Referidos vs Google Ads", "53 % vs 30 %")],
        hallazgos=[
            "El crecimiento depende de clientes nuevos. Un flujo de correos para la segunda compra (días 7, 21 y 45) es la palanca más barata.",
            "Un cliente Campeón generó $1.315 en promedio, cuatro veces más que uno Perdido. Hay 190 clientes En riesgo que compraban seguido y dejaron de hacerlo.",
            "Los clientes referidos recompran casi el doble que los de Google Ads: parte de ese presupuesto rendiría más en un programa de referidos.",
        ],
        codigo_archivo="sql/04_segmentacion_rfm.sql", lang="sql",
        codigo='''puntaje AS (
    SELECT *,
           NTILE(5) OVER (ORDER BY recencia_dias DESC) AS r,
           CASE WHEN frecuencia = 1 THEN 1 WHEN frecuencia = 2 THEN 2
                WHEN frecuencia = 3 THEN 3 WHEN frecuencia <= 5 THEN 4
                ELSE 5 END                             AS f,
           NTILE(5) OVER (ORDER BY monto)              AS m
    FROM base
)''',
    ),
    dict(
        slug="prediccion-abandono", carpeta="05-prediccion-abandono-clientes", img="churn.jpg",
        titulo="Predicción de abandono de clientes de un servicio por suscripción",
        corto="Predicción de abandono (churn)",
        pregunta="¿A qué clientes debería llamar primero el equipo de retención y por qué se van?",
        tecnica="scikit-learn, validación cruzada",
        metrica="0,82", metrica_label="AUC en datos de prueba", n="7.000 clientes",
        resumen="Un servicio de internet y TV pierde a uno de cada tres clientes. El equipo de retención no puede llamar a todos, así que necesita una lista ordenada por riesgo y una explicación de qué está detrás de las bajas.",
        contexto=[
            "El objetivo no era tener el modelo más complejo, sino uno que el equipo pudiera usar cada mes y entender. Por eso comparé un modelo simple con uno más flexible y me quedé con el que rendía igual y se explica mejor.",
        ],
        datos="7.000 clientes con tipo de contrato, plan, antigüedad, cargo mensual, método de pago, tickets de soporte, pagos atrasados y uso de la app. Datos simulados con efectos definidos de antemano, lo que permite comprobar que el modelo encuentra los factores correctos.",
        pasos=[
            "Preprocesamiento dentro de un Pipeline (One-Hot y estandarización), para que la partición de prueba no influya en el ajuste.",
            "Partición estratificada 75/25 y validación cruzada de cinco pliegues sobre el entrenamiento.",
            "Comparación de regresión logística y Random Forest. La logística tuvo AUC 0,807 en validación cruzada contra 0,795 del Random Forest.",
            "Importancia por permutación sobre la partición de prueba, para saber en qué variables se apoya el modelo.",
            "Curva de ganancia acumulada y una lista de clientes con probabilidad de baja mayor a 0,6.",
        ],
        resultados=[("Tasa de abandono", "33 %"), ("AUC en prueba (logística)", "0,82"), ("AUC en prueba (Random Forest)", "0,81"),
                    ("Bajas detectadas llamando al 20 % más riesgoso", "42 %"), ("Abandono con contrato mensual", "50 %"),
                    ("Abandono con contrato bianual", "7 %")],
        hallazgos=[
            "El tipo de contrato es el factor de mayor peso, seguido de la antigüedad, los tickets de soporte, los pagos atrasados y el uso de la app.",
            "Ofrecer pasar del contrato mensual al anual con un descuento ataca la causa principal.",
            "El segundo ticket de soporte y el primer pago atrasado sirven como alertas tempranas para llamar al cliente.",
        ],
        codigo_archivo="src/modelo.py", lang="python",
        codigo='''def preprocesador():
    return ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAS),
        ("num", StandardScaler(), NUMERICAS),
    ])

pipe = Pipeline([("prep", preprocesador()),
                 ("clf", LogisticRegression(max_iter=2000))])
cv_auc = cross_val_score(pipe, X_tr, y_tr, cv=cv, scoring="roc_auc")''',
    ),
    dict(
        slug="reporte-financiero-automatizado", carpeta="02-reporte-financiero-automatizado", img="finanzas.jpg",
        titulo="Reporte financiero mensual automatizado en Excel",
        corto="Reporte financiero automatizado",
        pregunta="¿Cómo dejar de armar a mano, cada mes, el estado de resultados para gerencia?",
        tecnica="Python, openpyxl, línea de comandos",
        metrica="1 comando", metrica_label="del CSV contable al Excel final", n="1.302 movimientos",
        resumen="El área contable de una pyme exporta los movimientos del sistema y pasa horas copiando, sumando y dando formato a un Excel. El script hace ese trabajo completo: valida el archivo, calcula el estado de resultados y entrega un Excel con formato y gráficos que se pueden editar.",
        contexto=[
            "En YPFB automaticé tareas parecidas y el ahorro de tiempo fue de alrededor de 30 %. Este proyecto reproduce ese tipo de trabajo con datos públicos de ejemplo.",
        ],
        datos="1.302 movimientos de 2025 (fecha, tipo, cuenta, monto) de una pyme de servicios simulada, con crecimiento mensual de ingresos y campañas de marketing en marzo y septiembre.",
        pasos=[
            "Valida la entrada: si faltan columnas o el tipo de movimiento no es Ingreso o Gasto, se detiene con un mensaje claro.",
            "Calcula ingresos, gastos, resultado y margen por mes, y el estado de resultados por cuenta.",
            "Escribe el Excel con openpyxl: tres hojas, encabezados con color, formato de miles, filtros, paneles inmovilizados y dos gráficos nativos.",
            "Acepta otros archivos por parámetro, así se puede programar para que corra solo cada mes.",
        ],
        resultados=[("Ingresos del año", "$1,21 M"), ("Gastos del año", "$0,80 M"), ("Margen neto", "33,6 %"),
                    ("Margen más bajo", "enero, 21,5 %"), ("Margen más alto", "diciembre, 45,2 %"), ("Peso de sueldos en el gasto", "51 %")],
        hallazgos=[
            "El margen sube durante el año porque los ingresos crecen y los costos fijos se mantienen.",
            "Los picos de gasto de marzo y septiembre coinciden con las campañas de marketing, algo que en el reporte manual pasaba desapercibido.",
        ],
        codigo_archivo="src/generar_reporte.py", lang="bash",
        codigo='''python src/generar_reporte.py \\
    --entrada movimientos_noviembre.csv \\
    --salida reporte_noviembre.xlsx''',
    ),
    dict(
        slug="ventas-retail", carpeta="01-dashboard-ventas-retail", img="ventas.jpg",
        titulo="Ventas y rentabilidad de una cadena retail",
        corto="Ventas y rentabilidad retail",
        pregunta="¿Qué categorías y regiones generan la ganancia y dónde se pierde margen?",
        tecnica="Pandas, Matplotlib",
        metrica="−6 pp", metrica_label="de margen en la región Occidente", n="21.680 transacciones",
        resumen="Una tienda con cuatro categorías y cuatro regiones veía las ventas en planillas separadas. Consolidé las transacciones de un año en un tablero que muestra ventas, ganancia y margen en una sola página.",
        contexto=[
            "Gerencia miraba sobre todo las ventas. Al cruzarlas con la ganancia apareció una región que vende tanto como las demás pero deja menos margen.",
        ],
        datos="21.680 transacciones de 2025 con fecha, categoría, región, unidades, venta y ganancia. Datos simulados con estacionalidad y una región con más descuentos.",
        pasos=[
            "Agregué ventas, ganancia y margen por mes, categoría y región.",
            "Calculé los indicadores principales: ventas, ganancia, margen promedio y ticket promedio.",
            "Los textos del tablero se calculan desde los datos, así se actualizan solos si cambia el archivo.",
        ],
        resultados=[("Ventas", "$8,74 M"), ("Ganancia", "$2,24 M"), ("Margen promedio", "25,6 %"), ("Ticket promedio", "$403"),
                    ("Participación de Tecnología en ventas", "55 %"), ("Margen de Moda", "44 %")],
        hallazgos=[
            "Tecnología vende más, pero Moda deja el mayor margen: conviene darle más visibilidad.",
            "Occidente queda 6 puntos de margen por debajo del resto. Antes de abrir más puntos ahí, hay que revisar descuentos y costos de envío.",
        ],
        codigo_archivo="src/analisis.py", lang="python",
        codigo='''por_reg = df.groupby("region")[["venta", "ganancia"]].sum()
por_reg["margen"] = por_reg.ganancia / por_reg.venta * 100
reg_baja = por_reg.margen.idxmin()
brecha = por_reg.drop(reg_baja).margen.mean() - por_reg.margen.min()''',
    ),
    dict(
        slug="mercado-inmobiliario", carpeta="06-mercado-inmobiliario", img="inmobiliario.jpg",
        titulo="Mercado inmobiliario para inversionistas",
        corto="Mercado inmobiliario",
        pregunta="¿En qué zona conviene invertir según el precio por m² y lo que tarda en venderse una propiedad?",
        tecnica="Pandas, Matplotlib",
        metrica="63 días", metrica_label="en venta en la periferia, frente a menos de 45", n="1.694 publicaciones",
        resumen="Basado en el tipo de trabajo que hice para NORA, una startup inmobiliaria de Colombia: ordenar publicaciones de inmuebles y convertirlas en indicadores para decidir dónde comprar.",
        contexto=[
            "Un inversionista compara cuatro zonas. Le interesan dos cosas: cuánto cuesta entrar y qué tan rápido podría vender si lo necesita.",
        ],
        datos="1.694 publicaciones simuladas de 2025 con zona, tipo de inmueble, superficie, precio por m², precio y días publicada.",
        pasos=[
            "Usé medianas en lugar de promedios, porque unas pocas propiedades de lujo distorsionan el promedio.",
            "Seguí la evolución mensual del precio por m² en cada zona.",
            "Medí la liquidez con los días promedio en venta y comparé precio contra superficie por tipo de inmueble.",
        ],
        resultados=[("Precio mediano por m²", "$1.247"), ("Variación en el año", "+5,1 %"), ("Ticket mediano", "$128.000"),
                    ("Días promedio en venta", "49"), ("Descuento de la periferia por m²", "37 %"), ("Prima de departamentos por m²", "4 %")],
        hallazgos=[
            "Zona Norte y Centro son más caras pero se venden en menos de 45 días: menos riesgo de quedarse con la propiedad.",
            "La periferia cuesta 37 % menos por m² y tarda 63 días en venderse. Sirve más para comprar y alquilar que para revender rápido.",
        ],
        codigo_archivo="src/analisis.py", lang="python",
        codigo='''zonas = df.groupby("zona").agg(
    publicaciones=("precio", "size"),
    precio_m2_mediano=("precio_m2", "median"),
    dias_promedio=("dias_en_venta", "mean"),
)''',
    ),
]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..100,400..800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">')


def head(titulo, desc, raiz=""):
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(titulo)}</title>
<meta name="description" content="{escape(desc)}">
<meta property="og:title" content="{escape(titulo)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:image" content="https://sub-cre.github.io/assets/preview.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{raiz}assets/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="{raiz}style.css?v={VER}">
<script>document.documentElement.classList.add("js")</script>
</head>
<body>
"""


def cabecera(raiz=""):
    return f"""<header class="top">
  <div class="progress" aria-hidden="true"></div>
  <div class="shell top-in">
    <a class="sig" href="{raiz}index.html">Oscar Arnez Loayza</a>
    <nav aria-label="Secciones">
      <a href="{raiz}index.html#trabajo">Trabajo</a>
      <a href="{raiz}index.html#servicios">Servicios</a>
      <a href="{raiz}index.html#experiencia">Experiencia</a>
      <a href="{raiz}index.html#contacto">Contacto</a>
    </nav>
  </div>
</header>
"""


def pie(raiz=""):
    return f"""<footer class="shell foot">
  <span>Oscar Arnez Loayza · Sucre, Bolivia</span>
  <span class="mono">Actualizado en noviembre de 2026</span>
</footer>
<script src="{raiz}site.js?v={VER}" defer></script>
</body>
</html>
"""


def index():
    filas = []
    for p in PROYECTOS:
        filas.append(f"""      <a class="row reveal" href="proyectos/{p['slug']}.html" data-peek="assets/{p['img']}">
        <span class="r-title" style="view-transition-name:t-{p['slug']}">{escape(p['corto'])}<small>{escape(p['pregunta'])}</small></span>
        <span class="r-tech">{escape(p['tecnica'])}</span>
        <span class="r-n mono">{escape(p['n'])}</span>
        <span class="r-metric"><b class="mono">{escape(p['metrica'])}</b><small>{escape(p['metrica_label'])}</small></span>
      </a>""")
    destacado = PROYECTOS[0]
    calidad = [("Nombre", 34.2, 100.0), ("Email", 60.7, 90.2), ("Teléfono", 15.4, 95.2),
               ("Ciudad", 26.4, 100.0), ("Fecha", 42.0, 97.4), ("Monto", 45.7, 100.0)]
    q_rows = "\n".join(
        f'      <div class="q-row" data-antes="{a}" data-despues="{d}"><span class="q-label">{c}</span>'
        f'<span class="q-track"><span class="q-fill" style="--w:{a}%"></span></span>'
        f'<span class="q-val mono">{round(a)} %</span></div>' for c, a, d in calidad)
    html = head("Oscar Arnez Loayza · Analista de datos",
                "Analista de datos en Sucre, Bolivia. Limpieza de bases, reportes automatizados en Excel y Python, SQL, Power BI y modelos predictivos. Trabajo remoto.")
    html += cabecera()
    html += f"""<main class="shell">

<section class="intro">
  <div class="intro-text">
    <p class="role" style="--i:0">Analista de datos <span class="avail">· disponible para nuevos proyectos</span></p>
    <h1 style="--i:1"><span class="ln">Oscar Arnez</span> <span class="ln">Loayza</span></h1>
    <p class="lede" style="--i:2">Ordeno datos que están dispersos entre planillas, sistemas y bases, y los convierto en reportes y tableros que la gente usa para decidir. Trabajo de forma remota con empresas y organizaciones de Latinoamérica y Estados Unidos.</p>
    <p style="--i:3">Antes analicé el mercado inmobiliario para NORA (Colombia), apoyé proyectos de DataKind, una ONG de ciencia de datos de Estados Unidos, y automaticé procesos internos en YPFB. Hoy también enseño Python en Algorithmics.</p>
    <p class="links" style="--i:4"><a class="btn" href="#contacto">Pedir una cotización</a><a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a><a href="{WORKANA}" target="_blank" rel="noopener">Workana</a></p>
  </div>
  <figure class="portrait">
    <img src="assets/oscar.jpg" alt="Foto de Oscar Arnez Loayza" width="640" height="640">
  </figure>
  <div class="clients" style="--i:5"><span class="mono">He trabajado con</span><b>NORA</b><b>DataKind</b><b>YPFB</b><b>Algorithmics</b><b>AWS User Group Sucre</b></div>
  <dl class="facts">
    <div><dt>Base</dt><dd>Sucre, Bolivia · <span class="clock mono" data-clock>GMT−4</span></dd></div>
    <div><dt>Modalidad</dt><dd>Remoto, por proyecto u horas</dd></div>
    <div><dt>Herramientas</dt><dd>Power BI, Excel, Python, SQL, Tableau</dd></div>
    <div><dt>Idiomas</dt><dd>Español nativo, inglés intermedio</dd></div>
  </dl>
  <figure class="sorter ruled" id="sorter">
    <div class="sorter-bar">
      <p class="ledger mono" aria-live="polite"><span>registros <b data-k="reg">2.016</b></span><span>duplicados <b data-k="dup">218</b></span><span>clientes únicos <b data-k="uni">1.798</b></span></p>
      <button type="button" class="replay" id="replay">Repetir</button>
    </div>
    <canvas id="sorter-canvas" aria-label="Animación: puntos desordenados que representan registros se fusionan cuando están duplicados y se ordenan en columnas por ciudad"></canvas>
    <figcaption><span class="mono">Fig. 0</span> Una base de 2.016 registros con duplicados y formatos mezclados, ordenada en 1.798 clientes por ciudad. Cada punto representa 6 clientes. Datos del <a href="proyectos/limpieza-base-clientes.html">proyecto de limpieza</a>.</figcaption>
  </figure>
</section>

<section id="trabajo" class="block">
  <div class="block-head">
    <h2>Trabajo seleccionado</h2>
    <p>Seis proyectos con el código y la documentación completos. Usan datos simulados para poder publicarlos sin exponer información de clientes.</p>
  </div>
  <figure class="quality ruled reveal" id="quality">
    <div class="q-head">
      <p class="q-title">% de registros con cada campo en formato estándar</p>
      <div class="seg" role="group" aria-label="Estado de la base">
        <button type="button" data-state="antes" aria-pressed="true">Base original</button>
        <button type="button" data-state="despues" aria-pressed="false">Después del pipeline</button>
      </div>
    </div>
    <div class="q-rows">
{q_rows}
    </div>
    <figcaption><span class="mono">Fig. 1</span> {escape(destacado['titulo'])}. Promedio de los seis campos: <b class="mono" data-avg>37 %</b>. <a href="proyectos/{destacado['slug']}.html">Ver el caso completo</a>.</figcaption>
  </figure>
  <div class="index ruled" role="list">
    <div class="row head" aria-hidden="true"><span>Proyecto</span><span>Técnica</span><span>Datos</span><span>Resultado</span></div>
{chr(10).join(filas)}
  </div>
</section>

<section id="servicios" class="block">
  <div class="block-head reveal">
    <h2>Servicios</h2>
    <p>Precio cerrado por proyecto. Envíame una muestra de tus datos, sin información sensible, y te respondo en menos de 24 horas con alcance, plazo y precio.</p>
  </div>
  <div class="table-wrap"><table class="services ruled">
    <thead><tr><th scope="col">Servicio</th><th scope="col">Qué recibes</th><th scope="col">Plazo típico</th></tr></thead>
    <tbody>
      <tr class="reveal"><th scope="row">Limpieza y estandarización de bases</th><td>Base sin duplicados, con formatos unificados y un informe de qué se corrigió</td><td class="mono">1–3 días</td></tr>
      <tr class="reveal"><th scope="row">Dashboards en Power BI</th><td>Archivo .pbix con modelo de datos, medidas DAX, filtros y una guía de uso</td><td class="mono">3–7 días</td></tr>
      <tr class="reveal"><th scope="row">Automatización de reportes</th><td>Excel o script de Python que arma el reporte con formato y gráficos en un clic</td><td class="mono">3–7 días</td></tr>
      <tr class="reveal"><th scope="row">Consultas SQL y análisis</th><td>Consultas documentadas y resultados en Excel o Power BI, con una explicación breve</td><td class="mono">2–4 días</td></tr>
      <tr class="reveal"><th scope="row">Análisis y modelos predictivos</th><td>Informe con hallazgos y recomendaciones, y el modelo listo para volver a usar</td><td class="mono">5–10 días</td></tr>
    </tbody>
  </table></div>
  <p class="svc-cta reveal"><a class="btn" href="#contacto">Pedir una cotización</a><span>Respuesta en menos de 24 horas, con alcance, plazo y precio.</span></p>
</section>

<section id="experiencia" class="block">
  <div class="block-head"><h2>Experiencia</h2></div>
  <ol class="cv ruled">
    <li class="reveal"><span class="when mono">2025</span><div><h3>Analista de datos · NORA</h3><p class="where">Startup inmobiliaria, Colombia · remoto · sep–oct 2025</p><p>Dashboards en Power BI para seguir el mercado (35 % más eficiente el monitoreo, 25 % más precisión en proyecciones de inversión) y limpieza de bases que redujo las inconsistencias en 40 %.</p></div></li>
    <li class="reveal"><span class="when mono">2025</span><div><h3>Analista de datos · DataKind</h3><p class="where">ONG de ciencia de datos, Estados Unidos · remoto · mar–jul 2025</p><p>Análisis exploratorio en Python y visualizaciones en Tableau para organizaciones de salud y educación. Presentación de resultados a patrocinadores.</p></div></li>
    <li class="reveal"><span class="when mono">2024</span><div><h3>Analista de datos · YPFB</h3><p class="where">Empresa estatal de hidrocarburos, Bolivia · jul–nov 2024</p><p>Automatización de procesos internos con Excel y Python, con alrededor de 30 % menos tiempo en tareas repetitivas.</p></div></li>
    <li class="reveal"><span class="when mono">2025–hoy</span><div><h3>Instructor de Python · Algorithmics Global</h3><p class="where">Edtech, Emiratos Árabes Unidos · remoto</p><p>Clases en línea de programación, con tasas de finalización superiores al 90 %.</p></div></li>
    <li class="reveal"><span class="when mono">2023–2025</span><div><h3>Instructor y coordinador de adquisiciones · American Space</h3><p class="where">Bolivia</p><p>Comparación de proveedores y cotizaciones, con ahorros de 15 a 20 % en compras.</p></div></li>
  </ol>
  <div class="aside-grid">
    <div><h3>Formación</h3><p>Ingeniería Industrial, Universidad Privada Domingo Savio, 2019–2025.</p></div>
    <div><h3>Certificaciones</h3><p>Google Advanced Data Analytics. Introducción a la Ciencia de Datos (Cisco). Excel intermedio, 93 % en la evaluación de Workana.</p></div>
    <div><h3>Comunidad</h3><p>Líder de AWS Sucre. Expositor en TechConnect Bolivia con la charla «Primeros pasos para convertirse en analista de datos» y en TEDx Sucre.</p></div>
  </div>
</section>

<section id="contacto" class="block contact">
  <div class="block-head"><h2>Contacto</h2></div>
  <p class="contact-line">Si tienes una base que ordenar, un reporte que hoy armas a mano o una pregunta que tus datos deberían responder, escríbeme. Respondo en menos de un día con una propuesta, un plazo y un precio.</p>
  <p class="mail"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
  <p><button type="button" class="copy" data-copy="{EMAIL}">Copiar correo</button></p>
  <p class="links"><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a><a href="{WORKANA}" target="_blank" rel="noopener">Workana</a><a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a></p>
</section>

</main>
"""
    html += pie()
    (SITE / "index.html").write_text(html, encoding="utf-8")


def caso(i, p):
    prev_p = PROYECTOS[i - 1]
    next_p = PROYECTOS[(i + 1) % len(PROYECTOS)]
    pasos = "\n".join(f"      <li>{escape(x)}</li>" for x in p["pasos"])
    res = "\n".join(f"      <tr><th scope=\"row\">{escape(a)}</th><td class=\"mono\">{escape(b)}</td></tr>" for a, b in p["resultados"])
    hall = "\n".join(f"      <li>{escape(x)}</li>" for x in p["hallazgos"])
    ctx = "\n".join(f"    <p>{escape(x)}</p>" for x in p["contexto"])
    html = head(f"{p['corto']} · Oscar Arnez", p["resumen"], raiz="../")
    html += cabecera("../")
    html += f"""<main class="shell case">
  <p class="back"><a href="../index.html#trabajo">← Trabajo seleccionado</a></p>
  <header class="case-head">
    <h1 style="view-transition-name:t-{p['slug']}">{escape(p['titulo'])}</h1>
    <p class="lede">{escape(p['resumen'])}</p>
    <dl class="meta">
      <div><dt>Pregunta</dt><dd>{escape(p['pregunta'])}</dd></div>
      <div><dt>Técnica</dt><dd>{escape(p['tecnica'])}</dd></div>
      <div><dt>Datos</dt><dd>{escape(p['n'])}, simulados</dd></div>
      <div><dt>Código</dt><dd><a href="{REPO}{p['carpeta']}" target="_blank" rel="noopener">{p['carpeta']}</a></dd></div>
    </dl>
  </header>

  <figure class="feature wide zoomable reveal">
    <img src="../assets/{p['img']}" alt="Tablero del proyecto: {escape(p['titulo'])}">
    <figcaption><span class="mono">Fig. 1</span> Tablero generado por el código del proyecto.</figcaption>
  </figure>

  <div class="prose">
    <h2 class="reveal">Contexto</h2>
{ctx}
    <h2 class="reveal">Datos</h2>
    <p>{escape(p['datos'])}</p>
    <h2 class="reveal">Qué hice</h2>
    <ol>
{pasos}
    </ol>
    <h2 class="reveal">Resultados</h2>
    <div class="table-wrap"><table class="ruled">
{res}
    </table></div>
    <h2 class="reveal">Qué recomendaría</h2>
    <ul>
{hall}
    </ul>
    <h2 class="reveal">Extracto del código</h2>
    <p class="code-label mono">{escape(p['codigo_archivo'])}</p>
    <pre><code>{escape(p['codigo'])}</code></pre>
    <p><a href="{REPO}{p['carpeta']}" target="_blank" rel="noopener">Ver el proyecto completo en GitHub</a>, con instrucciones para ejecutarlo.</p>
  </div>

  <nav class="pager" aria-label="Otros proyectos">
    <a href="{prev_p['slug']}.html"><small>Anterior</small>{escape(prev_p['corto'])}</a>
    <a href="{next_p['slug']}.html" class="next"><small>Siguiente</small>{escape(next_p['corto'])}</a>
  </nav>
</main>
"""
    html += pie("../")
    (SITE / "proyectos" / f"{p['slug']}.html").write_text(html, encoding="utf-8")


CSS = """/* Layout: hoja de trabajo de un analista. Columna de lectura a la izquierda, índice de proyectos como tabla,
   figuras con pie numerado. Sin tarjetas ni íconos; la jerarquía la da la tipografía. */
:root{
  --paper:#f7f8f8;      /* gris muy claro con sesgo frío */
  --ink:#14191f;
  --ink-soft:#4b5560;
  --rule:#d9dee2;
  --accent:#1f5fae;     /* azul de los gráficos, solo para enlaces y cifras */
  --tint:#e9eff6;
  --warm:#d0632f;     /* duplicados / estado "antes" */
  --display:"Archivo", "Arial Narrow", system-ui, sans-serif;
  --body:"IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono:"IBM Plex Mono", ui-monospace, "Cascadia Mono", Consolas, monospace;
  color-scheme:light;
}
@media (prefers-color-scheme:dark){
  :root{--paper:#12161b;--ink:#e6eaee;--ink-soft:#a3adb8;--rule:#2a323b;--accent:#7fb0ec;--tint:#1a2533;--warm:#e58a5c;color-scheme:dark}
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:400 17px/1.65 var(--body)}
img{max-width:100%;height:auto;display:block}
a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:3px}
a:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.mono{font-family:var(--mono);font-variant-numeric:tabular-nums}
.shell{max-width:1120px;margin:0 auto;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}

.top{border-bottom:1px solid var(--rule)}
.top-in{display:flex;justify-content:space-between;align-items:center;gap:20px;padding-block:18px}
.sig{font-family:var(--display);font-weight:700;font-stretch:85%;font-size:19px;color:var(--ink);text-decoration:none;letter-spacing:-.01em}
.top nav{display:flex;gap:24px;font-size:15px}
.top nav a{color:var(--ink-soft);text-decoration:none}
.top nav a:hover{color:var(--ink)}

h1,h2,h3{font-family:var(--display);color:var(--ink);text-wrap:balance;margin:0}
h1{font-size:clamp(44px,7vw,84px);line-height:.95;font-weight:800;font-stretch:78%;letter-spacing:-.015em}
h2{font-size:clamp(28px,3.4vw,38px);font-weight:700;font-stretch:82%;line-height:1.05}
h3{font-size:18px;font-weight:650;font-stretch:90%}
p{margin:0}

.intro{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,.7fr);gap:28px 56px;padding-block:64px 56px;align-items:start}
.intro-text{display:grid;gap:18px;max-width:640px}
.role{font-family:var(--mono);font-size:14px;color:var(--accent);letter-spacing:.02em}
.lede{font-size:21px;line-height:1.5;color:var(--ink)}
.intro-text p:not(.lede):not(.role){color:var(--ink-soft)}
.links{display:flex;flex-wrap:wrap;gap:8px 22px;font-weight:500}
.portrait{margin:0;grid-row:span 2}
.portrait img{border-radius:3px;filter:saturate(.9)}
.facts{grid-column:1;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin:12px 0 0;padding-top:20px;border-top:1px solid var(--rule)}
.facts dt{font-family:var(--mono);font-size:12.5px;color:var(--ink-soft);text-transform:uppercase;letter-spacing:.06em}
.facts dd{margin:4px 0 0;font-size:15px}

.block{padding-block:56px;border-top:1px solid var(--rule)}
.block-head{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px;align-items:end;margin-bottom:32px}
.block-head p{color:var(--ink-soft);font-size:15.5px;max-width:460px}

.feature{margin:0 0 36px}
.feature img{border:1px solid var(--rule);border-radius:3px;background:#f4f3ef}
figcaption{font-size:14px;color:var(--ink-soft);margin-top:10px}
figcaption .mono{color:var(--ink);margin-right:6px}

.index{border-top:2px solid var(--ink)}
.row{display:grid;grid-template-columns:minmax(0,2.3fr) minmax(0,1.3fr) minmax(0,.9fr) minmax(0,1.3fr);gap:20px;padding-block:18px;border-bottom:1px solid var(--rule);color:var(--ink);text-decoration:none;align-items:baseline}
.row.head{font-family:var(--mono);font-size:12.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-soft);padding-block:10px}
a.row:hover{background:var(--tint)}
a.row:hover .r-title{color:var(--accent)}
.r-title{font-weight:600;font-size:17px}
.r-title small,.r-metric small{display:block;font-weight:400;font-size:14.5px;color:var(--ink-soft);margin-top:3px;line-height:1.45}
.r-tech{font-size:14.5px;color:var(--ink-soft)}
.r-n{font-size:14px;color:var(--ink-soft)}
.r-metric b{font-size:22px;font-weight:500;color:var(--accent)}

.cv{list-style:none;margin:0;padding:0;border-top:2px solid var(--ink)}
.cv li{display:grid;grid-template-columns:140px minmax(0,1fr);gap:20px;padding-block:20px;border-bottom:1px solid var(--rule)}
.cv .when{font-size:14px;color:var(--ink-soft);padding-top:3px}
.cv .where{font-size:14.5px;color:var(--ink-soft);margin:2px 0 8px}
.cv li div{max-width:720px}
.aside-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px;margin-top:40px}
.aside-grid h3{margin-bottom:6px}
.aside-grid p{font-size:15.5px;color:var(--ink-soft)}

.contact-line{max-width:640px;font-size:19px}
.mail{font-family:var(--display);font-size:clamp(24px,4vw,40px);font-weight:700;font-stretch:82%;margin:18px 0 14px;overflow-wrap:anywhere}
.mail a{text-decoration:none}
.mail a:hover{text-decoration:underline}

.foot{display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;padding-block:28px 40px;border-top:1px solid var(--rule);font-size:14px;color:var(--ink-soft)}

/* casos de estudio */
.case{padding-block:36px 24px}
.back{font-size:15px;margin-bottom:28px}
.back a{text-decoration:none}
.case-head{display:grid;gap:20px;max-width:860px;margin-bottom:40px}
.case h1{font-size:clamp(36px,5.4vw,62px)}
.meta{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;margin:8px 0 0;padding-top:18px;border-top:1px solid var(--rule)}
.meta dt{font-family:var(--mono);font-size:12.5px;color:var(--ink-soft);text-transform:uppercase;letter-spacing:.06em}
.meta dd{margin:4px 0 0;font-size:15px;overflow-wrap:anywhere}
.prose{max-width:700px;display:grid;gap:16px}
.prose h2{font-size:26px;margin-top:22px}
.prose ol,.prose ul{margin:0;padding-left:22px;display:grid;gap:8px}
.table-wrap{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:15.5px;border-top:2px solid var(--ink)}
th,td{text-align:left;padding:10px 0;border-bottom:1px solid var(--rule);vertical-align:top}
th{font-weight:400;color:var(--ink-soft);padding-right:24px}
td{text-align:right;color:var(--ink);font-variant-numeric:tabular-nums}
.code-label{font-size:13px;color:var(--ink-soft);margin-bottom:-8px}
pre{margin:0;overflow-x:auto;background:var(--tint);border-left:3px solid var(--accent);padding:16px 18px;font:400 14px/1.6 var(--mono);color:var(--ink)}
.pager{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:56px;border-top:2px solid var(--ink);padding-top:18px}
.pager a{text-decoration:none;font-weight:600;color:var(--ink)}
.pager a:hover{color:var(--accent)}
.pager small{display:block;font-family:var(--mono);font-weight:400;font-size:12.5px;color:var(--ink-soft);text-transform:uppercase;letter-spacing:.06em}
.pager .next{text-align:right}

@media (max-width:900px){
  .intro{grid-template-columns:1fr;padding-block:40px}
  .portrait{grid-row:auto;max-width:260px;order:-1}
  .facts,.meta{grid-template-columns:repeat(2,minmax(0,1fr))}
  .block-head{grid-template-columns:1fr}
  .row{grid-template-columns:minmax(0,1fr) auto}
  .row.head{display:none}
  .r-tech,.r-n{display:none}
  .r-metric{text-align:right;max-width:170px}
  .aside-grid{grid-template-columns:1fr}
}
@media (max-width:560px){
  body{font-size:16px}
  .top nav{gap:14px;font-size:14px}
  .sig{font-size:16px}
  .row{grid-template-columns:1fr}
  .r-metric{text-align:left;max-width:none}
  .cv li{grid-template-columns:1fr;gap:4px}
  .pager{grid-template-columns:1fr}
  .pager .next{text-align:left}
}
@media (prefers-reduced-motion:no-preference){a.row{transition:background .15s}}

/* barra superior fija con progreso de lectura */
.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:var(--paper)}
.progress{position:absolute;left:0;bottom:-1px;height:2px;width:100%;background:var(--accent);transform-origin:0 50%;transform:scaleX(var(--p,0))}

/* Fig. 0: base desordenada que se ordena */
.sorter{grid-column:1/-1;margin:8px 0 0;border-top:2px solid var(--ink);padding-top:12px}
.sorter-bar{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.ledger{display:flex;flex-wrap:wrap;gap:6px 22px;font-size:13px;color:var(--ink-soft);margin:0}
.ledger b{color:var(--ink);font-weight:500}
.ledger span.on b{color:var(--accent)}
.replay{font:500 13px var(--mono);color:var(--ink-soft);background:none;border:1px solid var(--rule);border-radius:3px;padding:5px 10px;cursor:pointer}
.replay:hover{color:var(--ink);border-color:var(--ink-soft)}
.replay:focus-visible,.seg button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
#sorter-canvas{display:block;width:100%;height:300px;margin-top:10px}

/* Fig. 1: calidad antes / después */
.quality{margin:0 0 40px;border-top:2px solid var(--ink);padding-top:14px}
.q-head{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:14px}
.q-title{font-weight:600}
.seg{display:inline-flex;border:1px solid var(--rule);border-radius:3px;overflow:hidden}
.seg button{font:500 13.5px var(--body);background:none;border:0;padding:7px 12px;color:var(--ink-soft);cursor:pointer}
.seg button+button{border-left:1px solid var(--rule)}
.seg button[aria-pressed="true"]{background:var(--ink);color:var(--paper)}
.q-rows{display:grid;gap:10px}
.q-row{display:grid;grid-template-columns:90px minmax(0,1fr) 64px;gap:14px;align-items:center}
.q-label{font-size:15px;color:var(--ink-soft)}
.q-track{height:14px;background:var(--tint);position:relative}
.q-fill{position:absolute;inset:0 auto 0 0;width:var(--w);background:var(--warm);transition:width .9s cubic-bezier(.65,0,.35,1),background-color .6s}
.quality.done .q-fill{background:var(--accent)}
.q-val{text-align:right;font-size:15px}
.quality figcaption a{white-space:nowrap}
@media (max-width:560px){#sorter-canvas{height:260px}.q-row{grid-template-columns:72px minmax(0,1fr) 52px;gap:10px}}
@media (prefers-reduced-motion:reduce){.q-fill{transition:none}}

/* ===== v3: fondo de papel milimetrado, transiciones y detalles ===== */
:root{--grid:rgba(31,95,174,.055);--grid-major:rgba(31,95,174,.09)}
@media (prefers-color-scheme:dark){:root{--grid:rgba(127,176,236,.045);--grid-major:rgba(127,176,236,.075)}}
body{
  background-color:var(--paper);
  background-image:
    linear-gradient(var(--grid-major) 1px,transparent 1px),
    linear-gradient(90deg,var(--grid-major) 1px,transparent 1px),
    linear-gradient(var(--grid) 1px,transparent 1px),
    linear-gradient(90deg,var(--grid) 1px,transparent 1px);
  background-size:120px 120px,120px 120px,24px 24px,24px 24px;
  background-position:-1px -1px;
}
.top{background:color-mix(in srgb,var(--paper) 88%,transparent);backdrop-filter:blur(8px)}
.top nav a{position:relative}
.top nav a::after{content:"";position:absolute;left:0;right:0;bottom:-4px;height:1px;background:var(--accent);transform:scaleX(0);transform-origin:left;transition:transform .3s}
.top nav a:hover::after{transform:scaleX(1)}

.avail{color:var(--ink-soft)}
.avail::before{content:"";display:inline-block;width:7px;height:7px;border-radius:50%;background:#2fa36b;margin:0 6px 1px 4px;animation:pulse 2.4s ease-in-out infinite}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(47,163,107,.45)}50%{box-shadow:0 0 0 5px rgba(47,163,107,0)}}
h1 .ln{display:inline-block}

.btn{display:inline-flex;align-items:center;gap:8px;background:var(--ink);color:var(--paper);text-decoration:none;padding:10px 16px;border-radius:3px;font-weight:600;position:relative;overflow:hidden}
.btn::after{content:"→";transition:transform .25s}
.btn:hover::after{transform:translateX(4px)}
.btn:hover{background:var(--accent);color:#fff}
.links{align-items:center}

.clients{grid-column:1;display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 18px;padding-top:4px}
.clients .mono{font-size:12.5px;color:var(--ink-soft);text-transform:uppercase;letter-spacing:.06em}
.clients b{font-family:var(--display);font-stretch:85%;font-size:17px;font-weight:700;color:var(--ink-soft);transition:color .2s}
.clients b:hover{color:var(--ink)}
.clock{font-size:14px}

/* reglas que se dibujan como el eje de un gráfico */
.index,.cv,.quality,.sorter,table.ruled,table.services{border-top:0}
.ruled{position:relative}
.ruled::before{content:"";position:absolute;left:0;top:0;height:2px;width:100%;background:var(--ink);transform-origin:left;transition:transform 1.1s cubic-bezier(.65,0,.35,1)}
.js .ruled:not(.in)::before{transform:scaleX(0)}
table.ruled{border-collapse:separate;border-spacing:0}

/* aparición al hacer scroll */
.js .reveal{opacity:0;transform:translateY(18px);transition:opacity .7s ease,transform .7s cubic-bezier(.2,.7,.2,1)}
.js .reveal.in{opacity:1;transform:none}

/* secuencia de entrada del hero */
.js .intro-text>*,.js .clients{animation:rise .8s cubic-bezier(.2,.7,.2,1) both;animation-delay:calc(var(--i,0)*90ms + 80ms)}
.js .portrait img{animation:unveil 1.1s cubic-bezier(.65,0,.35,1) .25s both}
.js .facts{animation:rise .8s cubic-bezier(.2,.7,.2,1) .6s both}
@keyframes rise{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:none}}
@keyframes unveil{from{clip-path:inset(100% 0 0 0);transform:scale(1.06)}to{clip-path:inset(0);transform:none}}

/* servicios */
table.services{font-size:15.5px}
table.services thead th{font-family:var(--mono);font-size:12.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-soft);font-weight:400;padding-top:14px}
table.services tbody th{color:var(--ink);font-weight:600;width:30%;padding-right:24px}
table.services td{text-align:left;color:var(--ink-soft)}
table.services td.mono{white-space:nowrap;color:var(--ink);text-align:right}
table.services tbody tr{transition:background .2s}
table.services tbody tr:hover{background:var(--tint)}
.svc-cta{display:flex;align-items:center;flex-wrap:wrap;gap:12px 18px;margin-top:24px;color:var(--ink-soft);font-size:15px}

/* vista previa del tablero al pasar sobre un proyecto */
.peek{position:fixed;left:0;top:0;width:340px;pointer-events:none;z-index:30;opacity:0;transform:translate(-50%,-50%) scale(.92);transition:opacity .2s,transform .25s;border:1px solid var(--rule);box-shadow:0 18px 40px rgba(0,0,0,.18);background:#f4f3ef}
.peek.on{opacity:1;transform:translate(-50%,-50%) scale(1)}
@media (hover:none),(max-width:900px){.peek{display:none}}
a.row .r-title{transition:color .2s,transform .25s}
a.row:hover .r-title{transform:translateX(4px)}

/* copiar correo */
.copy{font:500 13.5px var(--mono);background:none;border:1px solid var(--rule);color:var(--ink-soft);padding:6px 12px;border-radius:3px;cursor:pointer}
.copy:hover{color:var(--ink);border-color:var(--ink-soft)}
.copy:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

/* figura ampliable en casos de estudio */
.zoomable img{cursor:zoom-in}
.lightbox{position:fixed;inset:0;z-index:50;background:rgba(10,14,18,.86);display:grid;place-items:center;padding:24px;opacity:0;pointer-events:none;transition:opacity .25s}
.lightbox.on{opacity:1;pointer-events:auto;cursor:zoom-out}
.lightbox img{max-width:min(1600px,96vw);max-height:92vh;transform:scale(.96);transition:transform .3s}
.lightbox.on img{transform:none}

/* transiciones entre páginas (navegadores compatibles) */
@view-transition{navigation:auto}
::view-transition-old(root){animation:vt-out .25s ease both}
::view-transition-new(root){animation:vt-in .35s ease both}
@keyframes vt-out{to{opacity:0;transform:translateY(-8px)}}
@keyframes vt-in{from{opacity:0;transform:translateY(10px)}}

@media (prefers-reduced-motion:reduce){
  .js .reveal{opacity:1;transform:none;transition:none}
  .js .intro-text>*,.js .clients,.js .facts,.js .portrait img{animation:none}
  .ruled::before{transition:none}.js .ruled:not(.in)::before{transform:none}
  .avail::before{animation:none}
  @view-transition{navigation:none}
}
@media (max-width:560px){table.services tbody th{width:auto}.clients b{font-size:15px}}
"""

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="4" fill="#14191f"/><path d="M9 23V15M16 23V9M23 23V18" stroke="#7fb0ec" stroke-width="3.2" stroke-linecap="square"/></svg>"""

if __name__ == "__main__":
    (SITE / "proyectos").mkdir(exist_ok=True)
    (SITE / "style.css").write_text(CSS, encoding="utf-8")
    (SITE / "assets" / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    index()
    for i, p in enumerate(PROYECTOS):
        caso(i, p)
    print("ok", len(PROYECTOS), "casos")
