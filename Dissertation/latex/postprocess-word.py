"""Add Word section numbering and a linked figure list to a Pandoc DOCX."""

import argparse
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
XML = "http://www.w3.org/XML/1998/namespace"
for prefix, namespace in [
    ("w", W), ("r", R), ("mc", MC), ("w14", W + "14"),
    ("w15", W + "15"), ("wp14", "http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"),
]:
    ET.register_namespace(prefix, namespace)


def qn(namespace, local):
    return f"{{{namespace}}}{local}"


def _set_child(parent, tag, attributes):
    child = parent.find(qn(W, tag))
    if child is None:
        child = ET.Element(qn(W, tag))
        if parent.tag == qn(W, "pPr"):
            order = [
                "pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr",
                "widowControl", "numPr", "suppressLineNumbers", "pBdr", "shd",
                "tabs", "suppressAutoHyphens", "kinsoku", "wordWrap",
                "overflowPunct", "topLinePunct", "autoSpaceDE", "autoSpaceDN",
                "bidi", "adjustRightInd", "snapToGrid", "spacing", "ind",
                "contextualSpacing", "mirrorIndents", "suppressOverlap", "jc",
            ]
            rank = {qn(W, item): index for index, item in enumerate(order)}
            index = next(
                (
                    i for i, existing in enumerate(parent)
                    if rank.get(existing.tag, len(order)) > rank.get(child.tag, len(order))
                ),
                len(parent),
            )
            parent.insert(index, child)
        else:
            parent.append(child)
    child.attrib.clear()
    child.attrib.update({qn(W, key): str(value) for key, value in attributes.items()})
    return child


def _style_node(styles, style_id, name, based_on="Normal"):
    style = next(
        (
            node
            for node in styles.findall(qn(W, "style"))
            if node.get(qn(W, "styleId")) == style_id
        ),
        None,
    )
    if style is None:
        style = ET.SubElement(
            styles,
            qn(W, "style"),
            {qn(W, "type"): "paragraph", qn(W, "styleId"): style_id},
        )
    style.set(qn(W, "type"), "paragraph")
    name_node = style.find(qn(W, "name"))
    if name_node is None:
        name_node = ET.Element(qn(W, "name"))
        style.insert(0, name_node)
    name_node.set(qn(W, "val"), name)
    based_node = style.find(qn(W, "basedOn"))
    if style_id == "Normal":
        if based_node is not None:
            style.remove(based_node)
    else:
        if based_node is None:
            based_node = ET.Element(qn(W, "basedOn"))
            style.insert(1, based_node)
        based_node.set(qn(W, "val"), based_on)
    paragraph_properties = style.find(qn(W, "pPr"))
    if paragraph_properties is None:
        paragraph_properties = ET.Element(qn(W, "pPr"))
        run_properties = style.find(qn(W, "rPr"))
        index = list(style).index(run_properties) if run_properties is not None else len(style)
        style.insert(index, paragraph_properties)
    run_properties = style.find(qn(W, "rPr"))
    if run_properties is None:
        run_properties = ET.SubElement(style, qn(W, "rPr"))
    return style, paragraph_properties, run_properties


def _set_style(
    styles,
    style_id,
    name,
    *,
    size=24,
    bold=False,
    caps=False,
    alignment="both",
    line=480,
    before=0,
    after=0,
    first_line=0,
    left=None,
    hanging=None,
    keep_next=False,
    based_on="Normal",
    tab_stop=None,
    tab_leader="dot",
    exact_line=False,
):
    _, paragraph_properties, run_properties = _style_node(
        styles, style_id, name, based_on
    )
    if style_id == "TOCHeading":
        outline = paragraph_properties.find(qn(W, "outlineLvl"))
        if outline is not None:
            paragraph_properties.remove(outline)

    fonts = run_properties.find(qn(W, "rFonts"))
    if fonts is None:
        fonts = ET.SubElement(run_properties, qn(W, "rFonts"))
    for theme_attribute in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "csTheme"):
        fonts.attrib.pop(qn(W, theme_attribute), None)
    for attribute in ("ascii", "hAnsi", "eastAsia", "cs"):
        fonts.set(qn(W, attribute), "Times New Roman")
    _set_child(run_properties, "sz", {"val": size})
    _set_child(run_properties, "szCs", {"val": size})

    for tag in ("b", "bCs"):
        node = run_properties.find(qn(W, tag))
        if bold:
            if node is None:
                node = ET.SubElement(run_properties, qn(W, tag))
            node.attrib.pop(qn(W, "val"), None)
        elif node is not None:
            run_properties.remove(node)
    for tag in ("caps", "smallCaps"):
        node = run_properties.find(qn(W, tag))
        if tag == "caps" and caps:
            if node is None:
                ET.SubElement(run_properties, qn(W, tag))
        elif node is not None:
            run_properties.remove(node)

    _set_child(
        paragraph_properties,
        "spacing",
        {"before": before, "after": after, "line": line, "lineRule": "auto"},
    )
    _set_child(paragraph_properties, "jc", {"val": alignment})
    indentation = {"firstLine": first_line}
    if left is not None:
        indentation["left"] = left
    if hanging is not None:
        indentation.pop("firstLine")
        indentation["hanging"] = hanging
    _set_child(paragraph_properties, "ind", indentation)
    if keep_next:
        if paragraph_properties.find(qn(W, "keepNext")) is None:
            _set_child(paragraph_properties, "keepNext", {})
    else:
        keep = paragraph_properties.find(qn(W, "keepNext"))
        if keep is not None:
            paragraph_properties.remove(keep)
    if exact_line:
        paragraph_properties.find(qn(W, "spacing")).set(qn(W, "lineRule"), "exact")
    if tab_stop is not None:
        tabs = _set_child(paragraph_properties, "tabs", {})
        for tab in list(tabs):
            tabs.remove(tab)
        ET.SubElement(
            tabs,
            qn(W, "tab"),
            {
                qn(W, "val"): "right",
                qn(W, "leader"): tab_leader,
                qn(W, "pos"): str(tab_stop),
            },
        )


def normalize_styles(styles):
    defaults = styles.find(qn(W, "docDefaults"))
    if defaults is not None:
        default_run = defaults.find(qn(W, "rPrDefault"))
        if default_run is None:
            default_run = ET.SubElement(defaults, qn(W, "rPrDefault"))
        default_properties = default_run.find(qn(W, "rPr"))
        if default_properties is None:
            default_properties = ET.SubElement(default_run, qn(W, "rPr"))
        fonts = default_properties.find(qn(W, "rFonts"))
        if fonts is None:
            fonts = ET.SubElement(default_properties, qn(W, "rFonts"))
        for theme_attribute in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "csTheme"):
            fonts.attrib.pop(qn(W, theme_attribute), None)
        for attribute in ("ascii", "hAnsi", "eastAsia", "cs"):
            fonts.set(qn(W, attribute), "Times New Roman")
        _set_child(default_properties, "sz", {"val": 24})
        _set_child(default_properties, "szCs", {"val": 24})

    styles_to_format = [
        ("Normal", "Normal", 24, False, False, "both", 480, 0, 0, 360, None, None, False, "Normal", None),
        ("BodyText", "Body Text", 24, False, False, "both", 480, 0, 0, 360, None, None, False, "Normal", None),
        ("FirstParagraph", "First Paragraph", 24, False, False, "both", 480, 0, 0, 0, None, None, False, "BodyText", None),
        ("Title", "Title", 24, False, True, "center", 480, 0, 0, 0, None, None, False, "Normal", None),
        ("Author", "Author", 24, False, False, "center", 240, 0, 0, 0, None, None, False, "Normal", None),
        ("Date", "Date", 24, False, False, "center", 240, 0, 0, 0, None, None, False, "Normal", None),
        ("TitlePageBody", "Title Page Body", 24, False, False, "center", 240, 0, 0, 0, None, None, False, "Normal", None),
        ("AbstractTitle", "Abstract Title", 24, False, True, "center", 480, 0, 240, 0, None, None, False, "Normal", None),
        ("AbstractAuthor", "Abstract Author", 24, False, False, "center", 480, 0, 0, 0, None, None, False, "Normal", None),
        ("AbstractInstitution", "Abstract Institution", 24, False, False, "center", 480, 0, 240, 0, None, None, False, "Normal", None),
        ("AbstractAdviser", "Abstract Adviser", 24, False, False, "left", 480, 0, 240, 0, None, None, False, "Normal", None),
        ("ResearchStatusHeading", "Research Status Heading", 24, False, False, "center", 480, 0, 240, 0, None, None, False, "Normal", None),
        ("Heading1", "Heading 1", 29, True, False, "left", 480, 1440, 720, 0, None, None, True, "Normal", None),
        ("Heading2", "Heading 2", 29, True, False, "left", 480, 480, 240, 0, None, None, True, "Normal", None),
        ("Heading3", "Heading 3", 24, True, False, "left", 480, 360, 120, 0, None, None, True, "Normal", None),
        ("Heading4", "Heading 4", 24, True, False, "left", 480, 240, 120, 0, None, None, True, "Normal", None),
        ("FigureListEntry", "Figure List Entry", 24, False, False, "left", 480, 0, 120, 0, 0, None, False, "Normal", 8640),
        ("Bibliography", "Bibliography", 24, False, False, "both", 480, 0, 0, 0, 360, 360, False, "Normal", None),
        ("ImageCaption", "Image Caption", 20, False, False, "both", 400, 0, 0, 0, None, None, False, "Normal", None),
    ]
    for (
        style_id, name, size, bold, caps, alignment, line, before, after,
        first_line, left, hanging, keep_next, based_on, tab_stop,
    ) in styles_to_format:
        _set_style(
            styles, style_id, name, size=size, bold=bold, caps=caps,
            alignment=alignment, line=line, before=before, after=after,
            first_line=first_line, left=left, hanging=hanging,
            keep_next=keep_next, based_on=based_on, tab_stop=tab_stop,
        )

    _set_style(
        styles, "TOCHeading", "TOC Heading", size=29, bold=True,
        alignment="left", line=480, exact_line=True, after=1000,
        keep_next=True,
    )
    # Number and title offsets from the text margin, matching LaTeX.
    toc_columns = ((0, 0), (360, 900), (910, 1680), (1260, 2100))
    for level, (number, title) in enumerate(toc_columns, 1):
        _set_style(
            styles, f"TOC{level}", f"toc {level}", bold=level == 1,
            alignment="left", line=480, exact_line=True,
            before=240 if level == 1 else 0, left=title,
            hanging=title - number, tab_stop=8640,
            tab_leader="none" if level == 1 else "dot",
        )
    for style in styles.findall(qn(W, "style")):
        style_id = style.get(qn(W, "styleId"))
        if style_id in {"TOCHeading", "TOC1", "TOC2", "TOC3", "TOC4"}:
            properties = style.find(qn(W, "pPr"))
            _set_child(style.find(qn(W, "rPr")), "color", {"val": "000000"})
            _set_child(properties, "contextualSpacing", {"val": "0"})
            if style_id != "TOCHeading":
                _set_child(properties, "keepLines", {})
                properties.find(qn(W, "ind")).set(qn(W, "right"), "360")
                level = int(style_id[-1])
                if level > 1:
                    properties.find(qn(W, "tabs")).insert(0, ET.Element(
                        qn(W, "tab"),
                        {qn(W, "val"): "left", qn(W, "pos"): str(toc_columns[level - 1][1])},
                    ))
        elif style_id in {"Heading2", "Heading3", "Heading4"}:
            level = int(style_id[-1])
            number, title = toc_columns[level - 1]
            tabs = _set_child(style.find(qn(W, "pPr")), "tabs", {})
            tabs[:] = [ET.Element(qn(W, "tab"), {
                qn(W, "val"): "left",
                qn(W, "pos"): str(max(title - number, 640) if level == 2 else title - number),
            })]


def normalize_template(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Word reference template does not exist: {path}")
    with ZipFile(path) as archive:
        files = {name: archive.read(name) for name in archive.namelist()}
    if "word/styles.xml" not in files:
        raise ValueError("Reference template is missing word/styles.xml")
    styles = ET.fromstring(files["word/styles.xml"])
    normalize_styles(styles)
    files["word/styles.xml"] = ET.tostring(
        styles, encoding="utf-8", xml_declaration=True
    )
    temporary = path.with_name(path.name + ".tmp")
    try:
        with ZipFile(temporary, "w", ZIP_DEFLATED) as archive:
            for name, data in files.items():
                archive.writestr(name, data)
        with ZipFile(temporary) as archive:
            if archive.testzip() is not None:
                raise ValueError("Normalized reference template failed ZIP validation")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def find_toc(body):
    for child in body:
        if child.tag != qn(W, "sdt"):
            continue
        gallery = child.find(".//" + qn(W, "docPartGallery"))
        if gallery is not None and gallery.get(qn(W, "val")) == "Table of Contents":
            return child
    raise ValueError("Pandoc did not generate the expected Table of Contents field")


def find_marker(body, name):
    matches = []
    for child in body:
        if child.tag != qn(W, "p"):
            continue
        if any(
            start.get(qn(W, "name")) == f"DISSERTATION_{name}"
            for start in child.findall(".//" + qn(W, "bookmarkStart"))
        ):
            matches.append(child)
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {name} marker; found {len(matches)}")
    return matches[0]


def section_properties(header_id=None, page_format=None):
    section = ET.Element(qn(W, "sectPr"))
    if header_id:
        ET.SubElement(
            section, qn(W, "headerReference"),
            {qn(W, "type"): "default", qn(R, "id"): header_id},
        )
    ET.SubElement(section, qn(W, "type"), {qn(W, "val"): "nextPage"})
    ET.SubElement(section, qn(W, "pgSz"), {qn(W, "w"): "12240", qn(W, "h"): "15840"})
    ET.SubElement(
        section,
        qn(W, "pgMar"),
        {
            qn(W, "top"): "2160",
            qn(W, "right"): "1440",
            qn(W, "bottom"): "1440",
            qn(W, "left"): "2160",
            qn(W, "header"): "1440",
            qn(W, "footer"): "720",
            qn(W, "gutter"): "0",
        },
    )
    if page_format:
        ET.SubElement(
            section,
            qn(W, "pgNumType"),
            {qn(W, "fmt"): page_format, qn(W, "start"): "1"},
        )
    return section


def replace_marker_with_section(body, name, section):
    marker = find_marker(body, name)
    for node in list(marker):
        if node.tag != qn(W, "pPr"):
            marker.remove(node)
    paragraph_properties = marker.find(qn(W, "pPr"))
    if paragraph_properties is None:
        paragraph_properties = ET.Element(qn(W, "pPr"))
        marker.insert(0, paragraph_properties)
    paragraph_properties.append(section)


def paragraph_style(paragraph):
    style = paragraph.find(qn(W, "pPr") + "/" + qn(W, "pStyle"))
    return style.get(qn(W, "val")) if style is not None else ""


def paragraph_text(paragraph):
    parts = []
    for node in paragraph.iter():
        if node.tag == qn(W, "t"):
            parts.append(node.text or "")
        elif node.tag == qn(W, "br"):
            parts.append(" ")
    return "".join(parts)


def set_paragraph_style(paragraph, style_id):
    properties = paragraph.find(qn(W, "pPr"))
    if properties is None:
        properties = ET.Element(qn(W, "pPr"))
        paragraph.insert(0, properties)
    style = properties.find(qn(W, "pStyle"))
    if style is None:
        style = ET.Element(qn(W, "pStyle"))
        properties.insert(0, style)
    style.set(qn(W, "val"), style_id)


def attach_marker_bookmark(body, marker_name, bookmark_name, style_id):
    marker = find_marker(body, marker_name)
    children = list(body)
    marker_index = children.index(marker)
    target = next(
        (child for child in children[marker_index + 1:] if child.tag == qn(W, "p")),
        None,
    )
    if target is None:
        raise ValueError(f"No paragraph follows the {marker_name} marker")
    starts = marker.findall(".//" + qn(W, "bookmarkStart"))
    ends = marker.findall(".//" + qn(W, "bookmarkEnd"))
    if len(starts) != 1 or len(ends) != 1:
        raise ValueError(f"Expected one bookmark pair in the {marker_name} marker")
    start, end = starts[0], ends[0]
    start.set(qn(W, "name"), bookmark_name)
    set_paragraph_style(target, style_id)
    properties = target.find(qn(W, "pPr"))
    target.insert(list(target).index(properties) + 1 if properties is not None else 0, start)
    target.append(end)
    body.remove(marker)
    return target


def reorder_title_page(body):
    paragraphs = body.findall(qn(W, "p"))
    status_index = next(
        (
            index
            for index, paragraph in enumerate(paragraphs)
            if paragraph_style(paragraph) == "ResearchStatusHeading"
        ),
        None,
    )
    if status_index is None:
        raise ValueError("The Research Status heading was not generated")
    title = next(
        (p for p in paragraphs[:status_index] if paragraph_style(p) == "Title"),
        None,
    )
    author = next(
        (p for p in paragraphs[:status_index] if paragraph_style(p) == "Author"),
        None,
    )
    date = next(
        (p for p in paragraphs[:status_index] if paragraph_style(p) == "Date"),
        None,
    )
    if title is None or author is None or date is None:
        raise ValueError("The title-page title, author, or date paragraph is missing")

    title_index = list(body).index(title)
    status_index = list(body).index(
        next(p for p in body.findall(qn(W, "p"))
             if paragraph_style(p) == "ResearchStatusHeading")
    )
    title_page = [
        child
        for child in list(body)[title_index + 1:status_index]
        if child.tag == qn(W, "p")
    ]
    by_paragraph = next(
        (p for p in title_page if paragraph_text(p).strip().lower() == "by"),
        None,
    )
    if by_paragraph is None:
        raise ValueError("The title-page 'by' paragraph is missing")
    body.remove(author)
    insert_after = list(body).index(by_paragraph) + 1
    body.insert(insert_after, author)
    set_paragraph_style(author, "TitlePageBody")
    body.remove(date)
    set_paragraph_style(date, "TitlePageBody")
    paragraphs = body.findall(qn(W, "p"))
    status_index = next(
        i for i, p in enumerate(paragraphs)
        if paragraph_style(p) == "ResearchStatusHeading"
    )
    body_paragraphs = [
        p for p in paragraphs[:status_index]
        if paragraph_style(p) in {"TitlePageBody", "TitlePageBody0"}
    ]
    if len(body_paragraphs) != 8:
        raise ValueError(
            "Expected eight title-page body paragraphs before the date (by, "
            f"author, degree, manuscript, college, institution, adviser, location); found {len(body_paragraphs)}"
        )
    body.insert(list(body).index(body_paragraphs[-1]) + 1, date)
    body_paragraphs.append(date)
    for paragraph in body_paragraphs:
        set_paragraph_style(paragraph, "TitlePageBody")

    spacing_before = (720, 720, 1080, 360, 1080, 360, 1080, 900, 216)
    for paragraph, before in zip(body_paragraphs, spacing_before):
        properties = paragraph.find(qn(W, "pPr"))
        if properties is None:
            properties = ET.Element(qn(W, "pPr"))
            paragraph.insert(0, properties)
        spacing = properties.find(qn(W, "spacing"))
        if spacing is None:
            spacing = ET.SubElement(properties, qn(W, "spacing"))
        spacing.set(qn(W, "before"), str(before))
        spacing.set(qn(W, "after"), "0")
        spacing.set(qn(W, "line"), "240")
        spacing.set(qn(W, "lineRule"), "auto")


def format_abstract_paragraph(body):
    paragraphs = body.findall(qn(W, "p"))
    adviser_index = next(
        (
            index for index, paragraph in enumerate(paragraphs)
            if paragraph_style(paragraph) == "AbstractAdviser"
        ),
        None,
    )
    if adviser_index is None:
        raise ValueError("The abstract adviser paragraph was not generated")
    first_abstract_paragraph = next(
        (
            paragraph
            for paragraph in paragraphs[adviser_index + 1:]
            if paragraph_text(paragraph).strip()
        ),
        None,
    )
    if first_abstract_paragraph is None:
        raise ValueError("The abstract has no body paragraph")
    set_paragraph_style(first_abstract_paragraph, "FirstParagraph")


def center_title_page(body):
    centered_styles = {"Title", "Author", "Date", "TitlePageBody", "TitlePageBody0"}
    for paragraph in body.findall(qn(W, "p")):
        properties = paragraph.find(qn(W, "pPr"))
        if properties is not None and properties.find(qn(W, "sectPr")) is not None:
            break
        if paragraph_style(paragraph) not in centered_styles:
            continue
        if properties is None:
            properties = ET.Element(qn(W, "pPr"))
            paragraph.insert(0, properties)
        alignment = properties.find(qn(W, "jc"))
        if alignment is None:
            alignment = ET.Element(qn(W, "jc"))
            style = properties.find(qn(W, "pStyle"))
            properties.insert(list(properties).index(style) + 1, alignment)
        alignment.set(qn(W, "val"), "center")


def figure_captions(body):
    active_bookmarks = {}
    figures = []
    for child in body:
        if child.tag == qn(W, "bookmarkStart"):
            active_bookmarks[child.get(qn(W, "id"))] = child.get(qn(W, "name"))
        elif child.tag == qn(W, "bookmarkEnd"):
            active_bookmarks.pop(child.get(qn(W, "id")), None)
        elif child.tag == qn(W, "p") and paragraph_style(child) == "ImageCaption":
            anchors = [name for name in active_bookmarks.values() if name]
            if not anchors:
                raise ValueError(
                    f"Figure caption has no bookmark: {paragraph_text(child)[:100]}"
                )
            figures.append((paragraph_text(child), anchors[-1]))
        elif child.tag == qn(W, "p"):
            for node in child.iter(qn(W, "bookmarkStart")):
                active_bookmarks[node.get(qn(W, "id"))] = node.get(qn(W, "name"))
            for node in child.iter(qn(W, "bookmarkEnd")):
                active_bookmarks.pop(node.get(qn(W, "id")), None)
    if not figures:
        raise ValueError("No Word figure captions were generated")
    return figures


def make_run(text, style=None):
    run = ET.Element(qn(W, "r"))
    if style:
        properties = ET.SubElement(run, qn(W, "rPr"))
        ET.SubElement(properties, qn(W, "rStyle"), {qn(W, "val"): style})
    text_node = ET.SubElement(run, qn(W, "t"))
    text_node.text = text
    if text[:1].isspace() or text[-1:].isspace():
        text_node.set(qn(XML, "space"), "preserve")
    return run


def make_figures_heading():
    paragraph = ET.Element(qn(W, "p"))
    properties = ET.SubElement(paragraph, qn(W, "pPr"))
    ET.SubElement(properties, qn(W, "pStyle"), {qn(W, "val"): "Heading1"})
    ET.SubElement(
        paragraph,
        qn(W, "bookmarkStart"),
        {qn(W, "id"): "990007", qn(W, "name"): "LIST_OF_FIGURES"},
    )
    paragraph.append(make_run("List of Figures"))
    ET.SubElement(paragraph, qn(W, "bookmarkEnd"), {qn(W, "id"): "990007"})
    return paragraph


def append_toc_entry_field(paragraph, label, identifier="C", level=1):
    paragraph.extend(
        [
            make_field_run("begin"),
            make_instruction_run(f' TC "{label}" \\f {identifier} \\l "{level}" '),
            make_field_run("end"),
        ]
    )


def make_figure_entry(caption, bookmark):
    paragraph = ET.Element(qn(W, "p"))
    properties = ET.SubElement(paragraph, qn(W, "pPr"))
    ET.SubElement(properties, qn(W, "pStyle"), {qn(W, "val"): "FigureListEntry"})
    hyperlink = ET.SubElement(
        paragraph,
        qn(W, "hyperlink"),
        {qn(W, "anchor"): bookmark, qn(W, "history"): "1"},
    )
    hyperlink.append(make_run(caption, "Hyperlink"))
    tab_run = ET.SubElement(paragraph, qn(W, "r"))
    ET.SubElement(tab_run, qn(W, "tab"))
    paragraph.extend(
        [
            make_field_run("begin"),
            make_instruction_run(f" PAGEREF {bookmark} \\h "),
            make_field_run("separate"),
            make_run("1"),
            make_field_run("end"),
        ]
    )
    return paragraph


def prepare_native_toc(toc):
    # Word suppresses paragraph space-before at the top after our page break.
    # Place the reference's chapter-opening offset outside the TOC field.
    content = toc.find(qn(W, "sdtContent"))
    content.insert(0, ET.fromstring(
        f'<w:p xmlns:w="{W}"><w:pPr><w:keepNext/>'
        '<w:spacing w:before="0" w:after="0" w:line="1440" w:lineRule="exact"/>'
        '</w:pPr></w:p>'
    ))
    instructions = [
        node for node in toc.iter(qn(W, "instrText"))
        if (node.text or "").strip().startswith("TOC ")
    ]
    if len(instructions) != 1:
        raise ValueError(
            f"Expected one native TOC field; found {len(instructions)}"
        )
    instructions[0].text = ' TOC \\o "1-4" \\h \\w \\z \\f C '
    begin_fields = [
        node for node in toc.iter(qn(W, "fldChar"))
        if node.get(qn(W, "fldCharType")) == "begin"
    ]
    if len(begin_fields) != 1:
        raise ValueError(
            f"Expected one TOC field start; found {len(begin_fields)}"
        )
    begin_fields[0].set(qn(W, "dirty"), "true")


def move_toc_to_marker(body, toc, marker):
    marker = find_marker(body, marker)
    if toc not in body:
        raise ValueError("The native TOC field is not a direct document child")
    body.remove(toc)
    index = list(body).index(marker)
    body.remove(marker)
    body.insert(index, toc)


def make_field_run(field_type):
    run = ET.Element(qn(W, "r"))
    ET.SubElement(run, qn(W, "fldChar"), {qn(W, "fldCharType"): field_type})
    return run


def make_instruction_run(instruction):
    run = ET.Element(qn(W, "r"))
    node = ET.SubElement(run, qn(W, "instrText"))
    node.set(qn(XML, "space"), "preserve")
    node.text = instruction
    return run


def replace_marker_with_figures(body, figures):
    marker = find_marker(body, "FIGURES")
    index = list(body).index(marker)
    body.remove(marker)
    entries = [make_figures_heading()]
    entries.extend(make_figure_entry(caption, anchor) for caption, anchor in figures)
    for offset, entry in enumerate(entries):
        body.insert(index + offset, entry)


def make_header():
    return ET.fromstring(
        f"""<w:hdr xmlns:w="{W}">
  <w:p>
            <w:pPr><w:spacing w:before="0" w:after="0"/><w:jc w:val="right"/></w:pPr>
    <w:r><w:fldChar w:fldCharType="begin"/></w:r>
    <w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>
    <w:r><w:fldChar w:fldCharType="separate"/></w:r>
    <w:r><w:t>1</w:t></w:r>
    <w:r><w:fldChar w:fldCharType="end"/></w:r>
  </w:p>
</w:hdr>"""
    )


def replace_section_properties(final_section, header_id):
    replace_tags = {
        qn(W, name)
        for name in ("headerReference", "footerReference", "type", "pgSz", "pgMar", "pgNumType")
    }
    for child in list(final_section):
        if child.tag in replace_tags:
            final_section.remove(child)
    replacement = section_properties(header_id, "decimal")
    for child in reversed(list(replacement)):
        final_section.insert(0, child)


def add_header_relationship(data, header_id, target):
    root = ET.fromstring(data)
    if any(item.get("Id") == header_id for item in root):
        raise ValueError(f"Relationship ID already exists: {header_id}")
    ET.SubElement(
        root,
        qn(REL, "Relationship"),
        {
            "Id": header_id,
            "Type": f"{R}/header",
            "Target": target,
        },
    )
    ET.register_namespace("", REL)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def add_header_content_type(data, part_name):
    root = ET.fromstring(data)
    if any(item.get("PartName") == part_name for item in root):
        raise ValueError(f"Content type already exists: {part_name}")
    ET.SubElement(
        root,
        qn(CT, "Override"),
        {
            "PartName": part_name,
            "ContentType": "application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml",
        },
    )
    ET.register_namespace("", CT)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def process(source, output):
    source = Path(source)
    output = Path(output)
    if source.resolve() == output.resolve():
        raise ValueError("Input and output must be separate DOCX files")
    with ZipFile(source) as archive:
        files = {name: archive.read(name) for name in archive.namelist()}
    for required in (
        "word/document.xml",
        "word/_rels/document.xml.rels",
        "[Content_Types].xml",
        "word/settings.xml",
        "word/styles.xml",
    ):
        if required not in files:
            raise ValueError(f"Input DOCX is missing {required}")

    document = ET.fromstring(files["word/document.xml"])
    document.attrib.pop(qn(MC, "Ignorable"), None)
    body = document.find(qn(W, "body"))
    if body is None:
        raise ValueError("Input DOCX has no document body")
    status_heading = attach_marker_bookmark(
        body, "STATUS", "RESEARCH_STATUS", "ResearchStatusHeading"
    )
    abstract_title = attach_marker_bookmark(
        body, "ABSTRACT", "ABSTRACT", "AbstractTitle"
    )
    append_toc_entry_field(status_heading, "Research Status")
    append_toc_entry_field(abstract_title, "Abstract")
    reorder_title_page(body)
    format_abstract_paragraph(body)
    center_title_page(body)
    figures = figure_captions(body)
    toc = find_toc(body)
    prepare_native_toc(toc)
    move_toc_to_marker(body, toc, "TOC")

    replace_marker_with_figures(body, figures)
    roman_header_id = "rIdWordReviewRoman"
    roman_header_target = "header-word-review-roman.xml"
    arabic_header_id = "rIdWordReviewArabic"
    arabic_header_target = "header-word-review-arabic.xml"
    replace_marker_with_section(
        body, "TITLE_SECTION_END", section_properties()
    )
    replace_marker_with_section(
        body,
        "ARABIC_SECTION_END",
        section_properties(roman_header_id, "lowerRoman"),
    )

    final_section = next(
        (child for child in body if child.tag == qn(W, "sectPr")), None
    )
    if final_section is None:
        raise ValueError("Input DOCX has no final section properties")
    replace_section_properties(final_section, arabic_header_id)
    files["word/document.xml"] = ET.tostring(
        document, encoding="utf-8", xml_declaration=True
    )
    for header_id, header_target in (
        (roman_header_id, roman_header_target),
        (arabic_header_id, arabic_header_target),
    ):
        files["word/_rels/document.xml.rels"] = add_header_relationship(
            files["word/_rels/document.xml.rels"], header_id, header_target
        )
        files["[Content_Types].xml"] = add_header_content_type(
            files["[Content_Types].xml"], f"/word/{header_target}"
        )
        files[f"word/{header_target}"] = ET.tostring(
            make_header(), encoding="utf-8", xml_declaration=True
        )

    settings = ET.fromstring(files["word/settings.xml"])
    update_fields = settings.find(qn(W, "updateFields"))
    if update_fields is None:
        update_fields = ET.SubElement(settings, qn(W, "updateFields"))
    update_fields.set(qn(W, "val"), "true")
    files["word/settings.xml"] = ET.tostring(
        settings, encoding="utf-8", xml_declaration=True
    )
    styles = ET.fromstring(files["word/styles.xml"])

    if len(body.findall(".//" + qn(W, "sectPr"))) != 3:
        raise ValueError("Expected distinct title, Roman-front-matter, and Arabic sections")
    if any(
        start.get(qn(W, "name"), "").startswith("DISSERTATION_")
        for start in document.findall(".//" + qn(W, "bookmarkStart"))
    ):
        raise ValueError("A Word conversion marker was not processed")
    if not any(
        paragraph_style(p) == "TOCHeading"
        and paragraph_text(p).strip() == "Table of Contents"
        for p in toc.iter(qn(W, "p"))
    ):
        raise ValueError("The Table of Contents heading was not placed")
    for bookmark_name in ("RESEARCH_STATUS", "ABSTRACT", "LIST_OF_FIGURES"):
        bookmark_names = [
            node.get(qn(W, "name"))
            for node in document.iter(qn(W, "bookmarkStart"))
        ]
        if bookmark_names.count(bookmark_name) != 1:
            raise ValueError(f"Expected one linked front-matter bookmark: {bookmark_name}")
    title_paragraph = next(
        (p for p in body.findall(qn(W, "p")) if paragraph_style(p) == "Title"),
        None,
    )
    status_paragraph = next(
        (p for p in body.findall(qn(W, "p"))
         if paragraph_style(p) == "ResearchStatusHeading"),
        None,
    )
    if title_paragraph is None or status_paragraph is None:
        raise ValueError("The title-page title or Research Status heading is missing")
    title_page_paragraphs = [
        p for p in body.findall(qn(W, "p"))
        if paragraph_style(p) == "TitlePageBody"
    ]
    title_texts = [paragraph_text(p).strip() for p in title_page_paragraphs]
    if len(title_texts) != 9 or title_texts[0].lower() != "by":
        raise ValueError("Title-page author/date order or content is invalid")
    if not title_texts[1] or not title_texts[-1]:
        raise ValueError("The title-page author or date is blank")
    if any(
        paragraph_style(p) == "Heading1"
        and paragraph_text(p).strip().lower() == "abstract"
        for p in body.findall(qn(W, "p"))
    ):
        raise ValueError("An extra Abstract heading was generated")
    toc_instructions = [
        node.text or ""
        for node in document.iter(qn(W, "instrText"))
        if (node.text or "").strip().startswith("TOC ")
    ]
    if len(toc_instructions) != 1 or '\\o "1-4"' not in toc_instructions[0] or "\\f C" not in toc_instructions[0]:
        raise ValueError("The dynamic Word TOC field is missing required switches")
    tc_instructions = [
        node.text or ""
        for node in document.iter(qn(W, "instrText"))
        if (node.text or "").strip().startswith("TC ")
    ]
    if not any('"Research Status"' in instruction for instruction in tc_instructions):
        raise ValueError("The dynamic TOC is missing its Research Status entry")
    if not any('"Abstract"' in instruction for instruction in tc_instructions):
        raise ValueError("The dynamic TOC is missing its Abstract entry")
    figure_entry_count = sum(
        paragraph_style(p) == "FigureListEntry" for p in body.findall(qn(W, "p"))
    )
    if figure_entry_count != len(figures):
        raise ValueError("A List of Figures entry was lost during Word postprocessing")
    if len([p for p in body.findall(qn(W, "p")) if paragraph_style(p) == "ImageCaption"]) != len(figures):
        raise ValueError("A figure caption was lost during Word postprocessing")
    for style_id in (
        "Normal", "Heading1", "Heading2", "Heading3", "Heading4",
        "TitlePageBody",
    ):
        style = next(
            (
                node for node in styles.findall(qn(W, "style"))
                if node.get(qn(W, "styleId")) == style_id
            ),
            None,
        )
        if style is None:
            raise ValueError(f"Word reference template is missing style {style_id}")

    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for name, data in files.items():
            archive.writestr(name, data)
    with ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise ValueError("Postprocessed DOCX package failed ZIP integrity validation")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--normalize-template", type=Path)
    args = parser.parse_args()
    if args.normalize_template:
        if args.input or args.output:
            parser.error("--normalize-template cannot be combined with --input or --output")
        normalize_template(args.normalize_template)
    elif args.input and args.output:
        process(args.input, args.output)
    else:
        parser.error("Provide --input and --output, or provide --normalize-template")


if __name__ == "__main__":
    main()
