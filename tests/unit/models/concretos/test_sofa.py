"""
Pruebas para la clase Sofa.
"""

import pytest

from src.models.categorias.asientos import Asiento
from src.models.concretos.sofa import Sofa
from src.models.mueble import Mueble


class TestSofaHerencia:
    """Pruebas de herencia de Sofa."""

    def test_hereda_de_asiento(self):
        """Verificar que Sofa hereda de Asiento."""
        assert issubclass(Sofa, Asiento)

    def test_hereda_de_mueble_indirecto(self):
        """Verificar herencia indirecta de Mueble."""
        assert issubclass(Sofa, Mueble)

    def test_instanciacion_correcta(self):
        """Verificar que se puede instanciar correctamente."""
        sofa = Sofa("Sofá", "Madera", "Gris", 500.0)
        assert isinstance(sofa, Sofa)
        assert isinstance(sofa, Asiento)
        assert isinstance(sofa, Mueble)


class TestSofaInicializacion:
    """Pruebas de inicialización de Sofa."""

    def test_inicializacion_basica(self):
        """Probar inicialización con parámetros básicos."""
        sofa = Sofa("Sofá Test", "Madera", "Gris", 500.0)

        assert sofa.nombre == "Sofá Test"
        assert sofa.material == "Madera"
        assert sofa.color == "Gris"
        assert sofa.precio_base == 500.0

    def test_inicializacion_valores_por_defecto(self):
        """Probar valores por defecto."""
        sofa = Sofa("Sofá", "Madera", "Gris", 500.0)

        assert sofa.capacidad_personas == 3
        assert sofa.tiene_respaldo is True
        assert sofa.material_tapizado is None
        assert sofa.tiene_brazos is True
        assert sofa.es_modular is False
        assert sofa.incluye_cojines is False

    def test_inicializacion_completa(self):
        """Probar inicialización con todos los parámetros."""
        sofa = Sofa(
            "Sofá Modular",
            "Madera",
            "Beige",
            700.0,
            capacidad_personas=4,
            tiene_respaldo=True,
            material_tapizado="cuero",
            tiene_brazos=True,
            es_modular=True,
            incluye_cojines=True,
        )

        assert sofa.capacidad_personas == 4
        assert sofa.material_tapizado == "cuero"
        assert sofa.es_modular is True
        assert sofa.incluye_cojines is True


class TestSofaPropiedades:
    """Pruebas de propiedades de Sofa."""

    def test_getter_tiene_brazos(self):
        """Probar getter de tiene_brazos."""
        sofa = Sofa("Sofá", "Madera", "Gris", 500.0, tiene_brazos=True)
        assert sofa.tiene_brazos is True

    def test_getter_es_modular(self):
        """Probar getter de es_modular."""
        sofa = Sofa("Sofá", "Madera", "Gris", 500.0, es_modular=True)
        assert sofa.es_modular is True

    def test_getter_incluye_cojines(self):
        """Probar getter de incluye_cojines."""
        sofa = Sofa("Sofá", "Madera", "Gris", 500.0, incluye_cojines=True)
        assert sofa.incluye_cojines is True


class TestSofaCalculoPrecio:
    """Pruebas de cálculo de precio de Sofa."""

    def test_calcular_precio_basico(self):
        """Probar cálculo de precio básico."""
        sofa = Sofa("Sofá", "Madera", "Gris", 500.0)
        precio = sofa.calcular_precio()

        # Precio base * factor comodidad + extras
        assert precio >= 500.0
        assert isinstance(precio, float)

    def test_precio_con_brazos(self):
        """Probar que los brazos aumentan el precio."""
        sofa_sin = Sofa("Sofá", "Madera", "Gris", 500.0, tiene_brazos=False)
        sofa_con = Sofa("Sofá", "Madera", "Gris", 500.0, tiene_brazos=True)

        precio_sin = sofa_sin.calcular_precio()
        precio_con = sofa_con.calcular_precio()

        assert precio_con > precio_sin

    def test_precio_modular(self):
        """Probar que ser modular aumenta el precio."""
        sofa_normal = Sofa("Sofá", "Madera", "Gris", 500.0, es_modular=False)
        sofa_modular = Sofa("Sofá", "Madera", "Gris", 500.0, es_modular=True)

        precio_normal = sofa_normal.calcular_precio()
        precio_modular = sofa_modular.calcular_precio()

        assert precio_modular > precio_normal

    def test_precio_con_cojines(self):
        """Probar que los cojines aumentan el precio."""
        sofa_sin = Sofa("Sofá", "Madera", "Gris", 500.0, incluye_cojines=False)
        sofa_con = Sofa("Sofá", "Madera", "Gris", 500.0, incluye_cojines=True)

        precio_sin = sofa_sin.calcular_precio()
        precio_con = sofa_con.calcular_precio()

        assert precio_con > precio_sin

    def test_precio_aumenta_con_capacidad(self):
        """Probar que mayor capacidad aumenta el precio (por factor comodidad)."""
        sofa_2 = Sofa("Sofá", "Madera", "Gris", 500.0, capacidad_personas=2)
        sofa_4 = Sofa("Sofá", "Madera", "Gris", 500.0, capacidad_personas=4)

        precio_2 = sofa_2.calcular_precio()
        precio_4 = sofa_4.calcular_precio()

        assert precio_4 > precio_2

    def test_precio_con_tapizado_cuero(self):
        """Probar que tapizado de cuero aumenta más el precio."""
        sofa_sin = Sofa("Sofá", "Madera", "Gris", 500.0, material_tapizado=None)
        sofa_cuero = Sofa("Sofá", "Madera", "Gris", 500.0, material_tapizado="cuero")

        precio_sin = sofa_sin.calcular_precio()
        precio_cuero = sofa_cuero.calcular_precio()

        assert precio_cuero > precio_sin


class TestSofaDescripcion:
    """Pruebas del método obtener_descripcion."""

    def test_obtener_descripcion_contiene_nombre(self):
        """Verificar que la descripción contiene el nombre."""
        sofa = Sofa("Sofá Test", "Madera", "Gris", 500.0)
        desc = sofa.obtener_descripcion()

        assert "Sofá" in desc

    def test_obtener_descripcion_contiene_material(self):
        """Verificar que la descripción contiene el material."""
        sofa = Sofa("Sofá", "Cuero", "Negro", 500.0)
        desc = sofa.obtener_descripcion()

        assert "Cuero" in desc

    def test_obtener_descripcion_contiene_caracteristicas(self):
        """Verificar que la descripción contiene características."""
        sofa = Sofa("Sofá", "Madera", "Gris", 500.0, es_modular=True, incluye_cojines=True)
        desc = sofa.obtener_descripcion()

        assert "Modular" in desc or "modular" in desc.lower()

    def test_obtener_descripcion_contiene_precio(self):
        """Verificar que la descripción contiene el precio."""
        sofa = Sofa("Sofá", "Madera", "Gris", 500.0)
        desc = sofa.obtener_descripcion()

        assert "Precio" in desc or "precio" in desc.lower()


class TestSofaParametrizacion:
    """Pruebas parametrizadas para diferentes configuraciones."""

    @pytest.mark.parametrize("capacidad", [2, 3, 4, 5])
    def test_diferentes_capacidades(self, capacidad):
        """Probar sofás con diferentes capacidades."""
        sofa = Sofa("Sofá", "Madera", "Gris", 500.0, capacidad_personas=capacidad)

        assert sofa.capacidad_personas == capacidad
        assert sofa.calcular_precio() > 500.0

    @pytest.mark.parametrize(
        "brazos,modular,cojines",
        [
            (True, False, False),
            (False, True, False),
            (False, False, True),
            (True, True, True),
        ],
    )
    def test_combinaciones_opciones(self, brazos, modular, cojines):
        """Probar diferentes combinaciones de opciones."""
        sofa = Sofa(
            "Sofá",
            "Madera",
            "Gris",
            500.0,
            tiene_brazos=brazos,
            es_modular=modular,
            incluye_cojines=cojines,
        )

        precio = sofa.calcular_precio()
        assert precio > 500.0  # Siempre mayor por factor comodidad

    @pytest.mark.parametrize(
        "material,color",
        [
            ("Madera", "Gris"),
            ("Tela", "Beige"),
            ("Cuero", "Negro"),
        ],
    )
    def test_diferentes_materiales(self, material, color):
        """Probar sofás con diferentes materiales."""
        sofa = Sofa("Sofá", material, color, 500.0)

        assert sofa.material == material
        assert sofa.color == color
        assert sofa.calcular_precio() >= 500.0

    @pytest.mark.parametrize("tapizado", [None, "tela", "cuero"])
    def test_diferentes_tapizados(self, tapizado):
        """Probar sofás con diferentes tapizados."""
        sofa = Sofa("Sofá", "Madera", "Gris", 500.0, material_tapizado=tapizado)

        assert sofa.material_tapizado == tapizado
        precio = sofa.calcular_precio()
        assert precio > 0
