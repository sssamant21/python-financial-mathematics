# Unimplemented E7/E8 policy tests

These are proposed cases,not executed tests,predicates,workflows or new historical methods.

| Policy | Proposed input | Required outcome | Status |
|---|---|---|---|
| Quote age | Quote exactly30minutes old,available before cutoff | Eligible under proposed inclusive rule;retain timestamp/age/carry flag | NOT IMPLEMENTED |
| Quote age | Quote30minutes+1second old | Reject/withhold;row count is irrelevant | NOT IMPLEMENTED |
| Quote age | Recent event published after decision cutoff | Ineligible despite recent event time | NOT IMPLEMENTED |
| Quote age | Future event,missing/naive time,wrong instrument/currency/adjustment basis | Reject invalid/incompatible input | NOT IMPLEMENTED |
| Quote age | Duplicate/revised quotes with same eligibility time | Apply documented source-backed precedence or reject ambiguity | NOT IMPLEMENTED |
| Zero-weight exception | Expected missing BETA at exact opening weight0 | Preserve BETA/data gap;optional separately flagged calculation eligibility under approved exception | NOT IMPLEMENTED |
| Zero-weight exception | Missing positive or tiny positive weight | Withhold calculation;no near-zero tolerance exemption | NOT IMPLEMENTED |
| Zero-weight exception | Zero-weight observed infinity or below−1 return | Reject invalid observation,do not suppress it | NOT IMPLEMENTED |
| Zero-weight exception | Unexpected/duplicate IDs or invalid weight sum | Preserve source identity/domain rejection | NOT IMPLEMENTED |
| Zero-weight exception | All prices/returns observed | Match original strict result and coverage | NOT IMPLEMENTED |

The actual runner exercises unchanged strict source for missingzero-weight,observedzero-weight,tinypositive and invalidobservedzero-weight cases. It does not claim the exception works. A changed eligibility rule needs separately named output fields,policy version,reproducible expected-universe evidence and external agreement before adoption. Likewise,maximum quote age must be justified by instrument/feed/use rather than copied universally. Neither policy permits a fabricated complete market-data history.
