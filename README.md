# Proyecto 3 - Bases de Datos 

Jean Pierre Sotomayor Cavero   100%

Angel Mucha Huaman             100%

Juan Torres                    100%

## Introducción




### Extracción de características
Para este proyecto, es escencial tener las caracteristicas de una canciones, ya que con esto podemos reconocer canciones parecidas gracias los siguientes caractersiticas:  
#### MFCC (Coeficientes Cepstrales de Frecuencia Mel)
Representa la forma en que el oído humano percibe diferentes frecuencias.  
Se calculan 20 coeficientes de MFCC a partir de la señal de audio, estos sirven para captura características fundamentales de la señal relacionadas con la percepción auditiva.  

```python
        chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
```
        sirve para extraer la intensidad de las notas musicasles dentro de una cancion.
       
