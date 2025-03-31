import "./Predict.css";
import { useState } from "react";
import axios from "axios";

export default function Predict() {
    const [text, setText] = useState("");
    const [output, setOutput] = useState("");
    const [loading, setLoading] = useState(false);  // State for loading

    const handleSave = async () => {
        setLoading(true);  // Start loading
        setOutput(""); // Clear previous output

        try {
            const response = await axios.post("https://pearl-natalia--flask-app-api.modal.run/predict_response", { text });

            if (response.status === 200 && response.data.anxiety_level) {
                setOutput(response.data.anxiety_level);
            } else {
                console.error("Unexpected response from server");
                setOutput("Error predicting anxiety levels. Is server running?");
            }
        } catch (error) {
            console.error("Error generating advice", error);
            setOutput("Error predicting anxiety levels. Is server running?");
        } finally {
            setLoading(false);  // Stop loading after response
        }
    };

    return (
        <div id="body-container">
            <div id="container">
                <div id="input-box">
                    <h1 className="text-2xl font-semibold text-gray-800" id="consultation-title">Predict Response</h1>
                    <textarea
                        className="textarea"
                        placeholder="Enter patient dialogue here..."
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                    />
                    <button
                        className="button"
                        onClick={handleSave}
                        disabled={loading || text.trim() === ""}  // Disable button if no input or loading
                    >
                        {loading ? "Predicting..." : "Predict Response Type"}  {/* Change button text based on loading state */}
                    </button>
                </div>
                <div id="output-box">
                    <h1 style={{ textAlign: 'center' }}>
                        {loading ? "Predicting..." : (output ? output : "Click the button to predict...")}
                    </h1>
                </div>
            </div>
        </div>
    );
}
