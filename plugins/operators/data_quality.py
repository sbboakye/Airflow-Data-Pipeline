from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 tables=[],
                 *args, **kwargs):
        """
        :param redshift_conn_id:
        :param tables: table name
        :param args:
        :param kwargs:
        """

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.tables = tables
        self.redshift_conn_id = redshift_conn_id

    def execute(self, context):
        redshift = PostgresHook(self.redshift_conn_id)

        for table, _ in self.tables:
            records = redshift.get_records(f"SELECT COUNT(*) FROM {table}")

            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError(f"{table} is empty. Data Quality check failed.")

            num_records = records[0][0]

            if num_records < 1:
                raise ValueError(f"{table} is empty. Data Quality check failed.")

            self.log.info(f"Data Quality check successful. {table} has {num_records} of records")
