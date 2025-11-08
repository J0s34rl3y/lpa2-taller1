"""
Pruebas para la clase abstracta Superficie.
"""

from abc import ABC

import pytest

from src.models.categorias.superficies import Superficie
from src.models.mueble import Mueble


class TestSuperficieClaseAbstracta:
    """Pruebas para verificar que Superficie es una clase abstracta."""

    def test_no_se_puede_instanciar_directamente(self):
        """Verificar que no se puede crear instancia directamente."""
        with pytest.raises(TypeError):
            superficie = Superficie("Mesa", "Madera", "Natural", 200.0, 120.0, 80.0, 75.0)

    def test_hereda_de_mueble(self):
        """Verificar que hereda de Mueble."""
        assert issubclass(Superficie, Mueble)

    def test_es_subclase_de_abc(self):
        """Verificar que es abstracta."""
        assert issubclass(Superficie, ABC)

    def test_tiene_metodos_abstractos(self):
        """Verificar que mantiene los métodos abstractos."""
        assert hasattr(Superficie, "calcular_precio")
        assert hasattr(Superficie, "obtener_descripcion")


class TestSuperficieFuncionalidad:
    """Pruebas de funcionalidad usando una clase concreta."""

    @pytest.fixture
    def superficie_concreta_class(self):
        """Crear clase concreta para pruebas."""

        class SuperficieConcreta(Superficie):
            def calcular_precio(self) -> float:
                return self.precio_base * self.calcular_factor_tamaño()

            def obtener_descripcion(self) -> str:
                return f"{self.nombre}"

        return SuperficieConcreta

    def test_inicializacion_correcta(self, superficie_concreta_class):
        """Probar inicialización con valores válidos."""
        sup = superficie_concreta_class("Mesa", "Madera", "Natural", 200.0, 120.0, 80.0, 75.0)

        assert sup.nombre == "Mesa"
        assert sup.material == "Madera"
        assert sup.color == "Natural"
        assert sup.precio_base == 200.0
        assert sup.largo == 120.0
        assert sup.ancho == 80.0
        assert sup.altura == 75.0

    def test_getter_largo(self, superficie_concreta_class):
        """Probar getter de largo."""
        sup = superficie_concreta_class("Mesa", "Madera", "Natural", 200.0, 150.0, 80.0, 75.0)
        assert sup.largo == 150.0

    def test_setter_largo_valido(self, superficie_concreta_class):
        """Probar setter con largo válido."""
        sup = superficie_concreta_class("Mesa", "Madera", "Natural", 200.0, 120.0, 80.0, 75.0)
        sup.largo = 180.0
        assert sup.largo == 180.0

    def test_setter_largo_cero_error(self, superficie_concreta_class):
        """Probar que largo = 0 genera error."""
        sup = superficie_concreta_class("Mesa", "Madera", "Natural", 200.0, 120.0, 80.0, 75.0)
        with pytest.raises(ValueError) as excinfo:
            sup.largo = 0
        assert "largo" in str(excinfo.value).lower()

    def test_setter_largo_negativo_error(self, superficie_concreta_class):
        """Probar que largo negativo genera error."""
        sup = superficie_concreta_class("Mesa", "Madera", "Natural", 200.0, 120.0, 80.0, 75.0)
        with pytest.raises(ValueError):
            sup.largo = -50.0

    def test_getter_ancho(self, superficie_concreta_class):
        """Probar getter de ancho."""
        sup = superficie_concreta_class("Mesa", "Madera", "Natural", 200.0, 120.0, 90.0, 75.0)
        assert sup.ancho == 90.0

    def test_setter_ancho_valido(self, superficie_concreta_class):
        """Probar setter con ancho válido."""
        sup = superficie_concreta_class("Mesa", "Madera", "Natural", 200.0, 120.0, 80.0, 75.0)
        sup.ancho = 100.0
        assert sup.ancho == 100.0

    def test_setter_ancho_cero_error(self, superficie_concreta_class):
        """Probar que ancho = 0 genera error."""
        sup = superficie_concreta_class("Mesa", "Madera", "Natural", 200.0, 120.0, 80.0, 75.0)
        with pytest.raises(ValueError) as excinfo:
            sup.ancho = 0
        assert "ancho" in str(excinfo.value).lower()

    def test_setter_ancho_negativo_error(self, superficie_concreta_class):
        """Probar que ancho negativo genera error."""
        sup = superficie_concreta_class("Mesa", "Madera", "Natural", 200.0, 120.0, 80.0, 75.0)
        with pytest.raises(ValueError):
            sup.ancho = -30.0

    def test_getter_altura(self, superficie_concreta_class):
        """Probar getter de altura."""
        sup = superficie_concreta_class("Mesa", "Madera", "Natural", 200.0, 120.0, 80.0, 80.0)
        assert sup.altura == 80.0

    def test_setter_altura_valida(self, superficie_concreta_class):
        """Probar setter con altura válida."""
        sup = superficie_concreta_class("Mesa", "Madera", "Natural", 200.0, 120.0, 80.0, 75.0)
        sup.altura = 85.0
        assert sup.altura == 85.0

    def test_setter_altura_cero_error(self, superficie_concreta_class):
        """Probar que altura = 0 genera error."""
        sup = superficie_concreta_class("Mesa", "Madera", "Natural", 200.0, 120.0, 80.0, 75.0)
        with pytest.raises(ValueError) as excinfo:
            sup.altura = 0
        assert "altura" in str(excinfo.value).lower()

    def test_setter_altura_negativa_error(self, superficie_concreta_class):
        """Probar que altura negativa genera error."""
        sup = superficie_concreta_class("Mesa", "Madera", "Natural", 200.0, 120.0, 80.0, 75.0)
        with pytest.raises(ValueError):
            sup.altura = -20.0

    def test_calcular_area(self, superficie_concreta_class):
        """Probar cálculo de área."""
        sup = superficie_concreta_class("Mesa", "Madera", "Natural", 200.0, 100.0, 50.0, 75.0)
        area = sup.calcular_area()

        assert area == 5000.0  # 100 * 50

    def test_calcular_area_grande(self, superficie_concreta_class):
        """Probar cálculo de área más grande."""
        sup = superficie_concreta_class("Mesa", "Madera", "Natural", 200.0, 200.0, 100.0, 75.0)
        area = sup.calcular_area()

        assert area == 20000.0  # 200 * 100

    def test_calcular_factor_tamaño_basico(self, superficie_concreta_class):
        """Probar cálculo del factor de tamaño."""
        sup = superficie_concreta_class("Mesa", "Madera", "Natural", 200.0, 120.0, 80.0, 75.0)
        factor = sup.calcular_factor_tamaño()

        assert isinstance(factor, float)
        assert factor >= 1.0

    def test_calcular_factor_aumenta_con_area(self, superficie_concreta_class):
        """Probar que el factor aumenta con el área."""
        sup_pequeña = superficie_concreta_class(
            "Mesa", "Madera", "Natural", 200.0, 80.0, 60.0, 75.0
        )
        sup_grande = superficie_concreta_class(
            "Mesa", "Madera", "Natural", 200.0, 200.0, 120.0, 75.0
        )

        factor_pequeño = sup_pequeña.calcular_factor_tamaño()
        factor_grande = sup_grande.calcular_factor_tamaño()

        assert factor_grande > factor_pequeño

    def test_obtener_info_superficie(self, superficie_concreta_class):
        """Probar método de información."""
        sup = superficie_concreta_class("Mesa", "Madera", "Natural", 200.0, 150.0, 90.0, 75.0)
        info = sup.obtener_info_superficie()

        assert "150" in info
        assert "90" in info
        assert "75" in info
        assert "Dimensiones" in info or "dimensiones" in info.lower()

    def test_info_superficie_incluye_area(self, superficie_concreta_class):
        """Probar que la información incluye el área."""
        sup = superficie_concreta_class("Mesa", "Madera", "Natural", 200.0, 100.0, 50.0, 75.0)
        info = sup.obtener_info_superficie()

        assert "5000" in info  # área calculada
        assert "Área" in info or "área" in info.lower()

    @pytest.mark.parametrize(
        "largo,ancho,altura,area_esperada",
        [
            (100.0, 50.0, 75.0, 5000.0),
            (120.0, 80.0, 75.0, 9600.0),
            (200.0, 100.0, 75.0, 20000.0),
            (150.0, 90.0, 80.0, 13500.0),
        ],
    )
    def test_diferentes_dimensiones(
        self, superficie_concreta_class, largo, ancho, altura, area_esperada
    ):
        """Probar diferentes dimensiones y áreas."""
        sup = superficie_concreta_class("Mesa", "Madera", "Natural", 200.0, largo, ancho, altura)

        assert sup.largo == largo
        assert sup.ancho == ancho
        assert sup.altura == altura
        assert sup.calcular_area() == area_esperada
