  
console.log('hello world')
const uploadForm = document.getElementById('upload-form')
const input = document.getElementById('id_document')
console.log(input)
const sentData = document.getElementById('sent-data')

const alertBox = document.getElementById('alert-box')
const progressBox = document.getElementById('progress-box')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

const spinnerBox = document.getElementById('spinner-box')
const dataBox = document.getElementById('data-box')

spinnerBox.classList.add('not-visible')


uploadForm.addEventListener('submit', function(evt){
    spinnerBox.classList.remove('not-visible')
    alertBox.innerHTML= "submitting..."


});

input.addEventListener('change', ()=>{
    progressBox.classList.remove('not-visible')
    const file_data = input.files[0]
    const url = URL.createObjectURL(file_data)
    console.log(file_data)
    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('image', file_data)

    $.ajax({
        type:'POST',
        url: uploadForm.action,
        enctype: 'multipart/form-data',
        data: fd,
        beforeSend: function(){
            console.log('before')
        },
        xhr: function(){
            alertBox.innerHTML= "Uploading..."

            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress', e=>{
                // console.log(e)
                if (e.lengthComputable) {
                    const percent = e.loaded / e.total * 100
                    console.log(percent)
                    progressBox.innerHTML = `<div class="progress">
                                                <div class="progress-bar" role="progressbar" style="width: ${percent}%" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100"></div>
                                            </div>
                                            <p>${percent.toFixed(1)}%</p>`
                }

            })
            return xhr

        },

        success: function(response){
            console.log(response)
            alertBox.innerHTML= "Done!"

        },

        error: function(error){
            console.log(error)

        },

        cache: false,
        contentType: false,
        processData: false,



    })
})


