import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { CheckCircle, XCircle, Loader2, RefreshCw } from "lucide-react";
import { complianceAPI, repoScanAPI, systemAPI } from "@/lib/api";

const NetworkDebug = () => {
  const [results, setResults] = useState([]);
  const [testing, setTesting] = useState(false);

  const tests = [
    {
      name: "API Root",
      fn: () => systemAPI.getInfo(),
      description: "GET /api/"
    },
    {
      name: "Health Check",
      fn: () => systemAPI.healthCheck(),
      description: "GET /api/health"
    },
    {
      name: "Get Controls",
      fn: () => systemAPI.getControls(),
      description: "GET /api/controls"
    },
    {
      name: "Get Reports",
      fn: () => complianceAPI.getReports(),
      description: "GET /api/compliance/reports"
    },
    {
      name: "Get Repository Scans",
      fn: () => repoScanAPI.getAllScans(),
      description: "GET /api/compliance/scan/repo"
    }
  ];

  const runTests = async () => {
    setTesting(true);
    setResults([]);
    
    const newResults = [];

    for (const test of tests) {
      try {
        const startTime = Date.now();
        const response = await test.fn();
        const duration = Date.now() - startTime;
        
        newResults.push({
          name: test.name,
          description: test.description,
          status: 'success',
          duration: `${duration}ms`,
          data: JSON.stringify(response).substring(0, 200) + '...'
        });
      } catch (error) {
        newResults.push({
          name: test.name,
          description: test.description,
          status: 'error',
          error: error.response?.data?.detail || error.message || 'Unknown error',
          statusCode: error.response?.status
        });
      }
      
      setResults([...newResults]);
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    setTesting(false);
  };

  const getStatusIcon = (status) => {
    if (status === 'success') return <CheckCircle className="h-5 w-5 text-green-600" />;
    if (status === 'error') return <XCircle className="h-5 w-5 text-red-600" />;
    return <Loader2 className="h-5 w-5 animate-spin text-blue-600" />;
  };

  const getStatusColor = (status) => {
    if (status === 'success') return 'border-green-200 bg-green-50';
    if (status === 'error') return 'border-red-200 bg-red-50';
    return 'border-blue-200 bg-blue-50';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-50 p-6">
      <div className="max-w-5xl mx-auto">
        <Card className="mb-6 border-slate-200">
          <CardHeader>
            <CardTitle className="text-2xl text-slate-900">Network Debug</CardTitle>
            <CardDescription>Test all API endpoints and check network connectivity</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="bg-slate-900 text-green-400 p-3 rounded-lg font-mono text-sm">
                Base URL: {process.env.REACT_APP_BACKEND_URL || 'relative (/api)'}
              </div>
              
              <Button
                onClick={runTests}
                disabled={testing}
                className="bg-blue-600 hover:bg-blue-700 text-white"
              >
                {testing ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Testing...
                  </>
                ) : (
                  <>
                    <RefreshCw className="mr-2 h-4 w-4" />
                    Run All Tests
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        {results.length > 0 && (
          <Card className="border-slate-200">
            <CardHeader>
              <CardTitle className="text-xl text-slate-900">Test Results</CardTitle>
              <CardDescription>
                {results.filter(r => r.status === 'success').length} / {results.length} passed
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {results.map((result, idx) => (
                  <div
                    key={idx}
                    className={`border rounded-lg p-4 ${getStatusColor(result.status)}`}
                  >
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center space-x-3">
                        {getStatusIcon(result.status)}
                        <div>
                          <h4 className="font-semibold text-slate-900">{result.name}</h4>
                          <code className="text-xs text-slate-600">{result.description}</code>
                        </div>
                      </div>
                      {result.status === 'success' && (
                        <Badge variant="outline" className="border-green-300 text-green-700">
                          {result.duration}
                        </Badge>
                      )}
                      {result.statusCode && (
                        <Badge variant="outline" className="border-red-300 text-red-700">
                          {result.statusCode}
                        </Badge>
                      )}
                    </div>
                    
                    {result.status === 'success' && (
                      <div className="mt-2 bg-white border border-slate-200 rounded p-2">
                        <p className="text-xs text-slate-600 font-mono">{result.data}</p>
                      </div>
                    )}
                    
                    {result.status === 'error' && (
                      <div className="mt-2 bg-white border border-red-200 rounded p-2">
                        <p className="text-sm text-red-700">{result.error}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default NetworkDebug;
