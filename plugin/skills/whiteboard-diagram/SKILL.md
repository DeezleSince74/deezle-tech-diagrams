---
name: whiteboard-diagram
description: Draw a Mermaid diagram (architecture-beta, flowchart, erDiagram, stateDiagram-v2) or an infrastructure-as-code export (Terraform, Pulumi, Bicep, CloudFormation) on a Claude Whiteboard, with open icons or the official AWS, Azure and Google Cloud icons the person imports. Use when someone asks to draw, diagram or map a system, data model, process or state machine on a whiteboard, or asks for a diagram they can share and edit with others.
---

# Whiteboard diagram

This skill turns a Mermaid diagram into a Claude Whiteboard. The board does the drawing.
This skill adds three things the board doesn't know: how each Mermaid part maps to a board
element, how to lay the parts out without a layout engine, and where to find icons.

## 1. Get the Mermaid source

- If the person gave Mermaid, use it.
- If they described a system, write the Mermaid first. Keep it to about 25 nodes or fewer.
  Past that, draw the top level and offer a second board for the detail.
- If they gave an infrastructure-as-code file, read it and list the resources and how they
  connect. Turn networks and resource groups into groups, resources into services, and
  references between resources into edges. Read `iac-types.md` in this skill's folder first:
  it shows how to turn any resource type (Terraform, Pulumi, CloudFormation or Bicep) into an
  icon ref, which resources to leave out, and examples.

## 2. Open a board

Find the Whiteboard type with the Artifact tool (`action: "quickstart"`, or a `types`
listing), then create the board from its `type_url` with a short `title`. Don't hardcode the
type link. The creation result includes the type's own instructions. **Follow those for the
element format, colors, spacing and how to write.** They win over anything here if the two
disagree, because the board format can change.

If no Whiteboard type is listed, Whiteboards is off for this account (it's a beta, off by
default on Enterprise plans). Say so in one line and give the Mermaid source instead.

## 3. Map each part

| Mermaid | Board element |
| --- | --- |
| `group id(icon)[Label]` | `container`, `text` = Label. Nested groups nest. |
| `service id(icon)[Label]` | `image` 64 × 64 with the icon, plus a `text` label |
| `service` with no icon found | `shape` `rounded`, 160 × 64, `text` = Label |
| `junction` | `shape` `ellipse`, 16 × 16 |
| edge `a:R --> L:b` | `arrow` from a to b, `fromSide` right, `toSide` left |
| edge with no arrowhead (`--`) | `arrow` with `head: "none"` |
| erDiagram entity | `table`, 3 columns: header row = entity name then two empty cells, then one row per attribute (name, type, key) |
| erDiagram relationship | `arrow` from the "one" side to the "many" side, `label` = the relationship text plus the cardinality in words: `||` is "1", `o|` "0 or 1", `|{` "1 or more", `o{` "0 or more", so `||--o{ : places` becomes `places (1 to 0 or more)` |
| flowchart `[ ]`, `( )`, `([ ])`, `[[ ]]` | `shape` `rect`, `rounded`, `pill`, `rect` |
| flowchart `{ }` | `shape` `diamond`, larger (at least 160 × 120) |
| flowchart `{{ }}`, `(( ))` | `shape` `hexagon`, `ellipse` |
| flowchart `[/ /]`, `[\ \]` | `shape` `parallelogram` |
| flowchart `[( )]` | `shape` `database` |
| flowchart `subgraph` | `container`, `text` = its title |
| flowchart `-.->` | `arrow` with `dash: true` |
| flowchart `==>` | plain `arrow` (the board has no thick arrows) |
| stateDiagram state | `shape` `pill`, 160 × 56 |
| stateDiagram `[*]` start or end | `shape` `ellipse`, 24 × 24, in the type's darkest color; each end gets its own dot |
| stateDiagram `<<choice>>` | `shape` `diamond`, 160 × 120 |
| stateDiagram composite `state X { }` | `container` with its own start and end dots inside |
| stateDiagram `note` | yellow `rounded` shape on the side Mermaid names, or the opposite side if an arrow runs there |
| any edge text (`-->|yes|`, `-- no -->`, `a --> b : text`) | the arrow's `label` |

Mermaid sides map to board sides: `L` left, `R` right, `T` top, `B` bottom.

**Icons.** An icon ref looks like `aws:amazon-rds`. First look it up in `icons/aliases.json`
(for example `aws:s3` becomes `aws:amazon-simple-storage-service`). Then search for the text
`"ref":"aws:amazon-rds"`. Each line holds one icon. Copy its `src` value exactly into the
image's `src`, with `"by": "claude"`. Never edit or retype an icon.

- **`aws`, `azure` and `gcp`** aren't shipped. Search the files the person imported in
  `~/.deezle-tech-diagrams/icons/` (`aws-1.json`, `aws-2.json`, …; search them all).
  Vendors rename icons between releases, so if a ref isn't found, try it once more with a
  leading `aws-` or `azure-` removed from the name.
- **`generic`, `open` (Simple Icons and Lucide) and `data` (data-platform logos)** are in
  this skill's `icons/` folder.

If a vendor ref isn't imported, use the `open:kind-*` icon that fits the service (`compute`,
`database`, `storage`, `network`, `security`, `analytics`, `marketplace`, `thirdparty`,
`other`), or `open:googlecloud` for a Google Cloud service with no better match. If nothing
fits, use the plain shape from the table. When vendor icons fell back, say so once in the
final reply and mention that the import-icons skill adds the official ones.

**Card style (only when asked).** If the person asks for cards, draw each service as one
`image`, 240 wide and 80 tall, instead of a bare icon. Build its `src` like this, all on one
line:

`data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 240 80' data-look='clean'>`
then three shadow boxes, `<rect x='2' y='6' width='236' height='66' rx='14' fill='%23142a5a' opacity='0.05'/>`
(again with x 3, y 8, width 234 and x 4, y 10, width 232, all height 66), then the card,
`<rect x='0.5' y='0.5' width='239' height='71' rx='14' fill='%23ffffff' stroke='ACCENT' stroke-opacity='0.45'/>`,
then `<g transform='translate(15,16) scale(S)'>ICON</g></svg>`.

ICON is the icon's `src` with the leading `data:image/svg+xml,<svg …>` and the final `</svg>`
removed. S is 40 divided by the icon's `w`. ACCENT is `%23FF9900` for AWS, `%230078D4` for
Azure, `%234285F4` for Google Cloud, and `%238A94AD` for everything else. Then add two `text`
elements at the card's x + 68: a `small` one at y + 16 with the provider and service
(`AWS · RDS`), and a bold one at y + 34 with the label. Arrows join the card image. Give the
card image and both text elements the same `groups` value, `["g-<card image id>"]`, so the
three drag as one piece. Don't lock them: a locked element loses its groups.

If a card's icon isn't found, draw the card without the `<g>` icon part and start its text at
x + 24. Keep the small line under about 22 characters (shorten the service name), and give the
label `wrap` 160. Place cards 320 apart across and 160 apart down.

**Labels.** Put a service's label where no arrow runs: to the left of the icon (right-aligned,
`wrap` 140) when arrows leave its top, bottom and right, otherwise below it (centered,
`wrap` 160).

## 4. Lay it out

There is no layout engine, so work out positions before writing anything.

1. **Order.** Follow the edges. `a:B --> T:b` puts b below a. `a:R --> L:b` puts b to the
   right of a. With no sides given, lay the main path left to right, whatever the Mermaid
   direction says, because boards read left to right. In an erDiagram, start on the left with
   an entity that has no "one" side above it (a parent, such as CUSTOMER), and follow the
   relationships right. If that doesn't fit on two rows, a "many" side may sit above.
2. **Rows.** Put the main path (the happy path) on the top row. After about 6 steps, start a
   second row back at the left, never running backward. Break between groups, not inside one.
   The arrow that wraps leaves the bottom of the last step, runs left through the gap between
   rows with `bends`, and enters the top of the next row's first step. If a branch already
   leaves that bottom (a decision's "no"), the wrap leaves the right side instead, turns down
   past the branch, then runs left under it, for example `bends: ["h", 170, -154]`. Put side branches
   (errors, rejections) on the row below the step they leave from, and leave 144 units
   between rows for the wrap arrow and branch labels.
3. **Spacing.** Measure gaps edge to edge, not center to center. Use 64 units between nodes an
   unlabeled arrow joins, and 144 when the arrow has a label (wider if the label is long:
   about 8 units per character plus 48). Put architecture icons on a grid
   of 260 between columns and 200 between rows, which leaves room for their labels. Size a
   table about 90 units wide per column and 32 tall per row. Line up the centers of anything
   an arrow joins, so arrows run straight.
4. **Groups.** Size each container to hold its children plus 24 units of padding. A nested
   container needs 52 units above it for its title. Leave 64 units between containers that an
   arrow crosses, or 144 if that arrow has a label.
5. **Crossings and back edges.** If an arrow would cross a node or a label, move the node to a
   free spot first. Give two arrows on one node different sides, so they don't share a line.
   An arrow that goes back to an earlier step (a retry, a loop) runs under
   the row with `bends`, never over the top, where the title sits.
6. **Color.** Use at most 4 colors, one per role (for example: steps, decisions, errors,
   notes). The type's instructions list the color names.
7. **Frame.** Start with a title (`size` title) and one takeaway line of 10 words or fewer
   (`size` large). Aim for about 1,500 × 750. If two rows with labeled arrows need more, go a
   little past it rather than shrinking the gaps.

## 5. Write it

If the board was opened with a claim id, do the type's claim step first. Then write
everything in one `ArtifactData` `batch` (50 writes and 1 MB per call; use more calls if
needed): `board/meta` first with every id in `order` back to front, then the containers, then
shapes, tables, text and icons, then the arrows. Element ids are `e1`, `e2`, and so on.

When editing an existing board, follow the type's instructions: read it fresh, change only
what the ask needs, and never rebuild it.

## What the board can't do

- **Animated connectors.** Board arrows don't animate. Use `dash: true` for async or optional
  flows instead. If the person asks for moving arrows, say the board can't animate them.
  Don't add `html` embeds to a diagram: everything on it stays a board element people can
  move and edit.
- **Gradients.** Imported icons that used gradients are flattened to one color, so a few
  Azure icons look flatter than the originals.

After the last write, reply in two or three sentences: what you drew, what you assumed, and
anything left off (for example, icons that fell back to plain shapes).
