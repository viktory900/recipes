from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import xml.etree.ElementTree as ET
from io import BytesIO
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


def index(request):
    theme = request.COOKIES.get('theme', 'light')  # По умолчанию 'light' если куки не установлены
    if request.method == 'POST':
        genre = request.POST.get('genre')
        print(f"Genre selected: {genre}")  # Отладочное сообщение
        if genre == 'comedy':
            return redirect(reverse('comedy'))
        elif genre == 'drama':
            return redirect(reverse('drama'))
        elif genre == 'horror':
            return redirect(reverse('horror'))
    return render(request, 'main/index.html', {'theme': theme})

def comedy(request):
    theme = request.COOKIES.get('theme', 'light')  # По умолчанию 'light' если куки не установлены
    if request.method == 'POST':
        genre = request.POST.get('genre')
        print(f"Genre selected: {genre}")  # Отладочное сообщение
        if genre == 'comedy':
            return redirect(reverse('comedy'))
        elif genre == 'drama':
            return redirect(reverse('drama'))
        elif genre == 'horror':
            return redirect(reverse('horror'))
    return render(request, 'main/comedy.html', {'theme': theme})

def drama(request):
    theme = request.COOKIES.get('theme', 'light')  # По умолчанию 'light' если куки не установлены
    if request.method == 'POST':
        genre = request.POST.get('genre')
        print(f"Genre selected: {genre}")  # Отладочное сообщение
        if genre == 'comedy':
            return redirect(reverse('comedy'))
        elif genre == 'drama':
            return redirect(reverse('drama'))
        elif genre == 'horror':
            return redirect(reverse('horror'))
    return render(request, 'main/drama.html', {'theme': theme})

def horror(request):
    theme = request.COOKIES.get('theme', 'light')  # По умолчанию 'light' если куки не установлены
    if request.method == 'POST':
        genre = request.POST.get('genre')
        print(f"Genre selected: {genre}")  # Отладочное сообщение
        if genre == 'comedy':
            return redirect(reverse('comedy'))
        elif genre == 'drama':
            return redirect(reverse('drama'))
        elif genre == 'horror':
            return redirect(reverse('horror'))
    return render(request, 'main/horror.html', {'theme': theme})

def main_page(request):
    theme = request.COOKIES.get('theme', 'light')  # По умолчанию 'light' если куки не установлены
    return render(request, 'main/index.html', {'theme': theme})

def toggle_theme(request):
    if request.method == 'POST':
        current_theme = request.COOKIES.get('theme', 'light')
        new_theme = 'dark' if current_theme == 'light' else 'light'
        current_path = request.POST.get('current_path', reverse('main_page'))
        response = redirect(current_path)
        response.set_cookie('theme', new_theme, max_age=3600)
        return response
    return redirect(reverse('main_page'))


def form_view(request):
    return render(request, 'main/index.html')

def export_to_xml(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        ingredients = request.POST.get('ingredients').split(',')
        instructions = request.POST.get('instructions')
        cooking_time = request.POST.get('cooking_time')

        root = ET.Element("recipe")
        ET.SubElement(root, "name").text = name
        ingredients_elem = ET.SubElement(root, "ingredients")
        for ingredient in ingredients:
            ET.SubElement(ingredients_elem, "ingredient").text = ingredient.strip()
        ET.SubElement(root, "instructions").text = instructions
        ET.SubElement(root, "cooking_time").text = cooking_time

        tree = ET.ElementTree(root)
        buffer = BytesIO()
        tree.write(buffer, encoding='utf-8', xml_declaration=True)
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename="recipe.xml"'
        return response

@csrf_exempt
def import_from_xml(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'uploads'))
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            data = {
                'name': root.find('name').text,
                'ingredients': [ing.text for ing in root.find('ingredients').findall('ingredient')],
                'instructions': root.find('instructions').text,
                'cooking_time': root.find('cooking_time').text
            }

            return render(request, 'main/index.html', {'data': data})
        except ET.ParseError:
            fs.delete(filename)
            return HttpResponse("Invalid XML file", status=400)

def list_files(request):
    folder_path = os.path.join(settings.BASE_DIR, 'uploads')
    files = os.listdir(folder_path)
    file_contents = []

    for file in files:
        file_path = os.path.join(folder_path, file)
        if file.endswith('.xml'):
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
                data = {
                    'name': root.find('name').text,
                    'ingredients': [ing.text for ing in root.find('ingredients').findall('ingredient')],
                    'instructions': root.find('instructions').text,
                    'cooking_time': root.find('cooking_time').text
                }
                file_contents.append({'filename': file, 'content': data})
            except ET.ParseError:
                continue

    if not file_contents:
        return HttpResponse("No files found")
    return render(request, 'myapp/file_list.html', {'files': file_contents})