function replacer(key, value) {
    if (typeof value === 'function') {
        return value.toString()
    }
    if (key === 'clave') {

    } else if (key === 'valor') {

    }
    console.log(key.name, value, "key y value en value nro llamada:")
    return value
}

// https://gomakethings.com/serializing-form-data-with-the-vanilla-js-formdata-object/
function serialize(form_id) {
    let obj = {};
    let formData = new FormData(document.getElementById(form_id));
    return formData
}

function guardarformulario(form_id, url) {
    console.log(form_id, "esto es form_id")
    console.log(url, "esto es url")

    if (document.getElementById(form_id).checkValidity()) {
        let datos = serialize(form_id)

        console.log(typeof (datos), datos, "esto es typeof")

        axios({
            method: 'post',
            url: url,
            data: datos,
            headers: {
                "Content-Type": "multipart/form-data",
            }
        })
            .then(function (respuesta) {

                console.log(respuesta, "esta es la respuesta por medio de axios")

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
