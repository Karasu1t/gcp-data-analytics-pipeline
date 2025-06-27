import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import fileio
from apache_beam.io.gcp.bigquery_tools import get_table_schema_from_string
import zipfile
import io
import csv

class ExtractCSVRowsWithFilename(beam.DoFn):
    def process(self, readable_file):
        file_path = readable_file.metadata.path
        with beam.io.filesystems.FileSystems.open(file_path) as f:
            zip_data = f.read()
            with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_file:
                for file_info in zip_file.infolist():
                    if file_info.filename.endswith('.csv'):
                        raw_bytes = zip_file.read(file_info)
                        decoded = raw_bytes.decode('shift_jis')
                        reader = csv.DictReader(decoded.splitlines())
                        table_name = file_info.filename.replace('.csv', '').lower()
                        for row in reader:
                            yield (table_name, row)

# 定数
PROJECT_ID = 'buoyant-sunbeam-461215-p9'
BQ_DATASET = 'analytics_dataset'

# スキーマ定義
SCHEMA_MAP = {
    'passengers': 'datetime:STRING,areacode:STRING,area:STRING,passengers:STRING,other:INTEGER',
    'regularemployee': 'datetime:STRING,areacode:STRING,area:STRING,employee:STRING,other:INTEGER',
    'nonregularemployee': 'datetime:STRING,areacode:STRING,area:STRING,employee:STRING,other:INTEGER',
    'salary': 'datetime:STRING,areacode:STRING,area:STRING,salary:INTEGER,other:STRING',
}

# スキーマとテーブル名を index で扱うために順番固定
TABLE_NAMES = list(SCHEMA_MAP.keys())
TABLE_INDEX = {name: idx for idx, name in enumerate(TABLE_NAMES)}
SCHEMA_OBJECTS = {name: get_table_schema_from_string(schema_str) for name, schema_str in SCHEMA_MAP.items()}

# パーティション関数
def partition_by_table(kv, n_partitions):
    table_name = kv[0]
    return TABLE_INDEX.get(table_name, -1)  # 想定外は -1（省くならフィルタしてもよい）

# パイプラインオプション
options = PipelineOptions(
    project=PROJECT_ID,
    runner='DataflowRunner',
    region='asia-east1',
    temp_location='gs://dev-karasuit-dataflow/temp',
    staging_location='gs://dev-karasuit-dataflow/staging'
)

# パイプライン実行
with beam.Pipeline(options=options) as p:
    extracted = (
        p
        | 'Match ZIP files' >> fileio.MatchFiles('gs://dev-karasuit-etldata/*.zip')
        | 'Read ZIP files' >> fileio.ReadMatches()
        | 'Extract CSV rows + filename' >> beam.ParDo(ExtractCSVRowsWithFilename())
    )

    partitions = extracted | 'Partition by table' >> beam.Partition(partition_by_table, len(TABLE_NAMES))

    for idx, table_name in enumerate(TABLE_NAMES):
        (
            partitions[idx]
            | f'Drop key for {table_name}' >> beam.Map(lambda kv: kv[1])
            | f'Write to BigQuery - {table_name}' >> beam.io.WriteToBigQuery(
                table=f'{PROJECT_ID}:{BQ_DATASET}.{table_name}',
                schema=SCHEMA_OBJECTS[table_name],
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                custom_gcs_temp_location='gs://dev-karasuit-etldata/temp'
            )
        )
