import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { ArrowLeft, Download, Loader2, Shield, CheckCircle2, XCircle, AlertCircle, Trash2 } from "lucide-react";
import { toast } from "sonner";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { complianceAPI, downloadBlob } from "@/lib/api";

const ReportView = () => {
  const { reportId } = useParams();
  const navigate = useNavigate();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(null);

  useEffect(() => {
    fetchReport();
  }, [reportId]);

  const fetchReport = async () => {
    try {
      setLoading(true);
      const reportData = await complianceAPI.getReport(reportId);
      setReport(reportData);
    } catch (error) {
      console.error("Error fetching report:", error);
      toast.error("Failed to load report");
      navigate('/');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async (format) => {
    try {
      setExporting(format);
      const blob = await complianceAPI.exportReport(reportId, format);
      downloadBlob(blob, `compliance_report_${reportId}.${format}`);
      toast.success(`Report exported as ${format.toUpperCase()}`);
    } catch (error) {
      console.error("Error exporting report:", error);
      toast.error(`Failed to export report as ${format.toUpperCase()}`);
    } finally {
      setExporting(null);
    }
  };

  const handleDelete = async () => {
    try {
      await complianceAPI.deleteReport(reportId);
      toast.success("Report deleted successfully");
      navigate('/');
    } catch (error) {
      console.error("Error deleting report:", error);
      toast.error("Failed to delete report");
    }
  };

  const getRiskBadgeColor = (risk) => {
    const colors = {
      prohibited: "bg-red-600 text-white hover:bg-red-700",
      high: "bg-red-500 text-white hover:bg-red-600",
      limited: "bg-amber-500 text-white hover:bg-amber-600",
      minimal: "bg-green-500 text-white hover:bg-green-600"
    };
    return colors[risk] || "bg-gray-500 text-white";
  };

  const getGradeBadgeColor = (grade) => {
    const colors = {
      A: "bg-green-500 text-white",
      B: "bg-blue-500 text-white",
      C: "bg-amber-500 text-white",
      D: "bg-red-500 text-white",
      F: "bg-red-700 text-white"
    };
    return colors[grade] || "bg-gray-500 text-white";
  };

  const getStatusIcon = (status) => {
    if (status === 'compliant') return <CheckCircle2 className="h-5 w-5 text-green-600" />;
    if (status === 'partially_compliant') return <AlertCircle className="h-5 w-5 text-amber-600" />;
    return <XCircle className="h-5 w-5 text-red-600" />;
  };

  const getStatusColor = (status) => {
    if (status === 'compliant') return "text-green-700 font-semibold";
    if (status === 'partially_compliant') return "text-amber-700 font-semibold";
    return "text-red-700 font-semibold";
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
          <p className="text-slate-600 text-lg">Loading compliance report...</p>
        </div>
      </div>
    );
  }

  if (!report) return null;

  const overallScore = report.compliance_results?.overall_score || {};
  const articles = Object.entries(report.compliance_results || {}).filter(([key]) => key !== 'overall_score');

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-6xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between mb-4">
            <Button
              variant="ghost"
              onClick={() => navigate('/')}
              className="text-slate-600 hover:text-slate-900"
              data-testid="back-to-dashboard-button"
            >
              <ArrowLeft className="h-5 w-5 mr-2" />
              Back to Dashboard
            </Button>
            <div className="flex space-x-2">
              <Button
                variant="outline"
                onClick={() => handleExport('html')}
                disabled={exporting !== null}
                className="border-slate-300"
                data-testid="export-html-button"
              >
                {exporting === 'html' ? (
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                ) : (
                  <Download className="h-4 w-4 mr-2" />
                )}
                Export HTML
              </Button>
              <Button
                variant="outline"
                onClick={() => handleExport('pdf')}
                disabled={exporting !== null}
                className="border-slate-300"
                data-testid="export-pdf-button"
              >
                {exporting === 'pdf' ? (
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                ) : (
                  <Download className="h-4 w-4 mr-2" />
                )}
                Export PDF
              </Button>
              <AlertDialog>
                <AlertDialogTrigger asChild>
                  <Button
                    variant="outline"
                    className="border-red-300 text-red-600 hover:bg-red-50"
                    data-testid="delete-report-button"
                  >
                    <Trash2 className="h-4 w-4 mr-2" />
                    Delete
                  </Button>
                </AlertDialogTrigger>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle>Delete Report?</AlertDialogTitle>
                    <AlertDialogDescription>
                      This action cannot be undone. This will permanently delete the compliance report.
                    </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel data-testid="cancel-delete-button">Cancel</AlertDialogCancel>
                    <AlertDialogAction
                      onClick={handleDelete}
                      className="bg-red-600 hover:bg-red-700"
                      data-testid="confirm-delete-button"
                    >
                      Delete Report
                    </AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="bg-blue-600 p-3 rounded-lg">
              <Shield className="h-8 w-8 text-white" data-testid="report-icon" />
            </div>
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }} data-testid="report-system-name">
                {report.system_name}
              </h1>
              <p className="text-sm text-slate-600 mt-1" data-testid="report-timestamp">Scanned on {formatDate(report.timestamp)}</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-6 py-8">
        {/* Overall Score Card */}
        <Card className="mb-8 border-slate-200" data-testid="overall-score-card">
          <CardHeader>
            <CardTitle className="text-2xl text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              Overall Compliance Score
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between mb-6">
              <div>
                <div className="flex items-center space-x-4 mb-4">
                  <Badge className={`${getGradeBadgeColor(overallScore.grade)} text-4xl px-6 py-3 font-bold`} data-testid="overall-grade-badge">
                    Grade {overallScore.grade}
                  </Badge>
                  <div>
                    <p className="text-4xl font-bold text-slate-900" data-testid="overall-percentage">{overallScore.percentage}%</p>
                    <p className="text-sm text-slate-600">Compliance Rate</p>
                  </div>
                </div>
                <div className="flex space-x-6 text-sm">
                  <div data-testid="compliant-count">
                    <span className="font-semibold text-green-700">{overallScore.compliant_articles}</span>
                    <span className="text-slate-600"> Compliant</span>
                  </div>
                  <div data-testid="partial-count">
                    <span className="font-semibold text-amber-700">{overallScore.partially_compliant_articles}</span>
                    <span className="text-slate-600"> Partial</span>
                  </div>
                  <div data-testid="non-compliant-count">
                    <span className="font-semibold text-red-700">{overallScore.non_compliant_articles}</span>
                    <span className="text-slate-600"> Non-Compliant</span>
                  </div>
                </div>
              </div>
            </div>
            <Progress value={overallScore.percentage} className="h-3" data-testid="overall-progress-bar" />
          </CardContent>
        </Card>

        {/* Risk Classification Card */}
        <Card className="mb-8 border-slate-200" data-testid="risk-classification-card">
          <CardHeader>
            <CardTitle className="text-2xl text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              Risk Classification
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <p className="text-sm text-slate-600 mb-2">Risk Level</p>
                <Badge className={`${getRiskBadgeColor(report.risk_classification?.risk_level)} text-lg px-4 py-2`} data-testid="risk-level-badge">
                  {report.risk_classification?.risk_level?.toUpperCase()}
                </Badge>
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-700">Article Reference</p>
                <p className="text-slate-900" data-testid="risk-article-reference">{report.risk_classification?.article_reference}</p>
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-700">Reasoning</p>
                <p className="text-slate-900" data-testid="risk-reasoning">{report.risk_classification?.reasoning}</p>
              </div>
              {report.risk_classification?.matched_terms && report.risk_classification.matched_terms.length > 0 && (
                <div>
                  <p className="text-sm font-semibold text-slate-700 mb-2">Matched Terms</p>
                  <div className="flex flex-wrap gap-2">
                    {report.risk_classification.matched_terms.map((term, idx) => (
                      <Badge key={idx} variant="outline" className="border-slate-300" data-testid={`matched-term-${idx}`}>
                        {term}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Detailed Compliance Results */}
        <Card className="border-slate-200" data-testid="detailed-results-card">
          <CardHeader>
            <CardTitle className="text-2xl text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              Detailed Compliance Results
            </CardTitle>
            <CardDescription>Analysis per EU AI Act article</CardDescription>
          </CardHeader>
          <CardContent>
            <Accordion type="single" collapsible className="w-full">
              {articles.map(([articleId, articleData], index) => (
                <AccordionItem key={articleId} value={articleId} data-testid={`article-accordion-${index}`}>
                  <AccordionTrigger className="hover:no-underline">
                    <div className="flex items-center justify-between w-full pr-4">
                      <div className="flex items-center space-x-3">
                        {getStatusIcon(articleData.status)}
                        <div className="text-left">
                          <p className="font-semibold text-slate-900" data-testid={`article-title-${index}`}>
                            {articleData.article_id.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}: {articleData.title}
                          </p>
                          <p className={`text-sm ${getStatusColor(articleData.status)}`} data-testid={`article-status-${index}`}>
                            {articleData.status.replace('_', ' ').toUpperCase()}
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-2xl font-bold text-slate-900" data-testid={`article-ratio-${index}`}>
                          {Math.round(articleData.compliance_ratio * 100)}%
                        </p>
                      </div>
                    </div>
                  </AccordionTrigger>
                  <AccordionContent>
                    <div className="pt-4 space-y-4">
                      <Progress value={articleData.compliance_ratio * 100} className="h-2" data-testid={`article-progress-${index}`} />
                      
                      {articleData.found_elements && articleData.found_elements.length > 0 && (
                        <div>
                          <p className="font-semibold text-green-700 mb-2">Found Elements</p>
                          <ul className="space-y-1">
                            {articleData.found_elements.map((element, idx) => (
                              <li key={idx} className="flex items-start text-sm" data-testid={`found-element-${index}-${idx}`}>
                                <CheckCircle2 className="h-4 w-4 text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                                <span className="text-slate-700">{element}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      {articleData.missing_elements && articleData.missing_elements.length > 0 && (
                        <div>
                          <p className="font-semibold text-red-700 mb-2">Missing Elements</p>
                          <ul className="space-y-1">
                            {articleData.missing_elements.map((element, idx) => (
                              <li key={idx} className="flex items-start text-sm" data-testid={`missing-element-${index}-${idx}`}>
                                <XCircle className="h-4 w-4 text-red-600 mr-2 mt-0.5 flex-shrink-0" />
                                <span className="text-slate-700">{element}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-4">
                        <p className="font-semibold text-blue-900 mb-1">Recommendation</p>
                        <p className="text-sm text-blue-800" data-testid={`article-recommendation-${index}`}>{articleData.recommendation}</p>
                      </div>
                    </div>
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default ReportView;
