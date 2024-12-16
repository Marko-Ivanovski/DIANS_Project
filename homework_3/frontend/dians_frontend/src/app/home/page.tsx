"use client";
import { useState, useEffect } from "react";
import axios from "axios";
import Select from "react-select";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

interface Firm {
  value: string;
  label: string;
}

interface Share {
  date: string;
  price_of_last_transaction: number;
}

const SharesPage: React.FC = () => {
  const [firms, setFirms] = useState<Firm[]>([]);
  const [selectedFirm, setSelectedFirm] = useState<Firm | null>(null);
  const [fromDate, setFromDate] = useState<string>("");
  const [toDate, setToDate] = useState<string>("");
  const [chartData, setChartData] = useState<any>(null);

  // Fetch firms for the dropdown
  useEffect(() => {
    axios
      .get(`http://localhost:8000/firms/`)
      .then((response) => {
        console.log("Firms fetched:", response.data);
        setFirms(
          response.data.map((firm: { firm_id: string }) => ({
            value: firm.firm_id,
            label: firm.firm_id,
          }))
        );
      })
      .catch((error) => console.error("Error fetching firms:", error));
  }, []);

  // Fetch shares based on the selected firm and date range
  const fetchShares = async () => {
    if (!selectedFirm || !fromDate || !toDate) {
      alert("Please select a firm and provide both dates.");
      return;
    }

    try {
      const response = await axios.get("http://localhost:8000/shares/average-price", {
        params: {
          firm_id: selectedFirm.value,
          from_date: fromDate,
          to_date: toDate,
        },
      });
      console.log("Response data:", response.data);
      prepareChartData(response.data);
    } catch (error: any) {
      console.error("Error fetching shares:", error.response?.data || error);
      alert(error.response?.data || "An error occurred.");
    }
  };

  // Prepare data for the chart
  const prepareChartData = (data: Share[]) => {
    setChartData({
      labels: data.map((share) => share.date),
      datasets: [
        {
          label: "Price of Last Transaction",
          data: data.map((share) => share.price_of_last_transaction), // Y-axis: Prices
          fill: false,
          backgroundColor: "rgba(75, 192, 192, 0.6)",
          borderColor: "rgba(75, 192, 192, 1)",
          tension: 0.1,
        },
      ],
    });
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Shares Viewer</h1>

      {/* Dropdown for firms */}
      <div>
        <label>Firm:</label>
        <Select
          options={firms}
          onChange={setSelectedFirm}
          placeholder="Select a firm"
        />
      </div>

      {/* Input fields for date range */}
      <div style={{ margin: "10px 0" }}>
        <label>From Date:</label>
        <input
          type="date"
          value={fromDate}
          onChange={(e) => setFromDate(e.target.value)}
        />
        <label style={{ marginLeft: "10px" }}>To Date:</label>
        <input
          type="date"
          value={toDate}
          onChange={(e) => setToDate(e.target.value)}
        />
      </div>

      {/* Button to fetch shares */}
      <button onClick={fetchShares} style={{ margin: "10px 0" }}>
        Fetch Shares
      </button>

      {/* Chart for share prices */}
      {chartData && (
        <div style={{ marginTop: "20px" }}>
          <Line
            data={chartData}
            options={{
              responsive: true,
              scales: {
                x: {
                  title: { display: true, text: "Date" },
                },
                y: {
                  title: { display: true, text: "Price" },
                },
              },
            }}
          />
        </div>
      )}
    </div>
  );
};

export default SharesPage;