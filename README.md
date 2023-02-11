# Taller

Ahora que ya conocemos la forma más básica de un APIView, podemos crear nuestro endpoint totalmente personalizado.

De la sesión anterior recordaremos lo siguiente:

```py
class GetAllTodo(APIView):
    def get(self, request):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
```

Mediante un APIView, podemos hacer querys a nuestra base de datos y retornar la información dependiendo de que tipo de operación se realice.

Ahora que ya tenemos el concepto de como funciona, crearemos nuestro primer endpoint completo.

Operaciones a implementar:

-   CREATE
    
-   UPDATE
    
-   RETRIEVE
    
-   DELETE
    

## Recordando nuestros modelos.

El modelo a utilizar para nuestros TODO'S, es el siguiente:

```py
class Todo(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    done_at = models.DateField(null=True)
    updated_at = models.DateField(auto_now_add=True)
    deleted_at = models.DateField(null=True)
    status = models.IntegerField(default=0)
```

Ahora, en base a este modelo es que vamos a crear todas nuestras operaciones.

## Creando nuestro EndPoint

La clase base a utilizar es la siguiente en `todos/api.py`:

```py
class AllTodo(APIView):
```

### Get

En primer lugar, tenemos que retornar toda la información de nuestra base de datos mediante una operación GET, para realizar la obtención de todo nuestro datos, añadimos el siguiente método a nuestro endpoint:

```py
class AllTodo(APIView):
    def get(self, request):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
```

> Si recordamos `many = True` indica al serializador que no se va a enviar un solo objeto, por lo que tiene que hacer la serialización en base a un conjunto de registros.

Ahora que tenemos nuestro endpoint, vamos a añadir la nueva ruta en `todos/urls.py`.

```py
# ...
from .api import AllTodo

urlpatterns = [
    # ...
    path('api/v2/todo/', AllTodo.as_view(), name = 'fullView'),
]

urlpatterns += router.urls
```

Con la nueva ruta añadida, ya podemos hacer uso de ella.

![GET](https://photos.silabuz.com/uploads/big/dddabdc429d067d7e683eda9ca1f4031.PNG)

Con esto, podemos ver que nos retorna toda nuestra información.

### Delete

Al tener la obtención de todos nuestros registros, ahora vamos a crear un tipo de delete especial, el cual va a eliminar todos nuestros registros.

```py
class AllTodo(APIView):
    # ...

    def delete(self, request):
        Todo.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

Lo único nuevo es la operación `.delete()`, la cual se hace respecto a todos los registros almacenados.

Si regresamos a nuestra vista, vemos que esta se actualizó:

![Delete](https://photos.silabuz.com/uploads/big/f413cb8ca49a0b6ca66d7dbe8d4a347b.PNG)

Al inicio donde obtenemos el `código 200`, podemos ver que existe una opción llamada `allow`, la cual muestra todos los tipos de operaciones permitidas. En este caso vemos que ya hemos añadido `GET` y `DELETE`, además en la esquina superior derecha, vemos un botón rojo que también indica la operación a realizar, si queremos eliminar todos los registros simplemente hacemos uso de él.

![All delete](https://photos.silabuz.com/uploads/big/7d7b9fffb8ba8dbd692315bd63c37022.PNG)

### Post

Para hace uso del método POST dentro de nuestra vista, añadimos el siguiente método:

```py
class AllTodo(APIView):
    # ...

    def post(self, request, *args, **kwargs):
        serializer = TodoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

¿Cómo funciona? En primer lugar, encontramos que del request que realizamos, toda la información es serializada. Luego, se hace la validación de que no existe problemas con algún campo (vacíos o datos que no sean admitidos). Y por ultimo, se hace el guardado del registro.

Si actualizamos nuestra vista, obtenemos el siguiente resultado.

![Post](https://photos.silabuz.com/uploads/big/535224da2d76c4f97098b7c46b37f6cf.PNG)

En la porte inferior DRF, nos genera una especie de form para poder hacer el ingreso de nuestros datos.

Para este caso haremos la prueba con la siguiente información.

```json
{
"title":"Title todo 1",
"body": "Body todo 1",
"status": 2
}
```

![Agregando información](https://photos.silabuz.com/uploads/big/e20f918265c7f7e157b9b853156e2e64.PNG)

![Completado](https://photos.silabuz.com/uploads/big/2a84c28e953dcf56b651bbcedd610cdd.PNG)

> Recordar que la información enviada debe ser en formato JSON.

Ahora ya tenemos 3 partes de nuestro CRUD. Ahora, ¿si queremos actualizar un registro? No podemos hacerlo al obtenerlos todos, o mandando el id como información. Por lo que, debemos crear una nueva vista especialmente para cada registro.

## Tarea

Creamos la nueva vista `OneTodo`:

```py
class OneTodo(APIView):
    def get_todo(self, pk):
        try:
            todo = Todo.objects.get(pk=pk)
            return todo
        except Todo.DoesNotExist:
            raise Http404()

    def get(self, request, pk):
        todo = self.get_todo(pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)
```

El método `get_todo`, es para obtener el registro en base a su id.

Luego, en el get vamos a retornar nuestro TODO. Ahora, añadimos la nueva ruta:

```py
# ...
from .api import OneTodo


urlpatterns = [
    # ...
    path('api/v2/todo/<int:pk>', OneTodo.as_view(), name = 'OneTodo'),
]

urlpatterns += router.urls
```

-   Crear el método PUT, PATCH y DELETE para un solo TODO.

Recordar

-   Put actualiza todo el registro.
    
-   Patch actualiza una parte del registro.
    

Luego de crear la vista, realizar la creación y modificación de 5 registros, tanto desde la misma vista de DRF, como de un cliente distinto como PostMan, etc.

### Opcional

Añadir JWT a las operaciones y realizar la simulación del CRUD con tokens.

LINKS

Videos:
[Teoria](https://www.youtube.com/watch?v=Cl1mw4OtaBM&list=PLxI5H7lUXWhgHbHF4bNrZdBHDtf0CbEeH&index=8&ab_channel=Silabuz)
[Practica](https://www.youtube.com/watch?v=Gxp6ehTxHJU&list=PLxI5H7lUXWhgHbHF4bNrZdBHDtf0CbEeH&index=9&ab_channel=Silabuz)
PPT:
[Slide](https://docs.google.com/presentation/d/e/2PACX-1vSzUf3RX8MoMlSYn_I0peRLhJ4azkDde87zndXGA05L_XeLVM5mV8n9wWg6glist_us6TpQZ5RiUZxu/embed?start=false&loop=false&delayms=3000)