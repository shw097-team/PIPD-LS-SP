// OPTIONAL_SITE_UI: excluded from the Web denominator (R-AUD-003). The Web pack is the five PIPD_*.md documents.
fetch('PROJECTION_IR.json').then(r => r.json()).then(ir => {document.getElementById('app').textContent = 'PIPD-LS-SP OPTIONAL_SITE_UI ' + ir.projection_parity_sha256;});
