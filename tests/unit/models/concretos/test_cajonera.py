"""
Pruebas para la clase Cajonera.
"""

import pytest

from src.models.concretos.cajonera import Cajonera


class TestCajoneraInicializacion:
    """Pruebas de inicialización de Cajonera."""

    def test_inicializacion_basica(self):
        """Probar inicialización con parámetros básicos."""
        cajonera = Cajonera("Cajonera Test", "Madera", "Natural", 200)

        assert cajonera.nombre == "Cajonera Test"
        assert cajonera.material == "Madera"
        assert cajonera.color == "Natural"
        assert cajonera.precio_base == 200

    def test_inicializacion_valores_por_defecto(self):
        """Probar valores por defecto."""
        cajonera = Cajonera("Cajonera", "Madera", "Natural", 200)

        assert cajonera.num_cajones == 3
        assert cajonera.tiene_ruedas is False

    def test_inicializacion_completa(self):
        """Probar inicialización con todos los parámetros."""
        cajonera = Cajonera(
            "Cajonera Oficina", "Metal", "Gris", 250, num_cajones=5, tiene_ruedas=True
        )

        assert cajonera.num_cajones == 5
        assert cajonera.tiene_ruedas is True


class TestCajoneraCalculoPrecio:
    """Pruebas de cálculo de precio de Cajonera."""

    def test_calcular_precio_basico(self):
        """Probar cálculo de precio básico."""
        cajonera = Cajonera("Cajonera", "Madera", "Natural", 200, num_cajones=3)
        precio = cajonera.calcular_precio()

        # precio_base + (num_cajones * 20)
        assert precio >= 200
        assert isinstance(precio, int)

    def test_precio_aumenta_con_cajones(self):
        """Probar que más cajones aumentan el precio."""
        cajonera_3 = Cajonera("Cajonera", "Madera", "Natural", 200, num_cajones=3)
        cajonera_5 = Cajonera("Cajonera", "Madera", "Natural", 200, num_cajones=5)

        precio_3 = cajonera_3.calcular_precio()
        precio_5 = cajonera_5.calcular_precio()

        assert precio_5 > precio_3
        assert precio_5 - precio_3 == 40  # 2 cajones * 20

    def test_precio_con_ruedas(self):
        """Probar que las ruedas aumentan el precio."""
        cajonera_sin = Cajonera("Cajonera", "Madera", "Natural", 200, tiene_ruedas=False)
        cajonera_con = Cajonera("Cajonera", "Madera", "Natural", 200, tiene_ruedas=True)

        precio_sin = cajonera_sin.calcular_precio()
        precio_con = cajonera_con.calcular_precio()

        assert precio_con > precio_sin
        assert precio_con - precio_sin == 30

    def test_precio_con_todas_opciones(self):
        """Probar precio con todas las opciones."""
        cajonera = Cajonera("Cajonera", "Madera", "Natural", 200, num_cajones=4, tiene_ruedas=True)

        precio = cajonera.calcular_precio()
        # 200 + (4*20) + 30 = 200 + 80 + 30 = 310
        assert precio == 310


class TestCajoneraDescripcion:
    """Pruebas del método obtener_descripcion."""

    def test_obtener_descripcion_contiene_nombre(self):
        """Verificar que la descripción contiene el nombre."""
        cajonera = Cajonera("Cajonera Test", "Madera", "Natural", 200)
        desc = cajonera.obtener_descripcion()

        assert "Cajonera Test" in desc

    def test_obtener_descripcion_contiene_caracteristicas(self):
        """Verificar que la descripción contiene las características."""
        cajonera = Cajonera("Cajonera", "Roble", "Oscuro", 200, num_cajones=5)
        desc = cajonera.obtener_descripcion()

        assert "Roble" in desc
        assert "Oscuro" in desc
        assert "5" in desc or "Cajones=5" in desc

    def test_obtener_descripcion_con_ruedas(self):
        """Verificar que menciona las ruedas."""
        cajonera = Cajonera("Cajonera", "Madera", "Natural", 200, tiene_ruedas=True)
        desc = cajonera.obtener_descripcion()

        assert "Sí" in desc or "sí" in desc.lower()


class TestCajoneraParametrizacion:
    """Pruebas parametrizadas para diferentes configuraciones."""

    @pytest.mark.parametrize(
        "cajones,ruedas,incremento",
        [
            (3, False, 60),  # 3*20 = 60
            (5, False, 100),  # 5*20 = 100
            (3, True, 90),  # 3*20 + 30 = 90
            (6, True, 150),  # 6*20 + 30 = 150
        ],
    )
    def test_diferentes_configuraciones(self, cajones, ruedas, incremento):
        """Probar diferentes configuraciones de cajonera."""
        precio_base = 200
        cajonera = Cajonera(
            "Cajonera", "Madera", "Natural", precio_base, num_cajones=cajones, tiene_ruedas=ruedas
        )

        precio = cajonera.calcular_precio()
        assert precio == precio_base + incremento

    @pytest.mark.parametrize(
        "material,color",
        [
            ("Madera", "Natural"),
            ("Metal", "Gris"),
            ("Plástico", "Blanco"),
        ],
    )
    def test_diferentes_materiales(self, material, color):
        """Probar cajoneras con diferentes materiales."""
        cajonera = Cajonera("Cajonera", material, color, 200)

        assert cajonera.material == material
        assert cajonera.color == color
        assert cajonera.calcular_precio() >= 200
