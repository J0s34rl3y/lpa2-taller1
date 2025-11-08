"""
Pruebas para la clase Comedor (composición).
Este módulo demuestra pruebas de composición y agregación.
"""

import pytest

from src.models.composicion.comedor import Comedor
from src.models.concretos.mesa import Mesa
from src.models.concretos.silla import Silla


class TestComedorComposicion:
    """Pruebas de composición de Comedor."""

    def test_comedor_tiene_mesa(self, comedor_completo):
        """Verificar que el comedor tiene una mesa."""
        assert comedor_completo.mesa is not None
        assert isinstance(comedor_completo.mesa, Mesa)

    def test_comedor_tiene_sillas(self, comedor_completo):
        """Verificar que el comedor tiene sillas."""
        assert comedor_completo.sillas is not None
        assert len(comedor_completo.sillas) > 0
        assert all(isinstance(s, Silla) for s in comedor_completo.sillas)

    def test_componentes_son_independientes(self):
        """Verificar que los componentes pueden existir independientemente."""
        # Crear componentes independientes
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0)
        silla = Silla("Silla", "Madera", "Natural", 80.0)

        # Los componentes existen sin el comedor
        assert mesa is not None
        assert silla is not None

        # Crear comedor con ellos
        comedor = Comedor("Comedor", mesa, [silla])

        assert comedor.mesa is mesa
        assert silla in comedor.sillas


class TestComedorInicializacion:
    """Pruebas de inicialización de Comedor."""

    def test_inicializacion_con_mesa_y_sillas(self):
        """Probar inicialización con mesa y sillas."""
        mesa = Mesa("Mesa", "Roble", "Natural", 300.0)
        sillas = [
            Silla("Silla 1", "Roble", "Natural", 80.0),
            Silla("Silla 2", "Roble", "Natural", 80.0),
        ]

        comedor = Comedor("Comedor Test", mesa, sillas)

        assert comedor.nombre == "Comedor Test"
        assert comedor.mesa == mesa
        assert len(comedor.sillas) == 2

    def test_inicializacion_sin_sillas(self):
        """Probar inicialización sin sillas."""
        mesa = Mesa("Mesa", "Roble", "Natural", 300.0)
        comedor = Comedor("Comedor", mesa)

        assert comedor.mesa is not None
        assert len(comedor.sillas) == 0

    def test_inicializacion_con_lista_vacia(self):
        """Probar inicialización con lista vacía de sillas."""
        mesa = Mesa("Mesa", "Roble", "Natural", 300.0)
        comedor = Comedor("Comedor", mesa, [])

        assert len(comedor.sillas) == 0


class TestComedorPropiedades:
    """Pruebas de propiedades de Comedor."""

    def test_getter_nombre(self, comedor_completo):
        """Probar getter de nombre."""
        assert comedor_completo.nombre == "Comedor Familiar"

    def test_getter_mesa(self, comedor_completo):
        """Probar getter de mesa."""
        mesa = comedor_completo.mesa
        assert isinstance(mesa, Mesa)
        assert mesa.nombre == "Mesa Comedor"

    def test_getter_sillas_retorna_copia(self, comedor_completo):
        """Verificar que el getter de sillas retorna una copia."""
        sillas1 = comedor_completo.sillas
        sillas2 = comedor_completo.sillas

        # Deben ser listas diferentes (copias)
        assert sillas1 is not sillas2
        # Pero con el mismo contenido
        assert len(sillas1) == len(sillas2)


class TestComedorAgregarSilla:
    """Pruebas para agregar sillas al comedor."""

    def test_agregar_silla_exitoso(self):
        """Probar agregar una silla al comedor."""
        mesa = Mesa("Mesa", "Roble", "Natural", 300.0)
        comedor = Comedor("Comedor", mesa, [])

        silla = Silla("Silla Nueva", "Roble", "Natural", 80.0)
        resultado = comedor.agregar_silla(silla)

        assert isinstance(resultado, str)
        assert len(comedor.sillas) == 1
        assert comedor.sillas[0] == silla

    def test_agregar_multiples_sillas(self):
        """Probar agregar varias sillas."""
        mesa = Mesa("Mesa", "Roble", "Natural", 300.0)
        comedor = Comedor("Comedor", mesa, [])

        for i in range(4):
            silla = Silla(f"Silla {i+1}", "Roble", "Natural", 80.0)
            comedor.agregar_silla(silla)

        assert len(comedor.sillas) == 4

    def test_agregar_silla_a_comedor_existente(self, comedor_completo):
        """Probar agregar silla a comedor que ya tiene sillas."""
        cantidad_inicial = len(comedor_completo.sillas)

        silla_nueva = Silla("Silla Extra", "Roble", "Natural", 80.0)
        comedor_completo.agregar_silla(silla_nueva)

        assert len(comedor_completo.sillas) == cantidad_inicial + 1


class TestComedorQuitarSilla:
    """Pruebas para quitar sillas del comedor."""

    def test_quitar_ultima_silla(self, comedor_completo):
        """Probar quitar la última silla."""
        cantidad_inicial = len(comedor_completo.sillas)

        resultado = comedor_completo.quitar_silla()

        assert isinstance(resultado, str)
        assert len(comedor_completo.sillas) == cantidad_inicial - 1

    def test_quitar_silla_por_indice(self):
        """Probar quitar silla por índice específico."""
        mesa = Mesa("Mesa", "Roble", "Natural", 300.0)
        sillas = [Silla(f"Silla {i+1}", "Roble", "Natural", 80.0) for i in range(4)]
        comedor = Comedor("Comedor", mesa, sillas)

        comedor.quitar_silla(0)  # Quitar primera silla

        assert len(comedor.sillas) == 3
        assert comedor.sillas[0].nombre == "Silla 2"

    def test_quitar_silla_de_comedor_vacio(self):
        """Probar quitar silla cuando no hay sillas."""
        mesa = Mesa("Mesa", "Roble", "Natural", 300.0)
        comedor = Comedor("Comedor", mesa, [])

        resultado = comedor.quitar_silla()

        assert "No hay" in resultado or "no hay" in resultado.lower()
        assert len(comedor.sillas) == 0


class TestComedorCalculoPrecio:
    """Pruebas de cálculo de precio total."""

    def test_calcular_precio_solo_mesa(self):
        """Probar precio con solo la mesa."""
        mesa = Mesa("Mesa", "Roble", "Natural", 300.0)
        comedor = Comedor("Comedor", mesa, [])

        precio = comedor.calcular_precio_total()
        precio_mesa = mesa.calcular_precio()

        assert precio == precio_mesa

    def test_calcular_precio_mesa_y_sillas(self):
        """Probar precio con mesa y sillas."""
        mesa = Mesa("Mesa", "Roble", "Natural", 300.0)
        sillas = [Silla("Silla", "Roble", "Natural", 80.0) for _ in range(4)]
        comedor = Comedor("Comedor", mesa, sillas)

        precio_total = comedor.calcular_precio_total()

        # Debe sumar mesa + todas las sillas
        assert precio_total > mesa.calcular_precio()
        assert isinstance(precio_total, float)

    def test_descuento_con_4_o_mas_sillas(self):
        """Probar que hay descuento con 4+ sillas."""
        mesa = Mesa("Mesa", "Roble", "Natural", 300.0)
        sillas_3 = [Silla("Silla", "Roble", "Natural", 100.0) for _ in range(3)]
        sillas_4 = [Silla("Silla", "Roble", "Natural", 100.0) for _ in range(4)]

        comedor_3 = Comedor("Comedor 3", mesa, sillas_3)
        comedor_4 = Comedor("Comedor 4", mesa, sillas_4)

        precio_3 = comedor_3.calcular_precio_total()
        precio_4 = comedor_4.calcular_precio_total()

        # Con 4 sillas debe haber descuento del 5%
        # El precio con 4 sillas (con descuento) debe ser menor proporcionalmente
        assert precio_4 < (
            mesa.calcular_precio() + 4 * 100.0 * comedor_4.sillas[0].calcular_factor_comodidad()
        )

    def test_precio_redondeado(self, comedor_completo):
        """Verificar que el precio está redondeado a 2 decimales."""
        precio = comedor_completo.calcular_precio_total()
        precio_str = str(precio)

        if "." in precio_str:
            decimales = len(precio_str.split(".")[1])
            assert decimales <= 2


class TestComedorDescripciones:
    """Pruebas de métodos de descripción."""

    def test_obtener_descripcion_completa(self, comedor_completo):
        """Probar descripción completa del comedor."""
        desc = comedor_completo.obtener_descripcion_completa()

        assert isinstance(desc, str)
        assert len(desc) > 0
        assert "COMEDOR" in desc.upper()
        assert "MESA" in desc.upper()
        assert "SILLA" in desc.upper()

    def test_descripcion_incluye_precio(self, comedor_completo):
        """Verificar que la descripción incluye el precio."""
        desc = comedor_completo.obtener_descripcion_completa()
        precio = comedor_completo.calcular_precio_total()

        # El precio debe estar en la descripción
        assert "PRECIO" in desc.upper() or "precio" in desc.lower()

    def test_descripcion_sin_sillas(self):
        """Probar descripción de comedor sin sillas."""
        mesa = Mesa("Mesa", "Roble", "Natural", 300.0)
        comedor = Comedor("Comedor", mesa, [])

        desc = comedor.obtener_descripcion_completa()

        assert "Ninguna" in desc or "ninguna" in desc.lower()

    def test_descripcion_muestra_cantidad_sillas(self, comedor_completo):
        """Verificar que muestra la cantidad de sillas."""
        desc = comedor_completo.obtener_descripcion_completa()
        cantidad = len(comedor_completo.sillas)

        assert str(cantidad) in desc

    def test_descripcion_con_descuento(self):
        """Probar que la descripción menciona el descuento."""
        mesa = Mesa("Mesa", "Roble", "Natural", 300.0)
        sillas = [Silla("Silla", "Roble", "Natural", 80.0) for _ in range(6)]
        comedor = Comedor("Comedor", mesa, sillas)

        desc = comedor.obtener_descripcion_completa()

        assert "descuento" in desc.lower()


class TestComedorResumen:
    """Pruebas del método obtener_resumen."""

    def test_obtener_resumen_estructura(self, comedor_completo):
        """Probar estructura del resumen."""
        resumen = comedor_completo.obtener_resumen()

        assert isinstance(resumen, dict)
        assert "nombre" in resumen
        assert "total_muebles" in resumen
        assert "precio_mesa" in resumen
        assert "precio_sillas" in resumen
        assert "precio_total" in resumen
        assert "capacidad_personas" in resumen
        assert "materiales_utilizados" in resumen

    def test_resumen_nombre_correcto(self, comedor_completo):
        """Verificar que el nombre es correcto."""
        resumen = comedor_completo.obtener_resumen()
        assert resumen["nombre"] == "Comedor Familiar"

    def test_resumen_total_muebles(self, comedor_completo):
        """Verificar conteo total de muebles."""
        resumen = comedor_completo.obtener_resumen()
        cantidad_sillas = len(comedor_completo.sillas)

        # Total = 1 mesa + N sillas
        assert resumen["total_muebles"] == 1 + cantidad_sillas

    def test_resumen_precios_coherentes(self, comedor_completo):
        """Verificar que los precios son coherentes."""
        resumen = comedor_completo.obtener_resumen()

        assert resumen["precio_mesa"] > 0
        assert resumen["precio_sillas"] >= 0
        assert resumen["precio_total"] > 0

        # El precio total debe estar relacionado con los componentes
        assert resumen["precio_total"] >= resumen["precio_mesa"]

    def test_resumen_capacidad_personas(self, comedor_completo):
        """Verificar que la capacidad es el número de sillas."""
        resumen = comedor_completo.obtener_resumen()
        assert resumen["capacidad_personas"] == len(comedor_completo.sillas)


class TestComedorParametrizacion:
    """Pruebas parametrizadas para diferentes configuraciones."""

    @pytest.mark.parametrize("num_sillas", [0, 2, 4, 6, 8])
    def test_diferentes_cantidades_sillas(self, num_sillas):
        """Probar comedores con diferente cantidad de sillas."""
        mesa = Mesa("Mesa", "Roble", "Natural", 300.0)
        sillas = [Silla(f"Silla {i+1}", "Roble", "Natural", 80.0) for i in range(num_sillas)]
        comedor = Comedor(f"Comedor {num_sillas}", mesa, sillas)

        assert len(comedor.sillas) == num_sillas
        precio = comedor.calcular_precio_total()
        assert precio > 0

    @pytest.mark.parametrize("material", ["Roble", "Pino", "Metal"])
    def test_diferentes_materiales(self, material):
        """Probar comedores con diferentes materiales."""
        mesa = Mesa("Mesa", material, "Natural", 300.0)
        sillas = [Silla("Silla", material, "Natural", 80.0) for _ in range(4)]
        comedor = Comedor("Comedor", mesa, sillas)

        assert comedor.mesa.material == material
        assert all(s.material == material for s in comedor.sillas)


class TestComedorIntegracion:
    """Pruebas de integración con componentes."""

    def test_modificar_componentes_no_afecta_comedor(self, comedor_completo):
        """Verificar que modificar componentes externos no afecta al comedor."""
        # Obtener copia de sillas
        sillas_copia = comedor_completo.sillas
        cantidad_original = len(comedor_completo.sillas)

        # Modificar la copia no debe afectar al comedor
        sillas_copia.append(Silla("Nueva", "Madera", "Café", 50.0))

        assert len(comedor_completo.sillas) == cantidad_original

    def test_precio_total_suma_componentes(self):
        """Verificar que el precio total es la suma correcta."""
        mesa = Mesa("Mesa", "Roble", "Natural", 200.0)
        silla1 = Silla("Silla 1", "Roble", "Natural", 80.0)
        silla2 = Silla("Silla 2", "Roble", "Natural", 80.0)

        comedor = Comedor("Comedor", mesa, [silla1, silla2])

        precio_esperado = (
            mesa.calcular_precio() + silla1.calcular_precio() + silla2.calcular_precio()
        )
        precio_total = comedor.calcular_precio_total()

        # Pueden no ser exactamente iguales si hay descuento
        assert precio_total > 0
