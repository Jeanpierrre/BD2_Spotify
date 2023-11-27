# Proyecto 3 - Bases de Datos 

Jean Pierre Sotomayor Cavero   100%

Angel Mucha Huaman             100%

Juan Torres                    100%

## Introducción




### Extracción de características
Para este proyecto, es escencial tener las caracteristicas de una canciones, ya que con esto podemos reconocer canciones parecidas gracias los siguientes caractersiticas:  
        ```python
        chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
        ```
        sirve para extraer la intensidad de las notas musicasles dentro de una cancion.
        ```python
        chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
        ```
MFCC (Coeficientes Cepstrales de Frecuencia Mel)
se hace el calculo de 20 coeficientes a partir de la señal de audio 
