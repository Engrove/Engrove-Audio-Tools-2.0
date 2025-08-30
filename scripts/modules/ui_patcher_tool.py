# scripts/modules/ui_patcher_tool.py
# Frankensteen Module: Standalone JSON_Diff Patcher Tool UI

def get_html():
    """Returns the HTML structure for the Patcher Tool tab."""
    return """
        <div class="tab-content" id="patcher-tool-content" style="display:none;">
            <h2>JSON Diff Patcher Tool</h2>
            <p>Applies a structured patch based on the <code>json_diff</code> protocol. Verifies base checksum before applying.</p>
            <div class="patcher-container">
                <div class="patcher-column">
                    <label for="base-content">Base File Content</label>
                    <textarea id="base-content" class="patcher-textarea" spellcheck="false" placeholder="Paste the full, original file content here..."></textarea>
                    <div class="checksum-display">
                        <strong>Calculated Base SHA-256:</strong> <code id="calculated-base-checksum">N/A</code>
                    </div>
                </div>
                <div class="patcher-column">
                    <label for="patch-object">JSON Patch Object (<code>json_diff</code>)</label>
                    <textarea id="patch-object" class="patcher-textarea" spellcheck="false" placeholder="Paste the json_diff object here..."></textarea>
                     <div class="checksum-display">
                        <strong>Required Base SHA-256:</strong> <code id="required-base-checksum">N/A</code>
                    </div>
                </div>
                <div class="patcher-column">
                    <label for="patched-result">Patched Result (Read-only)</label>
                    <textarea id="patched-result" class="patcher-textarea" readonly spellcheck="false"></textarea>
                     <div class="checksum-display">
                        <strong>Result SHA-256:</strong> <code id="calculated-result-checksum">N/A</code>
                    </div>
                </div>
            </div>
            <div class="patcher-controls">
                <button id="apply-patch-btn">Apply Patch</button>
                <div id="patcher-status"></div>
            </div>
        </div>
    """

def get_styles():
    """Returns the CSS for the Patcher Tool UI."""
    return """
        .patcher-container { display: flex; gap: 15px; width: 100%; height: 60vh; }
        .patcher-column { flex: 1; display: flex; flex-direction: column; }
        .patcher-textarea { width: 100%; flex-grow: 1; font-family: 'Fira Code', 'Courier New', monospace; font-size: 12px; background-color: #1a1a1a; color: #e0e0e0; border: 1px solid #444; border-radius: 4px; padding: 10px; resize: none; }
        .patcher-controls { margin-top: 15px; display: flex; align-items: center; gap: 15px; }
        #apply-patch-btn { padding: 10px 15px; font-weight: bold; background-color: #007acc; color: white; border: none; border-radius: 4px; cursor: pointer; }
        #apply-patch-btn:hover { background-color: #0099ff; }
        #patcher-status { font-weight: bold; }
        .status-success { color: #4CAF50; }
        .status-error { color: #F44336; }
        .status-warning { color: #FFC107; }
        .checksum-display { margin-top: 5px; font-size: 11px; color: #999; height: 20px; }
        #calculated-base-checksum.match { color: #4CAF50; font-weight: bold; }
        #calculated-base-checksum.mismatch { color: #F44336; font-weight: bold; }
    """

def get_js():
    """Returns the JavaScript logic for the Patcher Tool, including the adapted patcher module."""
    return r"""
// --- START: Standalone Patcher Module (Adapted for json_diff) ---
const PatcherModule = (() => {
    function canonText(text) {
        return (text || '').replace(/\uFEFF/g, '').replace(/\r\n?/g, '\\n');
    }

    async function sha256HexLF(text) {
        const enc = new TextEncoder().encode(canonText(text));
        const buf = await crypto.subtle.digest('SHA-256', enc);
        return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
    }

    function validatePatchObject(patch) {
        if (!patch || typeof patch !== 'object') return { valid: false, error: 'Patch must be a non-null object.' };
        if (patch.protocol_id !== 'json_diff') return { valid: false, error: `Invalid protocol_id: must be 'json_diff'.` };
        if (!patch.target || typeof patch.target.base_checksum_sha256 !== 'string' || !/^[a-f0-9]{64}$/.test(patch.target.base_checksum_sha256)) {
            return { valid: false, error: 'target.base_checksum_sha256 is missing or invalid.' };
        }
        if (!Array.isArray(patch.op_groups)) return { valid: false, error: 'op_groups must be an array.' };
        // Deeper validation can be added here based on schema.
        return { valid: true, error: null };
    }

    async function applyPatch(baseText, patchObject) {
        const validation = validatePatchObject(patchObject);
        if (!validation.valid) {
            return { success: false, patchedText: null, error: `Validation failed: ${validation.error}`, warnings: [] };
        }

        let newText = canonText(baseText);
        const warnings = [];
        const { op_groups, result_sha256 } = patchObject;

        try {
            const fullReplaceOp = op_groups.flatMap(g => g.targets).find(t => t.op === 'replace_entire_file');
            if (fullReplaceOp) {
                newText = canonText(fullReplaceOp.new_content || '');
            } else {
                let textBuffer = newText;
                for (const group of op_groups) {
                    const anchorText = canonText(group.anchor.text);
                    const anchorIndex = textBuffer.indexOf(anchorText);
                    if (anchorIndex === -1) {
                         warnings.push(`Anchor not found: "${anchorText.substring(0, 50)}..."`);
                         continue;
                    }
                    
                    let searchOffset = anchorIndex + anchorText.length;
                    
                    for (const targetOp of group.targets) {
                        const oldBlock = canonText(targetOp.old_block);
                        const newBlock = canonText(targetOp.new_block);

                        const blockIndex = textBuffer.indexOf(oldBlock, searchOffset);
                        if (blockIndex === -1) {
                            warnings.push(`Operation "${targetOp.op}" skipped: old_block not found after anchor.`);
                            continue;
                        }

                        if (targetOp.op === 'replace_block') {
                            const prefix = textBuffer.substring(0, blockIndex);
                            const suffix = textBuffer.substring(blockIndex + oldBlock.length);
                            textBuffer = prefix + newBlock + suffix;
                            searchOffset = prefix.length + newBlock.length;
                        } else if (targetOp.op === 'delete_block') {
                            const prefix = textBuffer.substring(0, blockIndex);
                            const suffix = textBuffer.substring(blockIndex + oldBlock.length);
                            textBuffer = prefix + suffix;
                            searchOffset = prefix.length;
                        }
                    }
                }
                newText = textBuffer;
            }

            if (typeof result_sha256 === 'string' && result_sha256.length === 64) {
                const finalHash = await sha256HexLF(newText);
                if (finalHash.toLowerCase() !== result_sha256.toLowerCase()) {
                    warnings.push(`Verification failed: The resulting content hash (${finalHash}) does not match the expected result_sha256 (${result_sha256}).`);
                }
            }
            return { success: true, patchedText: newText, error: null, warnings };
        } catch (e) {
            return { success: false, patchedText: null, error: e.message, warnings };
        }
    }

    return { sha256HexLF, applyPatch };
})();
// --- END: Standalone Patcher Module ---

// --- START: UI Glue Logic ---
document.addEventListener('DOMContentLoaded', () => {
    const baseContentEl = document.getElementById('base-content');
    const patchObjectEl = document.getElementById('patch-object');
    const patchedResultEl = document.getElementById('patched-result');
    const applyBtn = document.getElementById('apply-patch-btn');
    const statusEl = document.getElementById('patcher-status');
    const calcBaseChecksumEl = document.getElementById('calculated-base-checksum');
    const reqBaseChecksumEl = document.getElementById('required-base-checksum');
    const calcResultChecksumEl = document.getElementById('calculated-result-checksum');

    const updateStatus = (message, type) => {
        statusEl.textContent = message;
        statusEl.className = `status-${type}`;
    };
    
    const debounce = (func, delay) => {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    };

    const updateChecksums = async () => {
        const baseText = baseContentEl.value;
        const patchText = patchObjectEl.value;

        if (baseText) {
            const hash = await PatcherModule.sha256HexLF(baseText);
            calcBaseChecksumEl.textContent = hash;
        } else {
            calcBaseChecksumEl.textContent = 'N/A';
        }
        
        let requiredHash = 'N/A';
        try {
            const patch = JSON.parse(patchText);
            requiredHash = patch?.target?.base_checksum_sha256 || 'N/A';
        } catch (e) { /* ignore parse error for now */ }

        reqBaseChecksumEl.textContent = requiredHash;
        
        if (calcBaseChecksumEl.textContent !== 'N/A' && reqBaseChecksumEl.textContent !== 'N/A') {
             calcBaseChecksumEl.classList.toggle('match', calcBaseChecksumEl.textContent === reqBaseChecksumEl.textContent);
             calcBaseChecksumEl.classList.toggle('mismatch', calcBaseChecksumEl.textContent !== reqBaseChecksumEl.textContent);
        } else {
             calcBaseChecksumEl.className = '';
        }
    };

    baseContentEl.addEventListener('input', debounce(updateChecksums, 250));
    patchObjectEl.addEventListener('input', debounce(updateChecksums, 250));

    applyBtn.addEventListener('click', async () => {
        updateStatus('Applying patch...', 'warning');
        patchedResultEl.value = '';
        calcResultChecksumEl.textContent = 'N/A';
        
        const baseText = baseContentEl.value;
        let patchObject;

        try {
            patchObject = JSON.parse(patchObjectEl.value);
        } catch (e) {
            updateStatus(`Error: Invalid JSON in patch object. ${e.message}`, 'error');
            return;
        }

        const baseChecksum = await PatcherModule.sha256HexLF(baseText);
        if (baseChecksum !== patchObject.target.base_checksum_sha256) {
            updateStatus('Error: Base content checksum does not match required checksum in patch.', 'error');
            return;
        }

        const result = await PatcherModule.applyPatch(baseText, patchObject);

        if (result.success) {
            patchedResultEl.value = result.patchedText;
            const resultHash = await PatcherModule.sha256HexLF(result.patchedText);
            calcResultChecksumEl.textContent = resultHash;
            
            let statusMessage = 'Patch applied successfully.';
            if (result.warnings.length > 0) {
                statusMessage += ` With ${result.warnings.length} warning(s): ${result.warnings.join('; ')}`;
                updateStatus(statusMessage, 'warning');
            } else {
                updateStatus(statusMessage, 'success');
            }
        } else {
            updateStatus(`Error: ${result.error}`, 'error');
        }
    });
});
// --- END: UI Glue Logic ---
    """
