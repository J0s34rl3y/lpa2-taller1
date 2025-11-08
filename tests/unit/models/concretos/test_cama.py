"""
Pruebas para la clase Cama.
"""

import pytest

from src.models.concretos.cama import Cama
from src.models.mueble import Mueble


class TestCamaHerencia:
    """Pruebas de herencia de Cama."""

    def test_hereda_de_mueble(self):
        """Verificar que Cama hereda de Mueble."""
        assert issubclass(Cama, Mueble)

    def test_instanciacion_correcta(self):
        """Verificar que se puede instanciar correctamente."""
        cama = Cama("Cama", "Madera", "Blanco", 300.0)
        assert isinstance(cama, Cama)
        assert isinstance(cama, Mueble)


class TestCamaInicializacion:
    """Pruebas de inicialización de Cama."""

    def test_inicializacion_basica(self):
        """Probar inicialización con parámetros básicos."""
        cama = Cama("Cama Test", "Madera", "Blanco", 300.0)

        assert cama.nombre == "Cama Test"
        assert cama.material == "Madera"
        assert cama.color == "Blanco"
        assert cama.precio_base == 300.0

    def test_inicializacion_valores_por_defecto(self):
        """Probar valores por defecto."""
        cama = Cama("Cama", "Madera", "Blanco", 300.0)

        assert cama.tamaño == "individual"
        assert cama.incluye_colchon is False
        assert cama.tiene_cabecera is False

    def test_inicializacion_completa(self):
        """Probar inicialización con todos los parámetros."""
        cama = Cama(
            "Cama Queen",
            "Roble",
            "Natural",
            500.0,
            tamaño="queen",
            incluye_colchon=True,
            tiene_cabecera=True,
        )

        assert cama.tamaño == "queen"
        assert cama.incluye_colchon is True
        assert cama.tiene_cabecera is True


class TestCamaPropiedades:
    """Pruebas de propiedades de Cama."""

    def test_getter_tamaño(self):
        """Probar getter de tamaño."""
        cama = Cama("Cama", "Madera", "Blanco", 300.0, tamaño="matrimonial")
        assert cama.tamaño == "matrimonial"

    def test_setter_tamaño_valido(self):
        """Probar setter con tamaño válido."""
        cama = Cama("Cama", "Madera", "Blanco", 300.0)
        cama.tamaño = "queen"
        assert cama.tamaño == "queen"

    def test_setter_tamaño_invalido_error(self):
        """Probar que tamaño inválido genera error."""
        cama = Cama("Cama", "Madera", "Blanco", 300.0)
        with pytest.raises(ValueError):
            cama.tamaño = "gigante"

    def test_tamaños_validos(self):
        """Probar todos los tamaños válidos."""
        tamaños = ["individual", "matrimonial", "queen", "king"]
        for tamaño in tamaños:
            cama = Cama("Cama", "Madera", "Blanco", 300.0, tamaño=tamaño)
            assert cama.tamaño == tamaño


class TestCamaCalculoPrecio:
    """Pruebas de cálculo de precio de Cama."""

    def test_calcular_precio_basico(self):
        """Probar cálculo de precio básico."""
        cama = Cama("Cama", "Madera", "Blanco", 300.0, tamaño="individual")
        precio = cama.calcular_precio()

        assert precio == 300.0
        assert isinstance(precio, float)

    def test_precio_aumenta_con_tamaño_matrimonial(self):
        """Probar que tamaño matrimonial aumenta el precio."""
        cama_ind = Cama("Cama", "Madera", "Blanco", 300.0, tamaño="individual")
        cama_mat = Cama("Cama", "Madera", "Blanco", 300.0, tamaño="matrimonial")

        precio_ind = cama_ind.calcular_precio()
        precio_mat = cama_mat.calcular_precio()

        assert precio_mat > precio_ind
        assert precio_mat - precio_ind == 200.0

    def test_precio_aumenta_con_tamaño_queen(self):
        """Probar que tamaño queen aumenta más el precio."""
        cama_mat = Cama("Cama", "Madera", "Blanco", 300.0, tamaño="matrimonial")
        cama_queen = Cama("Cama", "Madera", "Blanco", 300.0, tamaño="queen")

        precio_mat = cama_mat.calcular_precio()
        precio_queen = cama_queen.calcular_precio()

        assert precio_queen > precio_mat

    def test_precio_aumenta_con_tamaño_king(self):
        """Probar que tamaño king es el más caro."""
        cama_queen = Cama("Cama", "Madera", "Blanco", 300.0, tamaño="queen")
        cama_king = Cama("Cama", "Madera", "Blanco", 300.0, tamaño="king")

        precio_queen = cama_queen.calcular_precio()
        precio_king = cama_king.calcular_precio()

        assert precio_king > precio_queen

    def test_precio_con_colchon(self):
        """Probar que incluir colchón aumenta el precio."""
        cama_sin = Cama("Cama", "Madera", "Blanco", 300.0, incluye_colchon=False)
        cama_con = Cama("Cama", "Madera", "Blanco", 300.0, incluye_colchon=True)

        precio_sin = cama_sin.calcular_precio()
        precio_con = cama_con.calcular_precio()

        assert precio_con > precio_sin
        assert precio_con - precio_sin == 300.0

    def test_precio_con_cabecera(self):
        """Probar que la cabecera aumenta el precio."""
        cama_sin = Cama("Cama", "Madera", "Blanco", 300.0, tiene_cabecera=False)
        cama_con = Cama("Cama", "Madera", "Blanco", 300.0, tiene_cabecera=True)

        precio_sin = cama_sin.calcular_precio()
        precio_con = cama_con.calcular_precio()

        assert precio_con > precio_sin
        assert precio_con - precio_sin == 100.0


class TestCamaDescripcion:
    """Pruebas del método obtener_descripcion."""

    def test_obtener_descripcion_contiene_nombre(self):
        """Verificar que la descripción contiene el nombre."""
        cama = Cama("Cama Test", "Madera", "Blanco", 300.0)
        desc = cama.obtener_descripcion()

        assert "Cama" in desc

    def test_obtener_descripcion_contiene_tamaño(self):
        """Verificar que la descripción contiene el tamaño."""
        cama = Cama("Cama", "Madera", "Blanco", 300.0, tamaño="queen")
        desc = cama.obtener_descripcion()

        assert "queen" in desc

    def test_obtener_descripcion_contiene_precio(self):
        """Verificar que la descripción contiene el precio."""
        cama = Cama("Cama", "Madera", "Blanco", 300.0)
        desc = cama.obtener_descripcion()

        assert "Precio" in desc or "precio" in desc.lower()


class TestCamaParametrizacion:
    """Pruebas parametrizadas para diferentes configuraciones."""

    @pytest.mark.parametrize(
        "tamaño,precio_base,incremento_esperado",
        [
            ("individual", 300.0, 0.0),
            ("matrimonial", 300.0, 200.0),
            ("queen", 300.0, 400.0),
            ("king", 300.0, 600.0),
        ],
    )
    def test_precios_por_tamaño(self, tamaño, precio_base, incremento_esperado):
        """Probar precios según tamaño."""
        cama = Cama("Cama", "Madera", "Blanco", precio_base, tamaño=tamaño)
        precio = cama.calcular_precio()

        assert precio == precio_base + incremento_esperado

    @pytest.mark.parametrize(
        "colchon,cabecera,incremento",
        [
            (False, False, 0.0),
            (True, False, 300.0),
            (False, True, 100.0),
            (True, True, 400.0),
        ],
    )
    def test_precios_con_extras(self, colchon, cabecera, incremento):
        """Probar precios con diferentes extras."""
        precio_base = 300.0
        cama = Cama(
            "Cama",
            "Madera",
            "Blanco",
            precio_base,
            incluye_colchon=colchon,
            tiene_cabecera=cabecera,
        )

        precio = cama.calcular_precio()
        assert precio == precio_base + incremento
