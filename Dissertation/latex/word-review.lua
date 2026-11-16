local function page_break()
  return pandoc.RawBlock(
    "openxml",
    '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
  )
end

function Pandoc(doc)
  local blocks = pandoc.List()
  local chapter = 0
  local figure = 0
  local status_found = false
  local notice_found = false

  doc.meta.subtitle = pandoc.MetaInlines({pandoc.Str("Working manuscript")})

  for _, block in ipairs(doc.blocks) do
    local text = pandoc.utils.stringify(block)
    if block.t == "Div" and block.classes:includes("titlepage") then
      -- Pandoc cannot expand the title page's internal LaTeX metadata macros.
    elseif block.t == "Para" and text == "RESEARCH STATUS" then
      blocks:insert(page_break())
      blocks:insert(pandoc.Header(
        1, "Research Status", pandoc.Attr("research-status", {"unnumbered"})
      ))
      status_found = true
    elseif status_found and not notice_found and block.t == "Para" then
      assert(
        text:find("Working manuscript, not a completed-results dissertation.", 1, true),
        "Expected the working-manuscript notice after Research Status"
      )
      blocks:insert(block)
      blocks:insert(page_break())
      blocks:insert(pandoc.Header(
        1, "Abstract", pandoc.Attr("abstract", {"unnumbered"})
      ))
      notice_found = true
    else
      if block.t == "Header" and block.level == 1 then
        blocks:insert(page_break())
        if not block.classes:includes("unnumbered") then
          chapter = chapter + 1
          figure = 0
        end
      elseif block.t == "Figure" then
        assert(chapter > 0, "Expected a numbered chapter before a figure")
        figure = figure + 1
        local caption = block.caption.long[1]
        assert(
          caption and (caption.t == "Para" or caption.t == "Plain"),
          "Expected a paragraph caption for figure " .. block.identifier
        )
        caption.content:insert(1, pandoc.Space())
        caption.content:insert(
          1, pandoc.Str("Figure " .. chapter .. "." .. figure .. ":")
        )
      end
      blocks:insert(block)
    end
  end

  assert(status_found and notice_found, "Missing dissertation research-status front matter")
  doc.blocks = blocks
  return doc
end
