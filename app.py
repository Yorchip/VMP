import streamlit as st
import os

# 1. Configuración de página para móviles
st.set_page_config(
    page_title="VMP Policial - Asistente de Intervención",
    page_icon="🚔",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Cabecera Visual Moderna
st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        padding: 14px;
        border-radius: 12px 12px 0 0;
        color: white;
        text-align: center;
    ">
        <h3 style="margin: 0; font-size: 1.3rem; color: #ffffff; letter-spacing: 1px;">🚔 POLICÍA LOCAL</h3>
        <p style="margin: 3px 0 0 0; font-size: 0.90rem; color: #93c5fd; font-weight: 600; text-transform: uppercase;">
            Control de Movilidad Urbana y VMP
        </p>
        <div style="margin-top: 6px;">
            <span style="
                background-color: #f59e0b;
                color: #0f172a;
                padding: 3px 10px;
                border-radius: 6px;
                font-size: 0.80rem;
                font-weight: 800;
                letter-spacing: 1px;
                display: inline-block;
            ">M0647CAM</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Imagen del patinete a tamaño completo
if os.path.exists("patipoli.jpg"):
    st.image("patipoli.jpg", use_container_width=True)
elif os.path.exists("patipoli.jpeg"):
    st.image("patipoli.jpeg", use_container_width=True)

st.info("📱 **Uso en Vía Pública**: Selecciona los parámetros detectados para obtener denuncias e inmovilización de forma automática.")

denuncias = []
requiere_inmovilizacion = False
motivos_inmovilizacion = []
observaciones_penales = []

# --- BLOQUE 1: CARACTERÍSTICAS TÉCNICAS Y VELOCIDAD ---
st.subheader("1. Características Técnicas del Vehículo")

velocidad_max = st.number_input("Velocidad máxima constatada / medida / declarada (km/h):", min_value=0.0, max_value=120.0, value=25.0, step=1.0)

# COMPROBACIÓN DE JUGUETE (<= 6 km/h)
if velocidad_max <= 6.0:
    st.warning("🧸 **CATEGORÍA: JUGUETE** (Directiva 2009/48/CE / RD 1205/2011).")
    st.error("❌ **NO ES UN VMP NI UN VPL**. El artefacto no supera la velocidad mínima de 6 km/h por diseño.")
    st.info("ℹ️ **FIN DE LA EVALUACIÓN**: Al tratarse de un juguete, no requiere ningún trámite ni autorización de tráfico (exento de seguro obligatorio, inscripción RNV, certificado DGT, matrícula, etiqueta y edad mínima).")
    st.stop()  # Finaliza la evaluación inmediatamente

trucado = st.checkbox("¿Manipulado / Deslimitado / Menú oculto P0(8) / Botón / Interruptor / App?")
sillin_sin_autoeq = st.checkbox("¿Dispone de asiento o sillín SIN sistema de autoequilibrado?")

es_ciclo_motor_l1ea = False
tiene_acelerador_directo = False
tiene_pedales = False

if sillin_sin_autoeq:
    tiene_pedales = st.checkbox("¿Dispone de pedales de tracción humana?")
    if tiene_pedales:
        potencia_gt_250w = st.checkbox("¿La potencia nominal continua supera los 250 W (hasta 1.000 W)?")
        funciona_sin_pedalear = st.checkbox("¿Dispone de gatillo / acelerador directo (el motor funciona sin necesidad de pedalear)?")
        
        # CASO 1: EPAC / Pedelec Estándar (<= 250W, sin acelerador directo, corte a <= 25 km/h)
        if not potencia_gt_250w and not funciona_sin_pedalear and velocidad_max <= 25.0:
            st.success("🚲 **CATEGORÍA DETERMINADA: BICICLETA DE PEDALEO ASISTIDO (EPAC / Pedelec - Norma UNE-EN 15194)**")
            st.markdown("""
            * **Definición**: Bicicleta equipada con motor auxiliar de potencia nominal continua ≤ 250 W, cuya asistencia se interrumpe a los 25 km/h o si se deja de pedalear.
            * **Régimen Legal**: Se rige por las normas aplicables a **bicicletas convencionales** (Reglamento General de Circulación).
            * **Exenciones Absolutas**: **NO es un VMP ni un vehículo a motor**. Al igual que una bicicleta convencional, **no requiere nada más** (exenta de Certificado VMP, inscripción RNV, matrícula/etiqueta, seguro obligatorio y permiso de conducir).
            """)
            st.info("ℹ️ **FIN DE LA EVALUACIÓN**: Al ser una EPAC/bicicleta convencional, no se continúa con preguntas de VMP/VPL.")
            st.stop()  # Parada inmediata para EPAC

        # CASO 2: Ciclo de Motor (Categoría L1e-A) (> 250W a 1000W, sin acelerador directo, asistencia <= 25 km/h)
        elif potencia_gt_250w and not funciona_sin_pedalear and velocidad_max <= 25.0:
            es_ciclo_motor_l1ea = True
            st.warning("🛵 **CATEGORÍA DETERMINADA: CICLO DE MOTOR (Categoría L1e-A - Reglamento UE 168/2013)**")
            st.markdown("""
            * **Definición**: Ciclo diseñado para pedalear equipado con propulsión auxiliar de potencia nominal continua > 250 W y ≤ 1.000 W, cuyo corte de asistencia se produce a ≤ 25 km/h.
            * **Requisitos Legales**:
              1. **Matrícula**: **SÍ EXIGE MATRÍCULA** (placa amarilla de ciclomotor).
              2. **Seguro**: **SÍ EXIGE SEGURO** de Responsabilidad Civil (cuantía no reflejada expresamente en el codificado de la DGT para VMP).
              3. **Permiso de Conducir**: **NO REQUIERE PERMISO DE CONDUCIR DE NINGÚN TIPO** (a diferencia de los ciclomotores L1e-B).
            * **Homologación**: Requiere homologación de tipo europea como vehículo Categoría L1e-A.
            """)
            st.info("ℹ️ **FIN DE LA EVALUACIÓN**: Al determinarse como Ciclo de Motor (L1e-A), no se continúa con preguntas de VMP/VPL.")
            st.stop()  # Parada inmediata para Ciclo de Motor
        else:
            if funciona_sin_pedalear:
                tiene_acelerador_directo = True
                st.warning("⚠️ **Pérdida de categoría EPAC / L1e-A**: Al disponer de acelerador directo/gatillo que acciona el motor sin necesidad de pedalear, excede la categoría de bicicleta asistida.")

# Evaluación de Exceso de Prestaciones / Ciclomotor / Trucaje
exceso_prestaciones = velocidad_max > 25.0 or trucado or (sillin_sin_autoeq and not es_ciclo_motor_l1ea)

if exceso_prestaciones:
    es_ciclomotor = velocidad_max <= 45.0
    tipo_vehiculo_asimilado = "CICLOMOTOR (Categoría L1e-B)" if es_ciclomotor else "MOTOCICLETA (Categoría L3e)"
    permiso_requerido = "AM" if es_ciclomotor else "A1 / A2 / A"

    if trucado:
        # VMP MANIPULADO / TRUCADO: SÍ CONTINUAMOS LAS PREGUNTAS DE VMP/VPL
        st.error("🚨 **RESULTADO TÉCNICO: VMP MANIPULADO / TRUCADO (EXCEDE LA NORMA)**")
        st.markdown(f"""
        * **Situación**: Se trata de un VMP que ha sido **deslimitado, trucado o manipulado** (mediante menú oculto, botón, interruptor o app).
        * **Sanción por Manipulación**: Denuncia por circular con vehículo no autorizable / manipulado que ofrece prestaciones superiores a VMP (**Opción 1.1.5B - 500 € + Inmovilización**).
        * **Equiparación a Ciclomotor**: Al exceder la norma por trucaje, proceden las denuncias de ciclomotor / vehículo a motor que correspondan:
          - Carecer de Certificado de Circulación / Homologación de Ciclomotor.
          - Carecer de Matrícula.
          - Carecer de Seguro Obligatorio.
          - Carecer de Permiso de Conducir clase {permiso_requerido} (y posible vía penal por Art. 384 CP).
        * **Continuación del Asistente**: **Se continúa con las preguntas de Certificado, Registro RNV y Pegatina**, ya que el vehículo podría estar legalmente inscrito y disponer de tarjeta/etiqueta VMP a pesar de haber sido trucado.
        """)
        
        denuncias.append({
            "concepto": "Circular con vehículo no autorizable que ofrece prestaciones superiores a VMP por trucaje/manipulación",
            "codigo_dgt": "Opción 1.1.5B (Instrucción 2019/S-149)",
            "cuantía": "500 €",
            "reducido": "250 €",
            "inmoviliza": "SÍ"
        })
        requiere_inmovilizacion = True
        motivos_inmovilizacion.append("Vehículo no autorizable (VMP manipulado / deslimitado / trucado).")

        observaciones_penales.append(
            f"OBSERVACIÓN TÉCNICA / PENAL: VMP manipulado/trucado (Velocidad: {velocidad_max} km/h). Equiparable a {tipo_vehiculo_asimilado}. Proceden denuncias por carecer de certificado/homologación de ciclomotor, matrícula, seguro obligatorio y permiso de conducir clase {permiso_requerido}. De carecer de permiso, se requiere medición en dinamómetro e informe pericial para atestado por Art. 384 CP."
        )
    else:
        # CICLOMOTOR / MOTOCICLETA DE ORIGEN (NO TRUCADO): NO SE CONTINÚA CON PREGUNTAS VMP/VPL
        st.error(f"🚨 **CATEGORÍA DETERMINADA: {tipo_vehiculo_asimilado} (NO VMP)**")
        st.markdown(f"""
        * **Situación**: Por sus características de fabricación (asiento/sillín {'con acelerador directo' if tiene_acelerador_directo else ''} o velocidad por diseño > 25 km/h), el vehículo no es un VMP, sino un **{tipo_vehiculo_asimilado}**.
        * **Denuncias que proceden como Ciclomotor / Vehículo a Motor**:
          1. **Vehículo No Autorizable / Sin Homologación**: Opción 1.1.5B (500 € + Inmovilización).
          2. **Carecer de Certificado de Circulación / Homologación de Ciclomotor**.
          3. **Carecer de Matrícula** (placa amarilla).
          4. **Carecer de Seguro Obligatorio** de vehículos a motor (SDA).
          5. **Carecer de Permiso de Conducir** clase {permiso_requerido}.
        * **Vía Penal (Art. 384 CP)**: Si el conductor carece de permiso, proceden diligencias/atestado por Delito contra la Seguridad Vial (exige informe pericial técnico y medición en dinamómetro certificado).
        """)

        denuncias.append({
            "concepto": f"Circular con vehículo no autorizable como VMP / equipado como {tipo_vehiculo_asimilado} sin homologación",
            "codigo_dgt": "Opción 1.1.5B (Instrucción 2019/S-149)",
            "cuantía": "500 €",
            "reducido": "250 €",
            "inmoviliza": "SÍ"
        })
        denuncias.append({
            "concepto": f"Carecer de Permiso de Conducir de la clase {permiso_requerido} exigible para {tipo_vehiculo_asimilado}",
            "codigo_dgt": "LSV 61 1 5A",
            "cuantía": "500 €",
            "reducido": "250 €",
            "inmoviliza": "SÍ"
        })
        requiere_inmovilizacion = True
        motivos_inmovilizacion.append(f"Vehículo equipado como {tipo_vehiculo_asimilado} sin homologar y falta de autorización.")

        observaciones_penales.append(
            f"OBSERVACIÓN PENAL / TÉCNICA: Vehículo fabricado como {tipo_vehiculo_asimilado} no VMP. Proceden denuncias por carecer de certificado de circulación, matrícula, seguro obligatorio y permiso de conducir clase {permiso_requerido}. De carecer de permiso, se instruyen diligencias por Art. 384 CP con medición en dinamómetro."
        )

        # Mostrar resultado final e inmovilización para Ciclomotor no trucado, y NO seguir con VMP/VPL
        st.markdown("---")
        st.header("📋 Resultado de la Intervención")
        st.error("⛔ **PROCEDE LA INMOVILIZACIÓN Y TRASLADO AL DEPÓSITO MUNICIPAL**")
        for mot in motivos_inmovilizacion:
            st.write(f"- {mot}")

        st.subheader(f"Infracciones e Incidencias Registradas ({len(denuncias)}):")
        resumen_texto = "ACTA DE INTERVENCIÓN - VEHÍCULO EQUIPARADO A CICLOMOTOR (M0647CAM)\nInmovilización: SÍ\n\n"
        for idx, d in enumerate(denuncias, 1):
            with st.expander(f"#{idx} [{d['codigo_dgt']}] - {d['cuantía']}"):
                st.write(f"**Concepto**: {d['concepto']}")
                st.write(f"**Código DGT**: `{d['codigo_dgt']}`")
                st.write(f"**Cuantía Íntegra**: {d['cuantía']}")
                st.write(f"**Cuantía Reducida (50%)**: {d['reducido']}")
                st.write(f"**Inmovilización**: {d['inmoviliza']}")
            resumen_texto += f"#{idx} Código: {d['codigo_dgt']}\nConcepto: {d['concepto']}\nCuantía: {d['cuantía']} (Reducida: {d['reducido']})\n\n"

        resumen_texto += "--- DILIGENCIAS / OBSERVACIONES EN MATERIA PENAL / TÉCNICA ---\n"
        for obs in observaciones_penales:
            st.warning(obs)
            resumen_texto += f"{obs}\n\n"

        st.text_area("📋 Resumen para copiar/pegar en aviso o atestado:", value=resumen_texto, height=220)
        st.stop()  # No seguir con preguntas de VMP/VPL

# --- BLOQUE 2: CERTIFICACIÓN Y REGISTRO DGT ---
st.markdown("---")
st.subheader("2. Certificación y Registro DGT")

fecha_comercializacion = st.radio(
    "Fecha de comercialización del vehículo:",
    ["Hasta el 21/01/2024 (Régimen Transitorio hasta 22/01/2027)", "A partir del 22/01/2024 (Certificación Obligatoria)"]
)

es_posterior_2024 = "A partir del 22/01/2024" in fecha_comercializacion

if es_posterior_2024:
    st.caption("ℹ️ *Vehículo posterior a 22/01/2024: Evalúa Certificado, Registro RNV y Etiqueta DGT.*")
    tiene_certificado = st.checkbox("¿Tiene Certificado de Circulación DGT?", value=True)
    tiene_registro = st.checkbox("¿Inscrito en el Registro de Vehículos Ligeros (RNV)?", value=True)
    tiene_etiqueta = st.checkbox("¿Exhibe la Etiqueta Identificativa (Placa DGT)?", value=True)

    # Inconsistencia lógica registral
    if not tiene_certificado and tiene_registro:
        st.warning("⚠️ **Aviso de inconsistencia registral**: Un VMP comercializado tras el 22/01/2024 no puede estar oficialmente inscrito en el RNV si carece de Certificado DGT. Se aplicará la sanción matriz por carecer de certificado (VEH 22 B-2-5A).")

    # Evaluación de jerarquía (absorción administrativa de infracciones)
    if not tiene_certificado:
        denuncias.append({
            "concepto": "No disponer de certificado de circulación obligatorio para VMP (comercializado tras 22/01/2024)",
            "codigo_dgt": "VEH 22 B-2-5A",
            "cuantía": "200 €",
            "reducido": "100 €",
            "inmoviliza": "NO"
        })
    elif not tiene_registro:
        denuncias.append({
            "concepto": "No inscribir el VMP en el Registro Nacional de Vehículos Ligeros",
            "codigo_dgt": "VEH 22 B-2-5B",
            "cuantía": "100 €",
            "reducido": "50 €",
            "inmoviliza": "NO"
        })
    elif not tiene_etiqueta:
        denuncias.append({
            "concepto": "No disponer o no exhibir la etiqueta identificativa (placa) de la DGT en VMP inscrito",
            "codigo_dgt": "VEH 22 B-2-5C",
            "cuantía": "80 €",
            "reducido": "40 €",
            "inmoviliza": "NO"
        })
else:
    st.caption("✅ *Vehículo anterior a 22/01/2024: La inscripción otorga Certificado Provisional DGT y placa Serie 'B'.*")
    tiene_registro = st.checkbox("¿Inscrito en el Registro de Vehículos Ligeros (RNV)?", value=False)
    tiene_etiqueta = st.checkbox("¿Exhibe la Etiqueta Identificativa (Placa Serie 'B')?", value=False)
    
    # La inscripción previa a 2024 otorga el certificado provisional DGT
    tiene_certificado = tiene_registro

    # Evaluación de jerarquía para pre-2024
    if not tiene_registro:
        denuncias.append({
            "concepto": "No inscribir el VMP en el Registro Nacional de Vehículos Ligeros",
            "codigo_dgt": "VEH 22 B-2-5B",
            "cuantía": "100 €",
            "reducido": "50 €",
            "inmoviliza": "NO"
        })
    elif not tiene_etiqueta:
        denuncias.append({
            "concepto": "No disponer o no exhibir la etiqueta identificativa (placa Serie 'B') en VMP inscrito",
            "codigo_dgt": "VEH 22 B-2-5C",
            "cuantía": "80 €",
            "reducido": "40 €",
            "inmoviliza": "NO"
        })

# Detección de incidencia penal: Exhibe pegatina imitando la DGT pero NO figura en RNV
if not tiene_registro and tiene_etiqueta:
    st.error("🚨 **ALERTA DE SEGURIDAD / INCIDENCIA DOCUMENTAL**: El vehículo exhibe pegatina identificativa pero NO consta inscrito en el RNV.")
    observaciones_penales.append(
        "OBSERVACIÓN PENAL: El vehículo exhibe etiqueta identificativa imitando la oficial de la DGT sin constar alta ni registro en el RNV. Proceden diligencias informativas / atestado por presunto Delito de Falsedad Documental (Arts. 392/393 del Código Penal) con intervención cautelar del distintivo."
    )

# --- BLOQUE 3: SEGURO OBLIGATORIO ---
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
        cumple_triple_requisito = tiene_certificado and tiene_registro and tiene_etiqueta

        if cumple_triple_requisito:
            if estado_seguro == "Circular Sin Seguro":
                denuncias.append({
                    "concepto": "Circular sin seguro obligatorio (VPL registrado con Placa DGT/Serie B)",
                    "codigo_dgt": "SDA 5A",
                    "cuantía": "300 €",
                    "reducido": "150 €",
                    "inmoviliza": "SÍ"
                })
            else:
                denuncias.append({
                    "concepto": "Carecer de seguro obligatorio (VPL registrado con Placa DGT/Serie B)",
                    "codigo_dgt": "SDA 5B",
                    "cuantía": "200 €",
                    "reducido": "100 €",
                    "inmoviliza": "SÍ"
                })
            requiere_inmovilizacion = True
            motivos_inmovilizacion.append("Falta de Seguro Obligatorio en VPL registrado y matriculado.")
        else:
            st.warning("ℹ️ **Exento de denuncia de seguro**: Según la Instrucción SAC 2026/13, la sanción por seguro en VPL (< 25 kg) requiere cumplir simultáneamente los requisitos (Certificado/Provisional + Registro + Etiqueta/Placa 'B'). Al faltar la inscripción o la etiqueta, NO procede sancionar por seguro.")

# --- BLOQUE 4: INFRACCIONES DE CIRCULACIÓN Y EQUIPAMIENTO TÉCNICO ---
st.markdown("---")
st.subheader("4. Conducta del Conductor y Equipamiento Técnico (Anexo XXI RGVeh / SANC 2026/27)")

st.warning("💡 **Aviso de Vacatio Legis (Alumbrado)**: La obligación de llevar siempre encendido el alumbrado a todas horas (día y noche) del RD 518/2026 **entrará en vigor el 1 de octubre de 2027**. Actualmente solo es obligatorio de noche, en túneles o con escasa visibilidad.")

infracciones_conducta = st.multiselect(
    "Selecciona infracciones u anomalías observadas en la intervención:",
    [
        "Fallo / Deficiencia en Sistema de Frenado (Anexo XXI - VEH 22 B-2-5E)",
        "Carecer o no funcionar Timbre / Dispositivo sonoro o Pata de Cabra (Anexo XXI - VEH 22 B-2-5F)",
        "Conductor menor de 15 años de edad (CIR 155 3 5A)",
        "Sin Casco de protección homologado o mal abrochado (Art. 104.1.c LTSV / CIR 118 3 5D)",
        "Sin prenda/elemento luminoso o reflectante visible a 150m de noche (CIR 118 3 5E)",
        "Circular por Vía Interurbana, Travesía o Túnel prohibido (CIR 038 4 5B)",
        "Circular de noche/túnel sin alumbrado obligatorio (CIR 155 5 5A)",
        "Circular por la acera o zona peatonal (CIR 152 1 5A / CIR 121.5)",
        "Uso de Teléfono Móvil o Auriculares conectados (CIR 018 2 5C)",
        "Transportar a un segundo pasajero en VMP monoplaza (CIR 012 2 5A)",
        "Conducción bajo efectos del Alcohol (Positivo general o menor Tasa 0.0)",
        "Conducción bajo efectos de Drogas / Negativa a someterse a pruebas"
    ]
)

for inf in infracciones_conducta:
    if "Sistema de Frenado" in inf:
        denuncias.append({
            "concepto": "Circular con VMP que presenta deficiencias graves o ineficacia total en el sistema de frenado (Anexo XXI RGVeh)",
            "codigo_dgt": "VEH 22 B-2-5E",
            "cuantía": "200 €",
            "reducido": "100 €",
            "inmoviliza": "SÍ"
        })
        requiere_inmovilizacion = True
        motivos_inmovilizacion.append("Deficiencia grave en la seguridad activa (Fallo total o grave en el sistema de frenado).")
    elif "Timbre" in inf:
        denuncias.append({
            "concepto": "Carecer de dispositivo sonoro (timbre) o sistema de estabilización (pata de cabra) exigido en el Anexo XXI del RGVeh",
            "codigo_dgt": "VEH 22 B-2-5F",
            "cuantía": "80 €",
            "reducido": "40 €",
            "inmoviliza": "NO"
        })
    elif "menor de 15 años" in inf:
        denuncias.append({
            "concepto": "Conducir un vehículo de movilidad personal un menor de 15 años",
            "codigo_dgt": "CIR 155 3 5A (Art. 155.3 RGCir)",
            "cuantía": "200 €",
            "reducido": "100 €",
            "inmoviliza": "NO"
        })
    elif "Sin Casco" in inf:
        denuncias.append({
            "concepto": "Conducir VMP sin utilizar adecuadamente abrochado el casco de protección homologado o certificado",
            "codigo_dgt": "CIR 118 3 5D (Art. 118.3 RGCir)",
            "cuantía": "200 €",
            "reducido": "100 €",
            "inmoviliza": "SÍ"
        })
        requiere_inmovilizacion = True
        motivos_inmovilizacion.append("Conducir VMP sin casco de protección obligatorio (Art. 104.1.c LTSV).")
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
            "concepto": "Circular con VMP sin llevar encendido el alumbrado obligatorio (noche/túnel)",
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

# --- BLOQUE 5: RESULTADO DE LA INTERVENCIÓN ---
st.markdown("---")
st.header("📋 Resultado de la Intervención")

if requiere_inmovilizacion:
    st.error("⛔ **PROCEDE LA INMOVILIZACIÓN Y TRASLADO AL DEPÓSITO MUNICIPAL**")
    for mot in motivos_inmovilizacion:
        st.write(f"- {mot}")
else:
    st.success("🟢 **NO PROCEDE INMOVILIZACIÓN DEL VEHÍCULO**")

if denuncias or observaciones_penales:
    st.subheader(f"Infracciones e Incidencias Registradas ({len(denuncias)}):")
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

    if observaciones_penales:
        resumen_texto += "--- DILIGENCIAS / OBSERVACIONES EN MATERIA PENAL / TÉCNICA ---\n"
        for obs in observaciones_penales:
            st.warning(obs)
            resumen_texto += f"{obs}\n\n"

    st.text_area("📋 Resumen para copiar/pegar en aviso o atestado:", value=resumen_texto, height=220)
else:
    st.info("👌 No se han registrado infracciones con los datos seleccionados.")
