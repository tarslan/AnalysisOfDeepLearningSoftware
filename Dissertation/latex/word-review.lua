local W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
local chapter = 0
local figure = 0
local section_numbers = {0, 0, 0}
local status_found = false
local notice_found = false
local arabic_section_found = false
local abstract_metadata_pending = 0

local function raw_block(xml)
  return pandoc.RawBlock("openxml", xml)
end

local function page_break()
  return raw_block(
    '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
  )
end

local function marker(name, id)
  return raw_block(string.format(
    '<w:p><w:bookmarkStart w:id="%d" w:name="DISSERTATION_%s"/>' ..
    '<w:bookmarkEnd w:id="%d"/></w:p>',
    id, name, id
  ))
end

local function styled_block(block, style)
  local attr = pandoc.Attr("", {}, {["custom-style"] = style})
  return pandoc.Div({block}, attr)
end

local function metadata_inlines(value)
  if not value then
    return {}
  end
  if value.t == "MetaList" then
    return value[1] and value[1].c or {}
  end
  if value.t == "MetaInlines" then
    return value.c
  end
  return {pandoc.Str(pandoc.utils.stringify(value))}
end

local function is_unnumbered(header, bibliography_title)
  local attr = header.attr
  local title = pandoc.utils.stringify(header.content)
  return attr.classes:includes("unnumbered")
    or attr.identifier == "refs"
    or attr.identifier == "bibliography"
    or title == bibliography_title
end

local function add_chapter_number(header)
  chapter = chapter + 1
  figure = 0
  section_numbers = {0, 0, 0}
  local numbered = {
    pandoc.Str("Chapter"),
    pandoc.Space(),
    pandoc.Str(tostring(chapter)),
    pandoc.LineBreak()
  }
  for _, inline in ipairs(header.content) do
    numbered[#numbered + 1] = inline
  end
  header.content = numbered
end

local function add_section_number(header)
  if header.level < 2 or header.level > 4 then
    return
  end
  local counter_index = header.level - 1
  section_numbers[counter_index] = section_numbers[counter_index] + 1
  for index = counter_index + 1, #section_numbers do
    section_numbers[index] = 0
  end
  local parts = {tostring(chapter)}
  for index = 1, counter_index do
    parts[#parts + 1] = tostring(section_numbers[index])
  end
  local numbered = {
    pandoc.Str(table.concat(parts, ".")),
    pandoc.RawInline("openxml", "<w:r><w:tab/></w:r>")
  }
  for _, inline in ipairs(header.content) do
    numbered[#numbered + 1] = inline
  end
  header.content = numbered
end

local function process_blocks(input, bibliography_title, title_meta, author_meta)
  local output = pandoc.List()
  for _, block in ipairs(input) do
    if block.t == "Div" and block.classes:includes("titlepage") then
      block.attributes["custom-style"] = "Title Page Body"
      output:insert(block)
    elseif block.t == "Para"
      and pandoc.utils.stringify(block):upper() == "RESEARCH STATUS" then
      output:insert(marker("TITLE_SECTION_END", 990001))
      output:insert(marker("STATUS", 990005))
      output:insert(pandoc.Header(
        1, "RESEARCH STATUS",
        pandoc.Attr("research-status", {"unnumbered"})
      ))
      status_found = true
    elseif status_found and not notice_found and block.t == "Para" then
      assert(
        pandoc.utils.stringify(block):find(
          "Working manuscript, not a completed-results dissertation.", 1, true
        ),
        "Expected the working-manuscript notice after Research Status"
      )
      output:insert(block)
      output:insert(page_break())
      output:insert(marker("ABSTRACT", 990006))
      output:insert(styled_block(
        pandoc.Para(metadata_inlines(title_meta)),
        "Abstract Title"
      ))
      output:insert(styled_block(
        pandoc.Para(metadata_inlines(author_meta)),
        "Abstract Author"
      ))
      abstract_metadata_pending = 2
      notice_found = true
    elseif block.t == "Header" and block.level == 1
      and not is_unnumbered(block, bibliography_title) then
      add_chapter_number(block)
      if chapter == 1 then
        output:insert(page_break())
        output:insert(marker("TOC", 990002))
        output:insert(page_break())
        output:insert(marker("FIGURES", 990003))
        output:insert(marker("ARABIC_SECTION_END", 990004))
        arabic_section_found = true
      else
        output:insert(page_break())
      end
      output:insert(block)
    elseif block.t == "Header" then
      add_section_number(block)
      output:insert(block)
    elseif block.t == "Figure" then
      assert(chapter > 0, "A figure appeared before the first numbered chapter")
      figure = figure + 1
      local caption = block.caption.long[1]
      assert(
        caption and (caption.t == "Para" or caption.t == "Plain"),
        "Expected a paragraph caption for figure " .. block.identifier
      )
      table.insert(caption.content, 1, pandoc.Space())
      table.insert(
        caption.content, 1,
        pandoc.Str(string.format("Figure %d.%d:", chapter, figure))
      )
      output:insert(block)
    elseif abstract_metadata_pending > 0 and block.t == "Para" then
      abstract_metadata_pending = abstract_metadata_pending - 1
      output:insert(styled_block(
        block,
        abstract_metadata_pending == 1 and "Abstract Institution" or "Abstract Adviser"
      ))
    elseif block.t == "Div" or block.t == "BlockQuote" then
      block.content = process_blocks(
        block.content, bibliography_title, title_meta, author_meta
      )
      output:insert(block)
    else
      output:insert(block)
    end
  end
  return output
end

function Pandoc(doc)
  local bibliography_title = pandoc.utils.stringify(
    doc.meta["reference-section-title"] or pandoc.Str("Bibliography")
  )
  doc.blocks = process_blocks(
    doc.blocks, bibliography_title, doc.meta.title, doc.meta.author
  )
  assert(status_found and notice_found, "Missing dissertation status or abstract")
  assert(chapter > 0 and arabic_section_found, "Missing numbered dissertation chapters")
  return doc
end
