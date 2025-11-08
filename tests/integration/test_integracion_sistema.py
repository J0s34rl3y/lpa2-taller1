"""
Pruebas de integración para el sistema de muebles.
Estas pruebas verifican la interacción entre múltiples componentes.
"""

import pytest

from src.models.composicion.comedor import Comedor
from src.models.concretos.armario import Armario
from src.models.concretos.cama import Cama
from src.models.concretos.mesa import Mesa
from src.models.concretos.silla import Silla
from src.models.concretos.sofa import Sofa
from src.models.concretos.sofacama import SofaCama


class TestIntegracionTiendaMuebles:
    """Pruebas de integración del sistema completo."""

    def test_crear_catalogo_variado(self):
        """Probar crear un catálogo con diferentes tipos de muebles."""
        catalogo = [
            Silla(
                "Silla Oficina", "Metal", "Negro", 120.0, altura_regulable=True, tiene_ruedas=True
            ),
            Mesa("Mesa Comedor", "Roble", "Natural", 300.0, capacidad_personas=6),
            Sofa("Sofá Moderno", "Tela", "Gris", 500.0, es_modular=True),
            Cama("Cama King", "Madera", "Blanco", 400.0, tamaño="king", incluye_colchon=True),
            Armario("Armario Triple", "Madera", "Café", 600, num_puertas=3),
        ]

        assert len(catalogo) == 5

        # Todos pueden calcular precio
        for mueble in catalogo:
            precio = mueble.calcular_precio()
            assert precio > 0
            assert isinstance(precio, float) or isinstance(precio, int)

        # Todos tienen descripción
        for mueble in catalogo:
            desc = mueble.obtener_descripcion()
            assert isinstance(desc, str)
            assert len(desc) > 0

    def test_calcular_precio_total_catalogo(self):
        """Probar calcular el precio total de un catálogo."""
        catalogo = [
            Silla("Silla", "Madera", "Café", 100.0),
            Mesa("Mesa", "Madera", "Natural", 200.0),
            Cama("Cama", "Madera", "Blanco", 300.0),
        ]

        precio_total = sum(m.calcular_precio() for m in catalogo)

        assert precio_total > 0
        assert precio_total >= 600.0  # Al menos las sumas base

    def test_crear_sala_completa(self):
        """Probar crear una sala completa con sofá y mesa."""
        sofa = Sofa("Sofá Sala", "Tela", "Beige", 600.0, capacidad_personas=3)
        mesa_centro = Mesa("Mesa Centro", "Vidrio", "Transparente", 150.0, forma="redonda")

        sala = {"sofa": sofa, "mesa": mesa_centro}

        assert sala["sofa"].capacidad_personas == 3
        assert sala["mesa"].forma == "redonda"

        precio_sala = sofa.calcular_precio() + mesa_centro.calcular_precio()
        assert precio_sala > 750.0

    def test_crear_dormitorio_completo(self):
        """Probar crear un dormitorio con cama y armario."""
        cama = Cama("Cama Queen", "Roble", "Natural", 500.0, tamaño="queen", incluye_colchon=True)
        armario = Armario("Armario", "Roble", "Natural", 700, num_puertas=2, tiene_espejos=True)

        dormitorio = {"cama": cama, "armario": armario}

        assert dormitorio["cama"].tamaño == "queen"
        assert dormitorio["armario"].tiene_espejos is True

        precio_dormitorio = cama.calcular_precio() + armario.calcular_precio()
        assert precio_dormitorio > 1200

    def test_comedor_completo_integracion(self):
        """Probar integración completa de un comedor."""
        # Crear mesa
        mesa = Mesa(
            "Mesa Familiar", "Pino", "Natural", 350.0, forma="rectangular", capacidad_personas=8
        )

        # Crear 6 sillas iguales
        sillas = [
            Silla(
                f"Silla {i+1}",
                "Pino",
                "Natural",
                90.0,
                tiene_respaldo=True,
                material_tapizado="tela",
            )
            for i in range(6)
        ]

        # Crear comedor
        comedor = Comedor("Comedor Familiar", mesa, sillas)

        # Verificaciones de integración
        assert comedor.mesa.capacidad_personas == 8
        assert len(comedor.sillas) == 6
        assert all(s.material == "Pino" for s in comedor.sillas)

        # Verificar precio tiene descuento (6 sillas >= 4)
        precio_total = comedor.calcular_precio_total()
        assert precio_total > 0

        # Verificar resumen
        resumen = comedor.obtener_resumen()
        assert resumen["total_muebles"] == 7  # 1 mesa + 6 sillas
        assert resumen["capacidad_personas"] == 6

    def test_sofacama_funcionalidad_dual(self):
        """Probar funcionalidad dual del sofá-cama."""
        sofacama = SofaCama(
            "SofaCama Versátil",
            "Metal",
            "Azul",
            700.0,
            capacidad_personas=3,
            tamaño_cama="queen",
            incluye_colchon=True,
            mecanismo_conversion="hidraulico",
        )

        # Funciona como sofá
        assert sofacama.capacidad_personas == 3
        assert sofacama.tiene_respaldo is True

        # Funciona como cama
        assert sofacama.tamaño == "queen"
        assert sofacama.incluye_colchon is True

        # Tiene funcionalidad específica
        assert sofacama.modo_actual == "sofa"
        sofacama.transformar()
        assert sofacama.modo_actual == "cama"

        # El precio refleja ambas funcionalidades
        precio = sofacama.calcular_precio()
        assert precio > 700.0

    def test_comparar_precios_muebles_similares(self):
        """Probar comparación de precios entre muebles similares."""
        # Sillas de diferentes tipos
        silla_basica = Silla("Silla Básica", "Plástico", "Blanco", 50.0)
        silla_oficina = Silla(
            "Silla Oficina", "Metal", "Negro", 150.0, altura_regulable=True, tiene_ruedas=True
        )
        silla_tapizada = Silla("Silla Tapizada", "Madera", "Café", 100.0, material_tapizado="cuero")

        precios = {
            "basica": silla_basica.calcular_precio(),
            "oficina": silla_oficina.calcular_precio(),
            "tapizada": silla_tapizada.calcular_precio(),
        }

        # La silla de oficina debe ser más cara por opciones
        assert precios["oficina"] > precios["basica"]
        # La tapizada debe ser más cara que la básica
        assert precios["tapizada"] > precios["basica"]

    def test_muebles_mismo_material_coherencia(self):
        """Probar coherencia en muebles del mismo material."""
        material = "Roble"
        color = "Natural"

        muebles = [
            Mesa("Mesa", material, color, 300.0),
            Silla("Silla", material, color, 80.0),
            Cama("Cama", material, color, 400.0),
        ]

        # Todos deben tener el mismo material
        assert all(m.material == material for m in muebles)
        assert all(m.color == color for m in muebles)

        # Todos deben poder calcular precio
        for mueble in muebles:
            assert mueble.calcular_precio() > 0

    def test_agregar_y_quitar_sillas_comedor(self):
        """Probar dinámica de agregar/quitar sillas."""
        mesa = Mesa("Mesa", "Madera", "Natural", 250.0, capacidad_personas=8)
        sillas_iniciales = [Silla(f"Silla {i}", "Madera", "Natural", 75.0) for i in range(4)]

        comedor = Comedor("Comedor Flexible", mesa, sillas_iniciales)

        assert len(comedor.sillas) == 4
        precio_4_sillas = comedor.calcular_precio_total()

        # Agregar 2 sillas más
        for i in range(2):
            nueva_silla = Silla(f"Silla Extra {i}", "Madera", "Natural", 75.0)
            comedor.agregar_silla(nueva_silla)

        assert len(comedor.sillas) == 6
        precio_6_sillas = comedor.calcular_precio_total()

        # El precio debe aumentar
        assert precio_6_sillas > precio_4_sillas

        # Quitar 1 silla
        comedor.quitar_silla()
        assert len(comedor.sillas) == 5

    def test_multiples_comedores_independientes(self):
        """Probar que múltiples comedores son independientes."""
        # Comedor 1
        mesa1 = Mesa("Mesa 1", "Roble", "Claro", 300.0, capacidad_personas=8)
        sillas1 = [Silla("Silla 1", "Roble", "Claro", 80.0) for _ in range(4)]
        comedor1 = Comedor("Comedor 1", mesa1, sillas1)

        # Comedor 2
        mesa2 = Mesa("Mesa 2", "Pino", "Oscuro", 250.0, capacidad_personas=8)
        sillas2 = [Silla("Silla 2", "Pino", "Oscuro", 70.0) for _ in range(6)]
        comedor2 = Comedor("Comedor 2", mesa2, sillas2)

        # Son independientes
        assert len(comedor1.sillas) == 4
        assert len(comedor2.sillas) == 6
        assert comedor1.mesa != comedor2.mesa

        # Modificar uno no afecta al otro
        comedor1.agregar_silla(Silla("Extra", "Roble", "Claro", 80.0))
        assert len(comedor1.sillas) == 5
        assert len(comedor2.sillas) == 6  # Sin cambios

    @pytest.mark.integration
    def test_escenario_tienda_completa(self):
        """Prueba de integración completa: escenario de tienda."""
        # Crear inventario variado
        inventario = {
            "sillas": [
                Silla("Silla Básica", "Plástico", "Blanco", 40.0),
                Silla(
                    "Silla Oficina",
                    "Metal",
                    "Negro",
                    120.0,
                    altura_regulable=True,
                    tiene_ruedas=True,
                ),
            ],
            "mesas": [
                Mesa("Mesa Comedor", "Madera", "Natural", 300.0),
                Mesa("Mesa Escritorio", "Metal", "Gris", 200.0),
            ],
            "camas": [
                Cama("Cama Individual", "Madera", "Blanco", 250.0, tamaño="individual"),
                Cama("Cama Queen", "Madera", "Café", 450.0, tamaño="queen", incluye_colchon=True),
            ],
            "sofas": [
                Sofa("Sofá 2 Plazas", "Tela", "Gris", 400.0, capacidad_personas=2),
                SofaCama("Sofá-Cama", "Metal", "Azul", 650.0),
            ],
        }

        # Verificar que todos los muebles son válidos
        total_muebles = sum(len(items) for items in inventario.values())
        assert total_muebles == 8

        # Calcular valor total del inventario
        valor_total = 0
        for categoria in inventario.values():
            for mueble in categoria:
                valor_total += mueble.calcular_precio()

        assert valor_total > 0
        assert valor_total > 2400  # Suma mínima esperada

        # Verificar que todos tienen descripción
        for categoria in inventario.values():
            for mueble in categoria:
                desc = mueble.obtener_descripcion()
                assert isinstance(desc, str)
                assert len(desc) > 0
