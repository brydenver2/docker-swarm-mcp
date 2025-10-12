# doc-gateway Constitution
## Core Principles & Immutable Rules

### 🎯 Mission
Create lightweight gateway documentation that preserves context windows while providing quick reference to external dependencies.

### 📜 The Sacred Template Format
**This template structure is IMMUTABLE and validated through extensive use.**

Every gateway doc MUST follow this exact structure:
1. **Title** with dependency name
2. **Overview** sentence with one-line description
3. **Short Description** (2-3 sentences)
4. **Key Features** (exactly 5 items)
5. **MCP Tool Guidance** section (MUST reference DeepWiki)
6. **Static Backup Reference** link
7. **Official Source** link

### 🔧 The DeepWiki Doctrine
**DeepWiki MCP is the PRIMARY tool for preserving context windows.**

#### Quick Reference (During Active Development)
- **USE**: `DeepWiki ask_question()` for immediate answers
- **EXAMPLE**: `ask_question("How do I implement streaming with Vercel AI SDK?")`
- **BENEFIT**: Get precise answers without loading entire docs

#### Deep Research (Planning Phase)
- **USE**: Static-backup markdown files
- **WHEN**: Dedicated research/planning sessions
- **WHERE**: `./static-backup/[dependency].md`

#### The Golden Rule
> "DeepWiki for coding. Static files for planning."

Every gateway doc MUST include explicit DeepWiki instructions:
```
## USE DEEPWIKI MCP TO ACCESS DEPENDENCY KNOWLEDGE!
To access the most up-to-date documentation for this framework, use the DeepWiki MCP to retrieve information directly from the source repository. Access the repository at https://github.com/[user/repo] and use the `ask_question` function with specific queries like "how can I [specific task]" to get targeted guidance.

For broader context during planning, the full static docs are available at: 
[./static-backup/[filename].md](./static-backup/[filename].md)
```

### 🏗️ File Structure Rules

#### Naming Convention (STRICT)
- **Format**: `{type}_{name}_{descriptor}.md`
- **Examples**:
  - `framework_vercel_ai_sdk.md`
  - `api_stripe.md`
  - `library_lodash.md`
  - `tool_eslint.md`

#### Directory Structure (IMMUTABLE)
```
docs/
├── frameworks/
│   ├── framework_*.md           # Gateway docs (point to DeepWiki)
│   └── static-backup/           # Full documentation (for planning)
├── apis/
│   ├── api_*.md
│   └── static-backup/
├── libraries/
│   ├── library_*.md
│   └── static-backup/
└── tools/
    ├── tool_*.md
    └── static-backup/
```

### 🔄 API Priority Rules

#### Source Detection Order
1. **GitHub pattern** → ref.tools first
2. **NPM package** → Context7 first
3. **URL** → Firecrawl only

#### Fallback Chain (MANDATORY)
- **GitHub**: ref.tools → Firecrawl
- **NPM**: Context7 → ref.tools → Firecrawl
- **URL**: Firecrawl (no fallback)

### ⚡ Performance Standards
- **Max execution**: 10 seconds typical
- **Large repo timeout**: 60 seconds
- **User feedback**: Always show progress indicators

### 🚫 Forbidden Actions
- **NEVER** modify template structure
- **NEVER** change folder names from `static-backup`
- **NEVER** skip fallback chain
- **NEVER** mix naming conventions
- **NEVER** inline large docs in gateway files
- **NEVER** overwrite without confirmation
- **NEVER** omit DeepWiki instructions from gateway docs

### ✅ Quality Gates
All outputs MUST:
1. Match template compliance exactly
2. Include explicit DeepWiki MCP instructions
3. Create correct file structure
4. Follow naming convention strictly
5. Handle errors gracefully
6. Generate both gateway and static files

### 🎭 Philosophy
> "Context windows are precious real estate. Every token counts."

Gateway docs are **navigation aids**, not encyclopedias. They:
- Point to DeepWiki for quick answers during coding
- Reference static-backup for deep planning sessions
- Preserve context by keeping docs external
- Enable fast, targeted information retrieval

### 🏛️ Governance
This constitution can only be modified when:
1. Template format proves insufficient (3+ real failures)
2. New dependency type emerges (beyond current four)
3. Structure change saves >20% context
4. DeepWiki MCP is replaced by superior tool

---

**Remember**: 
- DeepWiki = Quick answers during coding
- Static-backup = Deep research during planning
- The template and structure are battle-tested. Honor them.

*Constitution Version: 1.1.0*
*Established: 2024*
*Updated: Added DeepWiki Doctrine*