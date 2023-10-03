from datetime import datetime

class SQLQuery:

    def __init__(self, vis_group_by_type, vis_aggregate_type, vis_time_period):
        self.vis_group_by_type = vis_group_by_type
        self.vis_aggregate_type = vis_aggregate_type
        self.vis_time_period = vis_time_period

    def get_date_range(self):
        start_date, end_date = self.vis_time_period.split(' to ')
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        return start_date, end_date
    
    def choose_grouping_strategy(self, start_date, end_date):
        interval_length = (end_date - start_date).days
        
        if interval_length <= 7:  
            return 'day'
        elif interval_length <= 30:  
            return 'week'
        elif interval_length <= 365: 
            return 'month'
        else:
            return 'year'
        
    def get_aggregate_type(self):
        aggregate_lookup = {"minimum": "MIN", "maximum": "MAX", "sum": "SUM", "average": "AVG"}
        return aggregate_lookup[self.vis_aggregate_type]
    
    def create(self):
        start_date, end_date = self.get_date_range()
        aggregate_type = self.get_aggregate_type()
        
        if self.vis_group_by_type == "category" or self.vis_group_by_type == "categories":
            sql_query = f"SELECT category, {aggregate_type}(amount) as {self.vis_aggregate_type}_amount FROM expense where date >= '{start_date.strftime('%Y-%m-%d')}' and date <= '{end_date.strftime('%Y-%m-%d')}' GROUP BY category"
        else:
            grouping_strategy = self.choose_grouping_strategy(start_date, end_date)
            if grouping_strategy == "week":
                sql_query = f"SELECT CONCAT('Week of ', MIN(date)) AS Week, {aggregate_type}(amount) as {self.vis_aggregate_type}_amount FROM expense where date >= '{start_date.strftime('%Y-%m-%d')}' and date <= '{end_date.strftime('%Y-%m-%d')}' GROUP BY DATEPART(WEEK, date)"
            elif grouping_strategy == "day":
                sql_query = f"SELECT date, {aggregate_type}(amount) as {self.vis_aggregate_type}_amount FROM expense where date >= '{start_date.strftime('%Y-%m-%d')}' and date <= '{end_date.strftime('%Y-%m-%d')}' GROUP BY date"
            elif grouping_strategy == "month":
                sql_query = f"SELECT DateName( month , DateAdd( month , DATEPART(MONTH, date) , -1 )) as Month, {aggregate_type}(amount) as {self.vis_aggregate_type}_amount FROM expense where date >= '{start_date.strftime('%Y-%m-%d')}' and date <= '{end_date.strftime('%Y-%m-%d')}' GROUP BY DATEPART(MONTH, date)"
            else:
                sql_query = f"SELECT DATEPART(YEAR, date) as Year, {aggregate_type}(amount) as {self.vis_aggregate_type}_amount FROM expense where date >= '{start_date.strftime('%Y-%m-%d')}' and date <= '{end_date.strftime('%Y-%m-%d')}' GROUP BY DATEPART(YEAR, date)"
        return sql_query