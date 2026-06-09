"""Modulo 6: rolling (STUB declarado, sin logica todavia).

Calcula la matriz de rolling A(c). Para un contacto {i, j} se define
u_ij = (c_i - c_j) / ||c_i - c_j||, y la restriccion linealizada es
<u_ij, dc_i - dc_j> = 0. A(c) tiene una fila por contacto.

Se implementa en su punto correspondiente (Modulo 6).
"""

_TODO = "rolling: pendiente de implementar (Modulo 6)"


def build_A(cs, contacts):
    raise NotImplementedError(_TODO)


def contact_residuals(cs, contacts):
    raise NotImplementedError(_TODO)


def validate_contacts(cs, contacts):
    raise NotImplementedError(_TODO)


def kernel_basis(A):
    raise NotImplementedError(_TODO)


def rolling_report(cs, contacts):
    raise NotImplementedError(_TODO)
