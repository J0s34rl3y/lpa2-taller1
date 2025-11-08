"""
Pruebas para la clase abstracta Mueble.
Este módulo prueba que Mueble es correctamente abstracta y define la interfaz base.
"""

from abc import ABC

import pytest

from src.models.mueble import Mueble


class TestMuebleClaseAbstracta:
    """Pruebas para verificar que Mueble es una clase abstracta."""

    def test_no_se_puede_instanciar_directamente(self):
        """Verificar que no se puede crear una instancia de Mueble directamente."""
        with pytest.raises(TypeError) as excinfo:
            mueble = Mueble("Mesa", "Madera", "Café", 100.0)

        assert "abstract" in str(excinfo.value).lower()

    def test_es_subclase_de_abc(self):
        """Verificar que Mueble hereda de ABC."""
        assert issubclass(Mueble, ABC)

    def test_tiene_metodos_abstractos(self):
        """Verificar que tiene los métodos abstractos requeridos."""
        assert hasattr(Mueble, "calcular_precio")
        assert hasattr(Mueble, "obtener_descripcion")

        # Verificar que son abstractos
        assert Mueble.calcular_precio.__isabstractmethod__
        assert Mueble.obtener_descripcion.__isabstractmethod__

    def test_cantidad_metodos_abstractos(self):
        """Verificar que tiene exactamente 2 métodos abstractos."""
        abstract_methods = [
            method
            for method in dir(Mueble)
            if hasattr(getattr(Mueble, method), "__isabstractmethod__")
            and getattr(Mueble, method).__isabstractmethod__
        ]
        assert len(abstract_methods) == 2


class TestMuebleConClaseConcreta:
    """Pruebas usando una clase concreta simple para probar funcionalidad de Mueble."""

    @pytest.fixture
    def mueble_concreto_class(self):
        """Crear una clase concreta temporal para pruebas."""

        class MuebleConcreto(Mueble):
            def calcular_precio(self) -> float:
                return self.precio_base

            def obtener_descripcion(self) -> str:
                return f"{self.nombre} - {self.material}"

        return MuebleConcreto

    def test_inicializacion_con_valores_validos(self, mueble_concreto_class):
        """Probar inicialización con valores válidos."""
        mueble = mueble_concreto_class("Mesa", "Madera", "Café", 100.0)

        assert mueble.nombre == "Mesa"
        assert mueble.material == "Madera"
        assert mueble.color == "Café"
        assert mueble.precio_base == 100.0

    def test_getter_nombre(self, mueble_concreto_class):
        """Probar el getter de nombre."""
        mueble = mueble_concreto_class("Silla", "Metal", "Negro", 50.0)
        assert mueble.nombre == "Silla"

    def test_setter_nombre_valido(self, mueble_concreto_class):
        """Probar el setter de nombre con valor válido."""
        mueble = mueble_concreto_class("Mesa", "Madera", "Café", 100.0)
        mueble.nombre = "Mesa Nueva"
        assert mueble.nombre == "Mesa Nueva"

    def test_setter_nombre_con_espacios(self, mueble_concreto_class):
        """Probar que el setter elimina espacios extra."""
        mueble = mueble_concreto_class("Mesa", "Madera", "Café", 100.0)
        mueble.nombre = "  Mesa con espacios  "
        assert mueble.nombre == "Mesa con espacios"

    def test_setter_nombre_vacio_error(self, mueble_concreto_class):
        """Probar que nombre vacío genera error."""
        mueble = mueble_concreto_class("Mesa", "Madera", "Café", 100.0)
        with pytest.raises(ValueError) as excinfo:
            mueble.nombre = ""
        assert "nombre" in str(excinfo.value).lower()

    def test_setter_nombre_solo_espacios_error(self, mueble_concreto_class):
        """Probar que nombre con solo espacios genera error."""
        mueble = mueble_concreto_class("Mesa", "Madera", "Café", 100.0)
        with pytest.raises(ValueError) as excinfo:
            mueble.nombre = "   "
        assert "nombre" in str(excinfo.value).lower()

    def test_getter_material(self, mueble_concreto_class):
        """Probar el getter de material."""
        mueble = mueble_concreto_class("Silla", "Metal", "Negro", 50.0)
        assert mueble.material == "Metal"

    def test_setter_material_valido(self, mueble_concreto_class):
        """Probar el setter de material con valor válido."""
        mueble = mueble_concreto_class("Mesa", "Madera", "Café", 100.0)
        mueble.material = "Roble"
        assert mueble.material == "Roble"

    def test_setter_material_vacio_error(self, mueble_concreto_class):
        """Probar que material vacío genera error."""
        mueble = mueble_concreto_class("Mesa", "Madera", "Café", 100.0)
        with pytest.raises(ValueError) as excinfo:
            mueble.material = ""
        assert "material" in str(excinfo.value).lower()

    def test_getter_color(self, mueble_concreto_class):
        """Probar el getter de color."""
        mueble = mueble_concreto_class("Silla", "Metal", "Negro", 50.0)
        assert mueble.color == "Negro"

    def test_setter_color_valido(self, mueble_concreto_class):
        """Probar el setter de color con valor válido."""
        mueble = mueble_concreto_class("Mesa", "Madera", "Café", 100.0)
        mueble.color = "Azul"
        assert mueble.color == "Azul"

    def test_setter_color_vacio_error(self, mueble_concreto_class):
        """Probar que color vacío genera error."""
        mueble = mueble_concreto_class("Mesa", "Madera", "Café", 100.0)
        with pytest.raises(ValueError) as excinfo:
            mueble.color = ""
        assert "color" in str(excinfo.value).lower()

    def test_getter_precio_base(self, mueble_concreto_class):
        """Probar el getter de precio_base."""
        mueble = mueble_concreto_class("Silla", "Metal", "Negro", 150.0)
        assert mueble.precio_base == 150.0

    def test_setter_precio_base_valido(self, mueble_concreto_class):
        """Probar el setter de precio_base con valor válido."""
        mueble = mueble_concreto_class("Mesa", "Madera", "Café", 100.0)
        mueble.precio_base = 200.0
        assert mueble.precio_base == 200.0

    def test_setter_precio_base_cero(self, mueble_concreto_class):
        """Probar que precio_base = 0 es válido."""
        mueble = mueble_concreto_class("Mesa", "Madera", "Café", 100.0)
        mueble.precio_base = 0.0
        assert mueble.precio_base == 0.0

    def test_setter_precio_base_negativo_error(self, mueble_concreto_class):
        """Probar que precio_base negativo genera error."""
        mueble = mueble_concreto_class("Mesa", "Madera", "Café", 100.0)
        with pytest.raises(ValueError) as excinfo:
            mueble.precio_base = -50.0
        assert "precio" in str(excinfo.value).lower()

    def test_str_method(self, mueble_concreto_class):
        """Probar el método __str__."""
        mueble = mueble_concreto_class("Mesa", "Roble", "Natural", 200.0)
        resultado = str(mueble)

        assert "Mesa" in resultado
        assert "Roble" in resultado
        assert "Natural" in resultado

    def test_repr_method(self, mueble_concreto_class):
        """Probar el método __repr__."""
        mueble = mueble_concreto_class("Silla", "Metal", "Negro", 100.0)
        resultado = repr(mueble)

        assert "Mueble" in resultado
        assert "Silla" in resultado
        assert "Metal" in resultado
        assert "Negro" in resultado
        assert "100.0" in resultado


class TestMuebleParametrizacion:
    """Pruebas parametrizadas para probar múltiples casos."""

    @pytest.fixture
    def mueble_concreto_class(self):
        """Crear una clase concreta temporal para pruebas."""

        class MuebleConcreto(Mueble):
            def calcular_precio(self) -> float:
                return self.precio_base

            def obtener_descripcion(self) -> str:
                return f"{self.nombre}"

        return MuebleConcreto

    @pytest.mark.parametrize(
        "nombre,material,color,precio",
        [
            ("Mesa", "Madera", "Café", 100.0),
            ("Silla", "Metal", "Negro", 50.0),
            ("Sofá", "Tela", "Gris", 500.0),
            ("Cama", "Roble", "Blanco", 300.0),
        ],
    )
    def test_diferentes_combinaciones_validas(
        self, mueble_concreto_class, nombre, material, color, precio
    ):
        """Probar diferentes combinaciones válidas de atributos."""
        mueble = mueble_concreto_class(nombre, material, color, precio)

        assert mueble.nombre == nombre
        assert mueble.material == material
        assert mueble.color == color
        assert mueble.precio_base == precio

    @pytest.mark.parametrize("precio_invalido", [-1, -10.0, -100.5, -0.01])
    def test_precios_negativos_invalidos(self, mueble_concreto_class, precio_invalido):
        """Probar que diferentes valores negativos son inválidos."""
        with pytest.raises(ValueError):
            mueble = mueble_concreto_class("Mesa", "Madera", "Café", precio_invalido)
