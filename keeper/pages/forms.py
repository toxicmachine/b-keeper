from django import forms


class KeeperFolderForm(forms.Form):
    keeper_root_field = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control me-2',
                                                                      'placeholder': 'Поиск осуществляется в каталоге /home/backup-user/ , поэтому укажите путь относительно данного каталога...',
                                                                      'autofocus': 'true',
                                                                      'id': 'search_input',
                                                                      'required': 'True',
                                                                      }),
                                          max_length=200,
                                          label=False,
                                          required=False,)