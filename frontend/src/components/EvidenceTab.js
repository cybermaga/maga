import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '@/components/ui/table';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { CheckCircle2, XCircle, AlertCircle, Clock, Eye, Play, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import { evidenceApi } from '@/lib/api';

const EvidenceTab = ({ scanId }) => {
  const [evidence, setEvidence] = useState(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [selectedEvidence, setSelectedEvidence] = useState(null);
  const [rawData, setRawData] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetchEvidence();
  }, [scanId]);

  const fetchEvidence = async () => {
    try {
      setLoading(true);
      const response = await evidenceApi.getEvidence(scanId);
      setEvidence(response.data);
    } catch (error) {
      console.error('Error fetching evidence:', error);
      if (error.response?.status !== 404) {
        toast.error('Failed to load evidence');
      }
      setEvidence({ evidence_list: [], total_evidence: 0, passed: 0, warned: 0, failed: 0, pending: 0 });
    } finally {
      setLoading(false);
    }
  };

  const runAnalyzers = async () => {
    try {
      setRunning(true);
      const response = await evidenceApi.runAnalyzers(scanId, ['deps', 'bandit', 'onnx_meta', 'dataset_sanity']);
      toast.success(response.data.message);
      
      // Poll for results
      setTimeout(() => {
        fetchEvidence();
      }, 5000);
    } catch (error) {
      console.error('Error running analyzers:', error);
      toast.error(error.response?.data?.detail || 'Failed to run analyzers');
    } finally {
      setRunning(false);
    }
  };

  const viewRawEvidence = async (ev) => {
    try {
      const response = await evidenceApi.getRawEvidence(scanId, ev.id);
      setRawData(response.data);
      setSelectedEvidence(ev);
      setShowModal(true);
    } catch (error) {
      console.error('Error fetching raw evidence:', error);
      toast.error('Failed to load raw evidence');
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'pass':
        return <CheckCircle2 className="h-5 w-5 text-green-600" />;
      case 'warn':
        return <AlertCircle className="h-5 w-5 text-amber-600" />;
      case 'fail':
        return <XCircle className="h-5 w-5 text-red-600" />;
      case 'pending':
        return <Clock className="h-5 w-5 text-blue-600" />;
      default:
        return <XCircle className="h-5 w-5 text-gray-600" />;
    }
  };

  const getStatusBadge = (status) => {
    const colors = {
      pass: 'bg-green-100 text-green-800 hover:bg-green-200',
      warn: 'bg-amber-100 text-amber-800 hover:bg-amber-200',
      fail: 'bg-red-100 text-red-800 hover:bg-red-200',
      pending: 'bg-blue-100 text-blue-800 hover:bg-blue-200',
      error: 'bg-gray-100 text-gray-800 hover:bg-gray-200',
    };
    return colors[status] || colors.error;
  };

  if (loading) {
    return (
      <Card data-testid="evidence-loading">
        <CardContent className="py-12 text-center">
          <Loader2 className="h-12 w-12 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-slate-600">Loading evidence...</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Evidence Summary */}
      <Card className="border-slate-200" data-testid="evidence-summary">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-xl text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              Evidence & Mapping
            </CardTitle>
            <Button
              onClick={runAnalyzers}
              disabled={running}
              className="bg-blue-600 hover:bg-blue-700 text-white"
              data-testid="run-analyzers-button"
            >
              {running ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Running...
                </>
              ) : (
                <>
                  <Play className="mr-2 h-4 w-4" />
                  Run Analyzers
                </>
              )}
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          {evidence && evidence.total_evidence > 0 ? (
            <>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
                <div className="text-center p-4 bg-slate-50 rounded-lg">
                  <p className="text-3xl font-bold text-slate-900">{evidence.total_evidence}</p>
                  <p className="text-sm text-slate-600">Total</p>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <p className="text-3xl font-bold text-green-700">{evidence.passed}</p>
                  <p className="text-sm text-green-600">Passed</p>
                </div>
                <div className="text-center p-4 bg-amber-50 rounded-lg">
                  <p className="text-3xl font-bold text-amber-700">{evidence.warned}</p>
                  <p className="text-sm text-amber-600">Warned</p>
                </div>
                <div className="text-center p-4 bg-red-50 rounded-lg">
                  <p className="text-3xl font-bold text-red-700">{evidence.failed}</p>
                  <p className="text-sm text-red-600">Failed</p>
                </div>
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <p className="text-3xl font-bold text-blue-700">{evidence.pending}</p>
                  <p className="text-sm text-blue-600">Pending</p>
                </div>
              </div>

              {/* Evidence Table */}
              <Table data-testid="evidence-table">
                <TableHeader>
                  <TableRow>
                    <TableHead>Rule</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>AI Act Articles</TableHead>
                    <TableHead>Summary</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {evidence.evidence_list.map((ev, index) => (
                    <TableRow key={ev.id} data-testid={`evidence-row-${index}`}>
                      <TableCell className="font-medium">
                        <code className="bg-slate-100 px-2 py-1 rounded text-sm">{ev.rule}</code>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center space-x-2">
                          {getStatusIcon(ev.status)}
                          <Badge className={getStatusBadge(ev.status)}>
                            {ev.status.toUpperCase()}
                          </Badge>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex flex-wrap gap-1">
                          {ev.articles && ev.articles.length > 0 ? (
                            ev.articles.map((article, idx) => (
                              <Badge key={idx} variant="outline" className="text-xs">
                                {article}
                              </Badge>
                            ))
                          ) : (
                            <span className="text-slate-400 text-sm">N/A</span>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <p className="text-sm text-slate-700 line-clamp-2">{ev.summary}</p>
                      </TableCell>
                      <TableCell className="text-right">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => viewRawEvidence(ev)}
                          data-testid={`view-evidence-${index}`}
                        >
                          <Eye className="h-4 w-4 mr-1" />
                          View JSON
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </>
          ) : (
            <div className="text-center py-12" data-testid="no-evidence">
              <AlertCircle className="h-16 w-16 mx-auto text-slate-300 mb-4" />
              <h3 className="text-xl font-semibold text-slate-700 mb-2">No Evidence Yet</h3>
              <p className="text-slate-500 mb-6">
                Upload artifacts and run analyzers to generate compliance evidence
              </p>
              <Button
                onClick={runAnalyzers}
                disabled={running}
                className="bg-blue-600 hover:bg-blue-700 text-white"
              >
                <Play className="mr-2 h-4 w-4" />
                Run Analyzers Now
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Raw Evidence Modal */}
      <Dialog open={showModal} onOpenChange={setShowModal}>
        <DialogContent className="max-w-3xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Raw Evidence - {selectedEvidence?.rule}</DialogTitle>
            <DialogDescription>
              {selectedEvidence?.summary}
            </DialogDescription>
          </DialogHeader>
          <div className="mt-4">
            <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto text-sm">
              {JSON.stringify(rawData || selectedEvidence?.details, null, 2)}
            </pre>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default EvidenceTab;
