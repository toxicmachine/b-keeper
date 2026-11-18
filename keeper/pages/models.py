from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import ForeignKey


class KeeperVersionChoice(models.Model):
    class Meta:
        verbose_name = 'Тип версии настроек'
        verbose_name_plural = 'Типы версии настроек'

    title = models.CharField(max_length=30,
                             verbose_name="Тип версии настроек",
                             unique=True,
                             )

    def __str__(self):
        return self.title

class KeeperRotateDay(models.Model):
    class Meta:
        verbose_name = 'Период ротации'
        verbose_name_plural = 'Периоды ротации'

    title = models.CharField(max_length=60,
                             verbose_name="Название периода",
                             default='Пустое имя',
                             unique=True,
                             )
    period = models.PositiveSmallIntegerField(verbose_name="Количество дней в периоде",
                                              validators=[
                                                  MinValueValidator(1),
                                                  MaxValueValidator(365)
                                              ]
                                              )

    def __str__(self):
        return self.title


class KeeperRotateSetting(models.Model):
    class Meta:
        verbose_name = 'Настройка ротации'
        verbose_name_plural = 'Настройки ротации'

    title = models.CharField(max_length=60,
                             verbose_name="Название настроек ротации",
                             unique=True,
                             )
    version = ForeignKey(KeeperVersionChoice,
                         on_delete=models.PROTECT,
                         verbose_name="Тип настроек",
                         )
    rotate_count_possible = models.BooleanField(verbose_name="Возможность ротации по количеству файлов")
    rotate_count = models.PositiveSmallIntegerField(verbose_name="Количество дней в периоде",
                                                    validators=[
                                                        MinValueValidator(1),
                                                        MaxValueValidator(1000)
                                                    ],
                                                    null=True,
                                                    blank=True,
                                                    )
    rotate_days_possible = models.BooleanField(verbose_name="Возможность ротации по периоду")
    rotate_days = ForeignKey(KeeperRotateDay, on_delete=models.PROTECT,
                             null=True,
                             blank=True,
                             )

    def __str__(self):
        return self.title


class KeeperDisplaySetting(models.Model):
    class Meta:
        verbose_name = 'Настройка отображения'
        verbose_name_plural = 'Настройки отображения'

    title = models.CharField(max_length=60,
                             verbose_name="Название настроек отображения",
                             unique=True,
                             )
    version = ForeignKey(KeeperVersionChoice,
                         on_delete=models.PROTECT,
                         verbose_name="Тип настроек",
                         )
    dirs_size = models.BooleanField(verbose_name="Отображать размер каталогов",
                               default=True,
                               )
    subdirs_show = models.BooleanField(verbose_name="Отображать подкаталоги",
                                       default=True,
                                       )
    files_show = models.BooleanField(verbose_name="Отображать файлы",
                                     default=True,
                                     )
    files_sizes = models.BooleanField(verbose_name="Отображать размеры файлов",
                                      default=True,
                                      )

    def __str__(self):
        return self.title


class KeeperObjectBasedType(models.Model):
    class Meta:
        verbose_name = 'Базовый тип объекта'
        verbose_name_plural = 'Базовые типы объекта'

    title = models.CharField(max_length=60,
                             verbose_name="Название типа объекта",
                             unique=True,
                             )
    display_settings = ForeignKey(KeeperDisplaySetting,
                                  on_delete=models.PROTECT,
                                  )
    rotate_settings = ForeignKey(KeeperRotateSetting,
                                 on_delete=models.PROTECT,)
    changeable = models.BooleanField(verbose_name="Может ли быть изменяемым",
                                     default=False,
                                     )

    def __str__(self):
        return self.title


class KeeperObject(models.Model):
    class Meta:
        verbose_name = 'Объект хранилища'
        verbose_name_plural = 'Объекты хранилища'

    name = models.CharField(max_length=30,
                             verbose_name="Название настроек объекта хранилища",
                             unique=True,
                             )
    path_dir = models.CharField(max_length=200,
                                verbose_name="Абсолютный путь до каталога",
                                unique=True,
                                )
    based_type = models.ForeignKey(KeeperObjectBasedType,
                                   on_delete=models.PROTECT,
                                   verbose_name="Базовый тип",
                                   default=1,
                                   )
    option = models.BooleanField(verbose_name="Изменяемый/Неизменяемый",
                                 default=True,
                                 )
    display_settings = ForeignKey(KeeperDisplaySetting,
                                  on_delete=models.PROTECT,
                                  verbose_name="Настройка отображения",
                                  default=1,
                                  )
    rotate_settings = ForeignKey(KeeperRotateSetting,
                                 on_delete=models.PROTECT,
                                 verbose_name="Настройка ротации",
                                 default=1,
                                 )

    def __str__(self):
        return self.name
