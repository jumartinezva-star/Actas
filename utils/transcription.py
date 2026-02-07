"""
Módulo para transcripción de audio usando Whisper
"""
import whisper
import torch
import streamlit as st
from pathlib import Path


@st.cache_resource
def load_whisper_model(model_size="base"):
    """
    Carga el modelo Whisper
    
    Args:
        model_size: Tamaño del modelo (tiny, base, small, medium, large)
        
    Returns:
        Modelo Whisper cargado
    """
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = whisper.load_model(model_size, device=device)
        return model
    except Exception as e:
        st.error(f"Error al cargar Whisper: {str(e)}")
        return None


def transcribe_audio(audio_file_path, model_size="base", language="es"):
    """
    Transcribe un archivo de audio usando Whisper
    
    Args:
        audio_file_path: Ruta al archivo de audio
        model_size: Tamaño del modelo Whisper
        language: Idioma del audio (default: español)
        
    Returns:
        dict: Diccionario con la transcripción y metadatos
    """
    try:
        # Cargar modelo
        model = load_whisper_model(model_size)
        if model is None:
            return None
        
        # Transcribir
        result = model.transcribe(
            str(audio_file_path),
            language=language,
            fp16=torch.cuda.is_available()
        )
        
        return {
            "text": result["text"],
            "segments": result.get("segments", []),
            "language": result.get("language", language)
        }
        
    except Exception as e:
        st.error(f"Error en transcripción: {str(e)}")
        return None


def get_transcription_with_timestamps(segments):
    """
    Formatea la transcripción con timestamps
    
    Args:
        segments: Segmentos de la transcripción con timestamps
        
    Returns:
        str: Transcripción formateada con timestamps
    """
    formatted_text = ""
    for segment in segments:
        start_time = format_timestamp(segment['start'])
        end_time = format_timestamp(segment['end'])
        text = segment['text'].strip()
        formatted_text += f"[{start_time} - {end_time}] {text}\n"
    
    return formatted_text


def format_timestamp(seconds):
    """
    Convierte segundos a formato HH:MM:SS
    
    Args:
        seconds: Tiempo en segundos
        
    Returns:
        str: Timestamp formateado
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"
