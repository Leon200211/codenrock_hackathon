<?php

session_start();

// File upload.php
// Если в $_FILES существует "image" и она не NULL
if (isset($_FILES['file'])) {
    require_once 'config.php';

    // Получаем нужные элементы массива "image"
    $fileTmpName = $_FILES['file']['tmp_name'];
    $errorCode = $_FILES['file']['error'];
    // Проверим на ошибки
    if ($errorCode !== UPLOAD_ERR_OK || !is_uploaded_file($fileTmpName)) {
        // Массив с названиями ошибок
        $errorMessages = [
            UPLOAD_ERR_INI_SIZE   => 'Размер файла превысил значение upload_max_filesize в конфигурации PHP.',
            UPLOAD_ERR_FORM_SIZE  => 'Размер загружаемого файла превысил значение MAX_FILE_SIZE в HTML-форме.',
            UPLOAD_ERR_PARTIAL    => 'Загружаемый файл был получен только частично.',
            UPLOAD_ERR_NO_FILE    => 'Файл не был загружен.',
            UPLOAD_ERR_NO_TMP_DIR => 'Отсутствует временная папка.',
            UPLOAD_ERR_CANT_WRITE => 'Не удалось записать файл на диск.',
            UPLOAD_ERR_EXTENSION  => 'PHP-расширение остановило загрузку файла.',
        ];
        // Зададим неизвестную ошибку
        $unknownMessage = 'При загрузке файла произошла неизвестная ошибка.';
        // Если в массиве нет кода ошибки, скажем, что ошибка неизвестна
        $outputMessage = isset($errorMessages[$errorCode]) ? $errorMessages[$errorCode] : $unknownMessage;
        // Выведем название ошибки
        die($outputMessage);
    } else {
        $audio = file_get_contents($_FILES['file']['tmp_name']);
        $audio_base64 = base64_encode($audio);

        $data = array('wav' => $audio_base64, 'coded' => 'base64');

        // use key 'http' even if you send the request to https://...
        $options = array(
            'http' => array(
                'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
                'method'  => 'POST',
                'content' => http_build_query($data)
            )
        );


        $context  = stream_context_create($options);
        $result = file_get_contents($connect_to_api, false, $context);
        if ($result === FALSE) {
            var_dump("Ошибка");
        }




        $_SESSION['result'] = $result;

    }
}

?>


<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <script src="assets/script/recorder.js"></script>
    <script src="assets/script/Fr.voice.js"></script>
    <script src="assets/script/jquery.js"></script>
    <script src="assets/script/app.js"></script>


    <link href="assets/css/style.css" rel="stylesheet">
    <link href="assets/css/send_form.css" rel="stylesheet">
    <link href="assets/css/main_style/style_header.css" rel="stylesheet">
    <link href="assets/css/main_style/style_footer.css" rel="stylesheet">
    <link href="assets/plugins/bootstrap/css/bootstrap.min.css" rel="stylesheet">


    <title>Fitlent</title>
</head>
<body>

<?php
require_once "include/header.php";
?>


<div class="second_img">
    <div class="second_img_blog">
        <div class="second_img_blog_title">
            СПИСКИ<br>И ТАБЛИЦЫ
        </div>
    </div>
</div>


<div class="second_page">
    <div class="second_page_title">РЕЗУЛЬТАТ</div>

    <div class="blog_table">
        <table class="second_page_table">
            <?php
            if(isset($_SESSION['result']) or !empty($result)){

                if(isset($_SESSION['result'])){
                    $result = $_SESSION['result'];
                }


                $lines = explode("\n", base64_decode($result));
                $arrays = array_map('str_getcsv', $lines);
                foreach ($arrays as $key => $array){
                    if($key == 0){
                        ?>
                        <tr>
                            <?php foreach ($array as $item): ?>
                                <th><?=$item?></th>
                            <?php endforeach; ?>
                        </tr>
                        <?php
                    }else{
                        ?>
                        <tr>
                            <?php foreach ($array as $item): ?>
                                <td><?=$item?></td>
                            <?php endforeach; ?>
                        </tr>
                        <?php
                    }
                }
            }
            ?>
        </table>

    </div>

    <div class="download">
        <a class="download_button" href="export.php">
            СКАЧАТЬ
        </a>
    </div>

</div>



<?php
require_once "include/footer.php";


?>

</body>
</html>





