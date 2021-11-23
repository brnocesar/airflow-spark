from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class TwitterOperator(BaseOperator):
    @apply_defaults
    def __init__(self, query, conn_id=None, start_time=None, end_time=None, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.query = query
        self.conn_id = conn_id or "twitter_default"
        self.start_time = start_time
        self.end_time = end_time
    
    def execute(self, context):
        pass