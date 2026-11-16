"""Create a page-image Word copy of the compiled dissertation PDF."""

import re
import struct
import subprocess
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile


BASE = Path(__file__).resolve().parent
PDF = BASE / "Dissertation.pdf"
OUTPUT = BASE / "Dissertation-visual.docx"
DPI = 300
WIDTH_EMU = 612 * 12700
HEIGHT_EMU = 792 * 12700


def page_paragraph(number):
    page_break = '<w:pageBreakBefore/>' if number > 1 else ''
    # Anchoring to the page avoids the extra line required by an inline image.
    return f"""
<w:p>
  <w:pPr>{page_break}<w:spacing w:before="0" w:after="0" w:line="20"
    w:lineRule="exact"/></w:pPr>
  <w:r><w:rPr><w:sz w:val="2"/></w:rPr><w:drawing>
    <wp:anchor distT="0" distB="0" distL="0" distR="0" simplePos="0"
      relativeHeight="0" behindDoc="1" locked="1" layoutInCell="1" allowOverlap="1">
      <wp:simplePos x="0" y="0"/>
      <wp:positionH relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionH>
      <wp:positionV relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionV>
      <wp:extent cx="{WIDTH_EMU}" cy="{HEIGHT_EMU}"/>
      <wp:effectExtent l="0" t="0" r="0" b="0"/>
      <wp:wrapNone/>
      <wp:docPr id="{number}" name="PDF page {number}" descr="Dissertation PDF page {number}"/>
      <wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>
      <a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
        <pic:pic>
          <pic:nvPicPr><pic:cNvPr id="{number}" name="page-{number}.png"/><pic:cNvPicPr/></pic:nvPicPr>
          <pic:blipFill><a:blip r:embed="rId{number}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
          <pic:spPr>
            <a:xfrm><a:off x="0" y="0"/><a:ext cx="{WIDTH_EMU}" cy="{HEIGHT_EMU}"/></a:xfrm>
            <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          </pic:spPr>
        </pic:pic>
      </a:graphicData></a:graphic>
    </wp:anchor>
  </w:drawing></w:r>
</w:p>"""


def build():
    info = subprocess.run(
        ["pdfinfo", str(PDF)], check=True, stdout=subprocess.PIPE,
        text=True, encoding="utf-8"
    ).stdout
    pages_match = re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE)
    if not pages_match:
        raise ValueError("pdfinfo did not report a page count")
    count = int(pages_match.group(1))
    page_info = subprocess.run(
        ["pdfinfo", "-f", "1", "-l", str(count), "-box", str(PDF)],
        check=True, stdout=subprocess.PIPE, text=True, encoding="utf-8"
    ).stdout
    sizes = re.findall(r"^Page\s+\d+ size:\s+([\d.]+) x ([\d.]+)", page_info, re.MULTILINE)
    rotations = re.findall(r"^Page\s+\d+ rot:\s+(-?\d+)", page_info, re.MULTILINE)
    if len(sizes) != count or any((float(w), float(h)) != (612, 792) for w, h in sizes):
        raise ValueError("The visual Word export requires letter-size PDF pages")
    if len(rotations) != count or any(int(rotation) != 0 for rotation in rotations):
        raise ValueError("The visual Word export requires unrotated PDF pages")

    title_match = re.search(r"^Title:\s+(.+)$", info, re.MULTILINE)
    title = escape(title_match.group(1) if title_match else "Dissertation")
    with tempfile.TemporaryDirectory(prefix="dissertation-word-") as directory:
        temporary = Path(directory)
        subprocess.run(
            ["pdftoppm", "-r", str(DPI), "-png", "-cropbox", "-progress",
             str(PDF), str(temporary / "page")],
            check=True
        )
        images = sorted(
            temporary.glob("page-*.png"),
            key=lambda image: int(image.stem.rsplit("-", 1)[1])
        )
        if len(images) != count:
            raise ValueError(f"Expected {count} rendered pages, found {len(images)}")
        for number, image in enumerate(images, 1):
            if int(image.stem.rsplit("-", 1)[1]) != number:
                raise ValueError(f"Missing rendered PDF page {number}")
            with image.open("rb") as stream:
                header = stream.read(24)
            if header[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", header[16:24]) != (2550, 3300):
                raise ValueError(f"PDF page {number} does not have the expected 300-DPI dimensions")

        document = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
 xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
 xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
 <w:body>{''.join(page_paragraph(number) for number in range(1, count + 1))}
  <w:sectPr><w:pgSz w:w="12240" w:h="15840"/>
   <w:pgMar w:top="0" w:right="0" w:bottom="0" w:left="0" w:header="0" w:footer="0" w:gutter="0"/>
  </w:sectPr>
 </w:body>
</w:document>"""
        relationships = [
            f'<Relationship Id="rId{number}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/page-{number}.png"/>'
            for number in range(1, count + 1)
        ]
        relationships.append(
            '<Relationship Id="settings" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>'
        )
        packaged = temporary / "Dissertation.docx"
        with ZipFile(packaged, "w", ZIP_DEFLATED) as docx:
            docx.writestr("[Content_Types].xml", """<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="png" ContentType="image/png"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>""")
            docx.writestr("_rels/.rels", """<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="document" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="core" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="app" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>""")
            docx.writestr("word/document.xml", document)
            docx.writestr(
                "word/_rels/document.xml.rels",
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                + "".join(relationships) + "</Relationships>"
            )
            docx.writestr("word/settings.xml", """<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:doNotAutoCompressPictures/>
</w:settings>""")
            docx.writestr("docProps/core.xml", f"""<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>{title}</dc:title></cp:coreProperties>""")
            docx.writestr("docProps/app.xml", f"""<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
<Application>Dissertation visual Word export</Application><Pages>{count}</Pages>
</Properties>""")
            for number, image in enumerate(images, 1):
                docx.write(image, f"word/media/page-{number}.png")
        packaged.replace(OUTPUT)
    print(f"Created {OUTPUT}: {count} PDF pages at {DPI} DPI")


if __name__ == "__main__":
    build()
