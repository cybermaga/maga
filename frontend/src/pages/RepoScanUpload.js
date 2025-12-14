import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Upload, Loader2, FileArchive, ArrowLeft, Shield } from 'lucide-react';
import { toast } from 'sonner';
import { complianceApi } from '@/lib/api';

const RepoScanUpload = () => {
  const navigate = useNavigate();
  const [uploading, setUploading] = useState(false);
  const [systemName, setSystemName] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!file.name.endsWith('.zip')) {
        toast.error('Please select a ZIP file');
        return;
      }
      setSelectedFile(file);
      // Auto-fill system name from filename
      if (!systemName) {
        const name = file.name.replace('.zip', '').replace(/-/g, ' ').replace(/_/g, ' ');
        setSystemName(name.charAt(0).toUpperCase() + name.slice(1));
      }
    }
  };

  const handleUpload = async () => {
    if (!selectedFile || !systemName) {
      toast.error('Please select a file and enter system name');
      return;
    }

    try {
      setUploading(true);
      
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('system_name', systemName);

      const response = await complianceApi.scanRepo(formData);
      
      toast.success('Repository scanned successfully!');
      navigate(`/repo-scan/${response.data.scan_id}`);
    } catch (error) {
      console.error('Upload error:', error);
      toast.error(error.response?.data?.detail || 'Failed to scan repository');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-5xl mx-auto px-6 py-6">
          <div className="flex items-center space-x-4">
            <Button
              variant="ghost"
              onClick={() => navigate('/')}
              className="text-slate-600 hover:text-slate-900"
              data-testid="back-button"
            >
              <ArrowLeft className="h-5 w-5 mr-2" />
              Back to Dashboard
            </Button>
          </div>
          <div className="flex items-center space-x-4 mt-4">
            <div className="bg-blue-600 p-3 rounded-lg">
              <Shield className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                Evidence-Based Scan
              </h1>
              <p className="text-sm text-slate-600 mt-1">Upload repository ZIP for automated compliance analysis</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto px-6 py-8">
        <Card className="border-slate-200" data-testid="repo-upload-card">
          <CardHeader>
            <CardTitle className="text-xl text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              Upload Repository
            </CardTitle>
            <CardDescription>
              Upload a ZIP file of your AI system repository for evidence-based compliance scanning
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* System Name */}
            <div>
              <Label htmlFor="system_name" className="text-slate-700 font-semibold">
                System Name <span className="text-red-500">*</span>
              </Label>
              <Input
                id="system_name"
                value={systemName}
                onChange={(e) => setSystemName(e.target.value)}
                placeholder="e.g., AI Recommendation System"
                className="mt-1.5 border-slate-300"
                data-testid="input-system-name"
              />
            </div>

            {/* File Upload */}
            <div>
              <Label htmlFor="repo_file" className="text-slate-700 font-semibold mb-2 block">
                Repository ZIP File <span className="text-red-500">*</span>
              </Label>
              
              <div
                className={`border-2 border-dashed rounded-lg p-8 text-center transition-all ${
                  selectedFile ? 'border-blue-500 bg-blue-50' : 'border-slate-300 hover:border-blue-400'
                }`}
              >
                {selectedFile ? (
                  <div className="space-y-4" data-testid="selected-file-info">
                    <FileArchive className="h-16 w-16 mx-auto text-blue-600" />
                    <div>
                      <p className="text-lg font-semibold text-slate-900">{selectedFile.name}</p>
                      <p className="text-sm text-slate-600">
                        {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                    <Button
                      variant="outline"
                      onClick={() => setSelectedFile(null)}
                      data-testid="remove-file-button"
                    >
                      Remove File
                    </Button>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <Upload className="h-16 w-16 mx-auto text-slate-400" />
                    <div>
                      <p className="text-lg font-semibold text-slate-700 mb-1">
                        Drop your repository ZIP here
                      </p>
                      <p className="text-sm text-slate-500">or click to browse</p>
                    </div>
                    <label>
                      <input
                        id="repo_file"
                        type="file"
                        accept=".zip"
                        onChange={handleFileSelect}
                        className="hidden"
                        data-testid="file-input"
                      />
                      <Button variant="outline" asChild>
                        <span>Browse Files</span>
                      </Button>
                    </label>
                  </div>
                )}
              </div>
              
              <p className="text-sm text-slate-500 mt-2">
                The scanner will analyze: documentation, code, configs, tests, and CI/CD setup
              </p>
            </div>

            {/* What Gets Scanned */}
            <Card className="bg-slate-50 border-slate-200">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm">What gets scanned?</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <div className="flex items-center space-x-2">
                    <span className="text-green-600">✓</span>
                    <span>README & Documentation</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-green-600">✓</span>
                    <span>Logging Configuration</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-green-600">✓</span>
                    <span>CI/CD Workflows</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-green-600">✓</span>
                    <span>Dependencies</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-green-600">✓</span>
                    <span>Test Coverage</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-green-600">✓</span>
                    <span>Audit Trail Code</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Action Buttons */}
            <div className="flex justify-end space-x-4 pt-4">
              <Button
                variant="outline"
                onClick={() => navigate('/')}
                className="px-8 py-6 text-base border-slate-300 text-slate-700"
              >
                Cancel
              </Button>
              <Button
                onClick={handleUpload}
                disabled={uploading || !selectedFile || !systemName}
                className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-6 text-base font-semibold"
                data-testid="upload-scan-button"
              >
                {uploading ? (
                  <>
                    <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                    Scanning...
                  </>
                ) : (
                  <>
                    <Shield className="mr-2 h-5 w-5" />
                    Scan Repository
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default RepoScanUpload;
