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
```

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
      Pendiente: `examples/figure8_4_1_manual.json` (micro-modulo de datos).
