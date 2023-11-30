import csv

from datetime import datetime, timedelta

class ManipulateCsv:
    def __init__(self, file):
        self.reader = None
        self.file = file
        self.date_format = '%Y-%m-%d'

    def process_apl(self):
        with open(self.file, newline='\n', encoding='utf-8') as csv_file:
            self.reader = csv.reader(csv_file)
            self.print_longest_case()


    def print_longest_case(self):
        rtop_sum = timedelta(days=0)
        rtoa_sum = timedelta(days=0)
        atop_sum = timedelta(days=0)
        longest_rtop = timedelta(days=0)
        longest_rtoa = timedelta(days=0)
        longest_atop = timedelta(days=0)

        for row in self.reader:
            duration = self.calculate_duration(row[5], row[7])
            if duration is not None:
                rtop_sum = rtop_sum + duration
            if duration is not None and longest_rtop < duration:
                longest_rtop = duration
                longest_rtop_info = (row[0], row[1], row[2], row[3], row[5], row[6], row[7], longest_rtop.days)

            duration = self.calculate_duration(row[5], row[6])
            if duration is not None:
                rtoa_sum = rtoa_sum + duration
            if duration is not None and longest_rtoa < duration:
                longest_rtoa = duration
                longest_rtoa_info = (row[0], row[1], row[2], row[3], row[5], row[6], row[7], longest_rtoa.days)

            duration = self.calculate_duration(row[6], row[7])
            if duration is not None:
                atop_sum = atop_sum + duration
            if duration is not None and longest_atop < duration:
                longest_atop = duration
                longest_atop_info = (row[0], row[1], row[2], row[3], row[5], row[6], row[7], longest_atop.days)
            if row[1] == '12':
                print(f"{row[0]}/{row[1]}/#{row[2]}, {row[7]} : {row[3]}")

        size = timedelta(days=self.reader.line_num)
        rtop_avg = rtop_sum / size
        rtoa_avg = rtoa_sum / size
        atop_avg = atop_sum / size
        print("")
        print(f"Longest case received to publish: {longest_rtop_info}")
        print(f"Longest case received to accept: {longest_rtoa_info}")
        print(f"Longest case accepted to publish: {longest_atop_info}")
        print("")
        print(f"Average received to publish: {rtop_avg}")
        print(f"Average received to accept: {rtoa_avg}")
        print(f"Average accepted to publish: {atop_avg}")


    def calculate_duration(self, start, end):
        try:
            return self.convert_date_time(end) - self.convert_date_time(start)
        except ValueError:
            return None

    def convert_date_time(self, date):
        return datetime.strptime(date, self.date_format)

if __name__ == '__main__':
    apl_csv = ManipulateCsv('apl_materials.csv')
    apl_csv.process_apl()

