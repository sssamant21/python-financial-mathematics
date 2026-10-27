"""Capstone requirements catalog: authored claims, not validation evidence."""
REQUIREMENTS = {
    "F1": "Validate paired cash flows and domain",
    "F2": "Specify rate convention and time units",
    "F3": "Provide independent benchmarks and checks",
    "F4": "Document tolerances and diagnostics",
    "F5": "Record source, inputs and environment",
    "F6": "Distinguish invalid input, numerical failure and missing evidence",
    "F7": "Report synthetic scenario assumptions and limitations",
    "F8": "Separate execution, review and approval",
}

def pending_record():
    """Create a fresh evidence record; no execution or approval is claimed."""
    return {"requirements": dict(REQUIREMENTS),
            "source_commit": None, "execution": "not run",
            "independent_review": "pending", "approval": "pending"}

def missing_fields(record):
    """Return missing evidence fields; field presence is not evidence verification."""
    fields = ("source_commit", "environment", "command", "result")
    return [key for key in fields if record.get(key) is None]

if __name__ == "__main__":
    record = pending_record()
    print("Requirements:", len(record["requirements"]))
    print("Missing execution evidence:", missing_fields(record))
    print("Execution and independent review remain pending.")
