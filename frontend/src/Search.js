import React, { useState } from 'react';
import axios from 'axios'; // Import axios
import './Search.css';

export const SearchBar = () => {
    const [query, setQuery] = useState('');
    const [showResults, setShowResults] = useState(false);
    const [results, setResults] = useState([]);
    const [expandedResults, setExpandedResults] = useState([]);
    const [noResults, setNoResults] = useState(false);
    const [loading, setLoading] = useState(false); // State to track loading

    // Handle search on button click
    const handleSearch = async () => {
        if (!query.trim()) {
            // If query is empty, don't show any results or "No results found"
            setShowResults(false);
            setNoResults(false);
            return;
        }

        setShowResults(true);
        setNoResults(false); // Reset "No results" state before fetching new results
        setLoading(true); // Start loading

        try {
            const response = await axios.post("https://pearl-natalia--flask-app-api.modal.run/search_results", { text: query });

            if (response.data.results.length === 0) {
                setNoResults(true); // Set to true if no results are found
                setResults([]); // Ensure results are cleared
            } else {
                setLoading(false);
                setResults(response.data.results);
            }
        } catch (error) {
            console.error("Error fetching search results:", error);
        } finally {
            setLoading(false); // Stop loading
        }
    };

    // Handle search on Enter key press
    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    };

    // Toggle expanded view for results
    const toggleExpand = (index) => {
        setExpandedResults(prevState =>
            prevState.includes(index)
                ? prevState.filter(item => item !== index)
                : [...prevState, index]
        );
    };

    return (
        <div id="body-container">
            <div className="search-container">
                <input
                    id="search-bar"
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Search for examples..."
                    className="search-bar"
                />
                <button onClick={handleSearch} className="search-button" disabled={loading}>
                    {loading ? "Loading..." : "Search"}
                </button>
                <div className={`results-list ${showResults ? 'show' : ''}`}>
                    {showResults && noResults && (
                        <div className="no-results">No results found</div>
                    )}
                    {showResults && results.length > 0 && (
                        results.map((result, index) => (
                            <div
                                key={index}
                                className={`result-item ${expandedResults.includes(index) ? 'expanded' : ''}`}
                                onClick={() => toggleExpand(index)}
                            >
                                <div className="result-summary"><b>{result.summary}</b></div>

                                {expandedResults.includes(index) && (
                                    <>
                                        <div className="result-patient-dialogue">
                                            <strong>Patient Dialogue:</strong> {result.patient_dialogue}
                                        </div>
                                        <div className="result-counselor-dialogue">
                                            <strong>Counselor Dialogue:</strong> {result.counselor_dialogue}
                                        </div>
                                    </>
                                )}
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
};

export default SearchBar;
