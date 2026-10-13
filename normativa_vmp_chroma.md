# Base de Datos de Normativa VMP y Tráfico (DGT) - Preparado para RAG / ChromaDB

## Documento 1: Definición Técnica, Prestaciones y Manipulación de VMP
- **Fuente**: Real Decreto 970/2020, RD 52/2026 (Anexo XXI RGVeh), Instrucción DGT 2019/S-149.
- **Categoría**: Normativa Técnica y Homologación.

### 1.1 Definición Legal de VMP
Un Vehículo de Movilidad Personal (VMP) es un vehículo de una o más ruedas dotado de una única plaza y propulsado exclusivamente por motores eléctricos que proporcionan una velocidad máxima por diseño comprendida entre 6 y 25 km/h. Solo pueden estar equipados con asiento o sillín si están dotados de un sistema de autoequilibrado.
- **Exclusiones**: Vehículos con sillín sin autoequilibrado, vehículos para personas de movilidad reducida, vehículos de competición, vehículos con tensión de trabajo > 100 VCC / 240 VAC, y los incluidos en el Reglamento (UE) nº 168/2013.
- **Juguetes**: Aparatos o vehículos con velocidad máxima por diseño < 6 km/h. Se rigen por la Directiva 2009/48/CE y RD 1205/2011. No son considerados VMP.

### 1.2 Vehículos con Prestaciones Superiores / Deslimitados / Trucados
Cuando un vehículo con apariencia de VMP sobrepasa los 25 km/h de velocidad máxima o presenta modificaciones (deslimitado, interruptor, potenciómetro, menú oculto P08 o P18, desvinculación de controladora):
- **Calificación**: NO es un VMP ni puede ser homologado bajo el Reglamento (UE) nº 168/2013 (al carecer de sillín de plaza completa).
- **Consecuencia legal**: Vehículo no autorizable para circular por las vías públicas.
- **Infracción**: Carecer de autorización administrativa para circular (Opción 1.1.5B).
- **Sanción**: 500 € (250 € con descuento reducido del 50%).
- **Medida Cautelar**: INMOVILIZACIÓN Y DEPÓSITO OBLIGATORIO del vehículo.

### 1.3 Comprobación de Velocidad y Pruebas Operativas
- **Velocímetro policial**: Los agentes pueden constatar la velocidad constante durante tiempo suficiente con el velocímetro del vehículo policial.
- **Prueba de velocidad en parado**: Alzando la rueda tractora con el vehículo en la última marcha y accionando el acelerador a fondo, comprobando el display y realizando fotografía para el informe.

---

## Documento 2: Certificación, Registro y Etiqueta Identificativa DGT
- **Fuente**: Real Decreto 970/2020, Resolución DGT 12/01/2022 (Manual de Características VMP), Anexo XX RGV.
- **Categoría**: Certificación y Régimen Transitorio.

### 2.1 Régimen Transitorio de Comercialización
- **VMP comercializados HASTA el 21/01/2024**: Pueden circular sin certificado de circulación DGT hasta el **22 de enero de 2027**.
- **VMP comercializados A PARTIR del 22/01/2024**: Obligatoriamente deben ser marcas y modelos certificados por la DGT con su correspondiente placa identificativa y certificado de circulación.
- **A partir del 22/01/2027**: Únicamente podrán circular VMP que dispongan de certificado de circulación DGT.

### 2.2 Cuadro Sancionador por Incumplimientos Documentales / Registrales
- **Sin Certificado de Circulación (Post. 22/01/2024)**: Código `VEH 22 B-2-5A`. Multa: 200 € (100 € reducido). Inmovilización: NO.
- **Sin Inscripción en el Registro Nacional de Vehículos**: Código `VEH 22 B-2-5B`. Multa: 100 € (50 € reducido). Inmovilización: NO.
- **Sin Exhibir la Etiqueta Identificativa (Placa DGT)**: Código `VEH 22 B-2-5C`. Multa: 80 € (40 € reducido). Inmovilización: NO.
- **Incumplimiento Muy Grave Anexo XXI (Trucaje/Modificación estructural)**: Código `VEH 22 B-2-5D`. Multa: 500 € (250 € reducido). Inmovilización: SEGÚN CASO.

---

## Documento 3: Seguro Obligatorio de Responsabilidad Civil (Ley 5/2025 y SAC 2026/13)
- **Fuente**: Ley 5/2025 (Art. 1 bis Ley RC), Instrucción SAC 2026/13.
- **Categoría**: Aseguramiento de Vehículos Personales.

### 3.1 Clasificación según Masa en Orden de Marcha (MOM) y Velocidad
- **VMP Pesados / Asimilados a Vehículos a Motor (MOM > 25 kg y Velocidad > 14 km/h)**:
  - Tributan obligatoriamente bajo la Ley de Responsabilidad Civil de Vehículos a Motor.
  - **Circular sin seguro**: Código `SDA 5N` (Art. 1 bis Ley RC). Multa: 800 € (400 € reducido). **Inmovilización: SÍ**.
  - **Carecer de seguro**: Código `SDA 5O` (Art. 1 bis Ley RC). Multa: 610 € (305 € reducido). **Inmovilización: SÍ**.
- **Vehículos Personales Ligeros - VPL (MOM < 25 kg y Velocidad ≤ 25 km/h)**:
  - **Con Certificación, Registro y Etiqueta**:
    - Circular sin seguro: Código `SDA 5A`. Multa: 300 € (150 € reducido). **Inmovilización: SÍ**.
    - Carecer de seguro: Código `SDA 5B`. Multa: 200 € (100 € reducido). **Inmovilización: SÍ**.
  - **Sin Certificación o Registro previo**: EXENTO de denuncia por seguro (Instrucción SAC 2026/13). Se denuncian únicamente las infracciones técnicas.

---

## Documento 4: Infracciones de Circulación y Conductor (RD 518/2026 e Instrucción SANC 2026/27)
- **Fuente**: Real Decreto 518/2026, Instrucción SANC 2026/27 (En vigor desde 01/10/2026).
- **Categoría**: Normas de Circulación y Codificación DGT.

### 4.1 Códigos Codificados Oficiales de Infracción (RGCir y LSV)
- **Edad mínima (Menor de 15 años conduciendo VMP)**:
  - Código DGT: `CIR 155 3 5A` (Art. 155.3 RGCir).
  - Sanción: 200 € (100 € reducido). Inmovilización: NO.
- **Conducir VMP sin Casco Homologado o mal abrochado**:
  - Código DGT: `CIR 118 3 5D` (Art. 118.3 RGCir).
  - Sanción: 200 € (100 € reducido). Inmovilización: NO.
- **Sin prenda/elemento luminoso o reflectante a 150m (Ocaso / Noche / Escasa visibilidad)**:
  - Código DGT: `CIR 118 3 5E` (Art. 118.3 RGCir).
  - Sanción: 200 € (100 € reducido). Inmovilización: NO.
- **Circular sin Alumbrado encendido**:
  - Código DGT: `CIR 155 5 5A` (Art. 155.5 RGCir - Obligatoriedad de encendido).
  - Sanción: 200 € (100 € reducido). Inmovilización: NO.
- **Circular por lugar prohibido (Travesía, Vía Interurbana, Túnel Urbano, Autovía/Autopista)**:
  - Código DGT: `CIR 038 4 5B` (Art. 38.4 RGCir) / `LSV 020 1 5A`.
  - Sanción: 200 € (100 € reducido). Inmovilización: NO.
- **Circular por la Acera o Zona Peatonal**:
  - Código DGT: `CIR 152 1 5A` / Art. 121.5 RGCir.
  - Sanción: 100 € - 200 € (50 € - 100 € reducido). Inmovilización: NO.
- **Uso de Teléfono Móvil o Auriculares conectados**:
  - Código DGT: `CIR 018 2 5C` (Art. 18.2 RGCir).
  - Sanción: 200 € (100 € reducido). Inmovilización: NO.
- **Transportar Pasajero en VMP Monoplaza**:
  - Código DGT: `CIR 012 2 5A` (Art. 9.1 RGCir).
  - Sanción: 80 € - 100 € (40 € - 50 € reducido). Inmovilización: NO.
- **Alcoholemia en VMP**:
  - Código DGT: `RGCIR 20.1` / `LSV 14.1`. Tasa 0.0 mg/l obligatoria en menores de edad.
  - Sanción: 500 € a 1.000 € (250 € a 500 € reducido). **Inmovilización: SÍ**.
- **Drogas o Negativa a someterse a Pruebas**:
  - Código DGT: `LSV 14.1.5.A` / `LSV 14.2.5.A`.
  - Sanción: 1.000 € (500 € reducido). **Inmovilización: SÍ**.

---

## Documento 5: Aclaraciones sobre Guantes y Calzado Cerrado
- **Fuente**: Instrucción DGT SANC 2026/25.
- **Categoría**: Equipamiento de Protección e Interpretación Legal.

### 5.1 Calzado Cerrado y Guantes en Motocicletas y Quads
- La obligación de llevar calzado cerrado (que sujete talón y dedos) y guantes en vías interurbanas se aplica a **motocicletas, ciclomotores, triciclos y quads** (Art. 118.1 RGCir).
- **Puntos**: Dichas infracciones **NO conllevan detracción de puntos** en el permiso de discutir.
- **VMP**: Esta exigencia de calzado cerrado / guantes **NO es exigible a conductores de VMP** según la regulación de la Instrucción SANC 2026/25.
