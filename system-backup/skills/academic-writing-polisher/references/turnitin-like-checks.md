# Turnitin-Like Academic Integrity Checks (Local Workflow)

## When to Use

Use this reference when the user asks to:

- Simulate a Turnitin similarity score.
- Detect plagiarism/local duplication without accessing Turnitin's private database.
- Analyze thesis/citation accuracy before official submission.

## Local Workflow (Non-Cloud)

### Tools
- **Pandoc**: Extract text from `.docx`/`.pdf`.
- **Python**: `difflib`, `re`, `web_search` (Hermes web search tool).
- **Local database**: None required.

### Steps
1. **Extract text** (e.g., `pandoc -i thesis.docx -o thesis.txt`).
2. **Clean text**: Remove citations, figures, appendices.
3. **Chunk text**: 30-word overlapping segments (50% overlap).
4. **Search top 3-5 chunks** via `web_search(query=f'"{chunk}" site:scholar.google.com OR site:pubmed.ncbi.nlm.nih.gov', limit=3)`.
5. **Flag high overlap**: If any chunk has >80% match to online content, flag for review.

### Limitations
- ❌ No access to Turnitin's private database (other students' submissions).
- ❌ Common phrases/methods may not trigger matches (false negatives).
- ✅ Fast, local, no credentials required.

## Interpretation Guide

| Score Range | Risk Level | Action |
|------------|------------|--------|
| `< 15%` | Low | Cite sources explicitly; no rewriting needed |
| `15–30%` | Medium | Add citations; rewrite paraphrased sections |
| `> 30%` | High | Full quotation/citation check; methodology rewrite |

## Manual Review Checklist

1. **Citations**: Are all claims backed by `(Author, Year)`?
2. **Paraphrasing**: Rewrite sentences ≥20 words identical to sources.
3. **Methods section**: Use active voice + precise verbs (e.g., "we measured" vs. "was measured").
4. **Common phrases**: Replace boilerplate (e.g., "green manure enhances soil fertility") with original phrasing + citation.

## Output Format

```markdown
**Similarity Estimate**
- Local check: X% (based on public sources)
- Turnitin risk: [Low/Medium/High]

**Flagged Chunks**
1. [30-word chunk] → [URL]
2. ...

**Suggested Fixes**
- Add citation `(Author, Year)` for [claim].
- Rewrite paragraph X as: [new phrasing].
```

## Notes
- For official submission, **always upload to Turnitin first**.
- This workflow is a *pre-flight check*, not a replacement.