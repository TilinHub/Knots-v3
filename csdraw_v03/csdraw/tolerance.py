"""Seccion 3: Tolerancia numerica.

En todos los tests numericos se usa

    EPS_TEST = 1e-9.

Una igualdad numerica  a = b   significa   |a - b| < EPS_TEST.
Una igualdad de vector o matriz  M = 0  significa  ||M|| < EPS_TEST.

No se cambia la tolerancia para hacer pasar un test. Si un test falla con
EPS_TEST, se corrige el modulo correspondiente.
"""

import numpy as np

EPS_TEST = 1e-9


def norm(M) -> float:
    """Norma euclidiana (de Frobenius) de un escalar, vector o matriz."""
    return float(np.linalg.norm(np.asarray(M, dtype=float)))


def num_equal(a: float, b: float, eps: float = EPS_TEST) -> bool:
    """Igualdad numerica: |a - b| < eps."""
    return abs(a - b) < eps


def approx_zero(M, eps: float = EPS_TEST) -> bool:
    """Igualdad a cero de vector o matriz: ||M|| < eps."""
    return norm(M) < eps


def check_equal(a: float, b: float, what: str = "value", eps: float = EPS_TEST):
    """Devuelve (ok, |a - b|). No lanza; el modulo decide que hacer."""
    diff = abs(a - b)
    return diff < eps, diff
