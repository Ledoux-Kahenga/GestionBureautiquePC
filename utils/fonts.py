"""
Utilitaires pour les polices - adaptation multiplateforme
"""
from PyQt5.QtGui import QFont
from config import (FONT_FAMILY, FONT_SIZE_XS, FONT_SIZE_SM, FONT_SIZE_MD, 
                    FONT_SIZE_LG, FONT_SIZE_XL, FONT_SIZE_XXL, FONT_SIZE_HUGE,
                    FONT_SIZE_GIANT, FONT_SIZE_MEGA)


def get_font(size="md", bold=False):
    """
    Retourne une police adaptée au système d'exploitation
    
    Args:
        size: Taille de la police ("xs", "sm", "md", "lg", "xl", "xxl", "huge", "giant", "mega")
        bold: Si True, police en gras
        
    Returns:
        QFont configuré
    """
    sizes = {
        "xs": FONT_SIZE_XS,
        "sm": FONT_SIZE_SM,
        "md": FONT_SIZE_MD,
        "lg": FONT_SIZE_LG,
        "xl": FONT_SIZE_XL,
        "xxl": FONT_SIZE_XXL,
        "huge": FONT_SIZE_HUGE,
        "giant": FONT_SIZE_GIANT,
        "mega": FONT_SIZE_MEGA
    }
    
    font_size = sizes.get(size, FONT_SIZE_MD)
    weight = QFont.Bold if bold else QFont.Normal
    
    return QFont(FONT_FAMILY, font_size, weight)


# Raccourcis pour les polices courantes
def font_xs(bold=False):
    return get_font("xs", bold)

def font_sm(bold=False):
    return get_font("sm", bold)

def font_md(bold=False):
    return get_font("md", bold)

def font_lg(bold=False):
    return get_font("lg", bold)

def font_xl(bold=False):
    return get_font("xl", bold)

def font_xxl(bold=False):
    return get_font("xxl", bold)

def font_huge(bold=False):
    return get_font("huge", bold)

def font_giant(bold=False):
    return get_font("giant", bold)

def font_mega(bold=False):
    return get_font("mega", bold)
