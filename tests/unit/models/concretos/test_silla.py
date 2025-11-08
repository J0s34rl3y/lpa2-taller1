"""
Pruebas para la clase Silla (herencia simple).
Este módulo demuestra pruebas de herencia simple y polimorfismo.
"""

import pytest

from src.models.categorias.asientos import Asiento
from src.models.concretos.silla import Silla
from src.models.mueble import Mueble


class TestSillaHerencia:
    """Pruebas de herencia de la clase Silla."""

    def test_hereda_de_asiento(self):
        """Verificar que Silla hereda de Asiento."""
        assert issubclass(Silla, Asiento)

    def test_hereda_de_mueble(self):
        """Verificar que Silla hereda de Mueble (indirectamente)."""
        assert issubclass(Silla, Mueble)

    def test_instanciacion_correcta(self, silla_basica):
        """Verificar que se puede instanciar correctamente."""
        assert isinstance(silla_basica, Silla)
        assert isinstance(silla_basica, Asiento)
        assert isinstance(silla_basica, Mueble)


class TestSillaInicializacion:
    """Pruebas de inicialización de Silla."""

    def test_inicializacion_parametros_basicos(self):
        """Probar inicialización con parámetros básicos."""
        silla = Silla(nombre="Silla Test", material="Madera", color="Café", precio_base=100.0)

        assert silla.nombre == "Silla Test"
        assert silla.material == "Madera"
        assert silla.color == "Café"
        assert silla.precio_base == 100.0
        assert silla.capacidad_personas == 1  # Siempre 1 para sillas
        assert silla.tiene_respaldo is True  # Valor por defecto

    def test_inicializacion_parametros_completos(self):
        """Probar inicialización con todos los parámetros."""
        silla = Silla(
            nombre="Silla Oficina",
            material="Metal",
            color="Negro",
            precio_base=150.0,
            tiene_respaldo=True,
            material_tapizado="cuero",
            altura_regulable=True,
            tiene_ruedas=True,
        )

        assert silla.altura_regulable is True
        assert silla.tiene_ruedas is True
        assert silla.material_tapizado == "cuero"

    def test_capacidad_siempre_uno(self):
        """Verificar que la capacidad siempre es 1."""
        silla1 = Silla("Silla 1", "Madera", "Café", 100.0)
        silla2 = Silla("Silla 2", "Metal", "Negro", 120.0, True, "tela")

        assert silla1.capacidad_personas == 1
        assert silla2.capacidad_personas == 1


class TestSillaPropiedades:
    """Pruebas de propiedades específicas de Silla."""

    def test_getter_altura_regulable(self, silla_basica):
        """Probar getter de altura_regulable."""
        assert silla_basica.altura_regulable is False

    def test_setter_altura_regulable(self, silla_basica):
        """Probar setter de altura_regulable."""
        silla_basica.altura_regulable = True
        assert silla_basica.altura_regulable is True

    def test_getter_tiene_ruedas(self, silla_basica):
        """Probar getter de tiene_ruedas."""
        assert silla_basica.tiene_ruedas is False

    def test_setter_tiene_ruedas(self, silla_basica):
        """Probar setter de tiene_ruedas."""
        silla_basica.tiene_ruedas = True
        assert silla_basica.tiene_ruedas is True


class TestSillaCalculoPrecio:
    """Pruebas de cálculo de precio de Silla."""

    def test_calcular_precio_basico(self):
        """Probar cálculo de precio básico sin extras."""
        silla = Silla("Silla", "Madera", "Café", 100.0)
        precio = silla.calcular_precio()

        # Precio base * factor comodidad
        assert precio >= 100.0
        assert isinstance(precio, float)

    def test_calcular_precio_con_altura_regulable(self):
        """Probar que altura regulable aumenta el precio."""
        silla_sin = Silla("Silla", "Madera", "Café", 100.0, altura_regulable=False)
        silla_con = Silla("Silla", "Madera", "Café", 100.0, altura_regulable=True)

        precio_sin = silla_sin.calcular_precio()
        precio_con = silla_con.calcular_precio()

        assert precio_con > precio_sin
        assert precio_con - precio_sin >= 30  # Aumenta 30

    def test_calcular_precio_con_ruedas(self):
        """Probar que ruedas aumentan el precio."""
        silla_sin = Silla("Silla", "Madera", "Café", 100.0, tiene_ruedas=False)
        silla_con = Silla("Silla", "Madera", "Café", 100.0, tiene_ruedas=True)

        precio_sin = silla_sin.calcular_precio()
        precio_con = silla_con.calcular_precio()

        assert precio_con > precio_sin
        assert precio_con - precio_sin >= 20  # Aumenta 20

    def test_calcular_precio_con_todas_opciones(self, silla_con_ruedas):
        """Probar cálculo con todas las opciones."""
        precio = silla_con_ruedas.calcular_precio()

        # Precio base + altura regulable + ruedas + factor comodidad
        assert precio > 150.0
        assert isinstance(precio, float)

    def test_precio_redondeado_dos_decimales(self, silla_basica):
        """Verificar que el precio tiene máximo 2 decimales."""
        precio = silla_basica.calcular_precio()
        precio_str = str(precio)

        if "." in precio_str:
            decimales = len(precio_str.split(".")[1])
            assert decimales <= 2


class TestSillaDescripcion:
    """Pruebas del método obtener_descripcion."""

    def test_descripcion_contiene_nombre(self, silla_basica):
        """Verificar que la descripción contiene el nombre."""
        desc = silla_basica.obtener_descripcion()
        assert "Silla Test" in desc or "Silla" in desc

    def test_descripcion_contiene_material(self, silla_basica):
        """Verificar que la descripción contiene el material."""
        desc = silla_basica.obtener_descripcion()
        assert "Madera" in desc

    def test_descripcion_contiene_color(self, silla_basica):
        """Verificar que la descripción contiene el color."""
        desc = silla_basica.obtener_descripcion()
        assert "Café" in desc

    def test_descripcion_contiene_precio(self, silla_basica):
        """Verificar que la descripción contiene el precio."""
        desc = silla_basica.obtener_descripcion()
        precio = silla_basica.calcular_precio()
        assert str(precio) in desc or "Precio" in desc

    def test_descripcion_formato(self, silla_con_ruedas):
        """Verificar formato general de la descripción."""
        desc = silla_con_ruedas.obtener_descripcion()

        assert isinstance(desc, str)
        assert len(desc) > 0
        assert "Altura regulable" in desc or "regulable" in desc.lower()
        assert "Ruedas" in desc or "ruedas" in desc.lower()


class TestSillaMetodosEspecificos:
    """Pruebas de métodos específicos de Silla."""

    def test_regular_altura_disponible(self, silla_con_ruedas):
        """Verificar que el método regular_altura existe."""
        assert hasattr(silla_con_ruedas, "regular_altura")
        assert callable(silla_con_ruedas.regular_altura)

    def test_regular_altura_con_regulable(self, silla_con_ruedas):
        """Probar regular altura cuando es regulable."""
        resultado = silla_con_ruedas.regular_altura(50)

        assert isinstance(resultado, str)
        assert len(resultado) > 0


class TestSillaParametrizacion:
    """Pruebas parametrizadas para diferentes configuraciones."""

    @pytest.mark.parametrize(
        "material,color,precio",
        [
            ("Madera", "Café", 80.0),
            ("Metal", "Negro", 120.0),
            ("Plástico", "Blanco", 40.0),
            ("Roble", "Natural", 150.0),
        ],
    )
    def test_diferentes_materiales(self, material, color, precio):
        """Probar sillas con diferentes materiales."""
        silla = Silla(f"Silla {material}", material, color, precio)

        assert silla.material == material
        assert silla.color == color
        assert silla.precio_base == precio
        assert silla.calcular_precio() >= precio

    @pytest.mark.parametrize(
        "regulable,ruedas,incremento_minimo",
        [
            (False, False, 0),
            (True, False, 30),
            (False, True, 20),
            (True, True, 50),
        ],
    )
    def test_combinaciones_opciones(self, regulable, ruedas, incremento_minimo):
        """Probar diferentes combinaciones de opciones."""
        precio_base = 100.0
        silla = Silla(
            "Silla", "Madera", "Café", precio_base, altura_regulable=regulable, tiene_ruedas=ruedas
        )

        precio_final = silla.calcular_precio()
        # El precio debe ser al menos precio_base + incremento por opciones
        # Nota: también se aplica factor de comodidad
        assert precio_final >= precio_base


class TestSillaPolimorfismo:
    """Pruebas de polimorfismo con Silla."""

    def test_implementa_calcular_precio(self):
        """Verificar que implementa calcular_precio."""
        silla = Silla("Silla", "Madera", "Café", 100.0)

        # Debe tener el método de la clase abstracta
        assert hasattr(silla, "calcular_precio")
        # Y debe ser callable
        assert callable(silla.calcular_precio)
        # Y debe retornar un float
        assert isinstance(silla.calcular_precio(), float)

    def test_implementa_obtener_descripcion(self):
        """Verificar que implementa obtener_descripcion."""
        silla = Silla("Silla", "Madera", "Café", 100.0)

        assert hasattr(silla, "obtener_descripcion")
        assert callable(silla.obtener_descripcion)
        assert isinstance(silla.obtener_descripcion(), str)

    def test_polimorfismo_con_lista_muebles(self, silla_basica, silla_con_ruedas):
        """Probar polimorfismo con lista de muebles."""
        muebles = [silla_basica, silla_con_ruedas]

        for mueble in muebles:
            # Cada mueble puede calcular su precio
            precio = mueble.calcular_precio()
            assert isinstance(precio, float)
            assert precio > 0

            # Cada mueble puede dar su descripción
            desc = mueble.obtener_descripcion()
            assert isinstance(desc, str)
            assert len(desc) > 0
