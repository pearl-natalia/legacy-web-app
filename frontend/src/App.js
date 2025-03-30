import { useState } from "react";
import axios from "axios";
import "./App.css";

export default function App() {
  const [text, setText] = useState("");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSave = async () => {
    setLoading(true);
    setOutput("");
    try {
      const response = await axios.post("https://pearl-natalia--flask-app-api.modal.run/generate_advice", { text });
      if (response.status === 200 && response.data.advice) {
        setOutput(response.data.advice);
      } else {
        setOutput("Error retrieving advice.");
      }
    } catch (error) {
      setOutput("Error retrieving advice.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div id="body-container">
      <div id="container">
        <div id="input-box">
          <h1 className="text-2xl font-semibold text-gray-800" id="consultation-title">Get Consultation</h1>
          <textarea
            className="textarea"
            placeholder="Type your consultation notes here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <button
            className="button"
            onClick={handleSave}
            disabled={loading || text.trim() === ""}
          >
            {loading ? "Processing..." : "Get Advice"}
          </button>
        </div>
        <div id="output-box">
          <h1>{loading ? "Processing..." : output ? "" : "Advice will appear here"}</h1>
          <p style={{ lineHeight: '1.6' }}>{output}</p>
        </div>
      </div>
    </div>
  );
}