#!/usr/bin/sh

dirname=./env1 # каталог, в котором создать виртуальное окружение
modules_list=(six numpy sklearn matplotlib pandas notebook) # список модулей необходимых в этом виртуальное окружении

if [ ! -f ${dirname}/pyvenv.cfg ]
then
  # виртуальное окружение ещё не было создано (каталог пустой или отсутствует)
  echo Initializing environment
  python -m venv $dirname # создать виртуальное окружение
  source ${dirname}/bin/activate # активировать виртуальное окружение
  echo Upgrading pip
  python -m pip install --upgrade pip # обновить pip в нём
else
  # виртуальное окружение уже существует
  source ${dirname}/bin/activate # активировать виртуальное окружение
fi

install_dir=${dirname}/_install # каталог, в который скачивать модули, также в нём будет создаваться маркерный файл указывающий на установленность модуля
cache_dir=${dirname}/_cache # каталог кэша для скаченных файлов
if [ ! -d $install_dir ]
then
  mkdir -p $install_dir
fi
if [ ! -d $cache_dir ]
then
  mkdir -p $cache_dir
fi

# Установка модулей перечисленных в modules_list
for module in ${modules_list[@]}
do
  if [ ! -f ${install_dir}/${module}.log ]
  then
    # этот модуль ещё не ставилcя
    mkdir -p ${install_dir}/${module}
    echo install module $module
    log_file=${install_dir}/${module}.log

    # скачать модуль (для возможной последующей offline-установки)
    echo --- download --- > $log_file
    pip3 download --log $log_file --cache-dir $cache_dir --dest ${install_dir}/${module} $module

    # установить модуль
    echo --- install --- >> $log_file
    pip3 install --no-index --find-links ${install_dir}/${module} --log $log_file $module

    echo --- complete --- >> $log_file
  fi
done

# список установленных модулей
pip3 list

# запуск скрипта в текущем виртуальном окружении
#python3 read_table.py
jupyter notebook &
