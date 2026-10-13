import streamlit as st
import os

# 1. Configuración de página para móviles y ordenadores
st.set_page_config(
    page_title="VMP Policial - Asistente de Intervención",
    page_icon="🚔",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Cabecera Visual Moderna (Tarjeta Operativa)
st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        padding: 18px;
        border-radius: 12px 12px 0 0;
        color: white;
        text-align: center;
    ">
        <h2 style="margin: 0; font-size: 1.4rem; color: #ffffff; letter-spacing: 1px;">🚔 POLICÍA LOCAL</h2>
        <p style="margin: 5px 0 0 0; font-size: 0.95rem; color: #93c5fd; font-weight: 600; text-transform: uppercase;">
            Control de Movilidad Urbana y VMP
        </p>
        <div style="margin-top: 10px;">
            <span style="
                background-color: #f59e0b;
                color: #0f172a;
                padding: 4px 12px;
                border-radius: 6px;
                font-size: 0.85rem;
                font-weight: 800;
                letter-spacing: 1px;
                display: inline-block;
            ">M0647CAM</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Cargar la imagen del patinete si existe en el directorio
if os.path.exists("patipoli.jpg"):
    st.image("patipoli.jpg", use_container_width=True)
elif os.path.exists("patipoli.jpeg"):
    st.image("patipoli.jpeg", use_container_width=True)

st.info("📱 **Uso en Vía Pública**: Selecciona las características detectadas en la intervención para obtener el desglose de denuncias e inmovilización.")

denuncias = []
requiere_inmovilizacion = False
motivos_inmovilizacion = []

# --- BLOQUE 1: CARACTERÍSTICAS TÉCNICAS Y PRESTACIONES ---
st.subheader("1. Características Técnicas del Vehículo")

velocidad_max = st.number_input("Velocidad máxima constatada / medida (km/h):", min_value=0.0, max_value=120.0, value=25.0, step=1.0)
trucado = st.checkbox("¿Manipulado / Deslimitado / Menú oculto P0(8) / Botón / Interruptor?")
sillin_sin_autoeq = st.checkbox("¿Dispone de asiento o sillín SIN sistema de autoequilibrado?")

es_juguete = velocidad_max < 6.0
exceso_prestaciones = velocidad_max > 25.0 or trucado or sillin_sin_autoeq

if es_juguete:
    st.warning("⚠️ **Categoría**: JUGUETE (Directiva 2009/48/CE). No considerado VMP.")
elif exceso_prestaciones:
    st.error("🚨 **RESULTADO TÉCNICO**: VEHÍCULO NO AUTORIZABLE POR EXCESO DE PRESTACIONES / TRUCAJE.")
    denuncias.append({
        "concepto": "Circular con vehículo no autorizable que ofrece prestaciones superiores a VMP sin homologación",
        "codigo_dgt": "Opción 1.1.5B (Instrucción 2019/S-149)",
        "cuantía": "500 €",
        "reducido": "250 €",
        "inmoviliza": "SÍ"
    })
    requiere_inmovilizacion = True
    motivos_inmovilizacion.append("Vehículo no autorizable (Exceso de velocidad / Manipulado / Sillín no permitido).")

# --- BLOQUE 2: CERTIFICACIÓN Y REGISTRO DGT ---
st.markdown("---")
st.subheader("2. Certificación y Registro DGT")

fecha_comercializacion = st.radio(
    "Fecha de comercialización del vehículo:",
    ["Hasta el 21/01/2024 (Régimen Transitorio hasta 2027)", "A partir del 22/01/2024 (Certificación Obligatoria)"]
)

if "A partir del 22/01/2024" in fecha_comercializacion:
    tiene_certificado = st.checkbox("¿Cuenta con Certificado de Circulación DGT?", value=True)
    tiene_registro = st.checkbox("¿Está inscrito en el Registro de Vehículos Ligeros?", value=True)
    tiene_etiqueta = st.checkbox("¿Exhibe la Etiqueta Identificativa (Placa DGT)?", value=True)

    if not tiene_certificado:
        denuncias.append({
            "concepto": "No disponer de certificado de circulación obligatorio para VMP (comercializado tras 22/01/2024)",
            "codigo_dgt": "VEH 22 B-2-5A",
            "cuantía": "200 €",
            "reducido": "100 €",
            "inmoviliza": "NO"
        })
    if not tiene_registro:
        denuncias.append({
            "concepto": "No inscribir el VMP en el Registro Nacional de Vehículos Ligeros",
            "codigo_dgt": "VEH 22 B-2-5B",
            "cuantía": "100 €",
            "reducido": "50 €",
            "inmoviliza": "NO"
        })
    if not tiene_etiqueta:
        denuncias.append({
            "concepto": "No disponer o no exhibir la etiqueta identificativa (placa) de la DGT",
            "codigo_dgt": "VEH 22 B-2-5C",
            "cuantía": "80 €",
            "reducido": "40 €",
            "inmoviliza": "NO"
        })
else:
    st.success("✅ VMP antiguo (hasta 21/01/2024): Exento de certificado obligatorio hasta el 22/01/2027.")
    tiene_certificado, tiene_registro, tiene_etiqueta = False, False, False

# --- BLOQUE 3: SEGURO OBLIGATORIO (Ley 5/2025 y SAC 2026/13) ---
st.markdown("---")
st.subheader("3. Requisitos de Seguro Obligatorio")

peso_mom = st.number_input("Masa en Orden de Marcha - MOM (kg):", min_value=0.0, max_value=150.0, value=20.0, step=1.0)
estado_seguro = st.selectbox("Estado del Seguro de Responsabilidad Civil:", ["Con Seguro Vigente", "Circular Sin Seguro", "Carecer de Seguro"])

if estado_seguro != "Con Seguro Vigente":
    if peso_mom > 25.0 and velocidad_max > 14.0:
        if estado_seguro == "Circular Sin Seguro":
            denuncias.append({
                "concepto": "Circular sin seguro obligatorio (VMP > 25 kg asimilado a vehículo a motor)",
                "codigo_dgt": "SDA 5N (Art. 1 bis Ley RC)",
                "cuantía": "800 €",
                "reducido": "400 €",
                "inmoviliza": "SÍ"
            })
        else:
            denuncias.append({
                "concepto": "Carecer de seguro obligatorio (VMP > 25 kg asimilado a vehículo a motor)",
                "codigo_dgt": "SDA 5O (Art. 1 bis Ley RC)",
                "cuantía": "610 €",
                "reducido": "305 €",
                "inmoviliza": "SÍ"
            })
        requiere_inmovilizacion = True
        motivos_inmovilizacion.append("Falta de Seguro Obligatorio en VMP > 25 kg.")
    else:
        if tiene_certificado and tiene_registro and tiene_etiqueta:
            if estado_seguro == "Circular Sin Seguro":
                denuncias.append({
                    "concepto": "Circular sin seguro obligatorio (VPL < 25 kg registrado)",
                    "codigo_dgt": "SDA 5A",
                    "cuantía": "300 €",
                    "reducido": "150 €",
                    "inmoviliza": "SÍ"
                })
            else:
                denuncias.append({
                    "concepto": "Carecer de seguro obligatorio (VPL < 25 kg registrado)",
                    "codigo_dgt": "SDA 5B",
                    "cuantía": "200 €",
                    "reducido": "100 €",
                    "inmoviliza": "SÍ"
                })
            requiere_inmovilizacion = True
            motivos_inmovilizacion.append("Falta de Seguro Obligatorio en VPL registrado.")
        else:
            st.warning("ℹ️ **Exento de denuncia de seguro**: Al no cumplir la triple certificación/registro previa, no procede denuncia por Ley de Seguro (Instrucción SAC 2026/13).")

# --- BLOQUE 4: INFRACCIONES DE CIRCULACIÓN (RD 518/2026 / SANC 2026/27) ---
st.markdown("---")
st.subheader("4. Conducta del Conductor (Codificación SANC 2026/27)")

infracciones_conducta = st.multiselect(
    "Selecciona infracciones observadas en la intervención:",
    [
        "Conductor menor de 15 años de edad (CIR 155 3 5A)",
        "Sin Casco de protección homologado o mal abrochado (CIR 118 3 5D)",
        "Sin prenda/elemento luminoso o reflectante visible a 150m de noche (CIR 118 3 5E)",
        "Circular por Vía Interurbana, Travesía o Túnel prohibido (CIR 038 4 5B)",
        "Circular sin alumbrado obligatorio (CIR 155 5 5A)",
        "Circular por la acera o zona peatonal (CIR 152 1 5A / CIR 121.5)",
        "Uso de Teléfono Móvil o Auriculares conectados (CIR 018 2 5C)",
        "Transportar a un segundo pasajero en VMP monoplaza (CIR 012 2 5A)",
        "Conducción bajo efectos del Alcohol (Positivo general o menor Tasa 0.0)",
        "Conducción bajo efectos de Drogas / Negativa a someterse a pruebas"
    ]
)

for inf in infracciones_conducta:
    if "menor de 15 años" in inf:
        denuncias.append({
            "concepto": "Conducir un vehículo de movilidad personal un menor de 15 años",
            "codigo_dgt": "CIR 155 3 5A (Art. 155.3 RGCir)",
            "cuantía": "200 €",
            "reducido": "100 €",
            "inmoviliza": "NO"
        })
    elif "Sin Casco" in inf:
        denuncias.append({
            "concepto": "Conducir VMP sin utilizar adecuadamente abrochado el casco de protección homologado",
            "codigo_dgt": "CIR 118 3 5D (Art. 118.3 RGCir)",
            "cuantía": "200 €",
            "reducido": "100 €",
            "inmoviliza": "NO"
        })
    elif "reflectante" in inf:
        denuncias.append({
            "concepto": "Conducir VMP de noche o baja visibilidad sin elemento luminoso o reflectante (150m)",
            "codigo_dgt": "CIR 118 3 5E (Art. 118.3 RGCir)",
            "cuantía": "200 €",
            "reducido": "100 €",
            "inmoviliza": "NO"
        })
    elif "Vía Interurbana" in inf:
        denuncias.append({
            "concepto": "Circular con VMP por lugar prohibido (travesía, vía interurbana, túnel urbano)",
            "codigo_dgt": "CIR 038 4 5B (Art. 38.4 RGCir)",
            "cuantía": "200 €",
            "reducido": "100 €",
            "inmoviliza": "NO"
        })
    elif "sin alumbrado" in inf:
        denuncias.append({
            "concepto": "Circular con VMP sin llevar encendido el alumbrado obligatorio",
            "codigo_dgt": "CIR 155 5 5A (Art. 155.5 RGCir)",
            "cuantía": "200 €",
            "reducido": "100 €",
            "inmoviliza": "NO"
        })
    elif "acera" in inf:
        denuncias.append({
            "concepto": "Circular con VMP por la acera o zona peatonal prohibida",
            "codigo_dgt": "CIR 152 1 5A / Art. 121.5 RGCir",
            "cuantía": "200 €",
            "reducido": "100 €",
            "inmoviliza": "NO"
        })
    elif "Móvil" in inf:
        denuncias.append({
            "concepto": "Conducir VMP utilizando auriculares o sosteniendo manualmente el teléfono móvil",
            "codigo_dgt": "CIR 018 2 5C (Art. 18.2 RGCir)",
            "cuantía": "200 €",
            "reducido": "100 €",
            "inmoviliza": "NO"
        })
    elif "pasajero" in inf:
        denuncias.append({
            "concepto": "Circular 2 personas en VMP cuya capacidad autorizada es de 1 sola plaza",
            "codigo_dgt": "CIR 012 2 5A (Art. 9.1 RGCir)",
            "cuantía": "100 €",
            "reducido": "50 €",
            "inmoviliza": "NO"
        })
    elif "Alcohol" in inf:
        denuncias.append({
            "concepto": "Conducir VMP con tasa de alcohol superior a la permitida (Tasa 0.0 en menores)",
            "codigo_dgt": "RGCIR 20.1 / LSV 14.1",
            "cuantía": "500 € / 1.000 €",
            "reducido": "250 € / 500 €",
            "inmoviliza": "SÍ"
        })
        requiere_inmovilizacion = True
        motivos_inmovilizacion.append("Conductor bajo los efectos del alcohol.")
    elif "Drogas" in inf:
        denuncias.append({
            "concepto": "Conducir VMP con presencia de drogas o negativa a efectuar las pruebas",
            "codigo_dgt": "LSV 14.1.5.A / LSV 14.2.5.A",
            "cuantía": "1.000 €",
            "reducido": "500 €",
            "inmoviliza": "SÍ"
        })
        requiere_inmovilizacion = True
        motivos_inmovilizacion.append("Conductor bajo los efectos de drogas o negativa.")

# --- BLOQUE 5: RESULTADO DE LA INTERVENCIÓN Y ACTA ---
st.markdown("---")
st.header("📋 Resultado de la Intervención")

if requiere_inmovilizacion:
    st.error("⛔ **PROCEDE LA INMOVILIZACIÓN Y TRASLADO AL DEPÓSITO MUNICIPAL**")
    st.write("**Motivos de inmovilización:**")
    for mot in motivos_inmovilizacion:
        st.write(f"- {mot}")
else:
    st.success("🟢 **NO PROCEDE INMOVILIZACIÓN DEL VEHÍCULO**")

if denuncias:
    st.subheader(f"Infracciones Registradas ({len(denuncias)}):")
    resumen_texto = "ACTA DE INTERVENCIÓN VMP - POLICÍA LOCAL (M0647CAM)\n"
    resumen_texto += f"Inmovilización: {'SÍ' if requiere_inmovilizacion else 'NO'}\n\n"

    for idx, d in enumerate(denuncias, 1):
        with st.expander(f"#{idx} [{d['codigo_dgt']}] - {d['cuantía']}"):
            st.write(f"**Concepto**: {d['concepto']}")
            st.write(f"**Código DGT**: `{d['codigo_dgt']}`")
            st.write(f"**Cuantía Íntegra**: {d['cuantía']}")
            st.write(f"**Cuantía Reducida (50%)**: {d['reducido']}")
            st.write(f"**Inmovilización**: {d['inmoviliza']}")
        
        resumen_texto += f"#{idx} Código: {d['codigo_dgt']}\nConcepto: {d['concepto']}\nCuantía: {d['cuantía']} (Reducida: {d['reducido']})\n\n"

    st.text_area("📋 Resumen para copiar/pegar en aviso o atestado:", value=resumen_texto, height=180)
else:
    st.info("👌 No se han registrado infracciones con los datos seleccionados.")
