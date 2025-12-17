// frontend/src/lib/api.js

const API_BASE =
  process.env.REACT_APP_API_BASE_URL ||
  process.env.REACT_APP_API_URL ||
  "http://localhost:8000/api";

async function request(path, opts = {}) {
  const url = path.startsWith("http") ? path : `${API_BASE}${path.startsWith("/api") ? path.slice(4) : path}`;

  const headers = opts.headers || {};
  const isFormData = typeof FormData !== "undefined" && opts.body instanceof FormData;

  const finalOpts = {
    ...opts,
    headers: isFormData
      ? headers
      : {
          "Content-Type": "application/json",
          ...headers,
        },
  };

  const res = await fetch(url, finalOpts);
  const text = await res.text();
  let data = null;

  try {
    data = text ? JSON.parse(text) : null;
  } catch (e) {
    data = text;
  }

  if (!res.ok) {
    const msg =
      (data && data.detail) ||
      (typeof data === "string" && data) ||
      `HTTP ${res.status}`;
    throw new Error(msg);
  }

  return data;
}

/**
 * What your UI expects (based on import errors):
 * - complianceAPI, complianceApi
 * - artifactsApi
 * - evidenceApi
 * - systemAPI
 * - repoScanAPI
 * - validateZipFile
 */

// ---- Compliance ----
export const complianceApi = {
  health: async () => request("/health", { method: "GET" }),
};
export const complianceAPI = complianceApi;

// ---- Artifacts ----
export const artifactsApi = {
  upload: async (file, type, scanId) => {
    const fd = new FormData();
    fd.append("file", file);
    if (type) fd.append("type", type);
    if (scanId) fd.append("scan_id", scanId);
    return request("/artifacts/upload", { method: "POST", body: fd });
  },
};

// ---- Evidence ----
export const evidenceApi = {
  getEvidence: async (scanId) =>
    request(`/evidence/${encodeURIComponent(scanId)}`, { method: "GET" }),

  runAnalyzers: async (scanId, analyzers = []) =>
    request("/evidence/run", {
      method: "POST",
      body: JSON.stringify({ scan_id: scanId, analyzers }),
    }),

  getRawEvidence: async (scanId, evidenceId) =>
    request(
      `/evidence/${encodeURIComponent(scanId)}/${encodeURIComponent(
        evidenceId
      )}/raw`,
      { method: "GET" }
    ),
};

// ---- System (NetworkDebug.js expects these functions) ----
export const systemAPI = {
  getInfo: async () => request("/health", { method: "GET" }),
  healthCheck: async () => request("/health", { method: "GET" }),
  getControls: async () => request("/health", { method: "GET" }),
};

// ---- Repo scan (stub to satisfy imports; implement later if endpoint exists) ----
export const repoScanAPI = {
  scan: async () => {
    throw new Error("repoScanAPI.scan is not implemented yet");
  },
};

// ---- validateZipFile (stub; components expect it) ----
async function validateZipFile() {
  // Minimal: always "valid". Replace with real checks later.
  return { ok: true };
}
// ---- formatFileSize (helper) ----
function formatFileSize(bytes) {
  if (bytes === undefined || bytes === null) return "";
  const n = Number(bytes);
  if (Number.isNaN(n)) return String(bytes);
  if (n < 1024) return `${n} B`;
  const kb = n / 1024;
  if (kb < 1024) return `${kb.toFixed(1)} KB`;
  const mb = kb / 1024;
  if (mb < 1024) return `${mb.toFixed(1)} MB`;
  const gb = mb / 1024;
  return `${gb.toFixed(1)} GB`;
}

export { formatFileSize };
export { request };
export { validateZipFile };
