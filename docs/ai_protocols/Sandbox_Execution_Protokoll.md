# Sandbox Execution Protokoll v1.0

* **Minimikrav:** Isolering (Docker+gVisor), CPU/RAM-limit, nätverk OFF (default), timeout 120s, deterministisk seed.
* **Artefakter:** fånga stdout/stderr, exit-code, tidsstämplar, resursnyttjande. Spara som sandbox_run.json.
* **Koppling:** SANDBOX_EXEC-steg i DynamicProtocols; följer P-GB-3.9 för logg/hash.
* Docker‑container, gVisor‑runtime  
* **Resource limits**: no‑net, 256 MB RAM, 2 s CPU  
* **FS:** readonly, förutom `/tmp` (RW)  
* `run_tests.sh` **måste** passera innan kod levereras.


