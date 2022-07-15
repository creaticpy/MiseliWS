function replacer(key, value) {
    if (typeof value === 'function') {
        return value.toString()
    }
    if (key === 'clave') {

    } else if (key === 'valor') {

    }

    return value
}

// https://gomakethings.com/serializing-form-data-with-the-vanilla-js-formdata-object/
function serialize(form_id) {
    let formData = new FormData(document.getElementById(form_id));
    return formData
}

function guardarformulario(form_id, url) {
    if (document.getElementById(form_id).checkValidity()) {
        let datos = serialize(form_id)

        axios({
            method: 'post',
            url: url,
            data: datos,
            headers: {
                "Content-Type": "multipart/form-data",
            }
        })
            .then(function (res) {

                alert_message(text = res.data['text'], type = res.data['type'], timelapse = res.data['timelapse'])
                // document.getElementById(form_id).reset(); funciona correctamente... ver cuando aplicar.
            }).catch(function (err) {
            console.log(err)
        })
    } else {
        console.log("el formulario no es valido")
    }
}

function submitForm(form_id) {
    console.log("que pasa?")
    let form = document.getElementById(form_id)
    console.log(form.checkValidity())

}

function alert_message(text, type, timelapse) {

    let alert_box = document.getElementById('alert-box')
    alert_box.innerHTML += `<div class="alert alert-${type}" data-bs-dismiss="alert" role="alert">${text}</div>`


    setTimeout(BorrarAlerta, timelapse)

    function BorrarAlerta() {
        let hijos = alert_box.querySelectorAll('div')
        hijos.forEach((cada, i) => {
            alert_box.removeChild(hijos.item(i))
        })


    }
}
