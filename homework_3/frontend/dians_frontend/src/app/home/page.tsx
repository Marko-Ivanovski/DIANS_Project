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

interface TechnicalIndicator {
  date: string;
  SMA_10: number; // Simple Moving Average (10-day)
  EMA_10: number; // Exponential Moving Average (10-day)
  RSI: number;    // Relative Strength Index
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

  // Fetch shares and technical analysis data
  const fetchShares = async () => {
    if (!selectedFirm || !fromDate || !toDate) {
      alert("Please select a firm and provide both dates.");
      return;
    }

    try {
      // Fetch share prices
      const sharesResponse = await axios.get("http://localhost:8000/shares/average-price", {
        params: {
          firm_id: selectedFirm.value,
          from_date: fromDate,
          to_date: toDate,
        },
      });
      console.log("Shares Data:", sharesResponse.data);

      // Fetch technical analysis data
      const analysisResponse = await axios.get("http://localhost:8000/shares/technical-analysis", {
        params: {
          firm_id: selectedFirm.value,
          from_date: fromDate,
          to_date: toDate,
        },
      });
      console.log("Technical Analysis Data:", analysisResponse.data);

      // Combine the two datasets into the chart
      prepareChartData(sharesResponse.data, analysisResponse.data);
    } catch (error: any) {
      console.error("Error fetching data:", error.response?.data || error);
      alert(error.response?.data || "An error occurred.");
    }
  };

  // Prepare data for the chart (shares + technical indicators)
  const prepareChartData = (sharesData: Share[], analysisData: TechnicalIndicator[]) => {
    setChartData({
      labels: sharesData.map((share) => share.date),
      datasets: [
        {
          label: "Price of Last Transaction",
          data: sharesData.map((share) => share.price_of_last_transaction), // Y-axis: Prices
          fill: false,
          backgroundColor: "rgba(75, 192, 192, 0.6)",
          borderColor: "rgba(75, 192, 192, 1)",
          tension: 0.1,
        },
        {
          label: "SMA (10-day)",
          data: analysisData.map((indicator) => indicator.SMA_10), // Simple Moving Average
          fill: false,
          checked: false,
          backgroundColor: "rgba(255, 206, 86, 0.6)",
          borderColor: "rgba(255, 206, 86, 1)",
          borderDash: [5, 5],
        },
        {
          label: "EMA (10-day)",
          data: analysisData.map((indicator) => indicator.EMA_10), // Exponential Moving Average
          fill: false,
          checked: false,
          backgroundColor: "rgba(54, 162, 235, 0.6)",
          borderColor: "rgba(54, 162, 235, 1)",
          borderDash: [10, 5],
        },
        {
          label: "RSI (14-day)",
          data: analysisData.map((indicator) => indicator.RSI), // Relative Strength Index
          fill: false,
          checked: false,
          backgroundColor: "rgba(255, 99, 132, 0.6)",
          borderColor: "rgba(255, 99, 132, 1)",
          tension: 0.1,
          yAxisID: "y2", // Separate Y-axis for RSI
        },
      ],
    });
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Shares Viewer with Technical Analysis</h1>

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

      {/* Button to fetch shares and analysis */}
      <button onClick={fetchShares} style={{ margin: "10px 0" }}>
        Fetch Shares
      </button>

      {/* Chart for share prices and analysis */}
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
                y2: {
                  position: "right",
                  title: { display: true, text: "RSI" },
                  grid: { drawOnChartArea: false },
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