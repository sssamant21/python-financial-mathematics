"""Illustrative checklist; this code does not approve or verify evidence."""
REQUIRED = ("specification", "tests", "mathematical_review", "business_review")

def evaluate_checklist(evidence):
    """Return completeness and reasons. Status strings are claims, not proof."""
    if not isinstance(evidence, dict):
        raise TypeError("evidence must be a dictionary")
    reasons = []
    for key in REQUIRED:
        entry = evidence.get(key)
        if not isinstance(entry, dict):
            reasons.append(f"{key}: missing")
            continue
        if entry.get("status") != "complete":
            reasons.append(f"{key}: not complete")
        reference = entry.get("reference")
        if not isinstance(reference, str) or not reference.strip():
            reasons.append(f"{key}: evidence reference missing")
    return {"checklist_complete": not reasons, "reasons": reasons,
            "release_approved": False}

if __name__ == "__main__":
    print(evaluate_checklist({}))
    print("Checklist completeness is not a release approval.")
