Se quiere evaluar el rendimiento de tres sistemas de almacenamiento en la nube diferentes en términos de velocidad de acceso a los archivos\. Se registraron los tiempos de acceso \(en milisegundos\) para una muestra de 30 archivos en cada sistema\.

a\)       Los tiempos para el Sistema 1 fueron: 15, 16, 14, 17, 15, 16, 16, 17, 14, 15, 16, 14, 17, 15, 16, 16, 17, 14, 15, 16, 14, 17, 15, 16, 16, 17, 14, 15, 16, 14\.

b\)      Los tiempos para el Sistema 2 fueron: 13, 14, 12, 15, 13, 14, 14, 15, 12, 13, 14, 12, 15, 13, 14, 14, 15, 12, 13, 14, 12, 15, 13, 14, 14, 15, 12, 13, 14, 12\.

c\)       Los tiempos para el Sistema 3 fueron: 16, 17, 15, 18, 16, 17, 17, 18, 15, 16, 17, 15, 18, 16, 17, 17, 18, 15, 16, 17, 15, 18, 16, 17, 17, 18, 15, 16, 17, 15\.

Utilice análisis de varianza \(ANOVA\) y determine si hay diferencias significativas en los tiempos de acceso entre los tres sistemas de almacenamiento en la nube\.

Solución:

PASO 1: PLANTEAMIENTO DE HIPOTESIS

Ho: µ1= µ 2= µ 3

H1: Por lo menos dos promedios de tiempos de acceso de los sistemas son diferentes

Paso 2 : Determinar el nivel de significancia:0\.05\(5%\)

Paso 3: Estadísticos descriptivos

Paso 4: Hallar la prueba de normalidad

Ho: los tiempos de acceso en los 3 sistemas presentan distribución normal \( Prueba paramétrica\)

H1: Por lo menos 1 sistema no presenta distribución normal respecto al tiempo de acceso \(\( Prueba no paramétrica\)

Teorema del limite Central :

El TLC dice que, si tomamos muchas muestras aleatorias de una población con cualquier distribución \(no necesariamente normal\) y calculamos sus medias, la distribución de esas medias se acercará a una distribución normal a medida que el tamaño de la muestra aumente \(n = 30, generalmente\)\.

En palabras simples:

No importa cómo sea la población original \(asimétrica, rara, lo que sea\)\.

Si tomás muchas muestras grandes y sacás el promedio de cada una\.\.\.

Esos promedios se distribuirán como una campana \(normal\)\.

Dado que el tamaño de muestra es mayor o igual a 30 muestras por sistema y aplicando el teorema del limite central, se podría deducir que las muestras presentan distribución normal\.

\( cuando veas mayor o igual a 30 el valor gl, ya no vemos el valor SIG\. Ya que por teorema presenta distribución normal\.\) \( OJIIIITO\)

Cuando hagamos nuestra tesis debemos usar tamaños de muestra mayores a 30 para aplicar pruebas paramatricas \)\.

Paso 5: Prueba de homegeniedad de varianzas\.

Ho: las varianzas de los sistemas son iguales \(TUKEY\)

H1: Por los menos la varianza de 2 grupos de sistemas son diferentes\. \( GAMES HOWELL\)

Dado que el p\-valor es 1\.00 no se rechaza la Ho, y se concluye que las varianzas de los sistemas son iguales\.

Paso 6: ANOVA

Los promedios de tiempo de los 3 sistemas son diferentes dado el valor de Sig\. Menor al valor de significancia\.

Agarramos el sistema con menor tiempo : 13,50

Conclusión: A un margen de error del 5% s concluye que hay diferencias significativas en los tiempos promedios de los 3 sistemas\. Si tuviera que elegir un sistema,me quedaría con el sistema numero 2 porque el tiempo promedio \(13\.50milisegundos\) es menor a los demás\.

