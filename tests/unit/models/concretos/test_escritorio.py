"""
Pruebas para la clase Escritorio.
"""

import pytest

from src.models.concretos.escritorio import Escritorio


class TestEscritorioInicializacion:
    """Pruebas de inicialización de Escritorio."""

    def test_inicializacion_basica(self):
        """Probar inicialización con parámetros básicos."""
        escritorio = Escritorio("Escritorio Test", "Madera", "Negro", 300)

        assert escritorio.nombre == "Escritorio Test"
        assert escritorio.material == "Madera"
        assert escritorio.color == "Negro"
        assert escritorio.precio_base == 300

    def test_inicializacion_valores_por_defecto(self):
        """Probar valores por defecto."""
        escritorio = Escritorio("Escritorio", "Madera", "Negro", 300)

        assert escritorio.forma == "rectangular"
        assert escritorio.tiene_cajones is False
        assert escritorio.num_cajones == 0
        assert escritorio.largo == 1.2
        assert escritorio.tiene_iluminacion is False

    def test_inicializacion_completa(self):
        """Probar inicialización con todos los parámetros."""
        escritorio = Escritorio(
            "Escritorio Ejecutivo",
            "Roble",
            "Oscuro",
            500,
            forma="curvo",
            tiene_cajones=True,
            num_cajones=3,
            largo=1.8,
            tiene_iluminacion=True,
        )

        assert escritorio.forma == "curvo"
        assert escritorio.tiene_cajones is True
        assert escritorio.num_cajones == 3
        assert escritorio.largo == 1.8
        assert escritorio.tiene_iluminacion is True


class TestEscritorioCalculoPrecio:
    """Pruebas de cálculo de precio de Escritorio."""

    def test_calcular_precio_basico(self):
        """Probar cálculo de precio básico."""
        escritorio = Escritorio("Escritorio", "Madera", "Negro", 300)
        precio = escritorio.calcular_precio()

        assert precio >= 300
        assert isinstance(precio, int)

    def test_precio_con_cajones(self):
        """Probar que los cajones aumentan el precio."""
        esc_sin = Escritorio("Escritorio", "Madera", "Negro", 300, tiene_cajones=False)
        esc_con = Escritorio(
            "Escritorio", "Madera", "Negro", 300, tiene_cajones=True, num_cajones=3
        )

        precio_sin = esc_sin.calcular_precio()
        precio_con = esc_con.calcular_precio()

        assert precio_con > precio_sin
        assert precio_con - precio_sin == 75  # 3 * 25

    def test_precio_con_largo_mayor(self):
        """Probar que largo mayor a 1.5m aumenta el precio."""
        esc_corto = Escritorio("Escritorio", "Madera", "Negro", 300, largo=1.2)
        esc_largo = Escritorio("Escritorio", "Madera", "Negro", 300, largo=1.8)

        precio_corto = esc_corto.calcular_precio()
        precio_largo = esc_largo.calcular_precio()

        assert precio_largo > precio_corto
        assert precio_largo - precio_corto == 50

    def test_precio_con_iluminacion(self):
        """Probar que la iluminación aumenta el precio."""
        esc_sin = Escritorio("Escritorio", "Madera", "Negro", 300, tiene_iluminacion=False)
        esc_con = Escritorio("Escritorio", "Madera", "Negro", 300, tiene_iluminacion=True)

        precio_sin = esc_sin.calcular_precio()
        precio_con = esc_con.calcular_precio()

        assert precio_con > precio_sin
        assert precio_con - precio_sin == 40

    def test_precio_forma_no_rectangular(self):
        """Probar que forma no rectangular aumenta el precio."""
        esc_rect = Escritorio("Escritorio", "Madera", "Negro", 300, forma="rectangular")
        esc_curvo = Escritorio("Escritorio", "Madera", "Negro", 300, forma="curvo")

        precio_rect = esc_rect.calcular_precio()
        precio_curvo = esc_curvo.calcular_precio()

        assert precio_curvo > precio_rect
        assert precio_curvo - precio_rect == 30


class TestEscritorioDescripcion:
    """Pruebas del método obtener_descripcion."""

    def test_obtener_descripcion_contiene_nombre(self):
        """Verificar que la descripción contiene el nombre."""
        escritorio = Escritorio("Escritorio Test", "Madera", "Negro", 300)
        desc = escritorio.obtener_descripcion()

        assert "Escritorio Test" in desc

    def test_obtener_descripcion_contiene_caracteristicas(self):
        """Verificar que la descripción contiene las características."""
        escritorio = Escritorio(
            "Escritorio", "Roble", "Oscuro", 300, tiene_cajones=True, num_cajones=2
        )
        desc = escritorio.obtener_descripcion()

        assert "Roble" in desc
        assert "Oscuro" in desc
        assert "2" in desc or "Cajones=2" in desc

    def test_obtener_descripcion_con_iluminacion(self):
        """Verificar que menciona la iluminación."""
        escritorio = Escritorio("Escritorio", "Madera", "Negro", 300, tiene_iluminacion=True)
        desc = escritorio.obtener_descripcion()

        assert "Sí" in desc or "sí" in desc.lower()


class TestEscritorioParametrizacion:
    """Pruebas parametrizadas para diferentes configuraciones."""

    @pytest.mark.parametrize(
        "cajones,largo,iluminacion,forma,incremento",
        [
            (0, 1.2, False, "rectangular", 0),
            (3, 1.2, False, "rectangular", 75),  # 3*25
            (0, 1.8, False, "rectangular", 50),  # largo > 1.5
            (0, 1.2, True, "rectangular", 40),  # iluminación
            (0, 1.2, False, "curvo", 30),  # forma
            (3, 1.8, True, "curvo", 195),  # todos: 75 + 50 + 40 + 30
        ],
    )
    def test_diferentes_configuraciones(self, cajones, largo, iluminacion, forma, incremento):
        """Probar diferentes configuraciones de escritorio."""
        precio_base = 300
        tiene_cajones = cajones > 0

        escritorio = Escritorio(
            "Escritorio",
            "Madera",
            "Negro",
            precio_base,
            forma=forma,
            tiene_cajones=tiene_cajones,
            num_cajones=cajones,
            largo=largo,
            tiene_iluminacion=iluminacion,
        )

        precio = escritorio.calcular_precio()
        assert precio == precio_base + incremento

    @pytest.mark.parametrize(
        "material,color",
        [
            ("Madera", "Negro"),
            ("Metal", "Gris"),
            ("Vidrio", "Transparente"),
        ],
    )
    def test_diferentes_materiales(self, material, color):
        """Probar escritorios con diferentes materiales."""
        escritorio = Escritorio("Escritorio", material, color, 300)

        assert escritorio.material == material
        assert escritorio.color == color
        assert escritorio.calcular_precio() >= 300
