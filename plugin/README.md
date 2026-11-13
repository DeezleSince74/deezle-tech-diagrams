# Deezle Tech Diagrams

Draw cloud architecture, data models, flowcharts and state machines on a
[Claude Whiteboard](https://claude.com/resources/articles/sheets-whiteboards-data).
Give Claude a Mermaid diagram, describe your system, or point it at a Terraform, Pulumi,
Bicep or CloudFormation export. Claude draws it on a board you can share, comment on and
edit with your team.

This is a skills-only plugin. It has no server and ships no code: it's instructions plus a
set of open icons stored as JSON (JavaScript Object Notation).

## What you need

- A paid Claude plan with Whiteboards turned on. Whiteboards is in beta. It's on by default
  for Team plans and off by default for Enterprise plans, where an admin turns it on under
  Organization settings > Artifacts.

## Install

**Now in Anthropic's plugin directory.** In Claude (web, desktop or mobile) or Cowork, open
**Customize > Plugins** and add **Deezle Tech Diagrams**.

In Claude Code 2.1.275 or later:

```
/plugin install deezle-tech-diagrams --marketplace DeezleSince74/deezle-tech-diagrams
```

## Try it

- *"Draw a 3-tier AWS web app with a VPC on a whiteboard."*
- *"Put this Mermaid on a whiteboard:"* followed by an `architecture-beta`, `flowchart`,
  `erDiagram` or `stateDiagram-v2` diagram.
- *"Diagram this Terraform state as a whiteboard."*

## What it supports

| Diagram | Drawn as |
| --- | --- |
| `architecture-beta` | Sections for groups, vendor icons for services, arrows for edges |
| `erDiagram` | One table per entity, arrows for relationships |
| `flowchart` | Shapes (diamonds for decisions), arrows, dashed arrows |
| `stateDiagram-v2` | Pill-shaped states with start and end dots |
| Terraform, Pulumi, Bicep or CloudFormation | Networks as sections, services as icons, connections as arrows |

About 150 open icons are included: plain cloud shapes, Simple Icons brand marks, Lucide
category icons (compute, database, storage, network and more), and data-platform logos.

## Infrastructure-as-code files

Hand Claude an infrastructure-as-code (IaC) file, such as a Terraform `.tf` file, a Pulumi
program, a Bicep file or a CloudFormation template. Claude reads each resource's type and works
out what to draw:

- **Sections:** networks, subnets and resource groups. A section with nothing in it is skipped.
- **Icons:** the services a person would point to, such as databases, functions, clusters,
  queues, buckets and load balancers. Claude matches each type to an icon, even types it has
  no example for, by working out the product name (`aws_opensearch_domain` becomes Amazon
  OpenSearch Service).
- **Arrows:** one resource pointing to another. Arrows follow the way data or calls flow, so a
  queue points to the function that reads it. A resource that only links two others, such as
  a Lambda event source mapping, becomes an arrow instead of a box.
- **Left out:** settings that only set up another resource, such as policies, security group
  rules, DNS (Domain Name System) records, bucket settings, and logging and monitoring setup.
  Ask for them if you want them drawn.

## Official AWS, Azure and Google Cloud icons

The official cloud icons belong to Amazon, Microsoft and Google, so this plugin doesn't ship
them. Each person gets their own copy, under the vendor's terms. Ask *"use the official AWS
icons"* (or Azure, or Google Cloud), and the **import-icons** skill:

1. Gives you the vendor's official icon page and asks you to read its terms.
2. Asks you to download the icon zip from that page yourself and hand Claude the file.
3. Converts the icons on your computer into `~/.deezle-tech-diagrams/icons`.

The plugin never downloads anything and makes no network requests. Until you import a
vendor's set, its services are drawn with open category icons or plain shapes. Ask *"which
icons do I have?"* to check, or *"remove the imported icons"* to undo it.

Ask for **card style** (*"draw it with cards"*) to get each service as a white card with its
icon, provider and name, like the Deezle Infra Diagrams look. Each card and its two text
lines are grouped, so they drag as one piece.

## Limits

- Claude places every box itself, with no layout engine. Diagrams up to about 25 nodes look
  clean. Larger ones are split across boards.
- Board arrows don't animate. Dashed arrows mark async or optional flows instead.
- Imported icons that used color gradients are shown in one flat color, and a few that the
  board can't draw are left out.
- Imported icons are saved on your computer, so they last in Claude Code and Cowork. In a
  chat with no saved files, they last only for that chat.

## Privacy, security and support

The plugin collects nothing and sends nothing. See `PRIVACY.md`. To report a security
problem, see `SECURITY.md`. For questions or bugs, open an
[issue](https://github.com/DeezleSince74/deezle-tech-diagrams/issues).

## Icons and trademarks

The bundled icons are open source. See `ATTRIBUTION.md`. Imported vendor icons are your own
copies, under each vendor's terms. All product names and icons are trademarks of their
owners.

## License

MIT. See `LICENSE.md`.
