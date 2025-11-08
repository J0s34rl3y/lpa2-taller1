"""
Pruebas para la clase SofaCama (herencia múltiple).
Este módulo demuestra pruebas de herencia múltiple y MRO (Method Resolution Order).
"""

import pytest

from src.models.categorias.asientos import Asiento
from src.models.concretos.cama import Cama
from src.models.concretos.sofa import Sofa
from src.models.concretos.sofacama import SofaCama
from src.models.mueble import Mueble


class TestSofaCamaHerenciaMultiple:
    """Pruebas de herencia múltiple de SofaCama."""

    def test_hereda_de_sofa(self):
        """Verificar que SofaCama hereda de Sofa."""
        assert issubclass(SofaCama, Sofa)

    def test_hereda_de_cama(self):
        """Verificar que SofaCama hereda de Cama."""
        assert issubclass(SofaCama, Cama)

    def test_hereda_de_asiento_indirecto(self):
        """Verificar herencia indirecta de Asiento (a través de Sofa)."""
        assert issubclass(SofaCama, Asiento)

    def test_hereda_de_mueble_indirecto(self):
        """Verificar herencia indirecta de Mueble."""
        assert issubclass(SofaCama, Mueble)

    def test_instanciacion_correcta(self, sofacama_basico):
        """Verificar que se puede instanciar correctamente."""
        assert isinstance(sofacama_basico, SofaCama)
        assert isinstance(sofacama_basico, Sofa)
        assert isinstance(sofacama_basico, Cama)

    def test_mro_orden_resolucion(self):
        """Verificar el orden de resolución de métodos (MRO)."""
        mro = SofaCama.__mro__

        # SofaCama debe estar primero
        assert mro[0] == SofaCama
        # Sofa debe venir antes que Cama (orden de herencia)
        sofa_index = mro.index(Sofa)
        cama_index = mro.index(Cama)
        assert sofa_index < cama_index


class TestSofaCamaInicializacion:
    """Pruebas de inicialización de SofaCama."""

    def test_inicializacion_parametros_basicos(self):
        """Probar inicialización con parámetros mínimos."""
        sofacama = SofaCama(
            nombre="SofaCama Test", material="Metal", color="Azul", precio_base=600.0
        )

        assert sofacama.nombre == "SofaCama Test"
        assert sofacama.material == "Metal"
        assert sofacama.color == "Azul"
        assert sofacama.precio_base == 600.0

    def test_inicializacion_con_valores_por_defecto(self):
        """Probar valores por defecto en la inicialización."""
        sofacama = SofaCama("SofaCama", "Metal", "Azul", 600.0)

        assert sofacama.capacidad_personas == 3
        assert sofacama.material_tapizado == "tela"
        assert sofacama.tamaño == "matrimonial"
        assert sofacama.incluye_colchon is True
        assert sofacama.mecanismo_conversion == "plegable"

    def test_inicializacion_parametros_completos(self):
        """Probar inicialización con todos los parámetros."""
        sofacama = SofaCama(
            nombre="SofaCama Deluxe",
            material="Madera",
            color="Gris",
            precio_base=800.0,
            capacidad_personas=4,
            material_tapizado="cuero",
            tamaño_cama="queen",
            incluye_colchon=True,
            mecanismo_conversion="hidraulico",
        )

        assert sofacama.capacidad_personas == 4
        assert sofacama.material_tapizado == "cuero"
        assert sofacama.tamaño == "queen"
        assert sofacama.incluye_colchon is True
        assert sofacama.mecanismo_conversion == "hidraulico"


class TestSofaCamaAtributosAmbospadres:
    """Pruebas de atributos de ambas clases padre."""

    def test_atributos_de_sofa(self, sofacama_basico):
        """Verificar que tiene atributos de Sofa."""
        assert hasattr(sofacama_basico, "capacidad_personas")
        assert hasattr(sofacama_basico, "tiene_respaldo")
        assert hasattr(sofacama_basico, "material_tapizado")

        assert sofacama_basico.capacidad_personas >= 1
        assert isinstance(sofacama_basico.tiene_respaldo, bool)

    def test_atributos_de_cama(self, sofacama_basico):
        """Verificar que tiene atributos de Cama."""
        assert hasattr(sofacama_basico, "tamaño")
        assert hasattr(sofacama_basico, "incluye_colchon")

        assert sofacama_basico.tamaño in ["individual", "matrimonial", "queen", "king"]
        assert isinstance(sofacama_basico.incluye_colchon, bool)

    def test_atributos_especificos_sofacama(self, sofacama_basico):
        """Verificar atributos específicos de SofaCama."""
        assert hasattr(sofacama_basico, "mecanismo_conversion")
        assert hasattr(sofacama_basico, "modo_actual")

        assert sofacama_basico.mecanismo_conversion in ["plegable", "hidraulico", "electrico"]
        assert sofacama_basico.modo_actual in ["sofa", "cama"]


class TestSofaCamaPropiedades:
    """Pruebas de propiedades específicas."""

    def test_getter_mecanismo_conversion(self, sofacama_basico):
        """Probar getter de mecanismo_conversion."""
        assert sofacama_basico.mecanismo_conversion == "plegable"

    def test_getter_modo_actual(self, sofacama_basico):
        """Probar getter de modo_actual."""
        assert sofacama_basico.modo_actual == "sofa"

    def test_getter_tamaño(self, sofacama_basico):
        """Probar getter de tamaño (redefinido para compatibilidad)."""
        assert sofacama_basico.tamaño == "matrimonial"


class TestSofaCamaCalculoPrecio:
    """Pruebas de cálculo de precio con herencia múltiple."""

    def test_calcular_precio_basico(self):
        """Probar cálculo de precio básico."""
        sofacama = SofaCama(
            "SofaCama",
            "Metal",
            "Azul",
            600.0,
            tamaño_cama="individual",
            incluye_colchon=False,
            mecanismo_conversion="plegable",
        )
        precio = sofacama.calcular_precio()

        assert isinstance(precio, float)
        assert precio >= 600.0  # Debe ser al menos el precio base

    def test_precio_aumenta_con_tamaño_cama(self):
        """Probar que el tamaño de cama afecta el precio."""
        precios = {}
        for tamaño in ["matrimonial", "queen", "king"]:
            sofacama = SofaCama(
                "SofaCama", "Metal", "Azul", 600.0, tamaño_cama=tamaño, incluye_colchon=False
            )
            precios[tamaño] = sofacama.calcular_precio()

        # Los precios deben aumentar con el tamaño
        assert precios["queen"] > precios["matrimonial"]
        assert precios["king"] > precios["queen"]

    def test_precio_con_colchon(self):
        """Probar que incluir colchón aumenta el precio."""
        sofacama_sin = SofaCama("SofaCama", "Metal", "Azul", 600.0, incluye_colchon=False)
        sofacama_con = SofaCama("SofaCama", "Metal", "Azul", 600.0, incluye_colchon=True)

        precio_sin = sofacama_sin.calcular_precio()
        precio_con = sofacama_con.calcular_precio()

        assert precio_con > precio_sin

    def test_precio_con_mecanismo_hidraulico(self):
        """Probar que mecanismo hidráulico aumenta el precio."""
        sofacama_plegable = SofaCama(
            "SofaCama", "Metal", "Azul", 600.0, mecanismo_conversion="plegable"
        )
        sofacama_hidraulico = SofaCama(
            "SofaCama", "Metal", "Azul", 600.0, mecanismo_conversion="hidraulico"
        )

        precio_plegable = sofacama_plegable.calcular_precio()
        precio_hidraulico = sofacama_hidraulico.calcular_precio()

        assert precio_hidraulico > precio_plegable

    def test_precio_con_mecanismo_electrico(self):
        """Probar que mecanismo eléctrico es el más caro."""
        sofacama_hidraulico = SofaCama(
            "SofaCama", "Metal", "Azul", 600.0, mecanismo_conversion="hidraulico"
        )
        sofacama_electrico = SofaCama(
            "SofaCama", "Metal", "Azul", 600.0, mecanismo_conversion="electrico"
        )

        precio_hidraulico = sofacama_hidraulico.calcular_precio()
        precio_electrico = sofacama_electrico.calcular_precio()

        assert precio_electrico > precio_hidraulico

    def test_precio_combina_ambas_clases(self, sofacama_basico):
        """Verificar que el precio combina características de ambas clases."""
        precio = sofacama_basico.calcular_precio()
        precio_base = sofacama_basico.precio_base

        # El precio debe ser mayor al precio base por todas las características
        assert precio > precio_base
        assert isinstance(precio, float)


class TestSofaCamaDescripcion:
    """Pruebas del método obtener_descripcion."""

    def test_descripcion_existe(self, sofacama_basico):
        """Verificar que el método obtener_descripcion existe."""
        assert hasattr(sofacama_basico, "obtener_descripcion")
        desc = sofacama_basico.obtener_descripcion()
        assert isinstance(desc, str)

    def test_descripcion_contiene_informacion_basica(self, sofacama_basico):
        """Verificar que la descripción contiene información básica."""
        desc = sofacama_basico.obtener_descripcion()

        # Debe mencionar aspectos del sofá-cama
        assert len(desc) > 0


class TestSofaCamaMetodosEspecificos:
    """Pruebas de métodos específicos de SofaCama."""

    def test_tiene_metodo_transformar(self, sofacama_basico):
        """Verificar que tiene método transformar."""
        assert hasattr(sofacama_basico, "transformar")

    def test_transformar_cambia_modo(self, sofacama_basico):
        """Probar que transformar cambia el modo."""
        modo_inicial = sofacama_basico.modo_actual
        assert modo_inicial == "sofa"

        resultado = sofacama_basico.transformar()

        assert isinstance(resultado, str)
        assert sofacama_basico.modo_actual == "cama"

    def test_transformar_alterna_modos(self, sofacama_basico):
        """Probar que transformar alterna entre modos."""
        # Inicial: sofa
        assert sofacama_basico.modo_actual == "sofa"

        # Transformar a cama
        sofacama_basico.transformar()
        assert sofacama_basico.modo_actual == "cama"

        # Transformar de vuelta a sofa
        sofacama_basico.transformar()
        assert sofacama_basico.modo_actual == "sofa"


class TestSofaCamaParametrizacion:
    """Pruebas parametrizadas para diferentes configuraciones."""

    @pytest.mark.parametrize(
        "tamaño,precio_minimo",
        [
            ("matrimonial", 600.0),
            ("queen", 800.0),
            ("king", 900.0),
        ],
    )
    def test_diferentes_tamaños(self, tamaño, precio_minimo):
        """Probar diferentes tamaños de cama."""
        sofacama = SofaCama(
            "SofaCama", "Metal", "Azul", 500.0, tamaño_cama=tamaño, incluye_colchon=True
        )

        assert sofacama.tamaño == tamaño
        precio = sofacama.calcular_precio()
        assert precio >= precio_minimo

    @pytest.mark.parametrize("capacidad", [2, 3, 4])
    def test_diferentes_capacidades(self, capacidad):
        """Probar diferentes capacidades de personas."""
        sofacama = SofaCama("SofaCama", "Metal", "Azul", 600.0, capacidad_personas=capacidad)

        assert sofacama.capacidad_personas == capacidad


class TestSofaCamaPolimorfismo:
    """Pruebas de polimorfismo y MRO."""

    def test_usa_calcular_precio_de_sofa_primero(self):
        """Verificar que usa el método de Sofa por MRO."""
        sofacama = SofaCama("SofaCama", "Metal", "Azul", 600.0)

        # El método calcular_precio debe ser el de SofaCama
        # que llama a super() que resuelve a Sofa por MRO
        assert hasattr(sofacama, "calcular_precio")
        precio = sofacama.calcular_precio()
        assert isinstance(precio, float)

    def test_polimorfismo_como_sofa(self):
        """Probar que un SofaCama puede usarse como Sofa."""
        sofacama = SofaCama("SofaCama", "Metal", "Azul", 600.0)

        # Debe tener métodos de Sofa
        assert hasattr(sofacama, "capacidad_personas")
        assert sofacama.capacidad_personas >= 1

    def test_polimorfismo_como_cama(self):
        """Probar que un SofaCama puede usarse como Cama."""
        sofacama = SofaCama("SofaCama", "Metal", "Azul", 600.0)

        # Debe tener atributos de Cama
        assert hasattr(sofacama, "tamaño")
        assert hasattr(sofacama, "incluye_colchon")
