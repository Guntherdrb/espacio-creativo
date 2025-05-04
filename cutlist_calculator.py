def calcular_cutlist(piezas, ancho_tablero_cm, largo_tablero_cm):
    area_tablero = ancho_tablero_cm * largo_tablero_cm
    area_total_piezas = 0

    for pieza in piezas:
        area_pieza = pieza['ancho'] * pieza['alto'] * pieza['cantidad']
        area_total_piezas += area_pieza

    tableros_necesarios = area_total_piezas / area_tablero
    tableros_necesarios_redondeado = int(tableros_necesarios) + (1 if tableros_necesarios % 1 > 0 else 0)

    return {
        'area_total_piezas': area_total_piezas,
        'area_por_tablero': area_tablero,
        'tableros_necesarios': tableros_necesarios_redondeado
    }
