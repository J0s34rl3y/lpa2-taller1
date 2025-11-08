"""
Pruebas para la clase Armario.
"""

import pytest

from src.models.concretos.armario import Armario


class TestArmarioInicializacion:
    """Pruebas de inicialización de Armario."""

    def test_inicializacion_basica(self):
        """Probar inicialización con parámetros básicos."""
        armario = Armario("Armario Test", "Madera", "Blanco", 500)

        assert armario.nombre == "Armario Test"
        assert armario.material == "Madera"
        assert armario.color == "Blanco"
        assert armario.precio_base == 500

    def test_inicializacion_con_valores_por_defecto(self):
        """Probar valores por defecto."""
        armario = Armario("Armario", "Madera", "Blanco", 500)

        assert armario.num_puertas == 2
        assert armario.num_cajones == 0
        assert armario.tiene_espejos is False

    def test_inicializacion_completa(self):
        """Probar inicialización con todos los parámetros."""
        armario = Armario(
            "Armario Completo",
            "Roble",
            "Natural",
            800,
            num_puertas=4,
            num_cajones=3,
            tiene_espejos=True,
        )

        assert armario.num_puertas == 4
        assert armario.num_cajones == 3
        assert armario.tiene_espejos is True


class TestArmarioCalculoPrecio:
    """Pruebas de cálculo de precio de Armario."""

    def test_calcular_precio_basico(self):
        """Probar cálculo de precio básico."""
        armario = Armario("Armario", "Madera", "Blanco", 500, num_puertas=2, num_cajones=0)
        precio = armario.calcular_precio()

        # precio_base + (num_puertas * 50)
        assert precio >= 500
        assert isinstance(precio, int)

    def test_precio_aumenta_con_puertas(self):
        """Probar que más puertas aumentan el precio."""
        armario_2 = Armario("Armario", "Madera", "Blanco", 500, num_puertas=2)
        armario_4 = Armario("Armario", "Madera", "Blanco", 500, num_puertas=4)

        precio_2 = armario_2.calcular_precio()
        precio_4 = armario_4.calcular_precio()

        assert precio_4 > precio_2
        assert precio_4 - precio_2 == 100  # 2 puertas * 50

    def test_precio_aumenta_con_cajones(self):
        """Probar que más cajones aumentan el precio."""
        armario_sin = Armario("Armario", "Madera", "Blanco", 500, num_cajones=0)
        armario_con = Armario("Armario", "Madera", "Blanco", 500, num_cajones=3)

        precio_sin = armario_sin.calcular_precio()
        precio_con = armario_con.calcular_precio()

        assert precio_con > precio_sin
        assert precio_con - precio_sin == 90  # 3 cajones * 30

    def test_precio_con_espejos(self):
        """Probar que los espejos aumentan el precio."""
        armario_sin = Armario("Armario", "Madera", "Blanco", 500, tiene_espejos=False)
        armario_con = Armario("Armario", "Madera", "Blanco", 500, tiene_espejos=True)

        precio_sin = armario_sin.calcular_precio()
        precio_con = armario_con.calcular_precio()

        assert precio_con > precio_sin
        assert precio_con - precio_sin == 100

    def test_precio_con_todas_opciones(self):
        """Probar precio con todas las opciones."""
        armario = Armario(
            "Armario Completo",
            "Madera",
            "Blanco",
            500,
            num_puertas=4,
            num_cajones=5,
            tiene_espejos=True,
        )

        precio = armario.calcular_precio()
        # 500 + (4*50) + (5*30) + 100 = 500 + 200 + 150 + 100 = 950
        assert precio == 950


class TestArmarioDescripcion:
    """Pruebas del método obtener_descripcion."""

    def test_obtener_descripcion_contiene_nombre(self):
        """Verificar que la descripción contiene el nombre."""
        armario = Armario("Armario Test", "Madera", "Blanco", 500)
        desc = armario.obtener_descripcion()

        assert "Armario Test" in desc

    def test_obtener_descripcion_contiene_caracteristicas(self):
        """Verificar que la descripción contiene las características."""
        armario = Armario("Armario", "Roble", "Natural", 500, num_puertas=3, num_cajones=2)
        desc = armario.obtener_descripcion()

        assert "Roble" in desc
        assert "Natural" in desc
        assert "3" in desc or "Puertas=3" in desc
        assert "2" in desc or "Cajones=2" in desc

    def test_obtener_descripcion_con_espejos(self):
        """Verificar que menciona los espejos."""
        armario = Armario("Armario", "Madera", "Blanco", 500, tiene_espejos=True)
        desc = armario.obtener_descripcion()

        assert "Sí" in desc or "sí" in desc.lower()


class TestArmarioParametrizacion:
    """Pruebas parametrizadas para diferentes configuraciones."""

    @pytest.mark.parametrize(
        "puertas,cajones,espejos,incremento",
        [
            (2, 0, False, 100),  # 2*50 = 100
            (3, 0, False, 150),  # 3*50 = 150
            (2, 2, False, 160),  # 2*50 + 2*30 = 160
            (2, 0, True, 200),  # 2*50 + 100 = 200
            (3, 2, True, 310),  # 3*50 + 2*30 + 100 = 310
        ],
    )
    def test_diferentes_configuraciones(self, puertas, cajones, espejos, incremento):
        """Probar diferentes configuraciones de armario."""
        precio_base = 500
        armario = Armario(
            "Armario",
            "Madera",
            "Blanco",
            precio_base,
            num_puertas=puertas,
            num_cajones=cajones,
            tiene_espejos=espejos,
        )

        precio = armario.calcular_precio()
        assert precio == precio_base + incremento

    @pytest.mark.parametrize(
        "material,color",
        [
            ("Madera", "Blanco"),
            ("Roble", "Natural"),
            ("MDF", "Negro"),
            ("Pino", "Café"),
        ],
    )
    def test_diferentes_materiales(self, material, color):
        """Probar armarios con diferentes materiales."""
        armario = Armario("Armario", material, color, 500)

        assert armario.material == material
        assert armario.color == color
        assert armario.calcular_precio() >= 500
