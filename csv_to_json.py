import pandas as pd
import json
from flask import Flask, request, render_template_string
import io

app = Flask(__name__)

HTML_FORM = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CSV to Nested JSON</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/json-viewer-js@1.0.0/dist/json-viewer.min.js"></script>
  <link href="https://cdn.jsdelivr.net/npm/json-viewer-js@1.0.0/dist/json-viewer.min.css" rel="stylesheet">
  <style>
    #json-renderer { background: #f8f9fa; padding: 1em; border-radius: 8px; }
    .spinner-border { display: none; }
    .preview-table th, .preview-table td { font-size: 0.95em; }
    #json-raw { background: #f8f9fa; padding: 1em; border-radius: 8px; font-size: 0.95em; }
  </style>
</head>
<body class="bg-light">
<div class="container py-5">
  <h2 class="mb-4">CSV to Nested JSON Converter</h2>
  <form method="post" enctype="multipart/form-data" id="csv-form" class="mb-4">
    <div class="mb-3">
      <input type="file" class="form-control" name="csvfile" required>
    </div>
    <button type="submit" class="btn btn-primary">Upload & Convert</button>
    <div class="spinner-border text-primary ms-3" role="status" id="loading-spinner">
      <span class="visually-hidden">Loading...</span>
    </div>
  </form>
  {% if error %}
    <div class="alert alert-danger">{{ error }}</div>
  {% endif %}
  {% if preview_html %}
    <h5>CSV Preview (first 5 rows):</h5>
    <div class="table-responsive mb-4">{{ preview_html|safe }}</div>
  {% endif %}
  {% if json_data %}
    <div class="mb-3">
      <button class="btn btn-success" id="download-json">Download JSON</button>
    </div>
    <h5>JSON Preview:</h5>
    <div id="json-renderer"></div>
    <h6 class="mt-3">Raw JSON:</h6>
    <pre id="json-raw">{{ json_data }}</pre>
    <textarea id="json-text" class="d-none">{{ json_data }}</textarea>
  {% endif %}
</div>
<script>
  $(function() {
    $('#csv-form').on('submit', function() {
      $('#loading-spinner').show();
    });
    {% if json_data %}
      var json = JSON.parse($('#json-text').val());
      new JSONViewer({ collapsed: false }).showJSON(json, document.getElementById('json-renderer'));
      $(document).off('click', '#download-json').on('click', '#download-json', function() {
        var blob = new Blob([JSON.stringify(json, null, 2)], {type: 'application/json'});
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = 'result.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      });
    {% endif %}
  });
</script>
</body>
</html>
'''

def parse_nested_csv(df):
    df = df.dropna(how='all')
    header_mask = pd.Series(~df.iloc[:,0].isna() & (df.iloc[:,0] != ''))
    if not header_mask.any():
        raise ValueError("No header row found in the CSV.")
    headers = df[header_mask].iloc[0].tolist()
    csv_buffer = io.StringIO(df.to_csv(index=False, header=False))
    df = pd.read_csv(csv_buffer, names=headers)
    parents = []
    current_parent = None
    for _, row in df.iterrows():
        if all(pd.isna(row)):
            continue
        # Use .iloc[0] for position-based access
        first_col = row.iloc[0]
        if not (isinstance(first_col, float) and pd.isna(first_col)) and first_col != '':
            current_parent = row.to_dict()
            current_parent['subRows'] = []
            parents.append(current_parent)
        else:
            if current_parent is not None:
                sub_row = row.to_dict()
                current_parent['subRows'].append(sub_row)
    return parents, df

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    json_data = None
    error = None
    preview_html = None
    if request.method == 'POST':
        file = request.files['csvfile']
        try:
            if file:
                df = pd.read_csv(file.stream, header=None)
                nested, preview_df = parse_nested_csv(df)
                json_data = json.dumps(nested, indent=2)
                # Show preview of first 5 rows (excluding subRows column)
                preview_html = preview_df.head(5).drop(columns=[col for col in preview_df.columns if col == 'subRows'], errors='ignore').to_html(classes='table table-bordered preview-table', index=False)
        except Exception as e:
            error = f"Error: {str(e)}"
    return render_template_string(HTML_FORM, json_data=json_data, error=error, preview_html=preview_html)

if __name__ == '__main__':
    app.run(debug=True)
