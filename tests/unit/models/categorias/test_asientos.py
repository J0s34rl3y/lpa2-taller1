"""
Pruebas para la clase abstracta Asiento.
"""

from abc import ABC

import pytest

from src.models.categorias.asientos import Asiento
from src.models.mueble import Mueble


class TestAsientoClaseAbstracta:
    """Pruebas para verificar que Asiento es una clase abstracta."""

    def test_no_se_puede_instanciar_directamente(self):
        """Verificar que no se puede crear instancia directamente."""
        with pytest.raises(TypeError):
            asiento = Asiento("Silla", "Madera", "Café", 100.0, 1, True, "tela")

    def test_hereda_de_mueble(self):
        """Verificar que hereda de Mueble."""
        assert issubclass(Asiento, Mueble)

    def test_es_subclase_de_abc(self):
        """Verificar que es abstracta."""
        assert issubclass(Asiento, ABC)

    def test_tiene_metodos_abstractos(self):
        """Verificar que mantiene los métodos abstractos."""
        assert hasattr(Asiento, "calcular_precio")
        assert hasattr(Asiento, "obtener_descripcion")


class TestAsientoFuncionalidad:
    """Pruebas de funcionalidad usando una clase concreta."""

    @pytest.fixture
    def asiento_concreto_class(self):
        """Crear clase concreta para pruebas."""

        class AsientoConcreto(Asiento):
            def calcular_precio(self) -> float:
                return self.precio_base * self.calcular_factor_comodidad()

            def obtener_descripcion(self) -> str:
                return f"{self.nombre}"

        return AsientoConcreto

    def test_inicializacion_correcta(self, asiento_concreto_class):
        """Probar inicialización con valores válidos."""
        asiento = asiento_concreto_class("Silla", "Madera", "Café", 100.0, 1, True, "tela")

        assert asiento.nombre == "Silla"
        assert asiento.material == "Madera"
        assert asiento.color == "Café"
        assert asiento.precio_base == 100.0
        assert asiento.capacidad_personas == 1
        assert asiento.tiene_respaldo is True
        assert asiento.material_tapizado == "tela"

    def test_inicializacion_sin_tapizado(self, asiento_concreto_class):
        """Probar inicialización sin material tapizado."""
        asiento = asiento_concreto_class("Banqueta", "Metal", "Negro", 50.0, 1, False, None)

        assert asiento.material_tapizado is None

    def test_getter_capacidad_personas(self, asiento_concreto_class):
        """Probar getter de capacidad."""
        asiento = asiento_concreto_class("Sofá", "Madera", "Gris", 300.0, 3, True, "cuero")
        assert asiento.capacidad_personas == 3

    def test_setter_capacidad_personas_valida(self, asiento_concreto_class):
        """Probar setter con capacidad válida."""
        asiento = asiento_concreto_class("Sofá", "Madera", "Gris", 300.0, 3, True, "cuero")
        asiento.capacidad_personas = 4
        assert asiento.capacidad_personas == 4

    def test_setter_capacidad_personas_cero_error(self, asiento_concreto_class):
        """Probar que capacidad = 0 genera error."""
        asiento = asiento_concreto_class("Silla", "Madera", "Café", 100.0, 1, True, "tela")
        with pytest.raises(ValueError) as excinfo:
            asiento.capacidad_personas = 0
        assert "capacidad" in str(excinfo.value).lower()

    def test_setter_capacidad_personas_negativa_error(self, asiento_concreto_class):
        """Probar que capacidad negativa genera error."""
        asiento = asiento_concreto_class("Silla", "Madera", "Café", 100.0, 1, True, "tela")
        with pytest.raises(ValueError):
            asiento.capacidad_personas = -1

    def test_getter_tiene_respaldo(self, asiento_concreto_class):
        """Probar getter de respaldo."""
        asiento = asiento_concreto_class("Silla", "Madera", "Café", 100.0, 1, True, "tela")
        assert asiento.tiene_respaldo is True

    def test_setter_tiene_respaldo(self, asiento_concreto_class):
        """Probar setter de respaldo."""
        asiento = asiento_concreto_class("Silla", "Madera", "Café", 100.0, 1, True, "tela")
        asiento.tiene_respaldo = False
        assert asiento.tiene_respaldo is False

    def test_getter_material_tapizado(self, asiento_concreto_class):
        """Probar getter de material tapizado."""
        asiento = asiento_concreto_class("Silla", "Madera", "Café", 100.0, 1, True, "cuero")
        assert asiento.material_tapizado == "cuero"

    def test_setter_material_tapizado(self, asiento_concreto_class):
        """Probar setter de material tapizado."""
        asiento = asiento_concreto_class("Silla", "Madera", "Café", 100.0, 1, True, "tela")
        asiento.material_tapizado = "cuero"
        assert asiento.material_tapizado == "cuero"

    def test_calcular_factor_comodidad_basico(self, asiento_concreto_class):
        """Probar cálculo del factor de comodidad básico."""
        asiento = asiento_concreto_class("Banqueta", "Metal", "Negro", 50.0, 1, False, None)
        factor = asiento.calcular_factor_comodidad()

        assert isinstance(factor, float)
        assert factor >= 1.0

    def test_calcular_factor_con_respaldo(self, asiento_concreto_class):
        """Probar que el factor aumenta con respaldo."""
        asiento_sin = asiento_concreto_class("Banqueta", "Metal", "Negro", 50.0, 1, False, None)
        asiento_con = asiento_concreto_class("Silla", "Metal", "Negro", 50.0, 1, True, None)

        factor_sin = asiento_sin.calcular_factor_comodidad()
        factor_con = asiento_con.calcular_factor_comodidad()

        assert factor_con > factor_sin

    def test_calcular_factor_con_tapizado_cuero(self, asiento_concreto_class):
        """Probar que cuero aumenta más el factor."""
        asiento_sin = asiento_concreto_class("Silla", "Madera", "Café", 100.0, 1, True, None)
        asiento_cuero = asiento_concreto_class("Silla", "Madera", "Café", 100.0, 1, True, "cuero")

        factor_sin = asiento_sin.calcular_factor_comodidad()
        factor_cuero = asiento_cuero.calcular_factor_comodidad()

        assert factor_cuero > factor_sin

    def test_calcular_factor_con_tapizado_tela(self, asiento_concreto_class):
        """Probar que tela aumenta el factor."""
        asiento_sin = asiento_concreto_class("Silla", "Madera", "Café", 100.0, 1, True, None)
        asiento_tela = asiento_concreto_class("Silla", "Madera", "Café", 100.0, 1, True, "tela")

        factor_sin = asiento_sin.calcular_factor_comodidad()
        factor_tela = asiento_tela.calcular_factor_comodidad()

        assert factor_tela > factor_sin

    def test_calcular_factor_cuero_mayor_que_tela(self, asiento_concreto_class):
        """Probar que cuero da mayor factor que tela."""
        asiento_tela = asiento_concreto_class("Silla", "Madera", "Café", 100.0, 1, True, "tela")
        asiento_cuero = asiento_concreto_class("Silla", "Madera", "Café", 100.0, 1, True, "cuero")

        factor_tela = asiento_tela.calcular_factor_comodidad()
        factor_cuero = asiento_cuero.calcular_factor_comodidad()

        assert factor_cuero > factor_tela

    def test_calcular_factor_aumenta_con_capacidad(self, asiento_concreto_class):
        """Probar que el factor aumenta con más capacidad."""
        asiento1 = asiento_concreto_class("Silla", "Madera", "Café", 100.0, 1, True, None)
        asiento3 = asiento_concreto_class("Sofá", "Madera", "Café", 100.0, 3, True, None)

        factor1 = asiento1.calcular_factor_comodidad()
        factor3 = asiento3.calcular_factor_comodidad()

        assert factor3 > factor1

    def test_obtener_info_asiento_completo(self, asiento_concreto_class):
        """Probar método de información completo."""
        asiento = asiento_concreto_class("Silla", "Madera", "Café", 100.0, 2, True, "cuero")
        info = asiento.obtener_info_asiento()

        assert "2" in info
        assert "cuero" in info.lower()
        assert "Capacidad" in info or "capacidad" in info.lower()

    def test_obtener_info_asiento_sin_tapizado(self, asiento_concreto_class):
        """Probar método de información sin tapizado."""
        asiento = asiento_concreto_class("Banqueta", "Metal", "Negro", 50.0, 1, False, None)
        info = asiento.obtener_info_asiento()

        assert "1" in info
        assert "No" in info or "no" in info.lower()

    @pytest.mark.parametrize(
        "capacidad,respaldo,tapizado",
        [
            (1, True, "tela"),
            (2, True, "cuero"),
            (3, True, None),
            (1, False, None),
        ],
    )
    def test_diferentes_configuraciones(
        self, asiento_concreto_class, capacidad, respaldo, tapizado
    ):
        """Probar diferentes configuraciones válidas."""
        asiento = asiento_concreto_class(
            "Asiento", "Madera", "Café", 100.0, capacidad, respaldo, tapizado
        )

        assert asiento.capacidad_personas == capacidad
        assert asiento.tiene_respaldo == respaldo
        assert asiento.material_tapizado == tapizado
