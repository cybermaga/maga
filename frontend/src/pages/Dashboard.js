import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { FileText, Plus, Shield, TrendingUp, AlertCircle, Upload, Code } from "lucide-react";
import { toast } from "sonner";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = () => {
  const navigate = useNavigate();
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    total: 0,
    compliant: 0,
    partial: 0,
    nonCompliant: 0
  });

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/compliance/reports`);
      setReports(response.data);
      calculateStats(response.data);
    } catch (error) {
      console.error("Error fetching reports:", error);
      // Don't show error toast on initial load - just set empty reports
      setReports([]);
      setStats({ total: 0, compliant: 0, partial: 0, nonCompliant: 0 });
      
      // Only show error if it's not a network/connection issue
      if (error.response && error.response.status !== 404) {
        toast.error("Failed to load reports");
      }
    } finally {
      setLoading(false);
    }
  };

  const calculateStats = (reportsData) => {
    const total = reportsData.length;
    let compliant = 0;
    let partial = 0;
    let nonCompliant = 0;

    reportsData.forEach(report => {
      const score = report.compliance_results?.overall_score;
      if (score) {
        if (score.percentage >= 80) compliant++;
        else if (score.percentage >= 40) partial++;
        else nonCompliant++;
      }
    });

    setStats({ total, compliant, partial, nonCompliant });
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
      A: "bg-green-500 text-white hover:bg-green-600",
      B: "bg-blue-500 text-white hover:bg-blue-600",
      C: "bg-amber-500 text-white hover:bg-amber-600",
      D: "bg-red-500 text-white hover:bg-red-600",
      F: "bg-red-700 text-white hover:bg-red-800"
    };
    return colors[grade] || "bg-gray-500 text-white";
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="bg-blue-600 p-3 rounded-lg">
                <Shield className="h-8 w-8 text-white" data-testid="logo-icon" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }} data-testid="app-title">
                  Emergent AI Compliance
                </h1>
                <p className="text-sm text-slate-600 mt-1" data-testid="app-subtitle">EU AI Act Compliance Analysis Tool</p>
              </div>
            </div>
            <div className="flex space-x-3">
              <Button
                onClick={() => navigate('/scan/repo')}
                variant="outline"
                className="border-blue-600 text-blue-600 hover:bg-blue-50 px-6 py-6 text-base font-semibold rounded-lg"
                data-testid="repo-scan-button"
              >
                <Upload className="mr-2 h-5 w-5" />
                Scan Repository
              </Button>
              <Button
                onClick={() => navigate('/scan/new')}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-6 text-base font-semibold rounded-lg"
                data-testid="new-scan-button"
              >
                <Plus className="mr-2 h-5 w-5" />
                New Compliance Scan
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="border-slate-200" data-testid="stat-card-total">
            <CardHeader className="pb-3">
              <CardDescription className="text-slate-600">Total Scans</CardDescription>
              <CardTitle className="text-4xl font-bold text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                {stats.total}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center text-sm text-slate-600">
                <FileText className="h-4 w-4 mr-2" />
                All compliance reports
              </div>
            </CardContent>
          </Card>

          <Card className="border-green-200 bg-green-50" data-testid="stat-card-compliant">
            <CardHeader className="pb-3">
              <CardDescription className="text-green-700">Compliant</CardDescription>
              <CardTitle className="text-4xl font-bold text-green-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                {stats.compliant}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center text-sm text-green-700">
                <TrendingUp className="h-4 w-4 mr-2" />
                ≥ 80% compliance
              </div>
            </CardContent>
          </Card>

          <Card className="border-amber-200 bg-amber-50" data-testid="stat-card-partial">
            <CardHeader className="pb-3">
              <CardDescription className="text-amber-700">Partial Compliance</CardDescription>
              <CardTitle className="text-4xl font-bold text-amber-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                {stats.partial}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center text-sm text-amber-700">
                <AlertCircle className="h-4 w-4 mr-2" />
                40-79% compliance
              </div>
            </CardContent>
          </Card>

          <Card className="border-red-200 bg-red-50" data-testid="stat-card-non-compliant">
            <CardHeader className="pb-3">
              <CardDescription className="text-red-700">Non-Compliant</CardDescription>
              <CardTitle className="text-4xl font-bold text-red-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                {stats.nonCompliant}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center text-sm text-red-700">
                <AlertCircle className="h-4 w-4 mr-2" />
                &lt; 40% compliance
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Reports List */}
        <Card className="border-slate-200" data-testid="reports-list-card">
          <CardHeader>
            <CardTitle className="text-2xl text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              Recent Compliance Scans
            </CardTitle>
            <CardDescription>View and manage your AI system compliance reports</CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center py-12" data-testid="loading-indicator">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent"></div>
                <p className="mt-4 text-slate-600">Loading reports...</p>
              </div>
            ) : reports.length === 0 ? (
              <div className="text-center py-12" data-testid="no-reports-message">
                <FileText className="h-16 w-16 mx-auto text-slate-300 mb-4" />
                <h3 className="text-xl font-semibold text-slate-700 mb-2">No compliance scans yet</h3>
                <p className="text-slate-500 mb-6">Start your first compliance scan to analyze your AI system</p>
                <Button
                  onClick={() => navigate('/scan/new')}
                  className="bg-blue-600 hover:bg-blue-700 text-white"
                  data-testid="empty-state-new-scan-button"
                >
                  <Plus className="mr-2 h-4 w-4" />
                  Create First Scan
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                {reports.map((report, index) => (
                  <div
                    key={report.id}
                    data-testid={`report-card-${index}`}
                    className="border border-slate-200 rounded-lg p-6 hover:border-blue-300 hover:shadow-md transition-all cursor-pointer bg-white"
                    onClick={() => navigate(`/report/${report.id}`)}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h3 className="text-lg font-semibold text-slate-900" data-testid={`report-name-${index}`}>
                            {report.system_name}
                          </h3>
                          <Badge className={getRiskBadgeColor(report.risk_classification?.risk_level)} data-testid={`report-risk-badge-${index}`}>
                            {report.risk_classification?.risk_level?.toUpperCase()}
                          </Badge>
                        </div>
                        <p className="text-sm text-slate-600 mb-3" data-testid={`report-date-${index}`}>
                          Scanned on {formatDate(report.timestamp)}
                        </p>
                        <p className="text-sm text-slate-600" data-testid={`report-reasoning-${index}`}>
                          {report.risk_classification?.reasoning}
                        </p>
                      </div>
                      <div className="text-right ml-6">
                        <Badge
                          className={`${getGradeBadgeColor(report.compliance_results?.overall_score?.grade)} text-2xl px-4 py-2 font-bold`}
                          data-testid={`report-grade-badge-${index}`}
                        >
                          {report.compliance_results?.overall_score?.grade}
                        </Badge>
                        <p className="text-sm text-slate-600 mt-2" data-testid={`report-percentage-${index}`}>
                          {report.compliance_results?.overall_score?.percentage}% compliant
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default Dashboard;
