<?php


#========================================================
# Отдаем пользователю файл на выгрузку
#========================================================



session_start();


$lines = explode("\n", base64_decode($_SESSION['result']));
$arrays = array_map('str_getcsv', $lines);

$file_name = uniqid();
$fp = fopen('download_files/' . $file_name . '.csv', 'w');

foreach ($arrays as $fields) {
    fputcsv($fp, $fields);
}

fclose($fp);



$file = 'download_files/' . $file_name . '.csv';

if (file_exists($file)) {
    // сбрасываем буфер вывода PHP, чтобы избежать переполнения памяти выделенной под скрипт
    // если этого не сделать файл будет читаться в память полностью!
    if (ob_get_level()) {
        ob_end_clean();
    }
    // заставляем браузер показать окно сохранения файла
    header('Content-Description: File Transfer');
    header('Content-Type: application/octet-stream');
    header('Content-Disposition: attachment; filename=' . basename($file));
    header('Content-Transfer-Encoding: binary');
    header('Expires: 0');
    header('Cache-Control: must-revalidate');
    header('Pragma: public');
    header('Content-Length: ' . filesize($file));
    // читаем файл и отправляем его пользователю
    readfile($file);

    unlink($file);
    exit;
}



