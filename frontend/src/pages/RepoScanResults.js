import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { ArrowLeft, Loader2, Shield, CheckCircle2, XCircle, AlertCircle, FileText } from 'lucide-react';
import { toast } from 'sonner';
import { complianceApi } from '@/lib/api';

const RepoScanResults = () => {
  const { scanId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [results, setResults] = useState(null);

  useEffect(() => {
    fetchResults();
  }, [scanId]);

  const fetchResults = async () => {
    try {
      setLoading(true);
      const response = await complianceApi.getRepoScan(scanId);
      setResults(response.data);
    } catch (error) {
      console.error('Error fetching results:', error);
      toast.error('Failed to load scan results');
      navigate('/');
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'compliant':
        return <CheckCircle2 className="h-5 w-5 text-green-600" />;
      case 'partial':
        return <AlertCircle className="h-5 w-5 text-amber-600" />;
      case 'non_compliant':
        return <XCircle className="h-5 w-5 text-red-600" />;
      default:
        return null;
    }
  };

  const getStatusBadge = (status) => {
    const colors = {
      compliant: 'bg-green-100 text-green-800',
      partial: 'bg-amber-100 text-amber-800',
      non_compliant: 'bg-red-100 text-red-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-16 w-16 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-slate-600 text-lg">Loading scan results...</p>
        </div>
      </div>
    );
  }

  if (!results) return null;

  const { scan, findings_by_article, critical_findings, recommendations, summary } = results;
  const { coverage } = scan;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <Button
            variant="ghost"
            onClick={() => navigate('/')}
            className="text-slate-600 hover:text-slate-900 mb-4"
          >
            <ArrowLeft className="h-5 w-5 mr-2" />
            Back to Dashboard
          </Button>
          <div className="flex items-center space-x-4">
            <div className="bg-blue-600 p-3 rounded-lg">
              <Shield className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                {scan.name}
              </h1>
              <p className="text-sm text-slate-600 mt-1">Evidence-Based Compliance Scan Results</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        {/* Summary */}
        <Card className="border-slate-200">
          <CardHeader>
            <CardTitle className="text-xl">Scan Summary</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-slate-700">{summary}</p>
          </CardContent>
        </Card>

        {/* Overall Coverage */}
        <Card className="border-slate-200">
          <CardHeader>
            <CardTitle className="text-2xl" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              Overall Compliance Coverage
            </CardTitle>
            <CardDescription>{coverage.coverage_percentage}% of controls checked</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <Progress value={coverage.coverage_percentage} className="h-4" />
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-slate-50 rounded-lg">
                <p className="text-3xl font-bold text-slate-900">{coverage.total_controls}</p>
                <p className="text-sm text-slate-600">Total Controls</p>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <p className="text-3xl font-bold text-green-700">{coverage.compliant}</p>
                <p className="text-sm text-green-600">Compliant</p>
              </div>
              <div className="text-center p-4 bg-amber-50 rounded-lg">
                <p className="text-3xl font-bold text-amber-700">{coverage.partial}</p>
                <p className="text-sm text-amber-600">Partial</p>
              </div>
              <div className="text-center p-4 bg-red-50 rounded-lg">
                <p className="text-3xl font-bold text-red-700">{coverage.non_compliant}</p>
                <p className="text-sm text-red-600">Non-Compliant</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Coverage by Article */}
        <Card className="border-slate-200">
          <CardHeader>
            <CardTitle className="text-xl">Coverage by EU AI Act Article</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {Object.entries(coverage.article_coverage || {}).map(([article, percentage]) => (
                <div key={article} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-slate-900">{article}</span>
                    <span className="text-slate-600">{percentage}%</span>
                  </div>
                  <Progress value={percentage} className="h-2" />
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Critical Findings */}
        {critical_findings && critical_findings.length > 0 && (
          <Card className="border-red-200 bg-red-50">
            <CardHeader>
              <CardTitle className="text-xl text-red-900">Critical Findings</CardTitle>
              <CardDescription className="text-red-700">
                {critical_findings.length} critical or high priority issues require attention
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {critical_findings.map((finding, idx) => (
                  <div key={idx} className="bg-white p-4 rounded-lg border border-red-200">
                    <div className="flex items-start space-x-3">
                      {getStatusIcon(finding.status)}
                      <div className="flex-1">
                        <p className="font-semibold text-slate-900">{finding.control_title}</p>
                        <p className="text-sm text-slate-600 mt-1">{finding.recommendation}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Detailed Findings */}
        <Card className="border-slate-200">
          <CardHeader>
            <CardTitle className="text-xl">Detailed Findings</CardTitle>
            <CardDescription>Evidence-based verification results for each control</CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Control</TableHead>
                  <TableHead>Article</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Evidence</TableHead>
                  <TableHead>Confidence</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {scan.findings.map((finding, idx) => (
                  <TableRow key={idx}>
                    <TableCell>
                      <div>
                        <p className="font-medium text-slate-900">{finding.control_title}</p>
                        <code className="text-xs text-slate-500">{finding.control_id}</code>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">{finding.article}</Badge>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        {getStatusIcon(finding.status)}
                        <Badge className={getStatusBadge(finding.status)}>
                          {finding.status.replace('_', ' ').toUpperCase()}
                        </Badge>
                      </div>
                    </TableCell>
                    <TableCell>
                      <span className="text-sm text-slate-600">
                        {finding.evidence_count} {finding.evidence_count === 1 ? 'item' : 'items'}
                      </span>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        <Progress value={finding.confidence * 100} className="h-2 w-20" />
                        <span className="text-sm text-slate-600">{Math.round(finding.confidence * 100)}%</span>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        {/* Recommendations */}
        {recommendations && recommendations.length > 0 && (
          <Card className="border-blue-200 bg-blue-50">
            <CardHeader>
              <CardTitle className="text-xl text-blue-900">Recommendations</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {recommendations.map((rec, idx) => (
                  <li key={idx} className="flex items-start space-x-2">
                    <FileText className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                    <span className="text-slate-700">{rec}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}
      </main>
    </div>
  );
};

export default RepoScanResults;
