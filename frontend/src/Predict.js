import { useState } from "react";
import axios from "axios";
import "./Predict.css";

export default function Predict() {
    const [text, setText] = useState("");
    const [output, setOutput] = useState("");
    const [loading, setLoading] = useState(false);  // State for loading

    const handleSave = async () => {
        setLoading(true);  // Start loading
        setOutput(""); // Clear previous output

        try {
            const response = await axios.post("https://pearl-natalia--flask-app-api.modal.run/predict_response", { text });

            if (response.status === 200 && response.data.advice) {
                setOutput(response.data.advice);
            } else {
                console.error("Unexpected response from server");
                setOutput("Error retrieving advice.");
            }
        } catch (error) {
            console.error("Error generating advice", error);
            setOutput("Error retrieving advice.");
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
                        disabled={loading || text.trim() === ""}  // Disable button if no input
                    >
                        Predict Resonse Type
                    </button>
                </div>
                <div id="output-box">
                    <h1>{loading ? "Please give me a moment..." : output ? "" : "Click the button to predict..."}</h1>  {/* Show dynamic status */}
                    <p>{loading || !output ? "" : output}</p>  {/* Only show output once loading is finished */}
                </div>
            </div>
        </div>
    );
}
