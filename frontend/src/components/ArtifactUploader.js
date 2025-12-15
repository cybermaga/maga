import { useState, useCallback } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Upload, X, FileText, Database, Code, FileCode, FileWarning } from 'lucide-react';
import { toast } from 'sonner';
import { artifactsApi } from '@/lib/api';

const ARTIFACT_TYPES = {
  code: { label: 'Code', icon: Code, accept: '.py,.js,.ts,.zip,.tar.gz' },
  model: { label: 'Model', icon: FileCode, accept: '.onnx,.pt,.pth,.h5' },
  dataset: { label: 'Dataset', icon: Database, accept: '.csv,.json,.jsonl' },
  doc: { label: 'Documentation', icon: FileText, accept: '.pdf,.docx,.txt,.md' },
  logs: { label: 'Logs', icon: FileWarning, accept: '.log,.txt' },
};

const ArtifactUploader = ({ scanId, onArtifactsChange }) => {
  const [artifacts, setArtifacts] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  const handleFileUpload = async (files, type) => {
    if (files.length === 0) return;

    setUploading(true);
    const uploadedArtifacts = [];

    try {
      for (const file of files) {
        const response = await artifactsApi.upload(file, type, scanId);
        uploadedArtifacts.push({
          ...response.data,
          type,
        });
        toast.success(`Uploaded: ${file.name}`);
      }

      const newArtifacts = [...artifacts, ...uploadedArtifacts];
      setArtifacts(newArtifacts);
      onArtifactsChange?.(newArtifacts.map(a => a.artifact_id));
    } catch (error) {
      console.error('Upload error:', error);
      toast.error(error.response?.data?.detail || 'Failed to upload file');
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = useCallback((e, type) => {
    e.preventDefault();
    setDragOver(false);
    const files = Array.from(e.dataTransfer.files);
    handleFileUpload(files, type);
  }, [artifacts]);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setDragOver(false);
  }, []);

  const removeArtifact = (artifactId) => {
    const newArtifacts = artifacts.filter(a => a.artifact_id !== artifactId);
    setArtifacts(newArtifacts);
    onArtifactsChange?.(newArtifacts.map(a => a.artifact_id));
    toast.info('Artifact removed');
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <Card className="border-slate-200" data-testid="artifact-uploader">
      <CardHeader>
        <CardTitle className="text-xl text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
          Attach Artifacts
        </CardTitle>
        <CardDescription>
          Upload code, models, datasets, documentation, or logs for analysis
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Upload Areas */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.entries(ARTIFACT_TYPES).map(([type, config]) => {
            const Icon = config.icon;
            return (
              <div
                key={type}
                className={`border-2 border-dashed rounded-lg p-4 text-center transition-all cursor-pointer ${
                  dragOver ? 'border-blue-500 bg-blue-50' : 'border-slate-300 hover:border-blue-400'
                }`}
                onDrop={(e) => handleDrop(e, type)}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                data-testid={`upload-zone-${type}`}
              >
                <Icon className="h-10 w-10 mx-auto mb-2 text-slate-400" />
                <p className="text-sm font-semibold text-slate-700 mb-1">{config.label}</p>
                <p className="text-xs text-slate-500 mb-3">{config.accept}</p>
                <label>
                  <input
                    type="file"
                    className="hidden"
                    accept={config.accept}
                    multiple
                    onChange={(e) => handleFileUpload(Array.from(e.target.files), type)}
                    disabled={uploading}
                  />
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    className="w-full"
                    disabled={uploading}
                    asChild
                  >
                    <span>
                      <Upload className="h-4 w-4 mr-2" />
                      Browse
                    </span>
                  </Button>
                </label>
              </div>
            );
          })}
        </div>

        {/* Uploaded Artifacts List */}
        {artifacts.length > 0 && (
          <div className="mt-6" data-testid="uploaded-artifacts-list">
            <p className="text-sm font-semibold text-slate-700 mb-3">
              Uploaded Artifacts ({artifacts.length})
            </p>
            <div className="space-y-2">
              {artifacts.map((artifact) => (
                <div
                  key={artifact.artifact_id}
                  className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-200"
                  data-testid={`artifact-${artifact.artifact_id}`}
                >
                  <div className="flex items-center space-x-3 flex-1">
                    {ARTIFACT_TYPES[artifact.type] && 
                      (() => {
                        const Icon = ARTIFACT_TYPES[artifact.type].icon;
                        return <Icon className="h-5 w-5 text-slate-500" />;
                      })()
                    }
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-slate-900 truncate">
                        {artifact.filename}
                      </p>
                      <p className="text-xs text-slate-500">
                        {formatFileSize(artifact.size)}
                      </p>
                    </div>
                    <Badge variant="outline" className="capitalize">
                      {artifact.type}
                    </Badge>
                  </div>
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={() => removeArtifact(artifact.artifact_id)}
                    className="ml-2 text-red-600 hover:text-red-700 hover:bg-red-50"
                    data-testid={`remove-artifact-${artifact.artifact_id}`}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          </div>
        )}

        {uploading && (
          <div className="text-center py-4" data-testid="upload-progress">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent mb-2"></div>
            <p className="text-sm text-slate-600">Uploading...</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default ArtifactUploader;
