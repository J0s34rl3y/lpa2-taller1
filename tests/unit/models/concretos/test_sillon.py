"""
Pruebas para la clase Sillon.
"""

import pytest

from src.models.concretos.sillon import Sillon


class TestSillonInicializacion:
    """Pruebas de inicialización de Sillón."""

    def test_inicializacion_basica(self):
        """Probar inicialización con parámetros básicos."""
        sillon = Sillon("Sillón Test", "Madera", "Café", 400)

        assert sillon.nombre == "Sillón Test"
        assert sillon.material == "Madera"
        assert sillon.color == "Café"
        assert sillon.precio_base == 400

    def test_inicializacion_valores_por_defecto(self):
        """Probar valores por defecto."""
        sillon = Sillon("Sillón", "Madera", "Café", 400)

        assert sillon.capacidad_personas == 2
        assert sillon.tiene_respaldo is True
        assert sillon.material_tapizado is None
        assert sillon.tiene_brazos is True
        assert sillon.es_reclinable is False
        assert sillon.tiene_reposapiés is False

    def test_inicializacion_completa(self):
        """Probar inicialización con todos los parámetros."""
        sillon = Sillon(
            "Sillón Relax",
            "Cuero",
            "Negro",
            600,
            capacidad_personas=1,
            tiene_respaldo=True,
            material_tapizado="cuero",
            tiene_brazos=True,
            es_reclinable=True,
            tiene_reposapiés=True,
        )

        assert sillon.capacidad_personas == 1
        assert sillon.material_tapizado == "cuero"
        assert sillon.es_reclinable is True
        assert sillon.tiene_reposapiés is True


class TestSillonCalculoPrecio:
    """Pruebas de cálculo de precio de Sillón."""

    def test_calcular_precio_basico(self):
        """Probar cálculo de precio básico."""
        sillon = Sillon("Sillón", "Madera", "Café", 400)
        precio = sillon.calcular_precio()

        assert precio >= 400
        assert isinstance(precio, int)

    def test_precio_con_tapizado(self):
        """Probar que el tapizado aumenta el precio."""
        sillon_sin = Sillon("Sillón", "Madera", "Café", 400, material_tapizado=None)
        sillon_con = Sillon("Sillón", "Madera", "Café", 400, material_tapizado="tela")

        precio_sin = sillon_sin.calcular_precio()
        precio_con = sillon_con.calcular_precio()

        assert precio_con > precio_sin
        assert precio_con - precio_sin == 200

    def test_precio_con_brazos(self):
        """Probar que los brazos aumentan el precio."""
        sillon_sin = Sillon("Sillón", "Madera", "Café", 400, tiene_brazos=False)
        sillon_con = Sillon("Sillón", "Madera", "Café", 400, tiene_brazos=True)

        precio_sin = sillon_sin.calcular_precio()
        precio_con = sillon_con.calcular_precio()

        assert precio_con > precio_sin
        assert precio_con - precio_sin == 100

    def test_precio_reclinable(self):
        """Probar que ser reclinable aumenta el precio."""
        sillon_normal = Sillon("Sillón", "Madera", "Café", 400, es_reclinable=False)
        sillon_reclinable = Sillon("Sillón", "Madera", "Café", 400, es_reclinable=True)

        precio_normal = sillon_normal.calcular_precio()
        precio_reclinable = sillon_reclinable.calcular_precio()

        assert precio_reclinable > precio_normal
        assert precio_reclinable - precio_normal == 250

    def test_precio_con_reposapiés(self):
        """Probar que el reposapiés aumenta el precio."""
        sillon_sin = Sillon("Sillón", "Madera", "Café", 400, tiene_reposapiés=False)
        sillon_con = Sillon("Sillón", "Madera", "Café", 400, tiene_reposapiés=True)

        precio_sin = sillon_sin.calcular_precio()
        precio_con = sillon_con.calcular_precio()

        assert precio_con > precio_sin
        assert precio_con - precio_sin == 80

    def test_precio_con_todas_opciones(self):
        """Probar precio con todas las opciones."""
        sillon = Sillon(
            "Sillón Completo",
            "Madera",
            "Café",
            400,
            material_tapizado="cuero",
            tiene_brazos=True,
            es_reclinable=True,
            tiene_reposapiés=True,
        )

        precio = sillon.calcular_precio()
        # 400 + 200 (tapizado) + 100 (brazos) + 250 (reclinable) + 80 (reposapiés) = 1030
        assert precio == 1030


class TestSillonDescripcion:
    """Pruebas del método obtener_descripcion."""

    def test_obtener_descripcion_contiene_nombre(self):
        """Verificar que la descripción contiene el nombre."""
        sillon = Sillon("Sillón Test", "Madera", "Café", 400)
        desc = sillon.obtener_descripcion()

        assert "Sillón Test" in desc

    def test_obtener_descripcion_contiene_caracteristicas(self):
        """Verificar que la descripción contiene las características."""
        sillon = Sillon("Sillón", "Cuero", "Negro", 400, es_reclinable=True)
        desc = sillon.obtener_descripcion()

        assert "Cuero" in desc
        assert "Negro" in desc

    def test_obtener_descripcion_reclinable(self):
        """Verificar que menciona si es reclinable."""
        sillon = Sillon("Sillón", "Madera", "Café", 400, es_reclinable=True)
        desc = sillon.obtener_descripcion()

        assert "Sí" in desc or "sí" in desc.lower() or "Reclinable" in desc


class TestSillonParametrizacion:
    """Pruebas parametrizadas para diferentes configuraciones."""

    @pytest.mark.parametrize(
        "tapizado,brazos,reclinable,reposapiés,incremento",
        [
            (None, True, False, False, 100),  # Solo brazos
            ("tela", False, False, False, 200),  # Solo tapizado
            (None, False, True, False, 250),  # Solo reclinable
            (None, False, False, True, 80),  # Solo reposapiés
            ("tela", True, True, True, 630),  # Todos: 200+100+250+80
        ],
    )
    def test_diferentes_configuraciones(self, tapizado, brazos, reclinable, reposapiés, incremento):
        """Probar diferentes configuraciones de sillón."""
        precio_base = 400
        sillon = Sillon(
            "Sillón",
            "Madera",
            "Café",
            precio_base,
            material_tapizado=tapizado,
            tiene_brazos=brazos,
            es_reclinable=reclinable,
            tiene_reposapiés=reposapiés,
        )

        precio = sillon.calcular_precio()
        assert precio == precio_base + incremento

    @pytest.mark.parametrize("capacidad", [1, 2])
    def test_diferentes_capacidades(self, capacidad):
        """Probar sillones con diferentes capacidades."""
        sillon = Sillon("Sillón", "Madera", "Café", 400, capacidad_personas=capacidad)

        assert sillon.capacidad_personas == capacidad
        assert sillon.calcular_precio() >= 400

    @pytest.mark.parametrize(
        "material,color",
        [
            ("Madera", "Café"),
            ("Cuero", "Negro"),
            ("Tela", "Gris"),
        ],
    )
    def test_diferentes_materiales(self, material, color):
        """Probar sillones con diferentes materiales."""
        sillon = Sillon("Sillón", material, color, 400)

        assert sillon.material == material
        assert sillon.color == color
        assert sillon.calcular_precio() >= 400
