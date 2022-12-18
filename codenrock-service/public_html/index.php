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
    <link href="assets/css/main_style/style_change.css" rel="stylesheet">
    <link href="assets/css/main_style/style_footer.css" rel="stylesheet">
    <link href="assets/plugins/bootstrap/css/bootstrap.min.css" rel="stylesheet">

    <title>Fitlent</title>
</head>
<body>

    <?php
    require_once 'include/header.php';
    ?>


    <div class="main_img">
        <div class="main_img_blog">
            <div class="main_img_blog_title">
               ТРАНСКРИБАЦИЯ<br>ГОЛОСА
            </div>
            <div class="main_img_blog_text">
                Сервис, который расшифровывает аудиозапись пользователя и выдает отчет в виде<br>
                таблицы с описанием каждого предмета с возможностью дальнейшей выгрузки этой таблицы.
            </div>
        </div>
    </div>


    <div class="main_body">

        <div class="room_list">
            <div id="room_list" class="room_list">
                <button class="common_button_room_list show">ЗАПИСЬ АУДИО</button>
                <button class="common_button_room_list">ЗАГРУЗКА АУДИО</button>
            </div>
        </div>


        <div class="main_field_div_for_room">
            <div class="room_main_info show">
                <audio controls id="audio"></audio>
                <div class="under_audio">
                    <a class="button recordButton" id="record">Запись</a>
                    <a class="button disabled one" id="pause">Пауза</a>
                    <a class="button disabled one" id="stop">Перезагрузить</a>
                </div><br/>
                <div>
                    <input class="button" type="checkbox" id="live"/>
                    <label class="live_voice" for="live">Живой вывод</label>
                </div>
                <div class="bottom_line" data-type="wav">
                    <a class="button disabled one" id="play">Воспроизвести</a>
                    <a class="button disabled one" id="download">Скачать</a>
                    <a class="button disabled one" id="base64">Base64 URL</a>
                    <a class="button disabled one" id="save">Преобразовать данные</a>
                </div>
                <canvas class="audio_canvas" id="level" height="200" width="500"></canvas>
            </div>


            <div class="room_main_info">
                <form method="post" action="uploade_file.php" enctype="multipart/form-data">
                    <div class="input-file-row">
                        <label class="input-file">
                            <input type="file" name="file">
                            <span>Выберите файл</span>
                        </label>
                        <div class="input-file-list"></div>
                    </div>
                    <script src="https://snipp.ru/cdn/jquery/2.1.1/jquery.min.js"></script>
                    <script src="assets/script/image_upload_form.js" defer></script>
                    <br>
                    <button class="button" type="submit">Преобразовать данные</button>
                </form>
            </div>
        </div>
        <script>
            menu = document.getElementById("room_list");
            blocks = Array.from(document.getElementsByClassName("room_main_info"));
            lists = Array.from(menu.getElementsByClassName("common_button_room_list"));
            lists.forEach(element => element.onclick = function() {
                index = lists.indexOf(element);
                blocks.forEach(block => block.classList.remove("show"));
                blocks[index].classList.add("show");

                lists.forEach(block => block.classList.remove("show"));
                lists[index].classList.add("show");
            });
        </script>
    </div>


<?php
require_once "include/footer.php";
?>


</body>
</html>
