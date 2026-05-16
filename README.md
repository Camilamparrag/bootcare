# BootcampConnect

Red social privada para estudiantes, graduados e instructores de un bootcamp tecnológico. Construida con Django 6.0.

---

## Stack Tecnológico

| Componente | Tecnología |
|---|---|
| Backend | Django 6.0 |
| Base de Datos | SQLite (desarrollo) |
| Frontend | Django Templates + TailwindCSS |
| ORM | Django ORM |
| Autenticación | `django.contrib.auth` |
| Imágenes | Pillow |

---

## Estructura del Proyecto

```
bootcampconnect/
├── accounts/        # Gestión de usuarios, perfiles y seguidores
├── posts/           # Publicaciones, feed, likes y comentarios
├── comments/        # Modelo de comentarios (vistas en posts)
├── confessions/     # Sección anónima "Lo que callamos en el Bootcamp"
├── chat/            # Mensajería privada 1 a 1
├── core/            # Utilidades compartidas (templatetags, landing)
├── bootcampconnect/ # Configuración del proyecto (settings, urls raíz)
├── templates/       # Plantillas HTML organizadas por app
├── media/           # Archivos subidos por usuarios
├── static/          # Archivos estáticos
└── db.sqlite3       # Base de datos local
```

---

## Models

### accounts.models.User

Modelo de usuario personalizado que extiende `AbstractUser` de Django.

| Campo | Tipo | Propósito |
|---|---|---|
| `avatar` | `ImageField` (opcional) | Foto de perfil del usuario. Subida a `avatars/` |
| `bio` | `TextField` (max 500) | Biografía o descripción personal |
| `github_url` | `URLField` | Enlace al perfil de GitHub |
| `linkedin_url` | `URLField` | Enlace al perfil de LinkedIn |
| `following` | `ManyToManyField("self", symmetrical=False)` | Relación asimétrica de seguimiento. `related_name="followers"` permite acceder a los seguidores de un usuario |

**Por qué extiende AbstractUser**: Para reutilizar toda la lógica de autenticación de Django (login, logout, passwords, sesiones) y añadir campos sociales sin reescribir el sistema.

---

### posts.models.Post

Representa una publicación en el feed.

| Campo | Tipo | Propósito |
|---|---|---|
| `user` | `ForeignKey(User, on_delete=CASCADE)` | Autor de la publicación. Se elimina si el usuario se borra |
| `image` | `ImageField(upload_to="posts/")` | Imagen principal de la publicación |
| `caption` | `TextField` (max 1000) | Descripción o texto de la publicación |
| `hashtags` | `CharField` (max 500) | Hashtags como texto plano separado por espacios |
| `created_at` | `DateTimeField(auto_now_add=True)` | Fecha de creación (solo lectura, se asigna automáticamente al crear) |
| `likes` | `ManyToManyField(User, related_name="liked_posts")` | Usuarios que dieron like. `related_name` permite hacer `user.liked_posts.all()` |

**Meta**: ordenado por `-created_at` (más recientes primero).

---

### comments.models.Comment

Comentarios asociados a publicaciones.

| Campo | Tipo | Propósito |
|---|---|---|
| `post` | `ForeignKey(Post, on_delete=CASCADE, related_name="comments")` | Publicación a la que pertenece el comentario |
| `user` | `ForeignKey(User, on_delete=CASCADE)` | Autor del comentario |
| `text` | `CharField` (max 500) | Contenido del comentario |
| `created_at` | `DateTimeField(auto_now_add=True)` | Fecha de creación |

---

### confessions.models.AnonymousConfession

Confesión anónima en la sección "Lo que callamos en el Bootcamp".

| Campo | Tipo | Propósito |
|---|---|---|
| `user` | `ForeignKey(User, on_delete=SET_NULL, null=True)` | Autor real (oculto al público, solo para moderación interna). `SET_NULL` evita borrar confesiones si el usuario se elimina |
| `content` | `TextField` (max 2000) | Texto de la confesión |
| `created_at` | `DateTimeField(auto_now_add=True)` | Fecha de creación |
| `likes` | `ManyToManyField(User, related_name="liked_confessions")` | Likes de la confesión |

### confessions.models.AnonymousComment

Comentario anónimo dentro de una confesión.

| Campo | Tipo | Propósito |
|---|---|---|
| `confession` | `ForeignKey(AnonymousConfession, on_delete=CASCADE, related_name="comments")` | Confesión a la que pertenece |
| `text` | `CharField` (max 500) | Texto del comentario |
| `created_at` | `DateTimeField(auto_now_add=True)` | Fecha de creación |

---

### chat.models.ChatMessage

Mensaje privado entre dos usuarios.

| Campo | Tipo | Propósito |
|---|---|---|
| `sender` | `ForeignKey(User, related_name="sent_messages")` | Usuario que envía el mensaje |
| `receiver` | `ForeignKey(User, related_name="received_messages")` | Usuario que recibe el mensaje |
| `message` | `TextField` | Contenido del mensaje |
| `is_read` | `BooleanField(default=False)` | Indica si el mensaje ha sido leído |
| `timestamp` | `DateTimeField(auto_now_add=True)` | Fecha y hora de envío |

---

## URLs

### Raíz (`bootcampconnect/urls.py`)

| Ruta | Incluye | Propósito |
|---|---|---|
| `admin/` | `admin.site.urls` | Panel de administración de Django |
| `accounts/` | `accounts.urls` | Autenticación y perfiles |
| `""` (raíz) | `posts.urls` | Feed y publicaciones |
| `comments/` | `comments.urls` | (vacío, los comentarios se manejan desde posts) |
| `confessions/` | `confessions.urls` | Sección anónima |
| `chat/` | `chat.urls` | Mensajería privada |

### accounts/urls.py

| Ruta | Name | View | Propósito |
|---|---|---|---|
| `login/` | `login` | `LoginView` (Django) | Inicio de sesión |
| `logout/` | `logout` | `LogoutView` (Django) | Cierre de sesión |
| `register/` | `register` | `register` | Registro de nuevo usuario |
| `profile/<str:username>/` | `profile` | `profile` | Perfil público de un usuario |
| `follow/<int:user_id>/` | `follow-toggle` | `follow_toggle` | Seguir/dejar de seguir |
| `search/` | `user-search` | `user_search` | Buscar usuarios |

### posts/urls.py

| Ruta | Name | View | Propósito |
|---|---|---|---|
| `""` (raíz) | `feed` | `feed` | Feed principal con publicaciones de seguidos |
| `post/<int:pk>/` | `post-detail` | `post_detail` | Detalle de una publicación con comentarios |
| `post/create/` | `post-create` | `post_create` | Crear nueva publicación |
| `post/<int:pk>/like/` | `like-toggle` | `like_toggle` | Dar/quitar like |
| `post/<int:pk>/comment/` | `add-comment` | `add_comment` | Agregar comentario |

### confessions/urls.py (app_name = "confessions")

| Ruta | Name | View | Propósito |
|---|---|---|---|
| `""` | `confessions:list` | `confession_list` | Lista de confesiones anónimas |
| `create/` | `confessions:create` | `confession_create` | Crear confesión |
| `<int:pk>/like/` | `confessions:like` | `confession_like` | Dar/quitar like anónimo |
| `<int:pk>/comment/` | `confessions:comment` | `confession_comment` | Comentar confesión |

### chat/urls.py (app_name = "chat")

| Ruta | Name | View | Propósito |
|---|---|---|---|
| `""` | `chat:inbox` | `inbox` | Bandeja de entrada con últimas conversaciones |
| `<int:user_id>/` | `chat:conversation` | `conversation` | Hilo de mensajes con un usuario |
| `send/<int:receiver_id>/` | `chat:send` | `send_message` | Enviar mensaje |

### core/urls.py

Vacío. El core no expone rutas propias; la vista `home` del core está conectada desde `posts/urls.py` originalmente, pero actualmente la raíz apunta al feed de posts.

---

## Settings (configuración clave)

### `bootcampconnect/settings.py`

| Variable | Valor | Propósito |
|---|---|---|
| `SECRET_KEY` | (clave generada) | Firma de sesiones, tokens CSRF, etc. |
| `DEBUG` | `True` | Modo desarrollo (nunca `True` en producción) |
| `INSTALLED_APPS` | `accounts`, `posts`, `comments`, `confessions`, `chat`, `core` | Apps propias registradas |
| `TEMPLATES.DIRS` | `BASE_DIR / "templates"` | Directorio global de plantillas |
| `AUTH_USER_MODEL` | `accounts.User` | Le dice a Django que use nuestro modelo User personalizado en lugar del `auth.User` por defecto |
| `LOGIN_URL` | `"login"` | URL a la que redirigir cuando se requiere `@login_required` |
| `LOGIN_REDIRECT_URL` | `"feed"` | URL después de iniciar sesión |
| `LOGOUT_REDIRECT_URL` | `"login"` | URL después de cerrar sesión |
| `MEDIA_URL` | `"media/"` | Prefijo URL para archivos subidos |
| `MEDIA_ROOT` | `BASE_DIR / "media"` | Directorio en disco para archivos subidos |
| `STATICFILES_DIRS` | `[BASE_DIR / "static"]` | Directorio de archivos estáticos en desarrollo |
| `DATABASES` | SQLite (`db.sqlite3`) | Base de datos local |

**Por qué `AUTH_USER_MODEL`**: Para añadir campos como `avatar`, `bio`, `following` al modelo de usuario sin tener que crear un perfil separado. Se declara antes de la primera migración.

**Por qué `MEDIA` config**: Django no sirve archivos multimedia por defecto en desarrollo. Se añade `static(settings.MEDIA_URL, ...)` en las URLs raíz solo cuando `DEBUG=True`.

---

## Views

### Core

| View | Decorador | Propósito |
|---|---|---|
| `home(request)` | Ninguno | Si el usuario está autenticado redirige a `feed`. Si no, renderiza `core/landing.html` (página de bienvenida con opciones de login/registro) |

### Accounts

| View | Decorador | Propósito |
|---|---|---|
| `register(request)` | Ninguno | GET: muestra formulario de registro (`UserRegistrationForm`). POST: valida, guarda el usuario, muestra mensaje de éxito y redirige a login |
| `profile(request, username)` | `@login_required` | Muestra perfil de un usuario con sus publicaciones, seguidores, seguidos. Usa `prefetch_related` para optimizar queries. Determina si el usuario autenticado sigue a este perfil |
| `user_search(request)` | `@login_required` | Busca usuarios por username (`icontains`). Excluye al usuario autenticado. Envía lista de `following_ids` para mostrar estado de seguimiento |
| `follow_toggle(request, user_id)` | `@login_required` | Si ya sigue al usuario, lo deja de seguir. Si no, lo sigue. Previene auto-seguimiento |

### Posts

| View | Decorador | Propósito |
|---|---|---|
| `feed(request)` | Ninguno (manejo manual) | Si no está autenticado, muestra landing. Si está autenticado, muestra publicaciones de usuarios que sigue más las propias, ordenadas por más reciente. Usa `select_related("user")` y `prefetch_related("likes", "comments")` para eficiencia |
| `post_detail(request, pk)` | `@login_required` | Muestra una publicación individual con su lista de comentarios y un formulario para comentar. Usa `select_related` + `prefetch_related` |
| `post_create(request)` | `@login_required` | GET: formulario de nueva publicación. POST: guarda la publicación asignando `request.user` como autor |
| `like_toggle(request, pk)` | `@login_required` | Alterna el like del usuario autenticado en la publicación |
| `add_comment(request, pk)` | `@login_required` | Agrega un comentario a la publicación. Crea el objeto `Comment` con `post` y `user` asignados automáticamente |

### Confessions

| View | Decorador | Propósito |
|---|---|---|
| `confession_list(request)` | `@login_required` | Muestra todas las confesiones con likes y comentarios. El autor nunca se expone en la plantilla (siempre muestra "Anónimo") |
| `confession_create(request)` | `@login_required` | POST: guarda la confesión vinculando el usuario real internamente (nunca se muestra) |
| `confession_like(request, pk)` | `@login_required` | Alterna like en una confesión |
| `confession_comment(request, pk)` | `@login_required` | Agrega comentario anónimo a una confesión (sin identidad del autor) |

### Chat

| View | Decorador | Propósito |
|---|---|---|
| `inbox(request)` | `@login_required` | Para cada usuario distinto al autenticado, obtiene el último mensaje intercambiado y cuenta los no leídos. Renderiza lista de conversaciones |
| `conversation(request, user_id)` | `@login_required` | Muestra el hilo completo de mensajes con otro usuario. Marca como leídos los mensajes recibidos no leídos |
| `send_message(request, receiver_id)` | `@login_required` | POST: crea un nuevo mensaje con el texto enviado y redirige a la conversación |

---

## Django Template Tags (Jinja)

El proyecto usa el sistema de templates de Django (no Jinja2 puro, sino el motor Django Templates que está inspirado en Jinja). A continuación se explican todas las etiquetas y filtros utilizados en las plantillas.

### Tags incorporados de Django

#### `{% extends "base.html" %}`

**Qué hace**: Hereda de una plantilla base. El bloque `{% block content %}` en el hijo reemplaza al mismo bloque definido en `base.html`.

**Por qué se usa**: Para no repetir el HTML común (header, nav, mensajes flash, estructura) en cada página. Todas las páginas extienden `base.html`.

**Dónde**: En todas las plantillas (`landing.html`, `feed.html`, `detail.html`, `create.html`, `login.html`, `register.html`, `profile.html`, `search.html`, `list.html`, `inbox.html`, `conversation.html`).

---

#### `{% block title %}...{% endblock %}` y `{% block content %}...{% endblock %}`

**Qué hace**: Define secciones que pueden ser reemplazadas por plantillas hijas.

**Por qué se usa**: `title` permite personalizar el `<title>` de cada página. `content` es donde cada página inyecta su contenido principal.

---

#### `{% url 'name' arg1 arg2 %}`

**Qué hace**: Resuelve el nombre de una URL (definido con `name=` en `urlpatterns`) a su ruta real, reemplazando parámetros si es necesario.

**Por qué se usa**: En lugar de hardcodear rutas como `/post/5/`, se usa el nombre. Si la ruta cambia en `urls.py`, todas las referencias se actualizan automáticamente.

**Ejemplos en el proyecto**:
- `{% url 'feed' %}` → `/`
- `{% url 'profile' post.user.username %}` → `/accounts/profile/juan/`
- `{% url 'post-detail' post.id %}` → `/post/3/`
- `{% url 'like-toggle' post.id %}` → `/post/3/like/`
- `{% url 'confessions:create' %}` → `/confessions/create/`
- `{% url 'chat:conversation' user_obj.id %}` → `/chat/5/`

**Nota sobre namespaces**: `confessions` y `chat` usan `app_name` en sus urls.py, por lo que las URLs se referencian con prefijo (`confessions:list`, `chat:inbox`).

---

#### `{% csrf_token %}`

**Qué hace**: Inserta un campo oculto con un token CSRF único y firmado.

**Por qué se usa**: Protege contra ataques CSRF (Cross-Site Request Forgery). Django rechazará cualquier POST que no incluya este token. Es obligatorio en todo `<form method="post">`.

**Dónde**: En todos los formularios POST del proyecto (login, registro, crear publicación, likes, comentarios, seguir, mensajes, confesiones).

---

#### `{% for ... %}` ... `{% empty %}` ... `{% endfor %}`

**Qué hace**: Itera sobre una lista. Si la lista está vacía, ejecuta el bloque `{% empty %}`.

**Por qué se usa**: Para recorrer colecciones (posts, comentarios, usuarios, mensajes, confesiones) y renderizar cada elemento.

**Ejemplos**:
- `{% for post in posts %}` ... `{% empty %}` → "No hay publicaciones"
- `{% for comment in post.comments.all %}` ... `{% empty %}` → "Sin comentarios"
- `{% for u in users %}` ... `{% empty %}` → "No se encontraron usuarios"

---

#### `{% if ... %}` ... `{% else %}` ... `{% endif %}`

**Qué hace**: Renderizado condicional.

**Por qué se usa**: Para mostrar/ocultar elementos según el estado de la aplicación.

**Ejemplos de uso**:
- `{% if user.is_authenticated %}` → muestra el nav solo si hay sesión activa
- `{% if post.user.avatar %}` → muestra la imagen o un fallback con iniciales
- `{% if request.user in post.likes.all %}` → pinta el botón de like en rojo si ya dio like
- `{% if is_following %}` → muestra "Dejar de seguir" o "Seguir"
- `{% if u.id in following_ids %}` → estado del botón en búsqueda
- `{% if msg.sender == request.user %}` → alinear mensajes propios a la derecha
- `{% if unread %}` → badge de mensajes no leídos
- `{% if messages %}` → mostrar mensajes flash
- `{% if field.errors %}` → mostrar errores de validación

---

#### `{{ variable }}` y `{{ variable|filter }}`

**Qué hace**: Interpolación de variables. Los filtros transforman el valor.

**Por qué se usa**: Para mostrar datos dinámicos del backend en el HTML.

---

### Filtros de Django utilizados

#### `{{ variable|date:"d M Y H:i" }}`

**Qué hace**: Formatea un `datetime` de Python según el formato especificado.

**Por qué se usa**: Las fechas en la BD son objetos Python; sin este filtro se mostrarían como `2026-05-16 14:30:00+00:00`. Con el filtro se muestran como `16 May 2026 14:30`.

**Dónde**: En `feed.html`, `detail.html`, `inbox.html`, `profile.html`.

#### `{{ variable|first }}` y `{{ variable|upper }}`

**Qué hace**: `first` obtiene el primer carácter de un string. `upper` lo convierte a mayúsculas.

**Por qué se usa**: Para mostrar la inicial del username como avatar por defecto cuando no hay foto de perfil.

**Dónde**: En `feed.html`, `detail.html`, `profile.html`, `search.html`, `inbox.html`.

#### `{{ variable|truncate }}` (truncatechars/truncatewords implícito)

**Qué hace**: Corta texto largo con puntos suspensivos.

**Dónde**: En `inbox.html` con `{{ last_msg.message }}` (el navegador puede cortarlo con CSS `truncate`).

---

### Tags personalizados

#### `{% load form_tags %}`

**Qué hace**: Carga el módulo de tags personalizados definido en `core/templatetags/form_tags.py`.

**Por qué se usa**: Para registrar filtros custom en el motor de templates.

**Dónde**: En `login.html`, `register.html`, `create.html`.

---

#### `{{ field|add_class:"w-full border rounded p-2" }}`

**Qué hace**: Filtro personalizado definido en `core/templatetags/form_tags.py`. Toma un campo de formulario de Django y le añade la clase CSS especificada al atributo `class` del widget HTML.

**Código del filtro**:
```python
@register.filter(name="add_class")
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})
```

**Por qué se usa**: Django no permite pasar clases CSS directamente desde la vista a los widgets cuando se renderizan con `{{ form.as_p }}` o iterando campos. Este filtro permite aplicar estilos de TailwindCSS a los inputs sin modificar el widget en `forms.py`.

**Dónde**: En `login.html`, `register.html`, `create.html` para dar estilo consistente a todos los inputs del formulario.

---

### Variables de contexto disponibles

#### `request` (context processor)

**Disponible por**: `django.template.context_processors.request` en `TEMPLATES.OPTIONS.context_processors`.

**Uso**: `request.user` para el usuario autenticado, `request.GET.q` para el query de búsqueda.

#### `user` (context processor)

**Disponible por**: `django.contrib.auth.context_processors.auth`.

**Uso**: `user.is_authenticated`, `user.username`, `user.avatar.url`, etc.

#### `messages` (context processor)

**Disponible por**: `django.contrib.messages.context_processors.messages`.

**Uso**: `{% for message in messages %}` para mostrar notificaciones flash (éxito, error) después de acciones como registro, creación de post, follow, etc.

---

### Estructura de base.html

El template base `templates/base.html` proporciona:

1. **DOCTYPE HTML5** con idioma español (`lang="es"`)
2. **CDN de TailwindCSS** vía `<script>` para utilidades CSS sin build step
3. **Header** con:
   - Logo "BootcampConnect" que enlaza al feed
   - Navegación condicional (`{% if user.is_authenticated %}`):
     - Feed, Buscar, Anónimo, Chats
     - Nombre de usuario (enlace a perfil)
     - Botón "Salir" (POST con CSRF)
4. **Main** con ancho máximo `max-w-4xl` y padding
5. **Mensajes flash** con estilo condicional (rojo para error, verde para éxito)
6. **`{% block content %}`** para que cada página hija inyecte su contenido

**Por qué se separa así**: El patrón `extends` + `block` permite mantener consistencia visual (header, nav, estructura de mensajes) en todas las páginas sin duplicar HTML.

---

## Manejo de Formularios

| Formulario | App | Modelo | Campos | Propósito |
|---|---|---|---|---|
| `UserRegistrationForm` | accounts | User | username, email, password1, password2 | Registro de usuario (extiende `UserCreationForm`) |
| `PostForm` | posts | Post | image, caption, hashtags | Crear publicación |
| `CommentForm` | comments | Comment | text (con placeholder y clase) | Comentar publicación |
| `ConfessionForm` | confessions | AnonymousConfession | content (textarea) | Crear confesión |
| `AnonymousCommentForm` | confessions | AnonymousComment | text (con placeholder) | Comentar confesión |

### Patrón de renderizado en templates

Los formularios se renderizan campo por campo (no con `{{ form.as_p }}`) para:
1. Controlar el HTML de cada campo individualmente
2. Aplicar clases CSS con `{{ field\|add_class:"..." }}`
3. Mostrar errores por campo
4. Agregar `help_text` cuando existe (registro)

```html
{% for field in form %}
    <div class="mb-3">
        <label>{{ field.label }}</label>
        {{ field|add_class:"w-full border rounded p-2" }}
        {% if field.errors %}
            {% for error in field.errors %}
                <p class="text-red-500">{{ error }}</p>
            {% endfor %}
        {% endif %}
    </div>
{% endfor %}
```

---

## Seguridad

- **CSRF**: Todos los formularios POST incluyen `{% csrf_token %}`
- **@login_required**: La mayoría de las vistas requieren autenticación
- **Validación**: Todos los formularios usan `form.is_valid()` antes de procesar datos
- **Anonimato**: Las confesiones nunca exponen `confession.user` en las templates. Siempre se muestra "Anónimo"
- **SQL Injection**: Django ORM sanitiza automáticamente todos los queries (no se usa SQL raw)

---

## Optimización de Queries (ORM)

- `select_related("user")` para seguir FK en una sola query (Post → User)
- `prefetch_related("likes", "comments")` para M2M y reverse FK en queries separadas pero eficientes
- `values_list("id", flat=True)` para obtener solo IDs de seguidos sin cargar objetos completos
- `prefetch_related("posts", "followers", "following")` en perfil para evitar N+1 queries

---

## Instalación y ejecución

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
