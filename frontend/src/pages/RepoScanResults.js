import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  ArrowLeft, 
  Shield, 
  CheckCircle2, 
  XCircle, 
  AlertTriangle,
  FileText,
  Loader2,
  Download
} from "lucide-react";
import { toast } from "sonner";
import { repoScanAPI } from "@/lib/api";

const RepoScanResults = () => {
  const { scanId } = useParams();
  const navigate = useNavigate();
  const [scan, setScan] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchScanResults();
  }, [scanId]);

  const fetchScanResults = async () => {
    try {
      setLoading(true);
      const result = await repoScanAPI.getScanResult(scanId);
      setScan(result);
    } catch (error) {
      console.error("Error fetching scan results:", error);
      toast.error("Failed to load scan results");
      navigate('/');
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity) => {
    const colors = {
      critical: "bg-red-600 text-white",
      high: "bg-red-500 text-white",
      medium: "bg-amber-500 text-white",
      low: "bg-blue-500 text-white",
      info: "bg-slate-500 text-white"
    };
    return colors[severity] || "bg-slate-500 text-white";
  };

  const getStatusIcon = (status) => {
    if (status === 'pass') return <CheckCircle2 className="h-5 w-5 text-green-600" />;
    if (status === 'fail') return <XCircle className="h-5 w-5 text-red-600" />;
    return <AlertTriangle className="h-5 w-5 text-amber-600" />;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-50 flex items-center justify-center">
        <div className="text-center" data-testid="loading-spinner">
          <Loader2 className="h-16 w-16 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-slate-600 text-lg">Loading scan results...</p>
        </div>
      </div>
    );
  }

  if (!scan) return null;

  const coverageStats = scan.coverage_stats || {};
  const findings = scan.findings || [];
  const evidence = scan.evidence_items || [];
  
  // Group findings by article
  const findingsByArticle = findings.reduce((acc, finding) => {
    const article = finding.article_reference || 'Unknown';
    if (!acc[article]) acc[article] = [];
    acc[article].push(finding);
    return acc;
  }, {});

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <Button
            variant="ghost"
            onClick={() => navigate('/')}
            className="text-slate-600 hover:text-slate-900 mb-4"
            data-testid="back-button"
          >
            <ArrowLeft className="h-5 w-5 mr-2" />
            Back to Dashboard
          </Button>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="bg-blue-600 p-3 rounded-lg">
                <Shield className="h-8 w-8 text-white" data-testid="scan-icon" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }} data-testid="scan-name">
                  {scan.system_name}
                </h1>
                <p className="text-sm text-slate-600 mt-1" data-testid="scan-date">
                  Scanned on {formatDate(scan.timestamp)}
                </p>
              </div>
            </div>
            <Button
              variant="outline"
              className="border-blue-600 text-blue-600 hover:bg-blue-50"
              data-testid="download-report-button"
            >
              <Download className="mr-2 h-4 w-4" />
              Download Report
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Coverage Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="border-slate-200" data-testid="total-controls-card">
            <CardHeader className="pb-3">
              <CardDescription className="text-slate-600">Total Controls</CardDescription>
              <CardTitle className="text-4xl font-bold text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                {coverageStats.total_controls || 0}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-sm text-slate-600">Compliance checks</div>
            </CardContent>
          </Card>

          <Card className="border-green-200 bg-green-50" data-testid="passed-card">
            <CardHeader className="pb-3">
              <CardDescription className="text-green-700">Passed</CardDescription>
              <CardTitle className="text-4xl font-bold text-green-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                {coverageStats.controls_passed || 0}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-sm text-green-700">
                {coverageStats.coverage_percentage || 0}% coverage
              </div>
            </CardContent>
          </Card>

          <Card className="border-red-200 bg-red-50" data-testid="failed-card">
            <CardHeader className="pb-3">
              <CardDescription className="text-red-700">Failed</CardDescription>
              <CardTitle className="text-4xl font-bold text-red-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                {coverageStats.controls_failed || 0}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-sm text-red-700">Require attention</div>
            </CardContent>
          </Card>

          <Card className="border-amber-200 bg-amber-50" data-testid="evidence-card">
            <CardHeader className="pb-3">
              <CardDescription className="text-amber-700">Evidence Found</CardDescription>
              <CardTitle className="text-4xl font-bold text-amber-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                {evidence.length}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-sm text-amber-700">Compliance artifacts</div>
            </CardContent>
          </Card>
        </div>

        {/* Overall Progress */}
        <Card className="mb-8 border-slate-200" data-testid="progress-card">
          <CardHeader>
            <CardTitle className="text-xl text-slate-900">Overall Compliance Coverage</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-slate-600">Coverage</span>
                <span className="font-semibold text-blue-600">{coverageStats.coverage_percentage || 0}%</span>
              </div>
              <Progress value={coverageStats.coverage_percentage || 0} className="h-3" />
            </div>
          </CardContent>
        </Card>

        {/* Tabs for Findings and Evidence */}
        <Tabs defaultValue="findings" className="space-y-6">
          <TabsList className="grid w-full max-w-md grid-cols-2">
            <TabsTrigger value="findings" data-testid="findings-tab">
              Findings ({findings.length})
            </TabsTrigger>
            <TabsTrigger value="evidence" data-testid="evidence-tab">
              Evidence ({evidence.length})
            </TabsTrigger>
          </TabsList>

          {/* Findings Tab */}
          <TabsContent value="findings" className="space-y-4">
            {findings.length === 0 ? (
              <Card className="border-slate-200">
                <CardContent className="py-12 text-center">
                  <CheckCircle2 className="h-16 w-16 mx-auto text-green-500 mb-4" />
                  <h3 className="text-xl font-semibold text-slate-700 mb-2">No Issues Found</h3>
                  <p className="text-slate-500">All checks passed successfully</p>
                </CardContent>
              </Card>
            ) : (
              Object.entries(findingsByArticle).map(([article, articleFindings]) => (
                <Card key={article} className="border-slate-200" data-testid={`article-${article}-findings`}>
                  <CardHeader>
                    <CardTitle className="text-lg text-slate-900">{article}</CardTitle>
                    <CardDescription>{articleFindings.length} finding(s)</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {articleFindings.map((finding, idx) => (
                      <div
                        key={idx}
                        className="border border-slate-200 rounded-lg p-4 bg-white"
                        data-testid={`finding-${idx}`}
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex items-center space-x-2">
                            {getStatusIcon(finding.status)}
                            <h4 className="font-semibold text-slate-900">{finding.control_id}</h4>
                          </div>
                          <Badge className={getSeverityColor(finding.severity)}>
                            {finding.severity}
                          </Badge>
                        </div>
                        <p className="text-sm text-slate-700 mb-2">{finding.description}</p>
                        {finding.recommendation && (
                          <div className="bg-blue-50 border border-blue-200 rounded p-3 mt-2">
                            <p className="text-sm text-blue-800">
                              <strong>Recommendation:</strong> {finding.recommendation}
                            </p>
                          </div>
                        )}
                      </div>
                    ))}
                  </CardContent>
                </Card>
              ))
            )}
          </TabsContent>

          {/* Evidence Tab */}
          <TabsContent value="evidence" className="space-y-4">
            {evidence.length === 0 ? (
              <Card className="border-slate-200">
                <CardContent className="py-12 text-center">
                  <FileText className="h-16 w-16 mx-auto text-slate-300 mb-4" />
                  <h3 className="text-xl font-semibold text-slate-700 mb-2">No Evidence Found</h3>
                  <p className="text-slate-500">No compliance artifacts detected</p>
                </CardContent>
              </Card>
            ) : (
              <Card className="border-slate-200" data-testid="evidence-list-card">
                <CardHeader>
                  <CardTitle className="text-xl text-slate-900">Compliance Evidence</CardTitle>
                  <CardDescription>Artifacts found that support compliance claims</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {evidence.map((item, idx) => (
                      <div
                        key={idx}
                        className="flex items-start justify-between p-3 border border-slate-200 rounded-lg hover:bg-slate-50"
                        data-testid={`evidence-${idx}`}
                      >
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-1">
                            <FileText className="h-4 w-4 text-blue-600" />
                            <span className="font-mono text-sm text-slate-700">{item.file_path}</span>
                          </div>
                          <p className="text-sm text-slate-600">{item.control_id}: {item.description}</p>
                        </div>
                        <Badge variant="outline" className="border-green-300 text-green-700">
                          {item.status}
                        </Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
};

export default RepoScanResults;
