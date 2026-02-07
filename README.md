# 📝 Generador de Actas de Reunión - Versión 3.0

**¡Ahora puedes generar actas SIN audio!** Solo con notas escritas.

## 🆕 Novedades v3.0

### ✨ Generar actas sin audio
- **Nueva opción**: Escribir notas manualmente
- Ya no es obligatorio subir un archivo de audio
- Perfecto para reuniones donde no tienes grabación
- El análisis funciona igual de bien

### 🔧 Requirements.txt mejorado
- Sin conflictos de versiones
- Usa `>=` en lugar de `==` para flexibilidad
- Compatible con despliegue en línea (Streamlit Cloud, Hugging Face)
- Instalación más robusta

### 📋 Formato institucional completo
- Número de acta
- Información del comité
- Asistentes con cargos
- Agenda
- Desarrollo narrativo
- Decisiones y tareas

## 🚀 Instalación

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt
```

## 📖 Uso

### Opción A: Con Audio 🎤

1. **Información**: Completa datos de la reunión
2. **Contenido**: Selecciona "Transcribir audio" → Sube MP3/WAV
3. **Análisis**: Click en "Analizar con Phi-4"
4. **Generar**: Descarga el acta en Word

### Opción B: Sin Audio (Solo Notas) ✍️

1. **Información**: Completa datos de la reunión
2. **Contenido**: Selecciona "Escribir notas" → Escribe detalles
3. **Análisis**: Click en "Analizar con Phi-4"
4. **Generar**: Descarga el acta en Word

## 💡 Tips para Notas Manuales

Para obtener los mejores resultados al escribir notas:

```
✅ BUENO:

Punto 1 - Aprobación del acta:
Se presentó el acta No. 9. El Dr. Pérez solicitó 
corregir la fecha del proyecto X. Se aprobó por 
unanimidad.

Punto 2 - Nuevos proyectos:
La Dra. García presentó "Sistema de IA". 
Presupuesto: $50,000. Se discutió viabilidad 
técnica y cronograma.

Decisión: Aprobar condicionado a presentar 
cronograma detallado.

Tareas:
- Dr. Pérez: Revisar propuesta → 15/03/2024
- Dra. García: Cronograma → 10/03/2024

❌ MALO:

Se habló de cosas. Pérez dijo algo. Aprobado.
```

**Incluye**:
- Qué se discutió
- Quién dijo qué (si es relevante)
- Decisiones tomadas
- Responsables de tareas
- Fechas límite

## 📦 Dependencias

El nuevo `requirements.txt` usa rangos de versiones:

```
streamlit>=1.31.0      # No 1.31.0 exacto
torch>=2.0.0           # Cualquier versión 2.x
transformers>=4.36.0   # Compatible con actualizaciones
```

**Ventajas**:
- ✅ Más flexible
- ✅ Menos conflictos
- ✅ Actualización automática de parches de seguridad
- ✅ Compatible con plataformas en la nube

## 🌐 Despliegue en Línea

### Streamlit Cloud (Gratis)

1. Sube tu proyecto a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repositorio
4. Despliega

**Nota**: Phi-4 es pesado. Para producción considera usar APIs.

### Hugging Face Spaces

1. Crea un Space en [huggingface.co/spaces](https://huggingface.co/spaces)
2. Sube los archivos
3. Selecciona hardware con GPU (de pago)

## ⚙️ Configuración Opcional

### Usar modelo más ligero

Edita `utils/analysis.py` línea 17:

```python
# Cambiar:
model_name = "microsoft/Phi-4-multimodal-instruct"

# Por:
model_name = "microsoft/phi-2"  # Más ligero
```

### Usar Claude API (más rápido)

Si tienes API key de Anthropic, podemos crear una versión que use Claude API en lugar de Phi-4 local. Será mucho más rápido.

## 🐛 Solución de Problemas

### "ModuleNotFoundError: No module named 'X'"

```bash
pip install X
```

O reinstala todo:

```bash
pip install -r requirements.txt
```

### Phi-4 muy lento

**Causas**:
- Modelo pesado (~14GB)
- Sin GPU
- Poca RAM

**Soluciones**:
1. Usa modelo más ligero (phi-2)
2. Usa Claude API
3. Añade más RAM
4. Usa GPU

### Error de versiones

```bash
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

## 📁 Estructura del Proyecto

```
actas-reunion-v3/
├── app.py                 # App principal (con notas manuales)
├── requirements.txt       # Dependencias flexibles
├── utils/
│   ├── __init__.py
│   ├── transcription.py   # Whisper
│   ├── analysis.py        # Phi-4
│   └── document_gen.py    # Word
└── .streamlit/
    └── config.toml
```

## 🎯 Casos de Uso

### 1. Reunión grabada
✅ Usa transcripción de audio

### 2. Reunión sin grabación
✅ Escribe notas durante la reunión
✅ Genera acta profesional después

### 3. Acta de reunión pasada
✅ Reconstruye el acta con tus notas
✅ Formato institucional automático

### 4. Múltiples formatos
✅ Combina agenda + notas + transcripción
✅ Flexibilidad total

## 💻 Requisitos del Sistema

**Mínimo**:
- Python 3.8+
- 8GB RAM
- 10GB disco

**Recomendado**:
- Python 3.10+
- 16GB RAM
- GPU 8GB VRAM
- 20GB disco

## 📞 Soporte

**Problemas comunes resueltos en el README** ☝️

**¿Necesitas ayuda?**
- Revisa la sección "Solución de Problemas"
- Verifica que todas las dependencias estén instaladas
- Asegúrate de que el entorno virtual esté activado

## 🔄 Actualizar desde v2.0

Si ya tienes la v2.0 instalada:

```bash
# Actualizar archivos
# Copia app.py y requirements.txt nuevos

# Reinstalar dependencias
pip install -r requirements.txt --upgrade
```

## ⭐ Características Destacadas

- ✅ **Sin audio requerido** - Nueva opción
- ✅ **Formato institucional** - Profesional
- ✅ **Gestión de asistentes** - Dinámica
- ✅ **Análisis con IA** - Inteligente
- ✅ **Exportación Word** - Descarga directa
- ✅ **Flexible** - Audio o notas

---

**Versión**: 3.0  
**Fecha**: Febrero 2025  
**Licencia**: MIT

¿Te fue útil? ⭐ Dale una estrella en GitHub!
