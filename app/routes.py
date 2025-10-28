import io
import time
from datetime import datetime
from flask import Blueprint, request, jsonify, send_file, current_app
import pandas as pd
from utils import simulate_validation_row, generate_pdf_report, compute_aggregates

api_bp = Blueprint('api', __name__)
VALIDATED_STORE = []


@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'API running ✅', 'timestamp': datetime.utcnow().isoformat() + 'Z'})


@api_bp.route('/upload', methods=['POST'])
def upload_csv():
    start_time = time.time()
    if 'file' not in request.files:
        return jsonify({'error': "Missing 'file' in request"}), 400

    file = request.files['file']
    try:
        df = pd.read_csv(file)
    except Exception as e:
        current_app.logger.exception('Failed to read CSV')
        return jsonify({'error': 'Invalid CSV file', 'detail': str(e)}), 400

    required = {'Name', 'Phone', 'Address'}
    if not required.issubset(set(df.columns)):
        return jsonify({'error': f'CSV must contain columns: {required}'}), 400

    providers = []
    for _, row in df.iterrows():
        provider_input = {
            'name': str(row.get('Name', '')).strip(),
            'phone': str(row.get('Phone', '')).strip(),
            'address': str(row.get('Address', '')).strip(),
            'specialty': str(row.get('Specialty', '')).strip() if 'Specialty' in df.columns else '',
        }
        validated = simulate_validation_row(provider_input)
        providers.append(validated)
        VALIDATED_STORE.append(validated)

    elapsed = time.time() - start_time
    return jsonify({'providers': providers, 'processing_time_seconds': round(elapsed, 2)})


@api_bp.route('/report', methods=['POST'])
def report_pdf():
    data = request.get_json(force=True, silent=True)
    if not data or 'providers' not in data:
        return jsonify({'error': "Request JSON must include 'providers' list"}), 400

    providers = data['providers']
    aggregates = compute_aggregates(providers)
    pdf_bytes = generate_pdf_report(providers, aggregates)
    pdf_bytes.seek(0)

    now_ts = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    return send_file(pdf_bytes, mimetype='application/pdf', as_attachment=True, download_name=f'provider_report_{now_ts}.pdf')


@api_bp.route('/summary', methods=['GET'])
def summary():
    aggregates = compute_aggregates(VALIDATED_STORE)
    response = {
        'total_validated': len(VALIDATED_STORE),
        'average_confidence': aggregates.get('average_confidence'),
        'counts': aggregates.get('counts'),
        'last_updated': VALIDATED_STORE[-1]['timestamp'] if VALIDATED_STORE else None,
    }
    return jsonify(response)
