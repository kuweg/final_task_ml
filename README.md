# Real Estate price visualization
## Описание

Текущий репозиторий содержит финальное задание курса EPAM Python Basic.
В рамках него было разработан и реализован скрипт для сбора и визуализации 
цен на недвижимость.

## Описание задачи
1. Собрать базу данных цен на недвижимость по названию города
2. На основе собранных данных сделать следующие виды визуализации:
    - Тепловая карта цен недвижимости
    - Гистограмма с отображением средних цен по муниципальным округам города
    - Гистограмма с отображением средней площади квартиры по муниципальным округам города

## Требования
1. Проект должен содержать средства для сборки (Dockerfile, docker-compose)
2. Следование стилю PEP8 (или google styleguide)
3. Тайпинги во всех местах (кроме тестов)

# Список команд

```sh
usage: main.py [-h] {list,fetch_data,plot_bins,heatmap,filter} ...

Script for parsing a 'https://cian.ru' and visualize statistics from it.

options:
  -h, --help            show this help message and exit

subcommands:
  valid commands

  {list,fetch_data,plot_bins,heatmap,filter}
                        description
    list                display a list of available citites to parse
    fetch_data          running a script to parse data from 'https://cian.ru'
    plot_bins           creates bin plots and save them at '..output/' folder
    heatmap             creates a heatmap of parsed cityand saves it at '..output/' folder
    filter              manually apply filter script toto provided file
```
## Docker

Собрать образ:

```sh
docker build -t <container_name> .
```

Запустить контейнер:

```sh
docker run -i <container_name> [command]
```


