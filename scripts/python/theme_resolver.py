"""
Helper functions to resolve theme-dependent values (colors, fonts) from source presentation
and convert them to explicit values that don't depend on the target's theme.
"""
from pptx.util import Pt
from pptx.enum.dml import MSO_THEME_COLOR
from copy import deepcopy


def get_theme_color_rgb(presentation, theme_color_idx):
    """
    Get the actual RGB value for a theme color from a presentation's theme.
    
    Args:
        presentation: pptx.Presentation object
        theme_color_idx: MSO_THEME_COLOR enum value or integer
    
    Returns:
        RGB string like 'FF0000' or None
    """
    try:
        from lxml import etree
        
        # Get theme part from slide master
        master = presentation.slide_masters[0]
        theme_part = None
        
        for rel in master.part.rels.values():
            if 'theme' in rel.reltype.lower():
                theme_part = rel.target_part
                break
        
        if not theme_part:
            return None
        
        # Parse theme XML
        theme_xml = theme_part.blob
        root = etree.fromstring(theme_xml)
        
        ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
        
        # Find color scheme
        clrScheme = root.find('.//a:clrScheme', ns)
        if clrScheme is None:
            return None
        
        # Map theme color indices to XML element names
        color_map = {
            11: 'hlink',      # HYPERLINK
            12: 'folHlink',   # FOLLOWED_HYPERLINK
            1: 'dk1',         # DARK_1
            2: 'lt1',         # LIGHT_1
            3: 'dk2',         # DARK_2
            4: 'lt2',         # LIGHT_2
            5: 'accent1',     # ACCENT_1
            6: 'accent2',     # ACCENT_2
            7: 'accent3',     # ACCENT_3
            8: 'accent4',     # ACCENT_4
            9: 'accent5',     # ACCENT_5
            10: 'accent6',    # ACCENT_6
        }
        
        # Convert enum to int if needed
        if hasattr(theme_color_idx, 'value'):
            theme_color_idx = theme_color_idx.value
        
        elem_name = color_map.get(theme_color_idx)
        if not elem_name:
            return None
        
        color_elem = clrScheme.find(f'a:{elem_name}', ns)
        if color_elem is None:
            return None
        
        # Get RGB value
        srgbClr = color_elem.find('.//a:srgbClr', ns)
        if srgbClr is not None:
            return srgbClr.get('val')
        
        # Some themes use sysClr
        sysClr = color_elem.find('.//a:sysClr', ns)
        if sysClr is not None:
            return sysClr.get('lastClr')
        
    except Exception as e:
        pass
    
    return None


def resolve_run_color_to_rgb(run, source_presentation):
    """
    Get the actual RGB color for a run, resolving SCHEME colors to RGB.
    
    Returns:
        RGB string like 'FF0000' or None if no color
    """
    try:
        if not run.font.color.type:
            return None
        
        if run.font.color.type == 1:  # RGB
            # Already RGB
            return str(run.font.color.rgb)
        
        if run.font.color.type == 2:  # SCHEME
            # Resolve scheme color to RGB from source theme
            theme_color = run.font.color.theme_color
            rgb = get_theme_color_rgb(source_presentation, theme_color)
            return rgb
    except:
        pass
    
    return None


def get_theme_font_name_from_prs(presentation, is_major=False):
    """Get theme font name from presentation's theme."""
    try:
        master = presentation.slide_masters[0]
        master_elem = master._element
        ns_a = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
        
        themeElements = master_elem.find(f'.//{ns_a}themeElements')
        if themeElements is None:
            return None
        
        fontScheme = themeElements.find(f'{ns_a}fontScheme')
        if fontScheme is None:
            return None
        
        if is_major:
            font = fontScheme.find(f'{ns_a}majorFont')
        else:
            font = fontScheme.find(f'{ns_a}minorFont')
        
        if font is None:
            return None
        
        latin = font.find(f'{ns_a}latin')
        if latin is not None:
            typeface = latin.get('typeface')
            # Skip placeholder fonts
            if typeface and not typeface.startswith('+'):
                return typeface
    except:
        pass
    
    return None


def get_master_font_size(source_slide, placeholder_type='body', level=1):
    """Get the default font size from the source slide's master for a given placeholder type."""
    try:
        master = source_slide.slide_layout.slide_master
        master_elem = master._element
        ns = '{http://schemas.openxmlformats.org/presentationml/2006/main}'
        ns_a = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
        
        txStyles = master_elem.find(f'{ns}txStyles')
        if txStyles is not None:
            # Choose the right style based on placeholder type
            if placeholder_type == 'title':
                style = txStyles.find(f'{ns}titleStyle')
            elif placeholder_type == 'body':
                style = txStyles.find(f'{ns}bodyStyle')
            else:
                style = txStyles.find(f'{ns}otherStyle')
            
            if style is not None:
                # Get the level (lvl1pPr, lvl2pPr, etc.)
                lvlpPr = style.find(f'{ns_a}lvl{level}pPr')
                if lvlpPr is not None:
                    defRPr = lvlpPr.find(f'{ns_a}defRPr')
                    if defRPr is not None:
                        sz = defRPr.get('sz')
                        if sz:
                            # Size is in hundredths of a point
                            return int(sz) / 100
    except:
        pass
    return None


def apply_explicit_formatting(source_run, target_run, source_presentation, source_slide, shape, para):
    """
    Apply explicit formatting from source run to target run, resolving all theme-dependent values.
    
    This ensures the target run looks exactly like the source, regardless of theme differences.
    """
    from pptx.util import Pt
    from pptx.dml.color import RGBColor
    
    # 1. Font Size - ALWAYS make explicit
    if source_run.font.size:
        target_run.font.size = source_run.font.size
    else:
        # Get from master default
        placeholder_type = 'body'
        if hasattr(shape, 'is_placeholder') and shape.is_placeholder:
            try:
                ph_type = shape.placeholder_format.type
                if ph_type == 1:
                    placeholder_type = 'title'
                elif ph_type == 2:
                    placeholder_type = 'body'
                else:
                    placeholder_type = 'other'
            except:
                pass
        
        font_size = get_master_font_size(source_slide, placeholder_type, para.level + 1)
        if font_size:
            target_run.font.size = Pt(font_size)
        elif placeholder_type == 'title':
            # Fallback for title
            target_run.font.size = Pt(44)
        elif placeholder_type == 'body':
            # Fallback for body
            target_run.font.size = Pt(28)
    
    # 2. Font Name - try to get from theme, otherwise use common default
    if source_run.font.name:
        target_run.font.name = source_run.font.name
    else:
        # Get theme font
        is_major = False
        if hasattr(shape, 'is_placeholder') and shape.is_placeholder:
            try:
                if shape.placeholder_format.type == 1:  # TITLE
                    is_major = True
            except:
                pass
        
        theme_font = get_theme_font_name_from_prs(source_presentation, is_major)
        if theme_font:
            target_run.font.name = theme_font
        else:
            # Fallback - use Calibri as it's most common
            target_run.font.name = 'Calibri'
    
    # 3. Color - ALWAYS make explicit, resolving SCHEME to RGB
    rgb_color = resolve_run_color_to_rgb(source_run, source_presentation)
    if rgb_color:
        try:
            # Parse hex string to RGB
            r = int(rgb_color[0:2], 16)
            g = int(rgb_color[2:4], 16)
            b = int(rgb_color[4:6], 16)
            target_run.font.color.rgb = RGBColor(r, g, b)
        except:
            pass
    
    # 4. Bold, Italic, Underline
    if source_run.font.bold is not None:
        target_run.font.bold = source_run.font.bold
    if source_run.font.italic is not None:
        target_run.font.italic = source_run.font.italic
    if source_run.font.underline is not None:
        target_run.font.underline = source_run.font.underline
