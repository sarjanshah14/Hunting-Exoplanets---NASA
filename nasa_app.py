from flask import Flask, render_template_string, request, jsonify
from prediction_engine import ExoplanetPredictor
import os
import traceback

# Initialize Flask app
app = Flask(__name__)
predictor = ExoplanetPredictor()

# ------------------ HTML FRONTEND TEMPLATE ------------------
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>NASA Exoplanet Classifier</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background: #0b3d91; color: white; }
        .container { max-width: 720px; margin: auto; background: #1a237e; padding: 25px; border-radius: 12px; box-shadow: 0 0 20px rgba(0,0,0,0.4); }
        h1 { color: #ff6d00; text-align: center; margin-bottom: 10px; }
        p { text-align: center; margin-bottom: 25px; color: #eee; }
        .form-group { margin: 12px 0; }
        label { display: block; margin-bottom: 4px; font-weight: bold; }
        input { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; }
        button { background: #ff6d00; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; margin-top: 20px; width: 100%; transition: 0.3s; }
        button:hover { background: #ff8f00; }
        .result { margin-top: 25px; padding: 15px; border-radius: 6px; display: none; }
        .confirmed { background: #4caf50; }
        .candidate { background: #ff9800; }
        .false-positive { background: #f44336; }
        .error { background: #d32f2f; }
        h3 { margin-top: 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔭 NASA Exoplanet Classifier</h1>
        <p>Enter observed planetary features to predict if it’s a confirmed exoplanet, candidate, or false positive.</p>
        
        <form id="predictionForm">
            <div class="form-group"><label>NASA Confidence Score (0–1):</label>
                <input type="number" name="koi_score" step="0.01" min="0" max="1" value="0.95" required>
            </div>

            <div class="form-group"><label>Signal-to-Noise Ratio:</label>
                <input type="number" name="koi_model_snr" step="0.1" min="0" value="30.5" required>
            </div>

            <div class="form-group"><label>Transit Depth (ppm):</label>
                <input type="number" name="koi_depth" step="1" min="0" value="1200" required>
            </div>

            <div class="form-group"><label>Orbital Period (days):</label>
                <input type="number" name="koi_period" step="0.1" min="0" value="365.2" required>
            </div>

            <div class="form-group"><label>Transit Duration (hours):</label>
                <input type="number" name="koi_duration" step="0.1" min="0" value="8.0" required>
            </div>

            <div class="form-group"><label>Planet Radius (Earth radii):</label>
                <input type="number" name="koi_prad" step="0.1" min="0" value="1.2" required>
            </div>

            <div class="form-group"><label>Planet Temperature (K):</label>
                <input type="number" name="koi_teq" step="1" min="0" value="280" required>
            </div>

            <div class="form-group"><label>Not Transit Flag (0 or 1):</label>
                <input type="number" name="koi_fpflag_nt" min="0" max="1" value="0" required>
            </div>

            <div class="form-group"><label>Stellar Eclipse Flag (0 or 1):</label>
                <input type="number" name="koi_fpflag_ss" min="0" max="1" value="0" required>
            </div>

            <div class="form-group"><label>Centroid Offset Flag (0 or 1):</label>
                <input type="number" name="koi_fpflag_co" min="0" max="1" value="0" required>
            </div>

            <div class="form-group"><label>Ephemeris Match Flag (0 or 1):</label>
                <input type="number" name="koi_fpflag_ec" min="0" max="1" value="0" required>
            </div>

            <button type="submit">🚀 Classify Exoplanet</button>
        </form>
        
        <div id="result" class="result"></div>
    </div>

    <script>
        document.getElementById('predictionForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const data = {};
            formData.forEach((v, k) => data[k] = parseFloat(v));
            
            // Fill missing features with safe defaults
            Object.assign(data, {
                koi_impact: 0.1,
                koi_sma: 1.0,
                koi_ror: 0.008,
                koi_slogg: 4.44,
                koi_steff: 5700
            });

            fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
            .then(res => res.json())
            .then(displayResult)
            .catch(err => {
                const div = document.getElementById('result');
                div.innerHTML = '<div class="error"><h3>❌ Error</h3><p>' + err + '</p></div>';
                div.style.display = 'block';
            });
        });

        function displayResult(result) {
            const div = document.getElementById('result');
            let html = '<h2>🎯 CLASSIFICATION RESULT</h2>';
            
            if (result.status === 'error') {
                html += '<div class="error"><h3>❌ Prediction Error</h3><p>' + (result.error || 'Unknown issue') + '</p></div>';
                div.innerHTML = html;
                div.style.display = 'block';
                return;
            }

            if (result.prediction === 'CONFIRMED') html += '<div class="confirmed"><h3>✅ CONFIRMED PLANET</h3>';
            else if (result.prediction === 'CANDIDATE') html += '<div class="candidate"><h3>⏳ CANDIDATE PLANET</h3>';
            else html += '<div class="false-positive"><h3>❌ FALSE POSITIVE</h3>';

            html += `<p><strong>Confidence: ${(result.confidence * 100).toFixed(1)}%</strong></p><ul>`;
            for (const [k, v] of Object.entries(result.probabilities)) {
                html += `<li>${k}: ${(v * 100).toFixed(1)}%</li>`;
            }
            html += '</ul></div>';
            div.innerHTML = html;
            div.style.display = 'block';
        }
    </script>
</body>
</html>
'''

# ------------------ FLASK ROUTES ------------------

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.get_json()
        print("📡 Received prediction request with", len(input_data), "features")
        print("Features:", list(input_data.keys()))

        result = predictor.predict(input_data)
        print("🎯 Prediction result:", result)
        return jsonify(result)

    except Exception as e:
        print("❌ Prediction error:", e)
        traceback.print_exc()
        return jsonify({"error": str(e), "status": "error"}), 500


# ------------------ APP ENTRY ------------------

if __name__ == '__main__':
    print("🚀 NASA Exoplanet Classifier is live!")
    print("🌐 Open your browser and go to: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
