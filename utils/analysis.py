"""
Módulo para análisis de texto usando Phi-4 multimodal
"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import streamlit as st


@st.cache_resource
def load_phi4_model():
    """
    Carga el modelo Phi-4 multimodal
    
    Returns:
        tuple: (model, tokenizer)
    """
    try:
        model_name = "microsoft/Phi-4-multimodal-instruct"
        
        # Cargar tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )
        
        # Cargar modelo
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            torch_dtype="auto",
            device_map="auto"
        )
        
        return model, tokenizer
        
    except Exception as e:
        st.error(f"Error al cargar Phi-4: {str(e)}")
        return None, None


def analyze_with_phi4(transcription, manual_notes=""):
    """
    Analiza la transcripción y notas usando Phi-4
    
    Args:
        transcription: Texto de la transcripción
        manual_notes: Notas manuales (opcional)
        
    Returns:
        dict: Análisis estructurado de la reunión
    """
    try:
        model, tokenizer = load_phi4_model()
        if model is None or tokenizer is None:
            return None
        
        # Crear el prompt para Phi-4
        prompt = create_analysis_prompt(transcription, manual_notes)
        
        # Generar análisis
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=8000)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=2000,
                temperature=0.7,
                top_p=0.9,
                do_sample=True
            )
        
        analysis = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extraer solo la respuesta (después del prompt)
        if prompt in analysis:
            analysis = analysis.replace(prompt, "").strip()
        
        return parse_analysis(analysis)
        
    except Exception as e:
        st.error(f"Error en análisis: {str(e)}")
        return None


def create_analysis_prompt(transcription, manual_notes):
    """
    Crea el prompt para el análisis
    
    Args:
        transcription: Transcripción del audio
        manual_notes: Agenda de la reunión
        
    Returns:
        str: Prompt formateado
    """
    prompt = f"""Eres un asistente experto en análisis de reuniones institucionales. Analiza la siguiente transcripción de una reunión y genera un acta estructurada basándote en la agenda proporcionada.

TRANSCRIPCIÓN DE LA REUNIÓN:
{transcription}
"""
    
    if manual_notes:
        prompt += f"""
AGENDA DE LA REUNIÓN:
{manual_notes}
"""
    
    prompt += """
INSTRUCCIONES:
Genera un análisis estructurado profesional que incluya:

1. DESARROLLO DE LA REUNIÓN:
   - Narrativa coherente y profesional de cómo se desarrolló la reunión
   - Debe seguir el orden de la agenda
   - Incluir discusiones principales, argumentos y puntos de vista presentados
   - Escrito en tercera persona
   - Mínimo 3-4 párrafos bien estructurados

2. DECISIONES TOMADAS:
   - Lista clara de cada decisión acordada durante la reunión
   - Ser específico y concreto
   - Incluir el contexto de cada decisión

3. TAREAS Y RESPONSABLES:
   - Formato: Descripción de la tarea | Responsable | Fecha límite
   - Ejemplo: "Elaborar informe técnico | Ing. Juan Pérez | 15/03/2024"
   - Ser específico con nombres completos y fechas exactas

4. PRÓXIMOS PASOS:
   - Acciones futuras o seguimiento requerido
   - Fecha de próxima reunión si se mencionó

IMPORTANTE:
- Usa lenguaje formal y profesional
- Sé preciso y objetivo
- No inventes información que no esté en la transcripción
- Si algo no está claro, indícalo brevemente

Responde SOLO con el análisis estructurado:
"""
    
    return prompt


def parse_analysis(analysis_text):
    """
    Parsea el análisis en secciones estructuradas
    
    Args:
        analysis_text: Texto del análisis generado
        
    Returns:
        dict: Análisis estructurado por secciones
    """
    sections = {
        "desarrollo": "",
        "decisiones": [],
        "tareas": [],
        "proximos_pasos": []
    }
    
    try:
        # Dividir por secciones
        lines = analysis_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if "DESARROLLO" in line.upper():
                current_section = "desarrollo"
            elif "DECISIONES" in line.upper():
                current_section = "decisiones"
            elif "TAREAS" in line.upper():
                current_section = "tareas"
            elif "PRÓXIMOS PASOS" in line.upper() or "PROXIMOS PASOS" in line.upper():
                current_section = "proximos_pasos"
            elif line and current_section:
                if current_section == "desarrollo":
                    sections["desarrollo"] += line + " "
                elif line.startswith("-") or line.startswith("•") or line.startswith("*"):
                    item = line.lstrip("-•* ").strip()
                    if item:
                        sections[current_section].append(item)
        
        # Limpiar desarrollo
        sections["desarrollo"] = sections["desarrollo"].strip()
        
        return sections
        
    except Exception as e:
        st.warning(f"Advertencia al parsear análisis: {str(e)}")
        # Retornar análisis sin estructurar
        return {
            "desarrollo": analysis_text,
            "decisiones": [],
            "tareas": [],
            "proximos_pasos": []
        }
