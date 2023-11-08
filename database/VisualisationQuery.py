from datetime import datetime

class VisualisationQuery:

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
        pass