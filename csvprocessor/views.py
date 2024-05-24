from django.shortcuts import render
from django.http import HttpResponse
import csv
import io


def home(request):
    return render(request, 'csvprocessor/home.html')


def process_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endwith('.csv'):
            return render(request, 'csvprocessor/error.html', {'error': 'Please upload a .csv file'})

        data = csv_file.read().decode('utf-8')
        io_string = io.StringIO(data)
        reader = csv.reader(io_string)
        header = next(reader)

        sorted_data = sorted(reader, key=lambda row: row[0])

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(header)
        writer.writerows(sorted_data)

        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="processed.csv"'
        return response

    return render(request, 'csvprocessor/home.html')

