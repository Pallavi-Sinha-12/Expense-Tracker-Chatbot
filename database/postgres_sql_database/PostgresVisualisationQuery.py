from database.VisualisationQuery import VisualisationQuery

class PostgresVisualisationQuery(VisualisationQuery):

    def __init__(self, vis_group_by_type, vis_aggregate_type, vis_time_period):
        super().__init__(vis_group_by_type, vis_aggregate_type, vis_time_period)

    def get_date_range(self):
        return super().get_date_range()
    
    def get_aggregate_type(self):
        return super().get_aggregate_type()
    
    def choose_grouping_strategy(self, start_date, end_date):
        return super().choose_grouping_strategy(start_date, end_date)

    def create(self):
        start_date, end_date = self.get_date_range()
        aggregate_type = self.get_aggregate_type()
        
        if self.vis_group_by_type == "category" or self.vis_group_by_type == "categories":
            sql_query = f"SELECT category, {aggregate_type}(amount) as {self.vis_aggregate_type}_amount FROM tracker.expense where date >= '{start_date.strftime('%Y-%m-%d')}' and date <= '{end_date.strftime('%Y-%m-%d')}' GROUP BY category"
        else:
            grouping_strategy = self.choose_grouping_strategy(start_date, end_date)
            if grouping_strategy == "week":
                sql_query = f"SELECT 'Week of ' || MIN(date) AS Week, {aggregate_type}(amount) as {self.vis_aggregate_type}_amount FROM tracker.expense where date >= '{start_date.strftime('%Y-%m-%d')}' and date <= '{end_date.strftime('%Y-%m-%d')}' GROUP BY EXTRACT(WEEK FROM date)"
            elif grouping_strategy == "day":
                sql_query = f"SELECT date, {aggregate_type}(amount) as {self.vis_aggregate_type}_amount FROM tracker.expense where date >= '{start_date.strftime('%Y-%m-%d')}' and date <= '{end_date.strftime('%Y-%m-%d')}' GROUP BY date"
            elif grouping_strategy == "month":
                sql_query = f"SELECT TO_CHAR(date, 'Month') as Month, {aggregate_type}(amount) as {self.vis_aggregate_type}_amount FROM tracker.expense where date >= '{start_date.strftime('%Y-%m-%d')}' and date <= '{end_date.strftime('%Y-%m-%d')}' GROUP BY Month"
            else:
                sql_query = f"SELECT EXTRACT(YEAR FROM date) as Year, {aggregate_type}(amount) as {self.vis_aggregate_type}_amount FROM tracker.expense where date >= '{start_date.strftime('%Y-%m-%d')}' and date <= '{end_date.strftime('%Y-%m-%d')}' GROUP BY EXTRACT(YEAR FROM date)"
        return sql_query