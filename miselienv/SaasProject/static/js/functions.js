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
    for (let key of formData.keys()) {
        obj[key] = formData.get(key);
    }

    return JSON.stringify(obj)
    // return obj
}

function guardarformulario(form_id, url) {
    console.log(form_id, "esto es form_id")
    console.log(url, "esto es url")

    if (document.getElementById(form_id).checkValidity()) {
        let datos = serialize(form_id)
        // let csrf = JSON.parse(datos)
        // csrf = csrf["csrfmiddlewaretoken"]

        console.log(typeof (datos), datos, "esto es typeof")
        //
        //     axios.post(url, datos)
        //         .then(function (respuesta) {
        //             console.log(respuesta, "esta es la respuesta por medio de axios")
        //         }).catch(function (err) {
        //         console.log(err)
        //     })
        // } else {
        //     console.log("el formulario no es valido")
        // }


        axios({
            method: 'post',
            url: url,
            data: datos,
            headers: {
                //     // "X-CSRFToken": datos,
                //     Accept: "application/json",
                //     "Content-Type": "application/json;charset=UTF-8",
                //      "Content-Type": "multipart/form-data",
                //       "Content-Type": "text/plain",
                // "Content-Type": "text/html",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                //     // "content-type": "application/x-www-form-urlencoded",
                //     // "content-type": "application/json",
                //
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
