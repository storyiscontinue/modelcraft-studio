# Rubric Handling

Innovation and entrepreneurship rubrics often contain dimensions such as education, innovation,
team, commercial feasibility, and social value. Their names and weights vary by cycle, track, and
group.

Do not hard-code a year-specific weighting. Parse the current official rubric and create:

```json
{
  "criterion_id": "",
  "label": "",
  "weight": null,
  "official_text": "",
  "evidence_required": [],
  "red_flags": [],
  "source_url": "",
  "retrieved_at": ""
}
```

For every criterion, separate evidence from narrative quality. A polished slide cannot compensate
for a missing prototype test, fabricated interview, unsupported market number, or unverified patent.