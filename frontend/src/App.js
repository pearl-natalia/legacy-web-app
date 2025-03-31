import "./App.css";
import { useState, useEffect, useRef } from "react";
import axios from "axios";

export default function App() {
  const [text, setText] = useState("");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isOverflowing, setIsOverflowing] = useState(false); // Track overflow state

  const outputRef = useRef(null);  // Reference for the output box

  // Scroll to the top if the output is overflowing
  useEffect(() => {
    if (outputRef.current) {
      const isOverflowing = outputRef.current.scrollHeight > outputRef.current.clientHeight;
      setIsOverflowing(isOverflowing); // Update the state to track overflow

      if (isOverflowing) {
        outputRef.current.scrollTop = 0; // Scroll to the top if overflowing
      }
    }
  }, [output]); // Triggered when the output changes

  const handleSave = async () => {
    setLoading(true);
    setOutput("");
    try {
      const response = await axios.post("https://pearl-natalia--flask-app-api.modal.run/generate_advice", { text });
      if (response.status === 200 && response.data.advice) {
        setOutput(response.data.advice);
      } else {
        setOutput("Error retrieving advice. Is server running?");
      }
    } catch (error) {
      setOutput("Error retrieving advice. Is server running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div id="body-container">
      <div id="container">
        <div id="input-box">
          <h1 className="text-2xl font-semibold text-gray-800" id="consultation-title" style={{ overflowX: 'hidden', overflowY: 'hidden' }}>Get Consultation</h1>
          <textarea
            className="textarea"
            placeholder="Enter your consultation notes here..."
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
        <div
          id="output-box"
          ref={outputRef}
          className={isOverflowing ? "overflowing" : ""} // Add or remove the "overflowing" class
        >
          <h1>{loading ? "Processing..." : output ? "" : "No Advice Yet"}</h1>
          <p style={{ lineHeight: '1.6' }}>{output}</p>
        </div>
      </div>
    </div>
  );
}
