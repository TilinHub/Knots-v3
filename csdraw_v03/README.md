# csdraw

Software para medir, dibujar y luego optimizar la longitud de diagramas cs de
nudos.

## Tests obligatorios (en este orden)

1. `examples/stadium_2.json` — test geometrico minimo del motor cs. No es un
   nudo. Verifica puntos, longitud, SVG, contactos, rolling, kernel, gradiente
   reducido y descenso.
2. `examples/figure8_4_1_manual.json` — primer test real de diagrama de nudo
   (4_1), con una componente declarada y cuatro cruces over/under manuales.

## Regla principal de trabajo

Cada paso debe producir codigo ejecutable y una salida verificable.

Formato obligatorio de reporte por modulo:

```
Modulo:
Archivo:
Funcion:
Comando:
Salida esperada:
Salida obtenida:
Estado: OK / ERROR
```

Si el estado es `ERROR`, no se avanza. No se pasa al siguiente modulo si el
modulo actual no produce la salida esperada. La meta no es escribir mucho
codigo, sino mantener una cadena de pasos verificados.

## Pipeline completo

```
input -> puntos -> longitud -> SVG -> componentes -> cruces -> 4_1
      -> rolling -> reducido -> descenso -> variables -> validacion -> optimizacion
```

Estado por etapa (sobre `stadium_2.json`):

| Etapa | Estado | Modulo |
|---|---|---|
| input | VIVO | `io_json.load_diagram` |
| puntos | VIVO | `cs_geometry.point` |
| longitud | VIVO | `length.total_length` |
| SVG | VIVO | `render_svg.write_svg` |
| componentes | STUB | `knot_diagram` |
| cruces | STUB | `crossings` |
| 4_1 | DATOS | `examples/figure8_4_1_manual.json` (reporte de nudo: stub) |
| rolling | STUB | `rolling` |
| reducido | STUB | `reduced` |
| descenso | STUB | `descent` |
| variables | STUB | `variables` |
| validacion | STUB | `validation` |
| optimizacion | STUB | `optimise` |

Exigencia de la primera version: `stadium_2` funciona y `figure8_4_1_manual`
funciona como diagrama con 4 cruces. Si una flecha falla, se corrige esa flecha
antes de avanzar.

## Sin codigo de Gauss en la primera version

No se implementa codigo de Gauss ni reconocimiento automatico de nudos. La
estructura del diagrama se **declara**:

- `components`: lista de recorridos de piezas cs, p. ej.
  `[["s1", "a1", "s2", "a2"]]`. Una pieza es un segmento o un arco; no hay una
  tercera lista `pieces` en el JSON.
- `crossings`: tabla explicita con `id`, `over_piece`, `under_piece`, `point`.

El programa **no** reconstruye la componente a partir de los cruces ni intenta
reconocer el tipo de nudo: solo verifica que los datos declarados sean
internamente consistentes. `figure8_4_1_manual.json` declara que el dibujo
proviene de un diagrama conocido de 4_1.

Reglas de los datos de nudo:

- Para un nudo de una componente, `components` tiene longitud 1.
- El estadio, aunque no es un nudo, tambien lleva `components` y `crossings: []`,
  para poder testear `knot_diagram.py` en un caso simple.
- Las componentes se validan por el recorrido declarado de piezas; no se
  reconstruyen desde los cruces. Los cruces sirven para over/under y dibujo.
- El campo `point` de un cruce es solo una marca visual: no se usa para la
  longitud ni para construir la componente.

## Que significa verificar 4_1 en esta version

El programa no demuestra que el nudo sea 4_1. Verifica que los datos declarados
sean internamente consistentes. El test de 4_1 debe pasar estas 13
verificaciones:

1. el archivo tiene `"type": "knot_diagram"`
2. el archivo tiene `"knot_label": "4_1"`
3. hay exactamente cuatro cruces declarados
4. cada cruce tiene id unico
5. cada cruce tiene una pieza over y una pieza under
6. las piezas over/under existen
7. la pieza over y la pieza under no son la misma
8. hay exactamente una componente declarada
9. la componente usa solo piezas existentes
10. cada pieza de segments y arcs aparece exactamente una vez en la componente
11. la componente es cerrada
12. la longitud cs se puede calcular
13. se puede exportar SVG

Reporte esperado para 4_1:

```
knot label: 4_1
number of crossings: 4
number of components: 1
component pieces valid: True
all pieces used exactly once: True
component closed: True
crossing ids valid: True
crossing pieces valid: True
over/under valid: True
crossings valid: True
length valid: True
```

Ademas: `0 < Len < +inf`, y la longitud es reproducible entre ejecuciones si el
JSON no cambia. Este reporte lo producira `knot_diagram_report` (Modulo 5).

## Tolerancia numerica

En todos los tests numericos se usa `eps_test = 1e-9`.

- Igualdad numerica `a = b`  significa  `|a - b| < eps_test`.
- Igualdad de vector o matriz `M = 0`  significa  `||M|| < eps_test`.

No se cambia la tolerancia para hacer pasar un test. Si un test falla con
`1e-9`, se corrige el modulo correspondiente.

## Reglas de errores claros

Toda funcion debe fallar de forma clara. Si recibe un label, disco, pieza,
segmento, arco, contacto, componente o cruce inexistente, levanta `ValueError`
con un mensaje que diga donde esta el problema.

## Uso

```
python main.py examples/stadium_2.json
python main.py examples/figure8_4_1_manual.json
```

Verificar el diagrama de nudo 4_1 (las 13 verificaciones de la seccion 11):

```
python verify_4_1.py
```

Imprime el reporte de la seccion 11 y devuelve codigo 0 si pasan las 13
verificaciones, 1 si alguna falla. Es provisional: lo reemplazara
`knot_diagram_report` (Modulo 5).

## Estado del plan

- [x] Seccion 1, Objetivo del software: estructura del proyecto y motor cs
      basico. `stadium_2.json` da `Total length: 10.283185307179586` y SVG.
- [x] Seccion 2, Regla principal de trabajo: protocolo de reporte adoptado.
- [x] Seccion 3, Tolerancia numerica: `csdraw/tolerance.py` con `EPS_TEST = 1e-9`
      y los predicados `num_equal` y `approx_zero`. Verificado contra el estadio.
- [x] Seccion 4, Regla de errores claros: `ValueError` con mensajes exactos para
      label, disco, pieza, endpoint de segmento y contacto. Faltan los de cruce y
      componente, que llegan con `crossings.py` y `knot_diagram.py`.
- [x] Seccion 5, Arquitectura: estructura de la seccion 5 completa. Modulos del
      motor implementados; `rolling, reduced, descent, knot_diagram, crossings,
      variables, validation, optimise` como stubs declarados. Todos importan.
- [x] Seccion 6, Pipeline completo: flecha documentada y verificada etapa por
      etapa. Tramo vivo `input -> puntos -> longitud -> SVG`; el resto stub.
      Falta `4_1` (datos) para cerrar la exigencia de la primera version.
- [x] Seccion 7, Sin codigo de Gauss: confirmado que no hay Gauss ni
      reconocimiento de nudos; componentes y cruces se cargan como datos
      declarados. Verificado por busqueda y por el modelo de datos.
- [x] Seccion 8, Datos cs: esquema y formulas confirmados; regla de id de pieza
      unico (`Duplicate piece id`) y accesor `piece_ids()` = union de segmentos y
      arcos. Verificado contra el estadio.
- [x] Seccion 9, Datos de nudo: `components` y `crossings` promovidos a datos de
      primera clase; `Crossing` parseado (id, over_piece, under_piece, point).
      Verificadas las tres advertencias (estadio lleva components; componente no
      se reconstruye de cruces; `point` no afecta la longitud).
- [x] Seccion 10, Archivos JSON de test: `figure8_4_1_manual.json` construido
      (4 discos, lazo cerrado, 8 piezas, 4 cruces X1..X4). Carga, longitud
      finita positiva (22.2831853...), reproducible y SVG. Geometria es un layout
      consistente de marcador, no el minimizador 4_1; los cruces son marcas
      declaradas (permitido en v1). Se refina al construir el 4_1 geometrico.
- [x] Seccion 11, Verificar 4_1: las 13 verificaciones y el reporte esperado,
      ahora como comando reejecutable `python verify_4_1.py` (provisional). El 4_1
      da 13/13 (exit 0); un diagrama roto falla con detalle (exit 1). La version
      definitiva sera `knot_diagram_report` (Modulo 5).
