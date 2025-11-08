"""
Pruebas para la clase Mesa.
"""

import pytest

from src.models.categorias.superficies import Superficie
from src.models.concretos.mesa import Mesa
from src.models.mueble import Mueble


class TestMesaHerencia:
    """Pruebas de herencia de Mesa."""

    def test_hereda_de_superficie(self):
        """Verificar que Mesa hereda de Superficie."""
        assert issubclass(Mesa, Superficie)

    def test_hereda_de_mueble_indirecto(self):
        """Verificar herencia indirecta de Mueble."""
        assert issubclass(Mesa, Mueble)

    def test_instanciacion_correcta(self):
        """Verificar que se puede instanciar correctamente."""
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0)
        assert isinstance(mesa, Mesa)
        assert isinstance(mesa, Superficie)
        assert isinstance(mesa, Mueble)


class TestMesaInicializacion:
    """Pruebas de inicialización de Mesa."""

    def test_inicializacion_basica(self):
        """Probar inicialización con parámetros básicos."""
        mesa = Mesa("Mesa Test", "Madera", "Natural", 200.0)

        assert mesa.nombre == "Mesa Test"
        assert mesa.material == "Madera"
        assert mesa.color == "Natural"
        assert mesa.precio_base == 200.0

    def test_inicializacion_valores_por_defecto(self):
        """Probar valores por defecto."""
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0)

        assert mesa.forma == "rectangular"
        assert mesa.largo == 120.0
        assert mesa.ancho == 80.0
        assert mesa.altura == 75.0
        assert mesa.capacidad_personas == 4

    def test_inicializacion_completa(self):
        """Probar inicialización con todos los parámetros."""
        mesa = Mesa(
            "Mesa Grande",
            "Roble",
            "Oscuro",
            350.0,
            forma="redonda",
            largo=180.0,
            ancho=180.0,
            altura=75.0,
            capacidad_personas=8,
        )

        assert mesa.forma == "redonda"
        assert mesa.largo == 180.0
        assert mesa.capacidad_personas == 8


class TestMesaPropiedades:
    """Pruebas de propiedades de Mesa."""

    def test_getter_forma(self):
        """Probar getter de forma."""
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0, forma="redonda")
        assert mesa.forma == "redonda"

    def test_setter_forma_valida(self):
        """Probar setter con forma válida."""
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0)
        mesa.forma = "ovalada"
        assert mesa.forma == "ovalada"

    def test_setter_forma_invalida_error(self):
        """Probar que forma inválida genera error."""
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0)
        with pytest.raises(ValueError):
            mesa.forma = "triangular"

    def test_formas_validas(self):
        """Probar todas las formas válidas."""
        formas = ["rectangular", "redonda", "cuadrada", "ovalada"]
        for forma in formas:
            mesa = Mesa("Mesa", "Madera", "Natural", 200.0, forma=forma)
            assert mesa.forma == forma

    def test_getter_capacidad_personas(self):
        """Probar getter de capacidad."""
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0, capacidad_personas=6)
        assert mesa.capacidad_personas == 6

    def test_setter_capacidad_valida(self):
        """Probar setter con capacidad válida."""
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0)
        mesa.capacidad_personas = 8
        assert mesa.capacidad_personas == 8

    def test_setter_capacidad_cero_error(self):
        """Probar que capacidad = 0 genera error."""
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0)
        with pytest.raises(ValueError):
            mesa.capacidad_personas = 0

    def test_setter_capacidad_negativa_error(self):
        """Probar que capacidad negativa genera error."""
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0)
        with pytest.raises(ValueError):
            mesa.capacidad_personas = -1


class TestMesaCalculoPrecio:
    """Pruebas de cálculo de precio de Mesa."""

    def test_calcular_precio_basico(self):
        """Probar cálculo de precio básico."""
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0)
        precio = mesa.calcular_precio()

        assert precio >= 200.0
        assert isinstance(precio, float)

    def test_precio_forma_no_rectangular(self):
        """Probar que forma no rectangular aumenta el precio."""
        mesa_rect = Mesa("Mesa", "Madera", "Natural", 200.0, forma="rectangular")
        mesa_redonda = Mesa("Mesa", "Madera", "Natural", 200.0, forma="redonda")

        precio_rect = mesa_rect.calcular_precio()
        precio_redonda = mesa_redonda.calcular_precio()

        assert precio_redonda > precio_rect

    def test_precio_capacidad_mayor_4(self):
        """Probar que capacidad > 4 aumenta el precio."""
        mesa_4 = Mesa("Mesa", "Madera", "Natural", 200.0, capacidad_personas=4)
        mesa_6 = Mesa("Mesa", "Madera", "Natural", 200.0, capacidad_personas=6)

        precio_4 = mesa_4.calcular_precio()
        precio_6 = mesa_6.calcular_precio()

        assert precio_6 > precio_4

    def test_precio_capacidad_mayor_6(self):
        """Probar que capacidad > 6 aumenta más el precio."""
        mesa_6 = Mesa("Mesa", "Madera", "Natural", 200.0, capacidad_personas=6)
        mesa_8 = Mesa("Mesa", "Madera", "Natural", 200.0, capacidad_personas=8)

        precio_6 = mesa_6.calcular_precio()
        precio_8 = mesa_8.calcular_precio()

        assert precio_8 > precio_6

    def test_precio_con_area_mayor(self):
        """Probar que mayor área aumenta el precio por factor de tamaño."""
        mesa_pequeña = Mesa("Mesa", "Madera", "Natural", 200.0, largo=80.0, ancho=60.0)
        mesa_grande = Mesa("Mesa", "Madera", "Natural", 200.0, largo=200.0, ancho=120.0)

        precio_pequeña = mesa_pequeña.calcular_precio()
        precio_grande = mesa_grande.calcular_precio()

        assert precio_grande > precio_pequeña


class TestMesaDescripcion:
    """Pruebas del método obtener_descripcion."""

    def test_obtener_descripcion_contiene_nombre(self):
        """Verificar que la descripción contiene el nombre."""
        mesa = Mesa("Mesa Test", "Madera", "Natural", 200.0)
        desc = mesa.obtener_descripcion()

        assert "Mesa" in desc

    def test_obtener_descripcion_contiene_forma(self):
        """Verificar que la descripción contiene la forma."""
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0, forma="redonda")
        desc = mesa.obtener_descripcion()

        assert "redonda" in desc

    def test_obtener_descripcion_contiene_capacidad(self):
        """Verificar que la descripción contiene la capacidad."""
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0, capacidad_personas=6)
        desc = mesa.obtener_descripcion()

        assert "6" in desc
        assert "personas" in desc.lower()

    def test_obtener_descripcion_contiene_precio(self):
        """Verificar que la descripción contiene el precio."""
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0)
        desc = mesa.obtener_descripcion()

        assert "Precio" in desc or "precio" in desc.lower()


class TestMesaParametrizacion:
    """Pruebas parametrizadas para diferentes configuraciones."""

    @pytest.mark.parametrize("forma", ["rectangular", "redonda", "cuadrada", "ovalada"])
    def test_todas_las_formas(self, forma):
        """Probar todas las formas válidas."""
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0, forma=forma)

        assert mesa.forma == forma
        assert mesa.calcular_precio() >= 200.0

    @pytest.mark.parametrize("capacidad", [2, 4, 6, 8, 10])
    def test_diferentes_capacidades(self, capacidad):
        """Probar diferentes capacidades."""
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0, capacidad_personas=capacidad)

        assert mesa.capacidad_personas == capacidad
        assert mesa.calcular_precio() > 0

    @pytest.mark.parametrize(
        "material,color",
        [
            ("Madera", "Natural"),
            ("Roble", "Oscuro"),
            ("Vidrio", "Transparente"),
            ("Metal", "Gris"),
        ],
    )
    def test_diferentes_materiales(self, material, color):
        """Probar mesas con diferentes materiales."""
        mesa = Mesa("Mesa", material, color, 200.0)

        assert mesa.material == material
        assert mesa.color == color
        assert mesa.calcular_precio() >= 200.0
