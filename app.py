"""
Aplicación Streamlit para Generación de Actas de Reunión v3.0
Transcripción automática + Notas manuales + Análisis con IA + Documento Word
"""
import streamlit as st
import os
from datetime import datetime
import tempfile
from pathlib import Path

# Importar utilidades
from utils.transcription import transcribe_audio, get_transcription_with_timestamps
from utils.analysis import analyze_with_phi4
from utils.document_gen import generate_word_document, save_document


# Configuración de página
st.set_page_config(
    page_title="Generador de Actas de Reunión",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Función principal de la aplicación"""
    
    # Título principal
    st.title("📝 Generador de Actas de Reunión")
    st.markdown("### Con o sin audio • Análisis con IA • Documento Word profesional")
    st.markdown("---")
    
    # Sidebar con información
    with st.sidebar:
        st.header("ℹ️ Información")
        st.markdown("""
        Esta aplicación te permite:
        
        1. 📋 **Ingresar** datos institucionales
        2. 🎤 **Transcribir** audio O 📝 **Escribir** notas
        3. 🤖 **Analizar** con Phi-4 AI
        4. 📄 **Generar** acta en Word
        
        ### Novedades v3.0:
        - ✨ **Generar actas sin audio**
        - ✨ Solo con notas escritas
        - ✨ Formato institucional
        
        ### Modelos utilizados:
        - **Whisper**: Transcripción (opcional)
        - **Phi-4**: Análisis inteligente
        """)
        
        st.markdown("---")
        
        # Configuración de modelos
        st.header("⚙️ Configuración")
        whisper_model = st.selectbox(
            "Modelo Whisper",
            ["tiny", "base", "small", "medium"],
            index=1,
            help="Solo se usa si subes audio"
        )
        
        include_transcription = st.checkbox(
            "Incluir transcripción/notas en el acta",
            value=False,
            help="Agrega el contenido completo como anexo"
        )
        
        include_timestamps = st.checkbox(
            "Mostrar timestamps (solo audio)",
            value=False,
            help="Muestra tiempos en la transcripción"
        )
    
    # Área principal - 4 pestañas
    tab1, tab2, tab3, tab4 = st.tabs([
        "1️⃣ Información", 
        "2️⃣ Contenido", 
        "3️⃣ Análisis",
        "4️⃣ Generar Acta"
    ])
    
    # ==================== TAB 1: INFORMACIÓN ====================
    with tab1:
        st.header("📋 Información de la Reunión")
        
        col1, col2 = st.columns(2)
        
        with col1:
            meeting_number = st.text_input(
                "Número de Acta *",
                placeholder="Ej: 10"
            )
            
            committee_name = st.text_input(
                "Nombre del Comité *",
                placeholder="Ej: JEIF - Junta de Evaluación"
            )
            
            area_convoca = st.text_input(
                "Área que Convoca *",
                placeholder="Ej: Vicerrectoría de Investigación"
            )
            
            meeting_date = st.date_input(
                "Fecha de Realización *",
                value=datetime.now()
            )
        
        with col2:
            start_time = st.time_input(
                "Hora de Inicio *",
                value=datetime.now().replace(hour=14, minute=0)
            )
            
            end_time = st.time_input(
                "Hora de Finalización *",
                value=datetime.now().replace(hour=16, minute=0)
            )
            
            meeting_place = st.text_input(
                "Lugar *",
                placeholder="Sala de Juntas / Virtual - Teams"
            )
            
            notetaker = st.text_input(
                "Notas Tomadas Por *",
                placeholder="Ej: María García - Secretaria"
            )
        
        st.markdown("---")
        
        # Asistentes
        st.subheader("👥 Asistentes")
        st.info("💡 Agrega los asistentes uno por uno")
        
        if 'asistentes' not in st.session_state:
            st.session_state.asistentes = []
        
        col_asist1, col_asist2, col_asist3 = st.columns([2, 2, 1])
        
        with col_asist1:
            asistente_nombre = st.text_input(
                "Nombre Completo",
                key="input_nombre",
                placeholder="Dr. Juan Pérez González"
            )
        
        with col_asist2:
            asistente_cargo = st.text_input(
                "Cargo/Rol",
                key="input_cargo",
                placeholder="Director de Departamento"
            )
        
        with col_asist3:
            st.write("")
            st.write("")
            if st.button("➕ Agregar", type="primary"):
                if asistente_nombre and asistente_cargo:
                    st.session_state.asistentes.append({
                        "nombre": asistente_nombre,
                        "cargo": asistente_cargo
                    })
                    st.success(f"✅ Agregado")
                    st.rerun()
                else:
                    st.warning("⚠️ Completa ambos campos")
        
        # Mostrar lista
        if st.session_state.asistentes:
            st.markdown("##### 📋 Lista de Asistentes:")
            for idx, asist in enumerate(st.session_state.asistentes):
                c1, c2, c3 = st.columns([2, 2, 1])
                with c1:
                    st.text(asist["nombre"])
                with c2:
                    st.text(asist["cargo"])
                with c3:
                    if st.button("🗑️", key=f"del_{idx}"):
                        st.session_state.asistentes.pop(idx)
                        st.rerun()
        
        st.markdown("---")
        
        # Agenda
        st.subheader("📝 Agenda")
        agenda = st.text_area(
            "Agenda de la reunión (un punto por línea) *",
            placeholder="1. Aprobación del acta anterior\n2. Presentación de proyectos\n3. Discusión presupuesto\n4. Varios",
            height=120
        )
        
        # Guardar en session state
        st.session_state.meeting_info = {
            "numero_acta": meeting_number,
            "comite": committee_name,
            "area_convoca": area_convoca,
            "fecha": meeting_date.strftime("%d/%m/%Y"),
            "hora_inicio": start_time.strftime("%H:%M"),
            "hora_fin": end_time.strftime("%H:%M"),
            "lugar": meeting_place,
            "notas_por": notetaker,
            "asistentes": st.session_state.asistentes,
            "agenda": agenda
        }
        st.session_state.manual_notes = agenda
    
    # ==================== TAB 2: CONTENIDO ====================
    with tab2:
        st.header("📝 Contenido de la Reunión")
        
        # Selector de método
        method = st.radio(
            "¿Cómo quieres registrar el contenido?",
            ["🎤 Transcribir audio", "✍️ Escribir notas manualmente"],
            horizontal=True
        )
        
        st.markdown("---")
        
        if method == "🎤 Transcribir audio":
            st.info("""
            📌 **Formatos**: MP3, WAV, M4A, OGG  
            💡 **Tips**: Buena calidad, sin ruido, volumen adecuado
            """)
            
            uploaded_file = st.file_uploader(
                "Archivo de audio",
                type=["mp3", "wav", "m4a", "ogg"]
            )
            
            if uploaded_file:
                st.success(f"✅ {uploaded_file.name}")
                st.audio(uploaded_file)
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🚀 Transcribir", type="primary", use_container_width=True):
                        transcribe_audio_file(uploaded_file, whisper_model, include_timestamps)
            else:
                st.warning("⚠️ Sube un archivo de audio")
        
        else:  # Notas manuales
            st.info("""
            ✍️ **Escribe notas detalladas de la reunión**
            
            💡 **Para mejores resultados incluye**:
            - Qué se discutió en cada punto
            - Decisiones tomadas
            - Quién propuso qué
            - Responsables y fechas límite
            """)
            
            notas_manuales = st.text_area(
                "Notas de la reunión *",
                placeholder="""Ejemplo:

**Punto 1 - Aprobación del acta anterior:**
Se presentó el acta No. 9. El Dr. Pérez solicitó corregir la fecha del proyecto X. Se aprobó por unanimidad con la corrección.

**Punto 2 - Presentación de proyectos:**
La Dra. García presentó "Sistema de IA para análisis de datos". Presupuesto: $50,000. 

Discusión sobre:
- Viabilidad técnica
- Cronograma 
- Recursos necesarios

Decisión: Aprobar condicionado a cronograma detallado en próxima reunión.

**Punto 3 - Tareas asignadas:**
- Dr. Pérez: Revisar propuesta técnica → 15/03/2024
- Dra. García: Cronograma detallado → 10/03/2024
- Ing. Martínez: Evaluar costos → 12/03/2024

Próxima reunión: 20/03/2024
""",
                height=450,
                key="notas_text"
            )
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("✅ Usar estas notas", type="primary", use_container_width=True):
                    if notas_manuales and len(notas_manuales.strip()) >= 50:
                        st.session_state.transcription = notas_manuales
                        st.session_state.transcription_display = notas_manuales
                        st.session_state.using_manual_notes = True
                        st.success("✅ ¡Notas guardadas!")
                        st.balloons()
                        st.info("👉 Continúa en 'Análisis'")
                    else:
                        st.error("⚠️ Escribe al menos 50 caracteres")
    
    # ==================== TAB 3: ANÁLISIS ====================
    with tab3:
        st.header("🤖 Análisis con IA")
        
        if 'transcription' in st.session_state and st.session_state.transcription:
            
            # Indicar el origen
            if st.session_state.get('using_manual_notes'):
                st.success("📝 Usando notas escritas manualmente")
            else:
                st.success("🎤 Usando transcripción de audio")
            
            # Mostrar contenido
            with st.expander("📄 Ver Contenido Completo", expanded=False):
                st.text_area(
                    "Contenido",
                    value=st.session_state.transcription_display,
                    height=300,
                    disabled=True
                )
            
            st.markdown("---")
            
            # Botón analizar
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔍 Analizar con Phi-4", type="primary", use_container_width=True):
                    analyze_meeting()
            
            # Mostrar resultado
            if 'analysis' in st.session_state and st.session_state.analysis:
                display_analysis(st.session_state.analysis)
        
        else:
            st.info("ℹ️ Primero ingresa el contenido en la pestaña anterior (audio o notas)")
    
    # ==================== TAB 4: GENERAR ACTA ====================
    with tab4:
        st.header("📄 Generar Acta en Word")
        
        if 'analysis' in st.session_state and st.session_state.analysis:
            
            st.success("✅ Análisis completado")
            
            # Vista previa
            st.markdown("### 📋 El acta incluirá:")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                - ✓ Encabezado institucional
                - ✓ Información completa
                - ✓ Lista de asistentes
                - ✓ Agenda
                """)
            
            with col2:
                st.markdown(f"""
                - ✓ Desarrollo de la reunión
                - ✓ Decisiones tomadas
                - ✓ Tareas y responsables
                {f"- ✓ Contenido completo (anexo)" if include_transcription else ""}
                """)
            
            st.markdown("---")
            
            # Generar
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("📥 Generar Acta", type="primary", use_container_width=True):
                    generate_acta(include_transcription)
        
        else:
            st.info("ℹ️ Primero completa el análisis en la pestaña anterior")


def transcribe_audio_file(uploaded_file, model_size, show_timestamps):
    """Transcribe el archivo de audio"""
    
    with st.spinner("🎤 Transcribiendo... Puede tardar unos minutos"):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            
            result = transcribe_audio(tmp_path, model_size=model_size, language="es")
            os.unlink(tmp_path)
            
            if result:
                st.session_state.transcription = result["text"]
                
                if show_timestamps and result.get("segments"):
                    st.session_state.transcription_display = get_transcription_with_timestamps(result["segments"])
                else:
                    st.session_state.transcription_display = result["text"]
                
                st.session_state.using_manual_notes = False
                st.success("✅ ¡Transcripción completada!")
                st.balloons()
                st.info("👉 Continúa en 'Análisis'")
            else:
                st.error("❌ Error al transcribir")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def analyze_meeting():
    """Analiza el contenido con Phi-4"""
    
    with st.spinner("🤖 Analizando... Esto puede tardar varios minutos"):
        try:
            transcription = st.session_state.transcription
            manual_notes = st.session_state.get('manual_notes', '')
            
            analysis = analyze_with_phi4(transcription, manual_notes)
            
            if analysis:
                st.session_state.analysis = analysis
                st.success("✅ ¡Análisis completado!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Error al analizar")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def display_analysis(analysis):
    """Muestra el análisis"""
    
    st.markdown("---")
    st.markdown("### 📊 Resultado del Análisis")
    
    if analysis.get("desarrollo"):
        st.markdown("#### 📝 Desarrollo")
        st.info(analysis["desarrollo"])
    
    if analysis.get("decisiones"):
        st.markdown("#### ✅ Decisiones")
        for d in analysis["decisiones"]:
            st.markdown(f"- {d}")
    
    if analysis.get("tareas"):
        st.markdown("#### 📋 Tareas")
        for t in analysis["tareas"]:
            st.markdown(f"- {t}")
    
    if analysis.get("proximos_pasos"):
        st.markdown("#### 🎯 Próximos Pasos")
        for p in analysis["proximos_pasos"]:
            st.markdown(f"- {p}")


def generate_acta(include_content):
    """Genera el documento Word"""
    
    with st.spinner("📄 Generando documento..."):
        try:
            analysis = st.session_state.analysis
            meeting_info = st.session_state.meeting_info
            content = st.session_state.transcription if include_content else ""
            
            doc = generate_word_document(analysis, meeting_info, content)
            
            if doc:
                numero = meeting_info.get('numero_acta', '0')
                fecha = meeting_info.get('fecha', 'reunion').replace('/', '-')
                filename = f"Acta_No_{numero}_{fecha}.docx"
                filepath = save_document(doc, filename)
                
                if filepath:
                    with open(filepath, "rb") as file:
                        st.download_button(
                            label="📥 Descargar Acta",
                            data=file,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            type="primary",
                            use_container_width=True
                        )
                    
                    st.success("✅ ¡Acta generada!")
                    st.balloons()
                    os.unlink(filepath)
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
