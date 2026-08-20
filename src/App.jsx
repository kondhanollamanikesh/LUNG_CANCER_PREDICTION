import { useState } from "react";
import "./App.css";

const fields = [
  "YELLOW_FINGERS",
  "ANXIETY",
  "PEER_PRESSURE",
  "CHRONIC DISEASE",
  "FATIGUE",
  "ALLERGY",
  "WHEEZING",
  "ALCOHOL CONSUMING",
  "COUGHING",
  "SWALLOWING DIFFICULTY",
  "CHEST PAIN",
];

function App() {
  const [formData, setFormData] = useState(
    Object.fromEntries(fields.map((field) => [field, ""]))
  );

  const [prediction, setPrediction] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: Number(e.target.value),
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setPrediction("");
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error("Prediction failed");
      }

      const data = await response.json();

      setPrediction(data.prediction);
    } catch (error) {
      console.error(error);
      setError("Unable to connect to the FastAPI server.");
    }

    setLoading(false);
  };

  return (
    <div className="app">

      <div className="card">

        <div className="header">
          <h1>Health Prediction System</h1>

          <p>
            Enter the patient details below
          </p>
        </div>

        <form onSubmit={handleSubmit}>

          <div className="form-grid">

            {fields.map((field) => (

              <div
                className="input-group"
                key={field}
              >

                <label>
                  {field}
                </label>

                <select
                  name={field}
                  value={formData[field]}
                  onChange={handleChange}
                  required
                >

                  <option value="">
                    Select
                  </option>

                  <option value="1">
                    Yes
                  </option>

                  <option value="0">
                    No
                  </option>

                </select>

              </div>

            ))}

          </div>

          <button
            type="submit"
            disabled={loading}
          >

            {loading ? "Predicting..." : "Predict"}

          </button>

        </form>

        {prediction && (

          <div className="result">

            <h2>
              Prediction Result
            </h2>

            <p>
              {prediction}
            </p>

          </div>

        )}

        {error && (

          <div className="result error">

            <p>
              {error}
            </p>

          </div>

        )}

      </div>

    </div>
  );
}

export default App;