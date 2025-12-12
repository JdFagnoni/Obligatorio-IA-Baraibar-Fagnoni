Facultad de  
Ingenierı́a  
Bernard Wand-Polak  
Cuareim 1451  
11.100 Montevideo, Uruguay  
Tel. 2902 15 05 Fax 2908 13 70  
www.ort.edu.uy  

EVALUACIÓN Obligatorio GRUPO FECHA  
MATERIA Inteligencia Artificial  
CARRERA Ingenierı́a en Sistemas  
CONDICIONES - Puntaje máximo: 30 puntos  

- Puntaje mı́nimo: 0 punto  
- Fecha de entrega: 15/12/2025 hasta las 21:00 horas en gestion.ort.edu.uy (max.  
  40Mb en formato zip, rar o pdf)  

Uso de material de apoyo y/o consulta  

Inteligencia Artificial Generativa  

- Seguir las pautas de los docentes: Se deben seguir las instrucciones especı́fi-  
  cas de los docentes sobre cómo utilizar la IA en cada curso.  

- Citar correctamente las fuentes y usos de IA: Siempre que se utilice una herra-  
  mienta de IA para generar contenido, se debe citar adecuadamente la fuente  
  y la forma en que se utilizó.  

- Verificar el contenido generado por la IA: No todo el contenido generado por  
  la IA es correcto o preciso. Es esencial que los estudiantes verifiquen la infor-  
  mación antes de usarla.  

- Ser responsables con el uso de la IA: Conocer los riesgos y desafı́os, como  
  la creación de “alucinaciones”, los peligros para la privacidad, las cuestiones  
  de propiedad intelectual, los sesgos inherentes y la producción de contenido  
  falso.  

- En caso de existir dudas sobre la autorı́a, plagio o uso no atribuido de IAG, el  
  docente tendrá la opción de convocar al equipo de obligatorio a una defensa  
  especı́fica e individual sobre el tema.  

Defensa  
Fecha de defensa: 15/12/2025  
Defensa en forma de pregunta en el 2do parcial.  
Después de la defensa escrita, los docentes podrán solicitar una defensa oral.  

IMPORTANTE:  

1) Inscribirse  

2) Formar grupos de hasta 2 personas del mismo dictado  

3) Subir el trabajo a Gestión antes de la hora indicada (ver hoja al final del docu-  
   mento: “RECORDATORIO”)  

Aquellos de ustedes que presenten alguna dificultad con su inscripción o tengan  
inconvenientes técnicos, por favor contactarse con el Coordinador de cursos o  
Coordinación adjunta antes de las 20:00h del dı́a de la entrega, a través de los  
mails crosa@ort.edu.uy / posada_l@ort.edu.uy (matutino) / larrosa@ort.edu.uy  
(nocturno), o vı́a Ms Teams.  

Computación - Electrónica - Telecomunicaciones - Sistemas de Información  
Página 1 de 4  

www.ort.edu.uy  
crosa@ort.edu.uy  
posada_l@ort.edu.uy  
larrosa@ort.edu.uy  


Facultad de  
Ingenierı́a  
Bernard Wand-Polak  
Cuareim 1451  
11.100 Montevideo, Uruguay  
Tel. 2902 15 05 Fax 2908 13 70  
www.ort.edu.uy  

Contexto del problema  

Han sido seleccionados para formar parte del desarrollo de robots humanoides de propósito general,  
Pésimusk, de la aclamada empresa tecnológica Tosla. En su rol, estarán encargados de resolver dos  
problemas crı́ticos para el avance de nuestro ambicioso proyecto.  

Objetivos  

En Tosla, esperamos que demuestren su expertise en aplicar técnicas de Q-Learning y  
Minimax/Expectimax para resolver los problemas que se presentan a continuación:  

Módulo de Balance Dinámico (MBD)  

Nuestros prototipos Pésimusk, aunque estéticamente impecables, a veces muestran una tendencia  
alarmante a perder el equilibrio. Pero no hay problema, porque para eso están ustedes. Como primer  
paso para resolver esta problemática, deben programar una IA que aprenda a mantener un poste  
vertical sobre una plataforma móvil el mayor tiempo posible.  

Módulo de Estrategia Cognitiva (MEC)  

Una vez que nuestros Pésimusks caminen con estabilidad, deben demostrar su capacidad para la  
toma de decisiones complejas. Para ello, los pondremos a prueba en el juego 2048. Este entorno nos  
permitirá evaluar su capacidad para anticipar movimientos, planificar a largo plazo y optimizar resul-  
tados. Su tarea es crear un algoritmo que no solo resuelva el juego, sino que lo domine, demostrando  
que nuestros robots son mucho más que un simple cuerpo de metal.  

Tareas a desarrollar  

MBD  

La primera tarea está basada en el ambiente CartPole-v1. Concretamente, se pide:  

1. Discretizar las observaciones y acciones: Dado que las observaciones y acciones son con-  
   tinuaas, deben discretizarse. Se espera al menos 2 pruebas diferentes, justificando su elección  
   e impacto en el agente.  

2. Técnica: La técnica elegida para resolver el problema es Q-Learning.  

3. Exploración de hiperparámetros para encontrar el algoritmo que obtenga mejores resultados.  
   Se espera que se experimenten múltiples combinaciones de hiperparámetros, justificando su  
   forma de evaluar el rendimiento del agente, y la elección final de los mismos.  

4. Lectura de artı́culo: leer el artı́culo Stochastic Q-learning for Large Discrete Action Spaces e  
   implementar Stochastic Q-learning. Se espera que apliquen un análisis y experimentación  
   similares a su trabajo con Q-Learning.  

Computación - Electrónica - Telecomunicaciones - Sistemas de Información  
Página 2 de 4  

www.ort.edu.uy  
https://gymnasium.farama.org/environments/classic_control/cart_pole/  
https://arxiv.org/abs/2405.10310  


Facultad de  
Ingenierı́a  
Bernard Wand-Polak  
Cuareim 1451  
11.100 Montevideo, Uruguay  
Tel. 2902 15 05 Fax 2908 13 70  
www.ort.edu.uy  

MEC  

La segunda tarea está basada en el juego 2048. Concretamente, se les pide:  

1. Técnicas: implementar tanto Minimax como Expectimax para decidir cuál es la mejor técnica  
   para este caso. En el caso de Minimax, deben implementarlo utilizando Alpha-Beta Pruning y  
   analizar su impacto.  

2. Funciones de evaluación: implementar funciones de evaluación que permitan analizar un es-  
   tado dado. Se espera que experimenten con las funciones, intentando con distintas combina-  
   ciones de las mismas, y ponderadas de distintas formas.  

3. Experimentación: Definir pruebas para evaluar los agentes y hacer un registro completo de  
   los resultados obtenidos.  

Auditorı́a  

Para evaluar el desempeño de los agentes entrenados, deben entregar todo el código en Python (.py  
y .ipynb), los modelos computados (.pkl o formatos similares) y un informe de no más de 20 páginas  
más anexos, en formato .pdf. Todo el contenido debe ser entregado en un archivo .zip.  

Es obligatorio entregar al menos un modelo computado para el primer ejercicio. Caso contrario, el  
ejercicio será considerado como no hecho. El informe debe incluir:  

Resumen de cómo abordó cada tarea. Incluyendo información relevante. (Ej: Bitácora con: in-  
teracción con el simulador, parámetros utilizados, tiempo de ejecución y resultados obtenidos).  

Apoyo visual (gráficos) y comentarios que permitan entender el desempeño de sus soluciones.  

Cualquier nota de advertencia que desee comunicar. Por ejemplo, en caso de haber encontrado  
dificultades, elaborar en cuáles fueron y por qué no se pudieron solucionar.  

La evaluación se basará en la documentación entregada. Es fundamental que su informe sea claro,  
legible y contenga toda la información necesaria para comprender a fondo el enfoque, los resultados  
y las conclusiones de su trabajo.  

Ambiente  

Se utilizará Poetry para ambos ejercicios en entornos separados. Se les entregará código de ambos  
ambientes listo para ejecutar el simulador.  

Recomendación  

Les recomendamos que comiencen el trabajo con antelación, ya que las ejecuciones pueden tomar  
tiempo.  

Computación - Electrónica - Telecomunicaciones - Sistemas de Información  
Página 3 de 4  

www.ort.edu.uy  


Facultad de  
Ingenierı́a  
Bernard Wand-Polak  
Cuareim 1451  
11.100 Montevideo, Uruguay  
Tel. 2902 15 05 Fax 2908 13 70  
www.ort.edu.uy  

RECORDATORIO: IMPORTANTE PARA LA ENTREGA  

• Obligatorios  

La entrega de los obligatorios será en formato digital online, a excepción de algunas materias que se entregarán  
en Bedelı́a y en ese caso recibirá información especı́fica en el dictado de la misma.  

Los principales aspectos a destacar sobre la entrega online de obligatorios son:  

1. Ingresá al sistema de Gestión.  

2. En el menú, seleccioná el ı́tem “Evaluaciones” y la instancia de evaluación correspondiente, que figura  
   bajo el tı́tulo “Inscripto”.  

3. Para iniciar la entrega hacé clic en el ı́cono:  

4. Ingresá el número de estudiante de cada uno de los integrantes y hacé clic en “Agregar”. El sistema  
   confirmará que los integrantes estén inscriptos al obligatorio y, de ser ası́, mostrará el nombre y la  
   fotografı́a de cada uno de ellos. Una vez agregados todos los integrantes, hacé clic en “Crear equipo”.  

   Cualquier integrante podrá:  
   Modificar la integración del equipo.  
   Subir el archivo de la entrega.  

5. Seleccioná el archivo que deseás entregar. Verificá el nombre del archivo que aparecerá en la pantalla  
   y hacé clic en “Subir” para iniciar la entrega. Cada equipo (hasta 2 estudiantes) debe entregar un único  
   archivo en formato zip o rar (los documentos de texto deben ser pdf, y deben ir dentro del zip o rar). El  
   archivo a subir debe tener un tamaño máximo de 40mb.  

   Cuando el archivo quede subido, se mostrará el nombre generado por el sistema (1), el ta-  
   maño y la fecha en que fue subido.  

6. El sistema enviará un e-mail a todos los integrantes del equipo informando los detalles del archivo en-  
   tregado y confirmando que la entrega fue realizada correctamente.  

7. Podés cerrar la pestaña de entrega y continuar utilizando Gestión o salir del sistema.  

8. La hora tope para subir el archivo será las 21:00 del dı́a fijado para la entrega.  

9. La entrega se podrá realizar desde cualquier lugar (ej. hogar del estudiante, laboratorios de la Universi-  
   dad, etc).  

10. Aquellos de ustedes que presenten alguna dificultad con su inscripción o tengan inconvenientes técnicos,  
    por favor contactarse con el Coordinador de cursos o Coordinación adjunta antes de las 20:00h del dı́a  
    de la entrega, a través de los mails crosa@ort.edu.uy / posada_l@ort.edu.uy (matutino) / larrosa@  
    ort.edu.uy (nocturno), o vı́a Ms Teams.  

Computación - Electrónica - Telecomunicaciones - Sistemas de Información  
Página 4 de 4  

www.ort.edu.uy  
crosa@ort.edu.uy  
posada_l@ort.edu.uy  
larrosa@ort.edu.uy  
larrosa@ort.edu.uy  
