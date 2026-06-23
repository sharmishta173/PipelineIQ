import { useEffect, useState } from "react";
import axios from "axios";

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

import { Pie } from "react-chartjs-2";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend
);

function App() {

  const [stats, setStats] = useState({});
  const [runs, setRuns] = useState([]);
  const [selectedRun, setSelectedRun] = useState(null);

  useEffect(() => {

    axios
      .get("http://127.0.0.1:8000/stats")
      .then((res) => {
        setStats(res.data);
      });

    axios
      .get("http://127.0.0.1:8000/pipeline-runs")
      .then((res) => {
        setRuns(res.data);
      });

  }, []);

  const categoryCounts = {};

  runs.forEach((run) => {
    categoryCounts[run.category] =
      (categoryCounts[run.category] || 0) + 1;
  });

  const mostCommonFailure =
    Object.keys(categoryCounts).length > 0
      ? Object.entries(categoryCounts)
          .sort((a, b) => b[1] - a[1])[0][0]
      : "N/A";

  const chartData = {
    labels: Object.keys(categoryCounts),

    datasets: [
      {
        label: "Failures",
        data: Object.values(categoryCounts)
      }
    ]
  };

  return (
    <div
      style={{
        padding: "30px",
        backgroundColor: "#0f172a",
        minHeight: "100vh",
        color: "white"
      }}
    >

      <h1 style={{ marginBottom: "30px" }}>
        🚀 PipelineIQ Dashboard
      </h1>

      {/* Metric Cards */}

      <div
        style={{
          display: "flex",
          gap: "20px",
          flexWrap: "wrap",
          marginBottom: "40px"
        }}
      >

        <div
          style={{
            backgroundColor: "#1e293b",
            padding: "20px",
            borderRadius: "12px",
            minWidth: "220px"
          }}
        >
          <h3>Total Runs</h3>
          <h1>{stats.total_runs ?? 0}</h1>
        </div>

        <div
          style={{
            backgroundColor: "#7f1d1d",
            padding: "20px",
            borderRadius: "12px",
            minWidth: "220px"
          }}
        >
          <h3>Failed Runs</h3>
          <h1>{stats.failed_runs ?? 0}</h1>
        </div>

        <div
          style={{
            backgroundColor: "#14532d",
            padding: "20px",
            borderRadius: "12px",
            minWidth: "220px"
          }}
        >
          <h3>Success Rate</h3>
          <h1>{stats.success_rate ?? 0}%</h1>
        </div>

        <div
          style={{
            backgroundColor: "#312e81",
            padding: "20px",
            borderRadius: "12px",
            minWidth: "260px"
          }}
        >
          <h3>Top Failure</h3>
          <h2>{mostCommonFailure}</h2>
        </div>

      </div>

      <hr />

      {/* Pie Chart */}

      <h2
        style={{
          textAlign: "center",
          marginTop: "30px"
        }}
      >
        Failure Categories
      </h2>

      <div
        style={{
          width: "500px",
          margin: "auto",
          marginBottom: "40px"
        }}
      >
        <Pie data={chartData} />
      </div>

      {/* Pipeline Runs Table */}

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          backgroundColor: "#111827"
        }}
      >

        <thead>

          <tr
            style={{
              backgroundColor: "#1f2937"
            }}
          >
            <th style={{ padding: "12px" }}>Run ID</th>
            <th style={{ padding: "12px" }}>Category</th>
            <th style={{ padding: "12px" }}>Status</th>
            <th style={{ padding: "12px" }}>Confidence</th>
            <th style={{ padding: "12px" }}>Commit SHA</th>
            <th style={{ padding: "12px" }}>Timestamp</th>
          </tr>

        </thead>

        <tbody>

          {runs.map((run) => (

            <tr
              key={run.id}
              onClick={() => setSelectedRun(run)}
              style={{
                cursor: "pointer"
              }}
            >

              <td
                style={{
                  padding: "12px",
                  borderBottom: "1px solid #374151"
                }}
              >
                {run.run_id}
              </td>

              <td
                style={{
                  padding: "12px",
                  borderBottom: "1px solid #374151"
                }}
              >
                {run.category}
              </td>

              <td
                style={{
                  padding: "12px",
                  borderBottom: "1px solid #374151"
                }}
              >
                {run.status}
              </td>

              <td
                style={{
                  padding: "12px",
                  borderBottom: "1px solid #374151"
                }}
              >
                {run.confidence}
              </td>

              <td
                style={{
                  padding: "12px",
                  borderBottom: "1px solid #374151"
                }}
              >
                {run.commit_sha ? (
                  <a
                    href={`https://github.com/sharmishta173/PipelineIQ/commit/${run.commit_sha}`}
                    target="_blank"
                    rel="noreferrer"
                    onClick={(e) => e.stopPropagation()}
                  >
                    {run.commit_sha.slice(0, 7)}
                  </a>
                ) : (
                  "N/A"
                )}
              </td>

              <td
                style={{
                  padding: "12px",
                  borderBottom: "1px solid #374151"
                }}
              >
                {run.created_at
                  ? new Date(run.created_at).toLocaleString()
                  : "N/A"}
              </td>

            </tr>

          ))}

        </tbody>

      </table>

      {/* Failure Details Panel */}

      {selectedRun && (

        <div
          style={{
            marginTop: "40px",
            padding: "20px",
            borderRadius: "12px",
            backgroundColor: "#1e293b"
          }}
        >

          <h2>Failure Details</h2>

          <p>
            <strong>Run ID:</strong>{" "}
            {selectedRun.run_id}
          </p>

          <p>
            <strong>Category:</strong>{" "}
            {selectedRun.category}
          </p>

          <p>
            <strong>Status:</strong>{" "}
            {selectedRun.status}
          </p>

          <p>
            <strong>Confidence:</strong>{" "}
            {selectedRun.confidence}
          </p>

          <p>
            <strong>Timestamp:</strong>{" "}
            {selectedRun.created_at
              ? new Date(selectedRun.created_at).toLocaleString()
              : "N/A"}
          </p>

          <p>
            <strong>Failure Log:</strong>
          </p>

          <pre
            style={{
              backgroundColor: "#111827",
              padding: "15px",
              borderRadius: "8px",
              overflowX: "auto"
            }}
          >
            {selectedRun.failure_log}
          </pre>

          <p>
            <strong>AI Suggestion:</strong>
          </p>

          <pre
            style={{
              backgroundColor: "#111827",
              padding: "15px",
              borderRadius: "8px"
            }}
          >
            {selectedRun.ai_suggestion}
          </pre>

          {selectedRun.commit_sha && (
            <a
              href={`https://github.com/sharmishta173/PipelineIQ/commit/${selectedRun.commit_sha}`}
              target="_blank"
              rel="noreferrer"
              style={{
                display: "inline-block",
                marginTop: "15px",
                padding: "10px 16px",
                backgroundColor: "#2563eb",
                color: "white",
                textDecoration: "none",
                borderRadius: "8px"
              }}
            >
              View Commit on GitHub
            </a>
          )}

        </div>

      )}

    </div>
  );
}

export default App;