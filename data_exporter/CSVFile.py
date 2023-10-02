import csv
import uuid

class CSVFile:

    def __init__(self, data, column_list):
        self.data = data
        self.column_list = column_list

    def generate_random_file_name(self):
        return str(uuid.uuid4()) + ".csv"
    
    def get_csv_file_path(self):
        csv_file_path = f"data_exporter/exports/{self.generate_random_file_name()}"
        return csv_file_path
    
    def write(self):
        csv_file_path = self.get_csv_file_path()
        with open(csv_file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.column_list)
            writer.writerows(self.data)

        return csv_file_path