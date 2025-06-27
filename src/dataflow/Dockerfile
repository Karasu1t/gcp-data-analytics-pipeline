FROM gcr.io/dataflow-templates-base/python3-template-launcher-base:latest

WORKDIR /dataflow/template

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY etl.py .

ENV FLEX_TEMPLATE_PYTHON_PY_FILE="etl.py"
ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="requirements.txt"

ENTRYPOINT ["/opt/google/dataflow/python_template_launcher", "--runner=DataflowRunner"]
