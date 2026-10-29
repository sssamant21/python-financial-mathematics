# Outstanding platform and environment checks

All rows below remain open. No completion percentage is asserted.

| ID | Platform/workflow | Required evidence to close |
|---|---|---|
| ENV-01 | Windows launcher and venv | Actual py version/pip/create output and sys.executable from created environment |
| ENV-02 | Windows PowerShell and CMD activation | Both shells resolve the venv interpreter; direct python.exe works without activation; managed policy honored |
| ENV-03 | macOS bash/zsh | Actual environment creation, activation/direct execution and import outputs |
| ENV-04 | Notebook kernel | Successful real kernel startup, sys.executable matches selected venv; exact financial and NumPy cells executed, output retained |
| ENV-05 | JupyterLab server/UI | Authenticated local server starts; browser opens notebook; cell execution and kernel selection verified; server cleanly stopped; credentials excluded from evidence |
| ENV-06 | Wrong interpreter/package troubleshooting | Controlled import mismatch reproduced; interpreter/pip identified; repair verified in disposable environments |
| ENV-07 | Wrong notebook kernel troubleshooting | Controlled wrong kernel identified through sys.executable and corrected; outputs retained |
| ENV-08 | Recreate on supported platforms | Requirements/profile applied on each claimed OS/runtime; package check and smoke evidence retained; OS-specific dependency differences documented |

Linux setup and same-runtime recreation evidence do not close Windows/macOS or browser validation. Preserve the initial kernel failure when adding the successful follow-up.
