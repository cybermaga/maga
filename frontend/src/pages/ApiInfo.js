import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ExternalLink, FileText, Code, CheckCircle } from "lucide-react";

const API_DOCS_URL = process.env.REACT_APP_BACKEND_URL 
  ? `${process.env.REACT_APP_BACKEND_URL}/docs` 
  : '/docs';

const ApiInfo = () => {
  const endpoints = [
    {
      method: "GET",
      path: "/api/",
      description: "API information and version",
      status: "active"
    },
    {
      method: "GET",
      path: "/api/health",
      description: "Health check endpoint",
      status: "active"
    },
    {
      method: "GET",
      path: "/api/controls",
      description: "Get all compliance controls",
      status: "active"
    },
    {
      method: "POST",
      path: "/api/compliance/scan",
      description: "Create questionnaire-based scan",
      status: "active"
    },
    {
      method: "GET",
      path: "/api/compliance/reports",
      description: "Get all compliance reports",
      status: "active"
    },
    {
      method: "POST",
      path: "/api/compliance/scan/repo",
      description: "Upload and scan repository ZIP",
      status: "active"
    },
    {
      method: "GET",
      path: "/api/compliance/scan/repo/{id}",
      description: "Get repository scan results",
      status: "active"
    },
  ];

  const getMethodColor = (method) => {
    const colors = {
      GET: "bg-blue-500 text-white",
      POST: "bg-green-500 text-white",
      PUT: "bg-amber-500 text-white",
      DELETE: "bg-red-500 text-white"
    };
    return colors[method] || "bg-slate-500 text-white";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-50">
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center space-x-4">
            <div className="bg-blue-600 p-3 rounded-lg">
              <Code className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                API Documentation
              </h1>
              <p className="text-sm text-slate-600 mt-1">Emergent AI Compliance API Reference</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Interactive Docs Link */}
        <Card className="mb-8 border-blue-200 bg-blue-50">
          <CardHeader>
            <CardTitle className="text-xl text-blue-900">Interactive API Documentation</CardTitle>
            <CardDescription className="text-blue-700">
              Explore and test all API endpoints with Swagger UI
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button
              asChild
              className="bg-blue-600 hover:bg-blue-700 text-white"
            >
              <a href={API_DOCS_URL} target="_blank" rel="noopener noreferrer">
                <ExternalLink className="mr-2 h-4 w-4" />
                Open API Documentation
              </a>
            </Button>
          </CardContent>
        </Card>

        {/* Base URL Info */}
        <Card className="mb-8 border-slate-200">
          <CardHeader>
            <CardTitle className="text-xl text-slate-900">Base URL</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="bg-slate-900 text-green-400 p-4 rounded-lg font-mono text-sm">
              {process.env.REACT_APP_BACKEND_URL || window.location.origin}
            </div>
            <p className="mt-3 text-sm text-slate-600">
              All API endpoints are prefixed with <code className="bg-slate-100 px-2 py-1 rounded">/api</code>
            </p>
          </CardContent>
        </Card>

        {/* Endpoints List */}
        <Card className="border-slate-200">
          <CardHeader>
            <CardTitle className="text-xl text-slate-900">Available Endpoints</CardTitle>
            <CardDescription>All currently active API endpoints</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {endpoints.map((endpoint, idx) => (
                <div
                  key={idx}
                  className="flex items-center justify-between p-4 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors"
                >
                  <div className="flex items-center space-x-4 flex-1">
                    <Badge className={getMethodColor(endpoint.method)}>
                      {endpoint.method}
                    </Badge>
                    <code className="text-sm font-mono text-slate-700">
                      {endpoint.path}
                    </code>
                  </div>
                  <div className="flex items-center space-x-4">
                    <span className="text-sm text-slate-600">{endpoint.description}</span>
                    <Badge variant="outline" className="border-green-300 text-green-700">
                      <CheckCircle className="h-3 w-3 mr-1" />
                      {endpoint.status}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Quick Examples */}
        <Card className="mt-8 border-slate-200">
          <CardHeader>
            <CardTitle className="text-xl text-slate-900">Quick Examples</CardTitle>
            <CardDescription>Common API usage patterns</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h4 className="font-semibold text-slate-900 mb-2">Get API Info</h4>
              <div className="bg-slate-900 text-green-400 p-3 rounded-lg font-mono text-sm overflow-x-auto">
                curl {process.env.REACT_APP_BACKEND_URL || window.location.origin}/api/
              </div>
            </div>

            <div>
              <h4 className="font-semibold text-slate-900 mb-2">Get All Controls</h4>
              <div className="bg-slate-900 text-green-400 p-3 rounded-lg font-mono text-sm overflow-x-auto">
                curl {process.env.REACT_APP_BACKEND_URL || window.location.origin}/api/controls
              </div>
            </div>

            <div>
              <h4 className="font-semibold text-slate-900 mb-2">Upload Repository</h4>
              <div className="bg-slate-900 text-green-400 p-3 rounded-lg font-mono text-sm overflow-x-auto">
                curl -X POST {process.env.REACT_APP_BACKEND_URL || window.location.origin}/api/compliance/scan/repo \<br/>
                {"  "}-F "zip_file=@/path/to/repo.zip" \<br/>
                {"  "}-F "system_name=My AI System"
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Network Debug Info */}
        <Card className="mt-8 border-slate-200">
          <CardHeader>
            <CardTitle className="text-xl text-slate-900">Debug Information</CardTitle>
            <CardDescription>Current configuration and environment</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-slate-600">Environment:</span>
              <code className="text-slate-900">{process.env.NODE_ENV}</code>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-600">Backend URL:</span>
              <code className="text-slate-900">{process.env.REACT_APP_BACKEND_URL || 'relative'}</code>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-600">API Base:</span>
              <code className="text-slate-900">{process.env.REACT_APP_BACKEND_URL ? `${process.env.REACT_APP_BACKEND_URL}/api` : '/api'}</code>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default ApiInfo;
