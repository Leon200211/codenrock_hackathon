var dt = new DataTransfer();

$('.input-file input[type=file]').on('change', function(){
    let $files_list = $(this).closest('.input-file').next();
    $files_list.empty();

    for(var i = 0; i < this.files.length; i++){
        let file = this.files.item(i);
        dt.items.add(file);

        let reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = function(){
            let new_file_input = '<div class="input-file-list-item">' +
                '<img class="input-file-list-img" src="assets/img/1.png">' +
                '<span class="input-file-list-name">' + file.name + '</span>' +
                '<a href="#" onclick="removeFilesItem(this); return false;" class="input-file-list-remove">x</a>' +
                '</div>';
            $files_list.append(new_file_input);
        }
    };
    this.files = dt.files;
});

function removeFilesItem(target){
    let name = $(target).prev().text();
    let input = $(target).closest('.input-file-row').find('input[type=file]');
    $(target).closest('.input-file-list-item').remove();
    for(let i = 0; i < dt.items.length; i++){
        if(name === dt.items[i].getAsFile().name){
            dt.items.remove(i);
        }
    }
    input[0].files = dt.files;
}