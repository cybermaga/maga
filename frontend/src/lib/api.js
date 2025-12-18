/**
 * frontend/src/lib/api.js
 * Single source of truth for frontend API helpers.
 * Goal: keep exports stable so the app compiles.
 */

const API_BASE =
  process.env.REACT_APP_API_BASE_URL ||
  process.env.REACT_APP_API_URL ||
  process.env.REACT_APP_BACKEND_URL ||
  "http://localhost:8000/api";

async function request(path, opts = {}) {
  const url = path.startsWith("http") ? path : `${API_BASE}${path.startsWith("/") ? "" : "/"}${path}`;

  const headers = opts.headers || {};
  const isFormData = typeof FormData !== "undefined" && opts.body instanceof FormData;

  const finalOpts = {
    ...opts,
    headers: isFormData ? headers : { "Content-Type": "application/json", ...headers },
  };

  const res = await fetch(url, finalOpts);

  // Try to parse JSON; fall back to text
  const text = await res.text();
  let payload;
  try {
    payload = text ? JSON.parse(text) : null;
  } catch {
    payload = text;
  }

  if (!res.ok) {
    const msg = typeof payload === "string" ? payload : (payload?.detail || payload?.message || JSON.stringify(payload));
    throw new Error(msg || `API error ${res.status}`);
  }

  return payload;
}

/** Utilities used by UI */
export function formatFileSize(bytes) {
  if (!bytes && bytes !== 0) return "";
  const units = ["B", "KB", "MB", "GB"];
  let n = bytes;
  let i = 0;
  while (n >= 1024 && i < units.length - 1) {
    n = n / 1024;
    i++;
  }
  return `${n.toFixed(i === 0 ? 0 : 1)} ${units[i]}`;
}

export function validateZipFile(file) {
  if (!file) return { valid: false, error: "No file selected" };

  const nameOk = (file.name || "").toLowerCase().endsWith(".zip");
  const typeOk =
    file.type === "application/zip" ||
    file.type === "application/x-zip-compressed" ||
    file.type === "" /* some browsers */;

  if (!nameOk && !typeOk) return { valid: false, error: "Please select a .zip file" };

  const max = 100 * 1024 * 1024; // 100MB
  if (file.size > max) return { valid: false, error: "ZIP file is too large (max 100MB)" };

  return { valid: true, error: "" };
}

/** Repo Scan API (used by RepoScanUpload page) */
export const repoScanAPI = {
  uploadAndScan: (zipFile, systemName, onProgress) =>
    new Promise((resolve, reject) => {
      try {
        const fd = new FormData();
        fd.append("zip_file", zipFile);
        fd.append("system_name", systemName);

        const xhr = new XMLHttpRequest();
        xhr.open("POST", `${API_BASE}/compliance/scan/repo`);

        xhr.upload.onprogress = (evt) => {
          if (!onProgress) return;
          if (evt.lengthComputable) {
            const pct = Math.round((evt.loaded / evt.total) * 100);
            onProgress(pct);
          }
        };

        xhr.onload = () => {
          try {
            const text = xhr.responseText || "";
            let payload = null;
            try {
              payload = text ? JSON.parse(text) : null;
            } catch {
              payload = text;
            }

            if (xhr.status >= 200 && xhr.status < 300) return resolve(payload);

            const msg =
              typeof payload === "string"
                ? payload
                : payload?.detail || payload?.message || JSON.stringify(payload);
            return reject(new Error(msg || `Upload failed (${xhr.status})`));
          } catch (e) {
            return reject(e);
          }
        };

        xhr.onerror = () => reject(new Error("Network error during upload"));
        xhr.send(fd);
      } catch (e) {
        reject(e);
      }
    }),

  getResult: (id) => request(`/compliance/scan/repo/${id}`),
};

/** Artifacts API (used by ArtifactUploader component) */
export const artifactsApi = {
  upload: (file, type, scanId) => {
    const fd = new FormData();
    fd.append("type", type);
    fd.append("file", file);
    if (scanId) fd.append("scan_id", scanId);
    return request("/artifacts/upload", { method: "POST", body: fd });
  },
};

/** Evidence API (used by EvidenceTab component). Endpoints may be WIP; keep exports stable. */
export const evidenceApi = {
  getEvidence: (scanId) => request(`/compliance/scan/repo/${scanId}`),
  runAnalyzers: (scanId, analyzers) =>
    request("/evidence/run", { method: "POST", body: JSON.stringify({ scan_id: scanId, analyzers }) }),
  getRawEvidence: (scanId, evidenceId) => request(`/evidence/${scanId}/${evidenceId}`),
};

/** System API */
export const systemAPI = {
  health: () => request("/health", { method: "GET" }),
};

/** Reports */
export async function getReports() {
  return request("/reports", { method: "GET" });
}

/**
 * Compatibility exports — different files may import different casing.
 * Keep both, to stop build-breaking import errors.
 */
export const complianceAPI = {
  getReports,
  health: () => request("/health", { method: "GET" }),
};

export const complianceApi = complianceAPI;

// Also keep older helper name if something imports it:
export async function uploadRepoScan(zipFile, systemName) {
  return repoScanAPI.uploadAndScan(zipFile, systemName);
}
