"""
One chart style for every image figure on the Hatteras stakeholder pages: the site's body font (Roboto) and the
colours the interactive charts use (assets/hatteras/js), so a drawn figure and a live chart look like one site.

    import hatteras_fig_style as style
    style.apply()            # once, before drawing; style.apply(size=None) keeps the sizes another style set

Hannah asked (2026-10-04) for one chart style in the site's font across all the figure tools. Roboto must be
installed (fonts.google.com/specimen/Roboto); apply() stops with a message rather than fall back to DejaVu Sans.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-04
"""
import matplotlib
from matplotlib import font_manager

FONT = "Roboto"
INK, MUTED, GRID = "#1a1a1a", "#6b7378", "#e6e9eb"      # as INK, MUTED, GRID in the site's chart scripts
TEAL = "#2f7f93"                                         # the site's highlight colour (picked place, locator)


def apply(size=10):
    """Set matplotlib's font and text colours for the site's figures."""
    if not any(f.name == FONT for f in font_manager.fontManager.ttflist):
        raise SystemExit(f"{FONT} is not installed; install it so the figures match the site's font")
    matplotlib.rcParams.update({
        "font.family": FONT,
        "text.color": INK, "axes.labelcolor": INK, "axes.edgecolor": MUTED,
        "xtick.color": INK, "ytick.color": INK, "axes.titlecolor": INK,
    })
    if size is not None:
        matplotlib.rcParams["font.size"] = size
