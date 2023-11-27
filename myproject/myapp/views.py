import os
import csv
import shutil
import zipfile
from django.shortcuts import render, redirect, get_object_or_404
from myapp.models import GeneratedFile  # Import your GeneratedFile model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
steps = []
set_of_steps = []

def filter_nested_list(data, search_element):
    filtered_list = [sub_list for sub_list in data if sub_list[0] == search_element]
    return filtered_list


def pagenumberorder(example):      
        page_mapping = {}
        current_page = 1

        for row in example[1:]:
            page_no = row[0]
            if page_no not in page_mapping:
                page_mapping[page_no] = str(current_page)
                current_page += 1

        # Update the page numbers in the 'example' list
        for row in example[1:]:
            row[0] = page_mapping[row[0]]

        return example

def jumble(file_path, iterations,set_of_steps):
        csv_file_path = file_path

        data_list = []  # to store data from CSV
        temp_data_list = []
        jumbled_data_list = []  # to store new jumbled list

        with open(csv_file_path, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                data_list.append(row)

        data_list.pop(0)

        for i in range(iterations):
            steps = set_of_steps[i]
            for j in steps:
                temp_data_list = filter_nested_list(data_list, j)
                for line in temp_data_list:
                    jumbled_data_list.append(line)
                data_list = [line for line in data_list if line[0] != j]

            jumbled_data_list.extend(data_list)
            data_list = jumbled_data_list
            jumbled_data_list = []

        

        data_list.insert(0,["Page No.","Q#","Key"])

        data_list = pagenumberorder(data_list)

        return data_list

def handle_uploaded_file(uploaded_file):
    upload_dir = 'uploads'
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, uploaded_file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return file_path

@login_required
def home(request):
    generated_files = GeneratedFile.objects.all()  # Fetch all generated files from the database
    return render(request, 'myapp/home.html', {'generated_files': generated_files})

def extractname(inputname):
    i = inputname.index("csv")
    return inputname[:i-1]


@login_required
def process_csv(request):
    if request.method == 'POST':
        iterations = int(request.POST.get('iterations', 0))
        set_of_steps = []

        for i in range(iterations):
            order = request.POST.get(f'steps_{i}', '')
            steps = order.split(',')
            set_of_steps.append(steps)

        uploaded_file = request.FILES.get('csv_file', None)
        name = uploaded_file.name
        name = extractname(name)
        if uploaded_file:
            copies = int(request.POST.get('copies', 1))
            zip_filename = f'{name}s.zip'
            zip_filepath = os.path.join('uploads', zip_filename)

            with zipfile.ZipFile(zip_filepath, 'w') as zip_file:
                input_file_path = handle_uploaded_file(uploaded_file)

                for copy in range(copies):
                    # Create a unique output file for each copy
                    output_filename = f'{name}_{chr((copy + 1)+65)}.csv'
                    output_filepath = os.path.join('uploads', output_filename)

                    datalist = jumble(input_file_path, iterations, set_of_steps)

                    with open(output_filepath, 'w', newline='') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        for row in datalist:
                            csv_writer.writerow(row)

                    generated_file = GeneratedFile(name=output_filename, file=output_filepath)
                    generated_file.save()
                    zip_file.write(output_filepath, arcname=output_filename)

                    # Set the output file as the input for the next copy
                    input_file_path = output_filepath

                # Remove the temporary input file after creating the zip archive
                os.remove(input_file_path)

            # Remove the temporary output files
            for copy in range(copies):
                output_filepath = os.path.join('uploads', f'jumbled_key_{copy + 1}.csv')
                try:
                    os.remove(output_filepath)
                except FileNotFoundError:
                    pass  # Ignore if the file is not found

            with open(zip_filepath, 'rb') as zip_file:
                response = HttpResponse(zip_file.read(), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename={zip_filename}'

            # Remove the zip file after creating the response
            os.remove(zip_filepath)

            return response

    return render(request, 'myapp/process_csv.html')


@login_required
def download_file(request, file_id):
    generated_file = get_object_or_404(GeneratedFile, id=file_id)

    response = HttpResponse(generated_file.file.read(), content_type='application/csv')
    response['Content-Disposition'] = f'attachment; filename={generated_file.name}'
    return response


@login_required
def view_database(request):
    generated_files = GeneratedFile.objects.all()
    return render(request, 'myapp/view_database.html', {'generated_files': generated_files})


@login_required
def delete_file(request, file_id):
    generated_file = get_object_or_404(GeneratedFile, id=file_id)
    generated_file.delete()
    return redirect('view_database')