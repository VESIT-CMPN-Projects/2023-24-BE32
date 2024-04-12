import csv
import pandas as pd
from django.core.management.base import BaseCommand
from dashboard.models import PollingData
from dashboard.models import History

class Command(BaseCommand):
    help = 'Imports data from CSV files'

    def handle(self, *args, **options):
        # Import PollingData
        csv_file_path_polling = 'C:/Users/Admin/OneDrive/Desktop/be-project/project/data/pollsfinal.csv'
        try:
            with open(csv_file_path_polling, 'r') as file:
                reader = csv.DictReader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    # Handling empty values
                    for key, value in row.items():
                        if not value:
                            row[key] = None  # Replace empty string with None

                    # Create PollingData object without specifying id
                    PollingData.objects.create(
                        state=row['State'],
                        polling_station=row['Station'],
                        gmen=row['GMEN'] or 0,  # Provide default value if empty
                        gwomen=row['GWOMEN'] or 0,
                        gthird=row['GTHIRD'] or 0,
                        gtotal=row['GTOTAL'] or 0,  # Provide default value if empty
                        omen=row['OMEN'] or 0,
                        owomen=row['OWOMEN'] or 0,
                        othird=row['OTHIRD'] or 0,
                        ototal=row['OTOTAL'] or 0,
                        smen=row['SMEN'] or 0,
                        swomen=row['SWOMEN'] or 0,
                        stotal=row['STOTAL'] or 0,
                        overall_total=row['TOTAL'] or 0
                    )
            self.stdout.write(self.style.SUCCESS('PollingData imported successfully'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('CSV file not found at the specified path for PollingData.'))

        # Import History
        csv_file_path_history = 'C:/Users/Admin/OneDrive/Desktop/be-project/project/data/Loksabha_1962-2019 .csv'
        try:
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(csv_file_path_history)

            # Iterate over each row in the DataFrame and create ElectionResult objects
            for index, row in df.iterrows():
                # Add error handling for converting 'electors' to int
                try:
                    electors_value = int(row['electors'].replace(',', '')) if row['electors'] != '-' else None
                except ValueError:
                    # Handle the case where conversion to int fails
                    print(f"Error: Invalid value for 'electors' on row {index}: {row['electors']}")
                    continue  # Skip this row and move to the next one

                # Add error handling for converting 'votes' to int
                try:
                    votes_value = int(row['votes'].replace(',', ''))
                except ValueError:
                    # Handle the case where conversion to int fails
                    print(f"Error: Invalid value for 'votes' on row {index}: {row['votes']}")
                    continue  # Skip this row and move to the next one

                # Add error handling for converting 'Turnout' to float
                try:
                    turnout_value = float(row['Turnout'].rstrip('%'))
                except ValueError:
                    # Handle the case where conversion to float fails
                    print(f"Error: Invalid value for 'Turnout' on row {index}: {row['Turnout']}")
                    continue  # Skip this row and move to the next one

                # Add error handling for converting 'margin' to int
                try:
                    margin_value = int(row['margin'].replace(',', ''))
                except ValueError:
                    # Handle the case where conversion to int fails
                    print(f"Error: Invalid value for 'margin' on row {index}: {row['margin']}")
                    continue  # Skip this row and move to the next one

                # Add error handling for converting 'Margin%' to float
                try:
                    marginp_value = float(row['margin%'].rstrip('%'))
                except ValueError:
                    # Handle the case where conversion to float fails
                    print(f"Error: Invalid value for 'Margin%' on row {index}: {row['margin%']}")
                    marginp_value = None  # Assign None when value is invalid

                # Create History object
                History.objects.create(
                    pc_name=row['Pc_name'],
                    no=row['no'],
                    type=row['type'],
                    state=row['state'],
                    candidate_name=row['candidate_name'],
                    party=row['party'],
                    electors=electors_value,
                    votes=votes_value,
                    turnout=turnout_value,
                    margin=margin_value,
                    margin_percentage=marginp_value,
                    year=row['year']
                )

            self.stdout.write(self.style.SUCCESS('History imported successfully'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('CSV file not found at the specified path for History.'))
