import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Progress } from "@/components/ui/progress";
import { ArrowLeft, Upload, FileArchive, Loader2, AlertCircle } from "lucide-react";
import { toast } from "sonner";
import { repoScanAPI, validateZipFile, formatFileSize } from "@/lib/api";

const RepoScanUpload = () => {
  const navigate = useNavigate();
  const [systemName, setSystemName] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [fileError, setFileError] = useState("");

  const fileInputRef = useRef(null);
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setFileError("");
    
    if (!file) {
      setSelectedFile(null);
      return;
    }

    const validation = validateZipFile(file);
    if (!validation.valid) {
      setFileError(validation.error);
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!systemName.trim()) {
      toast.error("Please enter a system name");
      return;
    }

    if (!selectedFile) {
      toast.error("Please select a ZIP file");
      return;
    }

    try {
      setUploading(true);
      setUploadProgress(0); 
    console.log("CLICK upload", { systemName, selectedFile });
      const result = await repoScanAPI.uploadAndScan(
        selectedFile,
        systemName,
        (progress) => setUploadProgress(progress)
      );

      toast.success("Repository scan completed!");
      
      // Navigate to results page
      navigate(`/scan/repo/${result.id}`);
    } catch (error) {
      console.error("Error uploading repository:", error);
      const errorMessage = error.response?.data?.detail || "Failed to scan repository";
      toast.error(errorMessage);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-5xl mx-auto px-6 py-6">
          <Button
            variant="ghost"
            onClick={() => navigate('/')}
            className="text-slate-600 hover:text-slate-900 mb-4"
            data-testid="back-button"
          >
            <ArrowLeft className="h-5 w-5 mr-2" />
            Back to Dashboard
          </Button>
          <div className="flex items-center space-x-4">
            <div className="bg-blue-600 p-3 rounded-lg">
              <Upload className="h-8 w-8 text-white" data-testid="upload-icon" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }} data-testid="page-title">
                Repository Scan
              </h1>
              <p className="text-sm text-slate-600 mt-1" data-testid="page-subtitle">
                Upload your AI project repository for evidence-based compliance analysis
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto px-6 py-8">
        <form onSubmit={handleSubmit}>
          {/* Instructions Card */}
          <Card className="mb-6 border-blue-200 bg-blue-50" data-testid="instructions-card">
            <CardHeader>
              <CardTitle className="text-lg text-blue-900">How it works</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-blue-800 space-y-2">
              <p>1. <strong>Prepare your repository:</strong> Create a ZIP archive of your AI project code</p>
              <p>2. <strong>Upload:</strong> Select the ZIP file and provide a system name</p>
              <p>3. <strong>Automated analysis:</strong> Our scanner will analyze your code for compliance evidence</p>
              <p>4. <strong>Review results:</strong> Get detailed findings mapped to EU AI Act articles</p>
            </CardContent>
          </Card>

          {/* Upload Form */}
          <Card className="mb-6 border-slate-200" data-testid="upload-form-card">
            <CardHeader>
              <CardTitle className="text-xl text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                Upload Repository
              </CardTitle>
              <CardDescription>Upload a ZIP archive of your AI project for compliance scanning</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* System Name */}
              <div>
                <Label htmlFor="system_name" className="text-slate-700 font-semibold">
                  System Name <span className="text-red-500">*</span>
                </Label>
                <Input
                  id="system_name"
                  name="system_name"
                  value={systemName}
                  onChange={(e) => setSystemName(e.target.value)}
                  placeholder="e.g., Healthcare AI Assistant"
                  className="mt-1.5 border-slate-300"
                  required
                  disabled={uploading}
                  data-testid="input-system-name"
                />
              </div>

              {/* File Upload */}
              <div>
                <Label htmlFor="zip_file" className="text-slate-700 font-semibold">
                  Repository ZIP File <span className="text-red-500">*</span>
                </Label>
                <div className="mt-1.5">
                  <div>
 		    role="button"
		    tabIndex={0}
	            onClick={() => {
                      if (!uploading) fileInputRef.current?.click();
                    }}
 		    onKeyDown={(e) => {
   		      if (!uploading && (e.key === "Enter" || e.key === " ")) {
     		        fileInputRef.current?.click();
   		       }
                     }}
                    className={`
                      flex flex-col items-center justify-center w-full h-48
                      border-2 border-dashed rounded-lg cursor-pointer
                      transition-colors
                      ${fileError ? "border-red-300 bg-red-50" : "border-slate-300 hover:border-blue-400 bg-slate-50 hover:bg-blue-50"}
                      ${uploading ? "opacity-50 cursor-not-allowed" : ""}
                     `}
 		     data-testid="file-upload-area"
	        	>
                    <div className="flex flex-col items-center justify-center pt-5 pb-6">
                      {selectedFile ? (
                        <>
                          <FileArchive className="w-12 h-12 mb-3 text-blue-600" />
                          <p className="mb-2 text-sm font-semibold text-slate-700" data-testid="selected-file-name">
                            {selectedFile.name}
                          </p>
                          <p className="text-xs text-slate-500" data-testid="selected-file-size">
                            {formatFileSize(selectedFile.size)}
                          </p>
                        </>
                      ) : (
                        <>
                          <Upload className="w-12 h-12 mb-3 text-slate-400" />
                          <p className="mb-2 text-sm text-slate-600">
                            <span className="font-semibold">Click to upload</span> or drag and drop
                          </p>
                          <p className="text-xs text-slate-500">ZIP file (max 100MB)</p>
                        </>
                      )}
                    </div>
                    <input
                     ref={fileInputRef}
                     id="zip_file"
                     name="zip_file"
                     type="file"
                     accept=".zip,application/zip,application/x-zip-compressed"
                     className="sr-only"
                     onChange={handleFileChange}
                     disabled={uploading}
                     data-testid="file-input"
                   />	                     
                  </div>
                  {fileError && (
                    <div className="flex items-center mt-2 text-sm text-red-600" data-testid="file-error">
                      <AlertCircle className="w-4 h-4 mr-2" />
                      {fileError}
                    </div>
                  )}
                </div>
              </div>

              {/* Upload Progress */}
              {uploading && (
                <div className="space-y-2" data-testid="upload-progress">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-slate-600">Uploading and analyzing...</span>
                    <span className="font-semibold text-blue-600">{uploadProgress}%</span>
                  </div>
                  <Progress value={uploadProgress} className="h-2" />
                </div>
              )}

              {/* Info Box */}
              <div className="bg-slate-50 border border-slate-200 rounded-lg p-4">
                <h4 className="text-sm font-semibold text-slate-700 mb-2">What will be analyzed?</h4>
                <ul className="text-sm text-slate-600 space-y-1 list-disc list-inside">
                  <li>Code structure and documentation quality</li>
                  <li>Testing and validation procedures</li>
                  <li>Data handling and privacy controls</li>
                  <li>Security vulnerabilities (basic scan)</li>
                  <li>Logging and monitoring capabilities</li>
                  <li>Model governance artifacts</li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Submit Button */}
          <div className="flex justify-end space-x-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate('/')}
              disabled={uploading}
              className="px-8 py-6 text-base border-slate-300 text-slate-700"
              data-testid="cancel-button"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={uploading || !selectedFile || !systemName.trim()}
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-6 text-base font-semibold"
              data-testid="submit-button"
            >
              {uploading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Scanning...
                </>
              ) : (
                <>
                  <Upload className="mr-2 h-5 w-5" />
                  Upload and Scan
                </>
              )}
            </Button>
          </div>
        </form>
      </main>
    </div>
  );
};

export default RepoScanUpload;

