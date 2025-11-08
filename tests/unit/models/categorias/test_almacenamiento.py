"""
Pruebas para la clase abstracta Almacenamiento.
"""

from abc import ABC

import pytest

from src.models.categorias.almacenamiento import Almacenamiento
from src.models.mueble import Mueble


class TestAlmacenamientoClaseAbstracta:
    """Pruebas para verificar que Almacenamiento es una clase abstracta."""

    def test_no_se_puede_instanciar_directamente(self):
        """Verificar que no se puede crear instancia directamente."""
        with pytest.raises(TypeError):
            almacenamiento = Almacenamiento("Armario", "Madera", "Blanco", 200.0, 5, 100.0)

    def test_hereda_de_mueble(self):
        """Verificar que hereda de Mueble."""
        assert issubclass(Almacenamiento, Mueble)

    def test_es_subclase_de_abc(self):
        """Verificar que es abstracta."""
        assert issubclass(Almacenamiento, ABC)

    def test_tiene_metodos_abstractos(self):
        """Verificar que mantiene los métodos abstractos."""
        assert hasattr(Almacenamiento, "calcular_precio")
        assert hasattr(Almacenamiento, "obtener_descripcion")


class TestAlmacenamientoFuncionalidad:
    """Pruebas de funcionalidad usando una clase concreta."""

    @pytest.fixture
    def almacenamiento_concreto_class(self):
        """Crear clase concreta para pruebas."""

        class AlmacenamientoConcreto(Almacenamiento):
            def calcular_precio(self) -> float:
                return self.precio_base * self.calcular_factor_almacenamiento()

            def obtener_descripcion(self) -> str:
                return f"{self.nombre}"

        return AlmacenamientoConcreto

    def test_inicializacion_correcta(self, almacenamiento_concreto_class):
        """Probar inicialización con valores válidos."""
        almac = almacenamiento_concreto_class("Armario", "Madera", "Blanco", 300.0, 4, 150.0)

        assert almac.nombre == "Armario"
        assert almac.material == "Madera"
        assert almac.color == "Blanco"
        assert almac.precio_base == 300.0
        assert almac.num_compartimentos == 4
        assert almac.capacidad_litros == 150.0

    def test_getter_num_compartimentos(self, almacenamiento_concreto_class):
        """Probar getter de compartimentos."""
        almac = almacenamiento_concreto_class("Armario", "Madera", "Blanco", 300.0, 5, 200.0)
        assert almac.num_compartimentos == 5

    def test_setter_num_compartimentos_valido(self, almacenamiento_concreto_class):
        """Probar setter con valor válido."""
        almac = almacenamiento_concreto_class("Armario", "Madera", "Blanco", 300.0, 5, 200.0)
        almac.num_compartimentos = 8
        assert almac.num_compartimentos == 8

    def test_setter_num_compartimentos_cero_error(self, almacenamiento_concreto_class):
        """Probar que compartimentos = 0 genera error."""
        almac = almacenamiento_concreto_class("Armario", "Madera", "Blanco", 300.0, 5, 200.0)
        with pytest.raises(ValueError) as excinfo:
            almac.num_compartimentos = 0
        assert "compartimentos" in str(excinfo.value).lower()

    def test_setter_num_compartimentos_negativo_error(self, almacenamiento_concreto_class):
        """Probar que compartimentos negativo genera error."""
        almac = almacenamiento_concreto_class("Armario", "Madera", "Blanco", 300.0, 5, 200.0)
        with pytest.raises(ValueError):
            almac.num_compartimentos = -1

    def test_getter_capacidad_litros(self, almacenamiento_concreto_class):
        """Probar getter de capacidad."""
        almac = almacenamiento_concreto_class("Armario", "Madera", "Blanco", 300.0, 5, 250.0)
        assert almac.capacidad_litros == 250.0

    def test_setter_capacidad_litros_valida(self, almacenamiento_concreto_class):
        """Probar setter con capacidad válida."""
        almac = almacenamiento_concreto_class("Armario", "Madera", "Blanco", 300.0, 5, 250.0)
        almac.capacidad_litros = 300.0
        assert almac.capacidad_litros == 300.0

    def test_setter_capacidad_litros_cero_error(self, almacenamiento_concreto_class):
        """Probar que capacidad = 0 genera error."""
        almac = almacenamiento_concreto_class("Armario", "Madera", "Blanco", 300.0, 5, 250.0)
        with pytest.raises(ValueError) as excinfo:
            almac.capacidad_litros = 0
        assert "capacidad" in str(excinfo.value).lower()

    def test_setter_capacidad_litros_negativa_error(self, almacenamiento_concreto_class):
        """Probar que capacidad negativa genera error."""
        almac = almacenamiento_concreto_class("Armario", "Madera", "Blanco", 300.0, 5, 250.0)
        with pytest.raises(ValueError):
            almac.capacidad_litros = -10.0

    def test_calcular_factor_almacenamiento_basico(self, almacenamiento_concreto_class):
        """Probar cálculo del factor de almacenamiento."""
        almac = almacenamiento_concreto_class("Armario", "Madera", "Blanco", 300.0, 1, 100.0)
        factor = almac.calcular_factor_almacenamiento()

        assert isinstance(factor, float)
        assert factor >= 1.0

    def test_calcular_factor_aumenta_con_compartimentos(self, almacenamiento_concreto_class):
        """Probar que el factor aumenta con más compartimentos."""
        almac1 = almacenamiento_concreto_class("Armario", "Madera", "Blanco", 300.0, 2, 100.0)
        almac2 = almacenamiento_concreto_class("Armario", "Madera", "Blanco", 300.0, 5, 100.0)

        factor1 = almac1.calcular_factor_almacenamiento()
        factor2 = almac2.calcular_factor_almacenamiento()

        assert factor2 > factor1

    def test_calcular_factor_aumenta_con_capacidad(self, almacenamiento_concreto_class):
        """Probar que el factor aumenta con más capacidad."""
        almac1 = almacenamiento_concreto_class("Armario", "Madera", "Blanco", 300.0, 3, 100.0)
        almac2 = almacenamiento_concreto_class("Armario", "Madera", "Blanco", 300.0, 3, 500.0)

        factor1 = almac1.calcular_factor_almacenamiento()
        factor2 = almac2.calcular_factor_almacenamiento()

        assert factor2 > factor1

    def test_obtener_info_almacenamiento(self, almacenamiento_concreto_class):
        """Probar método de información."""
        almac = almacenamiento_concreto_class("Armario", "Madera", "Blanco", 300.0, 6, 180.0)
        info = almac.obtener_info_almacenamiento()

        assert "6" in info
        assert "180" in info
        assert "Compartimentos" in info or "compartimentos" in info.lower()

    @pytest.mark.parametrize(
        "compartimentos,capacidad",
        [
            (1, 50.0),
            (3, 100.0),
            (5, 200.0),
            (10, 500.0),
        ],
    )
    def test_diferentes_configuraciones(
        self, almacenamiento_concreto_class, compartimentos, capacidad
    ):
        """Probar diferentes configuraciones válidas."""
        almac = almacenamiento_concreto_class(
            "Armario", "Madera", "Blanco", 300.0, compartimentos, capacidad
        )

        assert almac.num_compartimentos == compartimentos
        assert almac.capacidad_litros == capacidad
