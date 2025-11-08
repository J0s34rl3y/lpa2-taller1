"""
Configuración compartida para todas las pruebas.
Este archivo contiene fixtures reutilizables y marcadores de pytest.
"""

import sys
from pathlib import Path

import pytest

# Agregar el directorio src al path para importaciones
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def pytest_configure(config):
    """Configurar marcadores personalizados para pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")


# ===== FIXTURES PARA MUEBLES BÁSICOS =====


@pytest.fixture
def silla_basica():
    """Fixture para una silla básica de prueba."""
    from src.models.concretos.silla import Silla

    return Silla(
        nombre="Silla Test",
        material="Madera",
        color="Café",
        precio_base=100.0,
        tiene_respaldo=True,
        material_tapizado="tela",
    )


@pytest.fixture
def silla_con_ruedas():
    """Fixture para una silla de oficina con ruedas."""
    from src.models.concretos.silla import Silla

    return Silla(
        nombre="Silla Oficina",
        material="Metal",
        color="Negro",
        precio_base=150.0,
        tiene_respaldo=True,
        material_tapizado="cuero",
        altura_regulable=True,
        tiene_ruedas=True,
    )


@pytest.fixture
def mesa_rectangular():
    """Fixture para una mesa rectangular de prueba."""
    from src.models.concretos.mesa import Mesa

    return Mesa(
        nombre="Mesa Test",
        material="Madera",
        color="Natural",
        precio_base=200.0,
        forma="rectangular",
        largo=120.0,
        ancho=80.0,
        altura=75.0,
        capacidad_personas=4,
    )


@pytest.fixture
def sofa_basico():
    """Fixture para un sofá básico."""
    from src.models.concretos.sofa import Sofa

    return Sofa(
        nombre="Sofá Test",
        material="Madera",
        color="Gris",
        precio_base=500.0,
        capacidad_personas=3,
        tiene_respaldo=True,
        material_tapizado="tela",
    )


@pytest.fixture
def cama_individual():
    """Fixture para una cama individual."""
    from src.models.concretos.cama import Cama

    return Cama(
        nombre="Cama Test",
        material="Madera",
        color="Blanco",
        precio_base=300.0,
        tamaño="individual",
        incluye_colchon=False,
        tiene_cabecera=False,
    )


@pytest.fixture
def sofacama_basico():
    """Fixture para un sofá-cama."""
    from src.models.concretos.sofacama import SofaCama

    return SofaCama(
        nombre="Sofá-Cama Test",
        material="Metal",
        color="Azul",
        precio_base=600.0,
        capacidad_personas=3,
        material_tapizado="tela",
        tamaño_cama="matrimonial",
        incluye_colchon=True,
        mecanismo_conversion="plegable",
    )


@pytest.fixture
def comedor_completo():
    """Fixture para un comedor completo con mesa y 4 sillas."""
    from src.models.composicion.comedor import Comedor
    from src.models.concretos.mesa import Mesa
    from src.models.concretos.silla import Silla

    mesa = Mesa(
        nombre="Mesa Comedor",
        material="Roble",
        color="Natural",
        precio_base=300.0,
        forma="rectangular",
        capacidad_personas=8,  # Permitir hasta 8 sillas para tests
    )

    sillas = [
        Silla(
            nombre=f"Silla Comedor {i+1}",
            material="Roble",
            color="Natural",
            precio_base=80.0,
            tiene_respaldo=True,
            material_tapizado="tela",
        )
        for i in range(4)
    ]

    return Comedor(nombre="Comedor Familiar", mesa=mesa, sillas=sillas)


@pytest.fixture
def lista_sillas():
    """Fixture para una lista de sillas variadas."""
    from src.models.concretos.silla import Silla

    return [
        Silla("Silla 1", "Madera", "Café", 100.0, True, "tela"),
        Silla("Silla 2", "Metal", "Negro", 120.0, True, "cuero", True, True),
        Silla("Silla 3", "Plástico", "Blanco", 50.0, False, None),
    ]


# ===== FIXTURES PARA DATOS DE PRUEBA =====


@pytest.fixture
def materiales_validos():
    """Lista de materiales válidos para pruebas."""
    return ["Madera", "Metal", "Plástico", "Vidrio", "Roble", "Pino"]


@pytest.fixture
def colores_validos():
    """Lista de colores válidos para pruebas."""
    return ["Blanco", "Negro", "Café", "Natural", "Gris", "Azul", "Rojo"]


@pytest.fixture
def precios_validos():
    """Rango de precios válidos para pruebas."""
    return [50.0, 100.0, 200.0, 500.0, 1000.0, 2000.0]


@pytest.fixture
def formas_mesa():
    """Formas válidas para mesas."""
    return ["rectangular", "redonda", "cuadrada", "ovalada"]


@pytest.fixture
def tamaños_cama():
    """Tamaños válidos para camas."""
    return ["individual", "matrimonial", "queen", "king"]
