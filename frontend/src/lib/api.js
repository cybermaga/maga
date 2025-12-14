import axios from 'axios';

const API_BASE = (process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001').replace(/\/$/, '');

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Compliance Scans
export const complianceApi = {
  createScan: (data) => api.post('/api/compliance/scan', data),
  getReports: () => api.get('/api/compliance/reports'),
  getReport: (id) => api.get(`/api/compliance/reports/${id}`),
  exportReport: (id, format) => api.get(`/api/compliance/reports/${id}/export?format=${format}`, {
    responseType: 'blob'
  }),
  deleteReport: (id) => api.delete(`/api/compliance/reports/${id}`),
  
  // Repo Scan (NEW)
  scanRepo: (formData) => api.post('/api/compliance/scan/repo', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  getRepoScan: (id) => api.get(`/api/compliance/scan/repo/${id}`),
  getControls: () => api.get('/api/controls'),
};

// Artifacts
export const artifactsApi = {
  upload: (file, type, scanId = null) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', type);
    if (scanId) {
      formData.append('scan_id', scanId);
    }
    return api.post('/api/artifacts/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  getArtifact: (id) => api.get(`/api/artifacts/${id}`),
};

// Evidence
export const evidenceApi = {
  runAnalyzers: (scanId, rules) => api.post('/api/evidence/run', {
    scan_id: scanId,
    rules: rules,
  }),
  getEvidence: (scanId) => api.get(`/api/evidence/${scanId}`),
  getRawEvidence: (scanId, evidenceId) => api.get(`/api/evidence/${scanId}/${evidenceId}/raw`),
};

// Health
export const healthApi = {
  check: () => api.get('/api/health'),
};

export default api;
