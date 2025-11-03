import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { ArrowLeft, Loader2, Shield } from "lucide-react";
import { toast } from "sonner";
import ArtifactUploader from "@/components/ArtifactUploader";
import { complianceApi } from "@/lib/api";

const NewScan = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [artifactIds, setArtifactIds] = useState([]);
  const [formData, setFormData] = useState({
    system_name: "",
    description: "",
    use_case: "",
    application_domain: "",
    model_type: "",
    provider: "",
    version: "1.0",
    risk_management: "",
    data_governance: "",
    technical_docs: "",
    testing_procedures: "",
    human_oversight: "",
    accuracy_metrics: "",
    artifact_ids: []
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.system_name || !formData.description || !formData.use_case) {
      toast.error("Please fill in all required fields");
      return;
    }

    try {
      setLoading(true);
      const response = await axios.post(`${API}/compliance/scan`, formData);
      toast.success("Compliance scan completed successfully!");
      navigate(`/report/${response.data.id}`);
    } catch (error) {
      console.error("Error creating scan:", error);
      toast.error(error.response?.data?.detail || "Failed to create compliance scan");
    } finally {
      setLoading(false);
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
              <Shield className="h-8 w-8 text-white" data-testid="scan-icon" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }} data-testid="page-title">
                New Compliance Scan
              </h1>
              <p className="text-sm text-slate-600 mt-1" data-testid="page-subtitle">Analyze your AI system for EU AI Act compliance</p>
            </div>
          </div>
        </div>
      </header>

      {/* Form */}
      <main className="max-w-5xl mx-auto px-6 py-8">
        <form onSubmit={handleSubmit}>
          {/* Basic Information */}
          <Card className="mb-6 border-slate-200" data-testid="basic-info-card">
            <CardHeader>
              <CardTitle className="text-xl text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                Basic Information
              </CardTitle>
              <CardDescription>Required information about your AI system</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="system_name" className="text-slate-700 font-semibold">
                  System Name <span className="text-red-500">*</span>
                </Label>
                <Input
                  id="system_name"
                  name="system_name"
                  value={formData.system_name}
                  onChange={handleChange}
                  placeholder="e.g., Healthcare Diagnosis Assistant"
                  className="mt-1.5 border-slate-300"
                  required
                  data-testid="input-system-name"
                />
              </div>

              <div>
                <Label htmlFor="description" className="text-slate-700 font-semibold">
                  Description <span className="text-red-500">*</span>
                </Label>
                <Textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  placeholder="Describe what your AI system does, its capabilities, and key features"
                  className="mt-1.5 border-slate-300 min-h-24"
                  required
                  data-testid="input-description"
                />
              </div>

              <div>
                <Label htmlFor="use_case" className="text-slate-700 font-semibold">
                  Use Case <span className="text-red-500">*</span>
                </Label>
                <Textarea
                  id="use_case"
                  name="use_case"
                  value={formData.use_case}
                  onChange={handleChange}
                  placeholder="Explain the primary use case and context where this AI system will be deployed"
                  className="mt-1.5 border-slate-300 min-h-20"
                  required
                  data-testid="input-use-case"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="application_domain" className="text-slate-700 font-semibold">
                    Application Domain
                  </Label>
                  <Input
                    id="application_domain"
                    name="application_domain"
                    value={formData.application_domain}
                    onChange={handleChange}
                    placeholder="e.g., Healthcare, Finance, Education"
                    className="mt-1.5 border-slate-300"
                    data-testid="input-application-domain"
                  />
                </div>

                <div>
                  <Label htmlFor="model_type" className="text-slate-700 font-semibold">
                    Model Type
                  </Label>
                  <Input
                    id="model_type"
                    name="model_type"
                    value={formData.model_type}
                    onChange={handleChange}
                    placeholder="e.g., Neural Network, Random Forest"
                    className="mt-1.5 border-slate-300"
                    data-testid="input-model-type"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="provider" className="text-slate-700 font-semibold">
                    Provider/Vendor
                  </Label>
                  <Input
                    id="provider"
                    name="provider"
                    value={formData.provider}
                    onChange={handleChange}
                    placeholder="e.g., OpenAI, Custom"
                    className="mt-1.5 border-slate-300"
                    data-testid="input-provider"
                  />
                </div>

                <div>
                  <Label htmlFor="version" className="text-slate-700 font-semibold">
                    Version
                  </Label>
                  <Input
                    id="version"
                    name="version"
                    value={formData.version}
                    onChange={handleChange}
                    placeholder="1.0"
                    className="mt-1.5 border-slate-300"
                    data-testid="input-version"
                  />
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Compliance Documentation */}
          <Card className="mb-6 border-slate-200" data-testid="compliance-docs-card">
            <CardHeader>
              <CardTitle className="text-xl text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                Compliance Documentation
              </CardTitle>
              <CardDescription>
                Optional: Provide documentation to improve compliance analysis accuracy
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="risk_management" className="text-slate-700 font-semibold">
                  Risk Management (Article 9)
                </Label>
                <Textarea
                  id="risk_management"
                  name="risk_management"
                  value={formData.risk_management}
                  onChange={handleChange}
                  placeholder="Describe your risk identification, assessment, and mitigation procedures"
                  className="mt-1.5 border-slate-300 min-h-20"
                  data-testid="input-risk-management"
                />
              </div>

              <div>
                <Label htmlFor="data_governance" className="text-slate-700 font-semibold">
                  Data Governance (Article 10)
                </Label>
                <Textarea
                  id="data_governance"
                  name="data_governance"
                  value={formData.data_governance}
                  onChange={handleChange}
                  placeholder="Describe training data quality, bias detection, and data management practices"
                  className="mt-1.5 border-slate-300 min-h-20"
                  data-testid="input-data-governance"
                />
              </div>

              <div>
                <Label htmlFor="technical_docs" className="text-slate-700 font-semibold">
                  Technical Documentation (Article 11)
                </Label>
                <Textarea
                  id="technical_docs"
                  name="technical_docs"
                  value={formData.technical_docs}
                  onChange={handleChange}
                  placeholder="Provide technical specifications, development process, and design documentation"
                  className="mt-1.5 border-slate-300 min-h-20"
                  data-testid="input-technical-docs"
                />
              </div>

              <div>
                <Label htmlFor="testing_procedures" className="text-slate-700 font-semibold">
                  Testing & Record-keeping (Articles 12)
                </Label>
                <Textarea
                  id="testing_procedures"
                  name="testing_procedures"
                  value={formData.testing_procedures}
                  onChange={handleChange}
                  placeholder="Describe testing procedures, logging, and audit trail mechanisms"
                  className="mt-1.5 border-slate-300 min-h-20"
                  data-testid="input-testing-procedures"
                />
              </div>

              <div>
                <Label htmlFor="human_oversight" className="text-slate-700 font-semibold">
                  Human Oversight (Article 14)
                </Label>
                <Textarea
                  id="human_oversight"
                  name="human_oversight"
                  value={formData.human_oversight}
                  onChange={handleChange}
                  placeholder="Describe human oversight measures, intervention capabilities, and monitoring"
                  className="mt-1.5 border-slate-300 min-h-20"
                  data-testid="input-human-oversight"
                />
              </div>

              <div>
                <Label htmlFor="accuracy_metrics" className="text-slate-700 font-semibold">
                  Accuracy, Robustness & Security (Article 15)
                </Label>
                <Textarea
                  id="accuracy_metrics"
                  name="accuracy_metrics"
                  value={formData.accuracy_metrics}
                  onChange={handleChange}
                  placeholder="Describe accuracy metrics, robustness testing, and cybersecurity measures"
                  className="mt-1.5 border-slate-300 min-h-20"
                  data-testid="input-accuracy-metrics"
                />
              </div>
            </CardContent>
          </Card>

          {/* Submit Button */}
          <div className="flex justify-end space-x-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate('/')}
              className="px-8 py-6 text-base border-slate-300 text-slate-700"
              data-testid="cancel-button"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-6 text-base font-semibold"
              data-testid="submit-scan-button"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Shield className="mr-2 h-5 w-5" />
                  Run Compliance Scan
                </>
              )}
            </Button>
          </div>
        </form>
      </main>
    </div>
  );
};

export default NewScan;
