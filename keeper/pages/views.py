import json
import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import resolve, reverse_lazy
from django.views.generic import TemplateView, FormView

from .forms import KeeperFolderForm
from .models import *


def get_directory_structure_old(path):
    """Возвращает структуру директории path."""
    structure = {}
    items = sorted(os.listdir(path))  # сортируем для удобочитаемости
    for item in items:
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):  # проверяем, папка это или файл
            children = get_directory_structure(full_path)  # рекурсивно получаем подпапки
            structure[item] = children
        elif os.path.isfile(full_path):
            structure[item] = {}  # обозначаем файл пустой структурой
    return structure


def get_directory_size(directory):
    """
    Возвращает суммарный размер всех файлов в указанной директории.
    """
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(file_path)
            except OSError as e:
                print(f'Ошибка при обработке файла "{filename}": {e}')
    return total_size


def get_directory_structure(path):
    """
    Возвращает структуру директории path вместе с размерами файлов и общим размером папок.
    """
    structure = {}
    items = sorted(os.listdir(path))

    for item in items:
        full_path = os.path.join(path, item)

        if os.path.isdir(full_path):
            # Рекурсивно собираем информацию о подпапках
            children = get_directory_structure(full_path)

            # Вычисляем суммарный размер текущей папки
            directory_size = get_directory_size(full_path)
            structure[item] = {"children": children, "total_size_bytes": directory_size}

        elif os.path.isfile(full_path):
            # Получаем размер текущего файла
            file_size = os.path.getsize(full_path)
            structure[item] = {"size_bytes": file_size}

    return structure


class KeeperBasic(TemplateView):
    extra_context = {
        'title': 'Хранитель резервных копий',
        'header': 'Хранитель резервных копий',
    }

    def is_in_group(self, group_name):
        return self.request.user.groups.filter(name=group_name).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем имя текущего маршрута
        resolved_url = resolve(self.request.path)
        context['current_urlname'] = resolved_url.url_name

        return context


class KeeperMainPage(KeeperBasic):
    template_name = 'pages/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем имя текущего маршрута
        resolved_url = resolve(self.request.path)
        context['current_urlname'] = resolved_url.url_name

        context['all_keeper_objects'] = KeeperObject.objects.all()

        return context


def get_keeper_object(request):
    if request.method == 'GET':
        one_keeper = KeeperObject.objects.get(name=request.GET['search_object'])
        path = ''
        base_dir = one_keeper.path_dir + path.strip('/')
        root_total_size = get_directory_size(base_dir)
        try:
            structure = get_directory_structure(base_dir)
        except OSError as e:
            structure = str(e)
        return render(request, 'pages/one-keeper-object.html',
                      {'structure': structure,
                       'keeper_object_folder': os.path.basename(one_keeper.path_dir),
                       'root_total_size': root_total_size,
                       'show_dir_sizes': one_keeper.display_settings.dirs_size,
                       'show_subdirs': one_keeper.display_settings.subdirs_show,
                       'show_files': one_keeper.display_settings.files_show,
                       'show_file_sizes': one_keeper.display_settings.files_sizes,
                       })


class KeeperEditorPage(KeeperBasic, FormView):
    template_name = 'pages/editor.html'
    form_class = KeeperFolderForm
    success_url = reverse_lazy('editor')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем имя текущего маршрута
        resolved_url = resolve(self.request.path)
        context['current_urlname'] = resolved_url.url_name

        context['folder_exist'] = True
        context['already_in_keeper'] = False
        context['based_types'] = KeeperObjectBasedType.objects.all().order_by('id')
        context['keeper_objects'] = KeeperObject.objects.all().order_by('name')

        return context


def check_is_folder_exist(request):
    search_folder = request.GET['search_folder']
    full_path = settings.BASE_PATH + search_folder
    exists_os = os.path.exists(full_path)
    if not KeeperObject.objects.filter(path_dir=full_path).exists():
        return render(request, 'pages/folder-editor.html',
                      {'folder_exist': exists_os,
                       'already_in_keeper': False,
                       'based_types': KeeperObjectBasedType.objects.all().order_by('id'),
                       'full_path': full_path,
                       })
    else:
        return render(request, 'pages/folder-editor.html',
                      {'folder_exist': exists_os,
                       'already_in_keeper': True,
                       'based_types': KeeperObjectBasedType.objects.all().order_by('id'),
                       'full_path': full_path,
                       })

def add_object_in_keeper(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        based_object = KeeperObjectBasedType.objects.get(id=data.get('based_type'))
        if not data.get('changeable'):
            KeeperObject(name=data.get('name_object'),
                         path_dir=data.get('full_path'),
                         based_type=based_object,
                         option=data.get('changeable'),
                         display_settings=based_object.display_settings,
                         rotate_settings=based_object.rotate_settings,
                         ).save()
        return JsonResponse({'success': True,
                             })
    else:
        return JsonResponse({'success': False,
                             })

class KeeperTypePage(KeeperBasic):
    template_name = 'pages/type-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем имя текущего маршрута
        resolved_url = resolve(self.request.path)
        context['current_urlname'] = resolved_url.url_name

        context['based_types'] = KeeperObjectBasedType.objects.all().order_by('id')
        context['keeper_objects'] = KeeperObject.objects.all().order_by('name')

        return context