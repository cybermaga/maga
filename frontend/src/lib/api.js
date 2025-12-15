import axios from 'axios';

// Use relative API path for Preview/Production, or explicit URL for development
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';
const API_BASE = BACKEND_URL ? `${BACKEND_URL}/api` : '/api';

console.log('API Base URL:', API_BASE);

// Configure axios defaults
axios.defaults.headers.common['Content-Type'] = 'application/json';
axios.defaults.timeout = 30000; // 30 second timeout

// Add response interceptor for better error handling
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', error.response.status, error.response.data);
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error: No response from server');
    } else {
      // Something else happened
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

/**
 * API Client for Emergent AI Compliance
 */

// ============================================
// Questionnaire-based Compliance Scans
// ============================================

export const complianceAPI = {
  /**
   * Create a new questionnaire-based compliance scan
   */
  createScan: async (scanData) => {
    const response = await axios.post(`${API_BASE}/compliance/scan`, scanData);
    return response.data;
  },

  /**
   * Get all compliance scan reports
   */
  getReports: async () => {
    const response = await axios.get(`${API_BASE}/compliance/reports`);
    return response.data;
  },

  /**
   * Get a specific compliance report by ID
   */
  getReport: async (reportId) => {
    const response = await axios.get(`${API_BASE}/compliance/reports/${reportId}`);
    return response.data;
  },

  /**
   * Export a compliance report
   * @param {string} reportId 
   * @param {string} format - 'html', 'pdf', or 'json'
   */
  exportReport: async (reportId, format = 'html') => {
    const response = await axios.get(
      `${API_BASE}/compliance/reports/${reportId}/export`,
      {
        params: { format },
        responseType: format === 'pdf' ? 'blob' : 'blob'
      }
    );
    return response.data;
  },

  /**
   * Delete a compliance report
   */
  deleteReport: async (reportId) => {
    const response = await axios.delete(`${API_BASE}/compliance/reports/${reportId}`);
    return response.data;
  }
};

// ============================================
// Evidence-based Repository Scans (NEW)
// ============================================

export const repoScanAPI = {
  /**
   * Upload a repository ZIP file and trigger a scan
   * @param {File} zipFile - The repository ZIP file
   * @param {string} systemName - Name of the AI system
   * @param {Function} onUploadProgress - Optional callback for upload progress
   */
  uploadAndScan: async (zipFile, systemName, onUploadProgress) => {
    const formData = new FormData();
    formData.append('zip_file', zipFile);
    formData.append('system_name', systemName);

    const response = await axios.post(
      `${API_BASE}/compliance/scan/repo`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: onUploadProgress ? (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onUploadProgress(percentCompleted);
        } : undefined,
        timeout: 300000, // 5 minutes timeout for large files
      }
    );
    return response.data;
  },

  /**
   * Get a specific repository scan result by ID
   */
  getScanResult: async (scanId) => {
    const response = await axios.get(`${API_BASE}/compliance/scan/repo/${scanId}`);
    return response.data;
  },

  /**
   * Get all repository scan results
   */
  getAllScans: async () => {
    const response = await axios.get(`${API_BASE}/compliance/scan/repo`);
    return response.data;
  },

  /**
   * Delete a repository scan
   */
  deleteScan: async (scanId) => {
    const response = await axios.delete(`${API_BASE}/compliance/scan/repo/${scanId}`);
    return response.data;
  }
};

// ============================================
// Controls and System Info
// ============================================

export const systemAPI = {
  /**
   * Get all defined compliance controls
   */
  getControls: async () => {
    const response = await axios.get(`${API_BASE}/controls`);
    return response.data;
  },

  /**
   * Health check
   */
  healthCheck: async () => {
    const response = await axios.get(`${API_BASE}/health`);
    return response.data;
  },

  /**
   * Get API root info
   */
  getInfo: async () => {
    const response = await axios.get(`${API_BASE}/`);
    return response.data;
  }
};

// ============================================
// Helper Functions
// ============================================

/**
 * Download a blob as a file
 */
export const downloadBlob = (blob, filename) => {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};

/**
 * Format file size for display
 */
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
};

/**
 * Validate ZIP file
 */
export const validateZipFile = (file) => {
  const maxSize = 100 * 1024 * 1024; // 100MB
  const allowedTypes = ['application/zip', 'application/x-zip-compressed'];
  
  if (!file) {
    return { valid: false, error: 'No file selected' };
  }
  
  if (!allowedTypes.includes(file.type) && !file.name.endsWith('.zip')) {
    return { valid: false, error: 'File must be a ZIP archive' };
  }
  
  if (file.size > maxSize) {
    return { valid: false, error: `File size exceeds ${formatFileSize(maxSize)}` };
  }
  
  return { valid: true };
};

export default {
  complianceAPI,
  repoScanAPI,
  systemAPI,
  downloadBlob,
  formatFileSize,
  validateZipFile
};
