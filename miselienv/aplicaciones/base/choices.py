sexo = (
    ('F', 'Femenino'),
    ('M', 'Masculino')
)

tipodocumento = (
    ('RUC', 'Registro unico de contribuyente'),
    ('CI', 'Cedula de identidad'),
    ('DNI', 'Documento nacional de identidad')
)

personeria = (
    ('F', 'Fisica'),
    ('J', 'Juridica')

)

estado = (
    ('true',  'Activo'),
    ('false', 'Inactivo')

)

estadocivil = (
    ('S', 'Soltero/a'),
    ('C', 'Casado/a'),
    ('D', 'Divorciado/a'),
    ('V', 'Viudo/a')
)

sino = (
    ('SI', 'SI'),
    ('NO', 'NO')
)

entradasalida = (
    ('E', 'ENTRADA'),
    ('S', 'SALIDA')
)

#  SIEMPRE LA SUMA O LA RESTA SE VE DESDE EL PUNTO DE VISTA DE LA EMPRESA
sumaoresta = (
    ('S', 'SUMA'),
    ('R', 'RESTA')
)

# choices para ventas
precioartpredeterminado = (
    ('UC', 'ULTIMA COMPRA'),
    ('UV', 'ULTIMA VENTA'),
    ('PR', 'PROMEDIO')
)

tipocomprobante = (
    ('LE', 'LEGAL'),
    ('IN', 'INTERNO')
)

dondemuevestock = (
    ('RE', 'REMISION'),
    ('FA', 'FACTURA')
)

obligatoriodesde = (
    ('PED', 'PEDIDO'),
    ('PRE', 'PRESUPUESTO'),
    ('REM', 'REMISION'),
    ('FAC', 'FACTURA')
)

contadocredito = (
    ('CONT', 'CONTADO'),
    ('CRED', 'CREDITO')
)

falsoverdadero = (
    ('true', 'true'),
    ('false', 'false')

)

entidadfinanciera = (
    ('BANCO', 'BANCO'),
    ('FINANCIERA', 'FINANCIERA'),
    ('COOPERATIVA', 'COOPERATIVA'),
)
