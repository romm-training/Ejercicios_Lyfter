## Preguntas reflexivas al agregar tabla Users e historial de compras

* **¿Cada factura debe tener relación con un usuario, o puede existir una factura sin cuenta?**

La factura es un documento oficial con validez contable y fiscal, por lo que no deberían existir facturas sin usuarios ya que se prestaría para fraude.

* **¿Necesita una tabla intermedia? ¿Por qué?**

No. El escenario planteado hasta ahora no lo amerita. Un usuario puede tener varias facturas y una factura solo puede tener un usuario, por lo que con una relacion de uno a muchos es suficiente. Sin embargo, eventualmente podria requerirse una o varias tablas adicionales para almacenar información adicional y complementaria a la factura, como puede ser la direccion de entrega.

* **Ahora se relaciona mediante el id del usuario, ¿es necesario mantener el correo del usuario como en el ejercicio anterior?**

No es necesario. La tabla de usuario conserva el correo y es unico, por lo que con solo la referencia del usuario se puede obtener el correo. Se podría pensar que un usuario puede cambiar su cuenta de correo y por eso se debe almacenar en la factura para saber cuales fueron hechas con un correo y cuales con otro. Sin embargo, el principio de unicidad de ese campo en la tabla Users sugiere que un cambio de correo por parte del usuario requiere la creacion de otro usuario.

## Pregunta reflexiva de la tabla Reviews

* **¿Una reseña puede existir sin un producto o sin un usuario?**

No, no se debe permitir una reseña sin usuario ni producto ya que ambos son necesarios para que la información tenga validez y pueda ser analizada para tomar decisiones.

## Pregunta reflexiva de la tabla Metodos de Pago

* **¿Cada factura debe tener exactamente un método de pago, o podría haber más de uno?**

Para este ejercicio, existe el supuesto de que cada factura debe tener solo un metodo de pago, ademas, es lo más utilizado en el mercado. Sin embargo, es razonable pensar que alguna tienda ofrezca a sus clientes la posibilidad de pueda pagar una parte con la tarjeta de crédito, otra con transferencia y otra con puntos de algún plan de lealtad. Incluso, también se puede pensar que para clientes muy exclusivos se les pueda dar una opción de crédito a N días.